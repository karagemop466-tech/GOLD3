/* GOLD3 — Interactive Calculator, Live Spot Updater & Verified Table Filter Engine */
(function () {
  "use strict";

  var TROY_OZ_GRAMS = 31.1034768;
  var DWT_GRAMS = 1.55517384;
  var CARAT_GRAMS = 0.20;

  var PURITY_MAP = {
    "24K": { label: "24K Pure Gold (99.95% / 999.5)", fraction: 0.9995 },
    "24K_THEO": { label: "24K Exact Theoretical (100.00%)", fraction: 1.0 },
    "22K": { label: "22K Gold (91.67% / 916.7)", fraction: 22 / 24 },
    "21K": { label: "21K Gold (87.50% / 875.0)", fraction: 21 / 24 },
    "18K": { label: "18K Solid Gold (75.00% / 750)", fraction: 18 / 24 },
    "14K": { label: "14K Solid Gold (58.33% / 583.3)", fraction: 14 / 24 },
    "10K": { label: "10K Solid Gold — US Legal Minimum (41.67% / 416.7)", fraction: 10 / 24 },
    "9K": { label: "9K Gold — UK Hallmarked Minimum (37.50% / 375)", fraction: 9 / 24 },
    "PLATED": { label: "Gold-Plated / Vermeil / Gold-Filled (0% Solid Gold Core)", fraction: 0.0 }
  };

  function fmtUSD(n) {
    return "$" + n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  function initCalculator() {
    var form = document.getElementById("gold-calc-form");
    if (!form) return;

    var elKarat = document.getElementById("calc-karat");
    var elWeight = document.getElementById("calc-weight");
    var elUnit = document.getElementById("calc-unit");
    var elGemCt = document.getElementById("calc-gem-ct");
    var elSpotOz = document.getElementById("calc-spot-oz");
    var elAskPrice = document.getElementById("calc-ask-price");

    var outSpotGram = document.getElementById("out-spot-gram");
    var outNetAlloy = document.getElementById("out-net-alloy");
    var outPureGrams = document.getElementById("out-pure-grams");
    var outPureOz = document.getElementById("out-pure-oz");
    var outMeltUsd = document.getElementById("out-melt-usd");
    var outMarkup = document.getElementById("out-markup");
    var outVerdict = document.getElementById("out-verdict");

    function compute() {
      var karatKey = elKarat.value;
      var purityInfo = PURITY_MAP[karatKey] || PURITY_MAP["14K"];
      var rawWeight = Math.max(0, parseFloat(elWeight.value) || 0);
      var unit = elUnit.value;
      var gemCt = Math.max(0, parseFloat(elGemCt.value) || 0);
      var spotOz = Math.max(0, parseFloat(elSpotOz.value) || 0);
      var askPrice = parseFloat(elAskPrice.value);

      var totalGrams = rawWeight;
      if (unit === "dwt") totalGrams = rawWeight * DWT_GRAMS;
      if (unit === "ozt") totalGrams = rawWeight * TROY_OZ_GRAMS;

      var gemGrams = gemCt * CARAT_GRAMS;
      var netAlloyGrams = Math.max(0, totalGrams - gemGrams);
      var pureGoldGrams = netAlloyGrams * purityInfo.fraction;
      var pureGoldOz = pureGoldGrams / TROY_OZ_GRAMS;
      var spotPerGram = spotOz / TROY_OZ_GRAMS;
      var meltUsd = pureGoldGrams * spotPerGram;

      outSpotGram.textContent = fmtUSD(spotPerGram) + " / g (24K)";
      outNetAlloy.textContent = netAlloyGrams.toFixed(3) + " g" + (gemCt > 0 ? " (minus " + gemGrams.toFixed(2) + "g stone)" : "");
      outPureGrams.textContent = pureGoldGrams.toFixed(4) + " g pure Au";
      outPureOz.textContent = pureGoldOz.toFixed(4) + " troy oz";
      outMeltUsd.textContent = fmtUSD(meltUsd);

      if (!isNaN(askPrice) && askPrice >= 0) {
        if (karatKey === "PLATED") {
          outMarkup.textContent = "∞ (0.0000 g solid karat gold core)";
          outVerdict.className = "verdict-box badge-bad";
          outVerdict.textContent =
            "REJECT (CHECKLIST #2 & #12): Gold-plated, vermeil, and gold-filled rings are NOT solid gold. Surface plating wears through quickly with daily wear.";
        } else if (meltUsd > 0 && askPrice < meltUsd * 0.98) {
          var pctBelow = (((meltUsd - askPrice) / meltUsd) * 100).toFixed(1);
          outMarkup.textContent = (askPrice / meltUsd).toFixed(2) + "x melt (" + pctBelow + "% BELOW MELT!)";
          outVerdict.className = "verdict-box badge-bad";
          outVerdict.textContent =
            "CRITICAL SCAM / MISREPRESENTATION ALERT (CHECKLIST #6 & #12): Asking price (" +
            fmtUSD(askPrice) +
            ") is BELOW raw gold melt value (" +
            fmtUSD(meltUsd) +
            ")! Genuine solid gold rings are never sold below spot melt value. Walk away immediately.";
        } else if (meltUsd > 0) {
          var ratio = askPrice / meltUsd;
          var sharePct = ((meltUsd / askPrice) * 100).toFixed(1);
          outMarkup.textContent = ratio.toFixed(2) + "x melt (" + sharePct + "% intrinsic gold value)";
          if (ratio <= 2.0) {
            outVerdict.className = "verdict-box badge-ok";
            outVerdict.textContent =
              "HIGH INTRINSIC GOLD VALUE (" +
              ratio.toFixed(2) +
              "x melt): Bullion-grade low markup. Compare with the sourced band rows, verify the return window and test via XRF on Day 1.";
          } else if (ratio <= 4.5) {
            outVerdict.className = "verdict-box badge-ok";
            outVerdict.textContent =
              "NORMAL FINE RETAIL RANGE (" +
              ratio.toFixed(2) +
              "x melt): Consistent with the verified traditional 14K solid gold retail bands in this dataset. Pay by credit card & verify hallmark upon arrival.";
          } else {
            outVerdict.className = "verdict-box badge-warn";
            outVerdict.textContent =
              "HIGH BRAND / DESIGN / GEMSTONE MARKUP (" +
              ratio.toFixed(2) +
              "x melt): Only " +
              sharePct +
              "% of price is raw gold. Ensure natural GIA diamond value or bespoke craftsmanship justifies the premium.";
          }
        } else {
          outMarkup.textContent = "Enter ring weight > 0 g to compare";
          outVerdict.className = "verdict-box badge-warn";
          outVerdict.textContent =
            "UNVERIFIED WEIGHT WARNING (CHECKLIST #4): Seller omitted gram weight! Request exact grams in writing before buying.";
        }
      } else {
        outMarkup.textContent = "Enter asking price ($) to evaluate markup";
        outVerdict.className = "verdict-box badge-neutral";
        outVerdict.textContent = "Tip: Enter the online listing's asking price to check whether it falls below melt value (scam red flag).";
      }

      // Update live karat reference table on calculator.html if present
      var liveRows = document.querySelectorAll("[data-karat-fraction]");
      liveRows.forEach(function (tr) {
        var frac = parseFloat(tr.getAttribute("data-karat-fraction"));
        var cellGram = tr.querySelector(".live-gram-usd");
        var cellOz = tr.querySelector(".live-oz-usd");
        if (cellGram) cellGram.textContent = fmtUSD(spotPerGram * frac);
        if (cellOz) cellOz.textContent = fmtUSD(spotOz * frac);
      });
    }

    [elKarat, elWeight, elUnit, elGemCt, elSpotOz, elAskPrice].forEach(function (el) {
      if (el) {
        el.addEventListener("input", compute);
        el.addEventListener("change", compute);
      }
    });

    var presets = document.querySelectorAll("[data-preset]");
    presets.forEach(function (btn) {
      btn.addEventListener("click", function () {
        elKarat.value = btn.getAttribute("data-karat") || "14K";
        elWeight.value = btn.getAttribute("data-weight") || "4.2";
        elUnit.value = "g";
        elGemCt.value = btn.getAttribute("data-gem") || "0";
        elAskPrice.value = btn.getAttribute("data-price") || "";
        compute();
      });
    });

    compute();
  }

  function initTableFilters() {
    var searchInput = document.getElementById("ring-search");
    var karatFilter = document.getElementById("ring-karat-filter");
    var statusFilter = document.getElementById("ring-status-filter");
    var countBadge = document.getElementById("visible-row-count");
    var rows = Array.prototype.slice.call(document.querySelectorAll("tbody tr[data-ring-row]"));

    if (!rows.length) return;

    function applyFilter() {
      var q = searchInput ? searchInput.value.trim().toLowerCase() : "";
      var kf = karatFilter ? karatFilter.value : "ALL";
      var sf = statusFilter ? statusFilter.value : "ALL";
      var shown = 0;

      rows.forEach(function (tr) {
        var text = tr.textContent.toLowerCase();
        var rk = tr.getAttribute("data-karat-group") || "";
        var rw = tr.getAttribute("data-weight-state") || "";
        var okQ = !q || text.indexOf(q) !== -1;
        var okK = kf === "ALL" || rk === kf;
        var okS = sf === "ALL" || rw === sf;
        var show = okQ && okK && okS;
        tr.style.display = show ? "" : "none";
        if (show) shown += 1;
      });

      if (countBadge) {
        countBadge.textContent = "Showing " + shown + " of " + rows.length + " verified listings";
      }
    }

    [searchInput, karatFilter, statusFilter].forEach(function (el) {
      if (el) {
        el.addEventListener("input", applyFilter);
        el.addEventListener("change", applyFilter);
      }
    });

    applyFilter();
  }

  document.addEventListener("DOMContentLoaded", function () {
    initCalculator();
    initTableFilters();
  });
})();

/* GOLD3 - small, dependency-free interactions.
   All numbers used here come from the rendered page (data-* attributes),
   which in turn come from data/prices.json. Nothing is hard-coded twice. */

(function () {
  "use strict";

  /* ------------------------------------------------ table filtering + search */
  function initTables() {
    document.querySelectorAll("[data-table-toolbar]").forEach(function (toolbar) {
      var tableId = toolbar.getAttribute("data-table-toolbar");
      var table = document.getElementById(tableId);
      if (!table) return;
      var rows = Array.prototype.slice.call(table.querySelectorAll("tbody tr"));
      var search = toolbar.querySelector("input[type='search']");
      var buttons = Array.prototype.slice.call(toolbar.querySelectorAll(".filter-btn"));
      var counter = toolbar.querySelector("[data-count]");
      var activeFilter = "all";

      function apply() {
        var q = (search && search.value || "").trim().toLowerCase();
        var shown = 0;
        rows.forEach(function (row) {
          var cats = (row.getAttribute("data-cats") || "").split(/\s+/);
          var text = (row.getAttribute("data-search") || row.textContent || "").toLowerCase();
          var okCat = activeFilter === "all" || cats.indexOf(activeFilter) !== -1;
          var okText = !q || text.indexOf(q) !== -1;
          var show = okCat && okText;
          row.classList.toggle("hidden", !show);
          if (show) shown++;
        });
        if (counter) counter.textContent = shown + " of " + rows.length + " listings";
      }

      buttons.forEach(function (btn) {
        btn.addEventListener("click", function () {
          buttons.forEach(function (b) { b.classList.remove("active"); });
          btn.classList.add("active");
          activeFilter = btn.getAttribute("data-filter") || "all";
          apply();
        });
      });
      if (search) search.addEventListener("input", apply);
      apply();
    });
  }

  /* --------------------------------------------------------------- calculator */
  function initCalculator() {
    var form = document.getElementById("gold-calc");
    if (!form) return;

    var spotEl = document.getElementById("calc-spot");
    var karatEl = document.getElementById("calc-karat");
    var gramsEl = document.getElementById("calc-grams");
    var stoneCtEl = document.getElementById("calc-stone-ct");
    var tolEl = document.getElementById("calc-tolerance");
    var priceEl = document.getElementById("calc-price");

    var out = {
      perGramSpot: document.getElementById("out-spot-gram"),
      meltPerGram: document.getElementById("out-melt-gram"),
      meltValue: document.getElementById("out-melt-value"),
      fineGold: document.getElementById("out-fine-gold"),
      tolNote: document.getElementById("out-tolerance-note"),
      purity: document.getElementById("out-purity"),
      implied: document.getElementById("out-implied"),
      ratio: document.getElementById("out-ratio"),
      premium: document.getElementById("out-premium"),
      verdict: document.getElementById("out-verdict")
    };

    var FINENESS = { "10K": 10 / 24, "14K": 14 / 24, "18K": 18 / 24, "19K": 19 / 24, "22K": 22 / 24, "24K": 0.9999 };
    var OZ_GRAMS = 31.1034768;

    function money(n) {
      if (!isFinite(n)) return "—";
      return "$" + n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }
    function grams(n) {
      if (!isFinite(n)) return "—";
      return n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " g";
    }

    function compute() {
      var spot = parseFloat(spotEl.value);
      if (!isFinite(spot) || spot <= 0) spot = NaN;
      var karat = karatEl.value;
      var f = FINENESS[karat];
      var wRaw = parseFloat(gramsEl.value);
      var stoneCt = stoneCtEl ? parseFloat(stoneCtEl.value) : 0;
      var stoneGrams = isFinite(stoneCt) && stoneCt > 0 ? stoneCt * 0.2 : 0;
      var validStone = !stoneCtEl || stoneCtEl.value.trim() === "" || (isFinite(stoneCt) && stoneCt >= 0);
      var w = validStone && isFinite(wRaw) && wRaw > 0 && stoneGrams <= wRaw ? wRaw - stoneGrams : NaN;
      var tol = tolEl ? tolEl.value : "none";
      var price = parseFloat(priceEl.value);

      var spotPerGram = spot / OZ_GRAMS;
      var meltPerGram = spotPerGram * f;
      var meltValue = meltPerGram * w;

      out.perGramSpot.textContent = money(spotPerGram);
      out.meltPerGram.textContent = money(meltPerGram);
      out.meltValue.textContent = money(meltValue);
      out.fineGold.textContent = grams(w * f);
      out.purity.textContent = karat + " · " + (f * 100).toFixed(1) + "% fine" +
        (stoneGrams > 0 && isFinite(w) ? " · " + w.toFixed(2) + " g remaining material (assumed metal)" : "");

      if (out.tolNote) {
        var deltaG = tol === "pct5" ? w * 0.05 : tol === "g05" ? 0.5 : tol === "g10" ? 1.0 : 0;
        if (deltaG > 0) {
          var lowMelt = meltPerGram * Math.max(0, w - deltaG);
          var highMelt = meltPerGram * (w + deltaG);
          out.tolNote.textContent = "range: " + money(lowMelt) + " – " + money(highMelt);
        } else {
          out.tolNote.textContent = stoneGrams > 0
            ? "after −" + stoneGrams.toFixed(2) + " g stone deduction"
            : "weight × melt per gram";
        }
      }

      if (isFinite(price) && price > 0) {
        var implied = price / meltPerGram;
        var ratio = price / meltValue;
        out.implied.textContent = grams(implied);
        out.ratio.textContent = isFinite(ratio) ? ratio.toFixed(1) + "×" : "—";
        out.premium.textContent = isFinite(meltValue) ? money(price - meltValue) : "—";

        var v = out.verdict;
        v.className = "verdict";
        if (isFinite(meltValue) && meltValue > 0) {
          v.classList.add("warn");
          v.textContent = (price < meltValue ? "The entered price is below the estimated gold value; check the inputs and investigate. " : "The price-to-estimated-metal-value ratio is " + ratio.toFixed(1) + "×. ") +
            "This comparison cannot verify purity, establish a typical markup, or prove a listing is genuine. Estimates depend on the dated or entered spot price and assumed metal-only weight.";
        } else {
          v.textContent = "Enter a valid metal weight and spot price to compare the asking price with estimated gold value.";
        }
      } else {
        out.implied.textContent = "—";
        out.ratio.textContent = "—";
        out.premium.textContent = "—";
        out.verdict.className = "verdict";
        out.verdict.textContent = "Enter a price to compare it with the gold value and see the break-even weight.";
      }
    }

    [spotEl, karatEl, gramsEl, stoneCtEl, tolEl, priceEl].forEach(function (el) {
      if (!el) return;
      el.addEventListener("input", compute);
      el.addEventListener("change", compute);
    });
    form.addEventListener("submit", function (e) { e.preventDefault(); compute(); });
    compute();
  }

  /* ------------------------------------------------------------- deep links */
  function highlightTarget() {
    if (!location.hash) return;
    var el = document.getElementById(location.hash.slice(1));
    if (!el) return;
    el.style.transition = "background .4s";
    el.style.background = "#fbf3dd";
    setTimeout(function () { el.style.background = ""; }, 2400);
  }

  document.addEventListener("DOMContentLoaded", function () {
    initTables();
    initCalculator();
    highlightTarget();
  });
})();

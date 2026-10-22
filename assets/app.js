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
    var priceEl = document.getElementById("calc-price");

    var out = {
      perGramSpot: document.getElementById("out-spot-gram"),
      meltPerGram: document.getElementById("out-melt-gram"),
      meltValue: document.getElementById("out-melt-value"),
      purity: document.getElementById("out-purity"),
      implied: document.getElementById("out-implied"),
      ratio: document.getElementById("out-ratio"),
      premium: document.getElementById("out-premium"),
      verdict: document.getElementById("out-verdict")
    };

    var FINENESS = { "10K": 10 / 24, "14K": 14 / 24, "18K": 18 / 24, "22K": 22 / 24, "24K": 24 / 24 };
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
      var karat = karatEl.value;
      var f = FINENESS[karat];
      var w = parseFloat(gramsEl.value);
      var price = parseFloat(priceEl.value);

      var spotPerGram = spot / OZ_GRAMS;
      var meltPerGram = spotPerGram * f;
      var meltValue = meltPerGram * (isFinite(w) ? w : 0);

      out.perGramSpot.textContent = money(spotPerGram);
      out.meltPerGram.textContent = money(meltPerGram);
      out.meltValue.textContent = money(meltValue);
      out.purity.textContent = karat + " · " + (f * 100).toFixed(1) + "% fine";

      if (isFinite(price) && price > 0) {
        var implied = price / meltPerGram;
        var ratio = price / meltValue;
        out.implied.textContent = grams(implied);
        out.ratio.textContent = isFinite(ratio) ? ratio.toFixed(1) + "×" : "—";
        out.premium.textContent = isFinite(meltValue) ? money(price - meltValue) : "—";

        var v = out.verdict;
        v.className = "verdict";
        if (price < meltValue) {
          v.classList.add("bad");
          v.innerHTML = "<strong>Impossible for solid gold.</strong> The price is below the gold value of the weight you entered. " +
            "Either the weight is wrong or the metal is not what the listing claims.";
        } else if (ratio < 1.5) {
          v.classList.add("warn");
          v.innerHTML = "<strong>Unusually cheap.</strong> At " + ratio.toFixed(1) + "× the gold value, something other than a normal retail margin is going on. " +
            "Verify the purity independently before buying.";
        } else if (ratio <= 4) {
          v.classList.add("good");
          v.innerHTML = "<strong>Low markup for jewellery retail.</strong> You are paying " + ratio.toFixed(1) + "× the raw gold value; " +
            "the rest covers labour, setting, stones and margin.";
        } else if (ratio <= 10) {
          v.classList.add("warn");
          v.innerHTML = "<strong>Typical branded retail range.</strong> " + ratio.toFixed(1) + "× the gold value. " +
            "Reasonable when a certified diamond is included — compare stone prices before accepting it.";
        } else {
          v.classList.add("warn");
          v.innerHTML = "<strong>Heavy premium.</strong> " + ratio.toFixed(1) + "× the gold value. The price is being driven by brand, " +
            "design or the stone, not the gold. Check what the premium buys.";
        }
      } else {
        out.implied.textContent = "—";
        out.ratio.textContent = "—";
        out.premium.textContent = "—";
        out.verdict.className = "verdict";
        out.verdict.textContent = "Enter a price to compare it with the gold value and see the break-even weight.";
      }
    }

    [spotEl, karatEl, gramsEl, priceEl].forEach(function (el) {
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

/* iPhone Springboard / Matrix Fly-In & Staggered Page Transitions across all CPG Portal Pages */
(function () {
  if (window.__CPG_IOS_MATRIX_LOADED__) return;
  window.__CPG_IOS_MATRIX_LOADED__ = true;

  var reduceMotion = false;
  try { reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}

  var style = document.createElement('style');
  style.textContent =
    '.ios-mx-prep { will-change: transform, opacity; }' +
    '@media (prefers-reduced-motion: reduce) { .ios-mx-prep { opacity: 1 !important; transform: none !important; transition: none !important; } }';
  document.head.appendChild(style);

  var MATRIX_SELECTORS = [
    /* Briefing Map (index.html) */
    '.hero > *', '.start', '.track', '.tile',
    /* Story Slides 00..06 */
    '.hero-grid > *', '.top-row > *', '.m-card', '.flow-card',
    '.cheese-canvas', '.slice-card', '.chart-card', '.sq-card',
    '.coex-box', '.thumb', '.stage-grid > *', '.cards > .card', '.cta-row > *',
    /* Pillar & Sub-Pillar Tree */
    '.p-hero > *', '.sp-tab', '.per-card',
    /* Persona Chessboard & Dossier */
    '.est-cell', '.board-shell', '.drawer', '.pw-card',
    '.hero-card', '.how-strip', '.ag-card',
    /* Agent Blueprint & Architecture / Surfaces / Proof */
    '.ab-hero', '.arch-stage', '.tech-box',
    '.ar-lane', '.ar-card', '.sf-btn', '#sfStage',
    '#citeGrid > article', 'main section > div > article', '#plan100 > div > div'
  ].join(', ');

  function collectVisibleMatrixItems(scope) {
    var root = scope || document;
    var raw = [].slice.call(root.querySelectorAll(MATRIX_SELECTORS));
    if (!raw.length) return [];

    /* Filter out hidden elements or nested duplicates (if an ancestor is already in the set, prefer the finer-grained child cards when inside grids) */
    var set = new Set(raw);
    var filtered = raw.filter(function (el) {
      if (!el || !el.getBoundingClientRect) return false;
      if (el.closest && el.closest('.genie-backdrop')) return false;
      var st = getComputedStyle(el);
      if (st.display === 'none' || st.visibility === 'hidden') return false;
      var r = el.getBoundingClientRect();
      if (r.width < 12 || r.height < 12) return false;
      /* Skip elements far below initial viewport fold (> 1.45x viewport height) so offscreen items stay immediately visible on scroll */
      if (r.top > window.innerHeight * 1.45 || r.bottom < -100) return false;
      /* Avoid animating both parent container and child cards simultaneously */
      var childMatch = el.querySelector && el.querySelector('.tile, .m-card, .flow-card, .slice-card, .per-card, .ag-card, .arch-stage, .ar-lane');
      if (childMatch && set.has(childMatch)) return false;
      return true;
    });

    /* Sort into top-to-bottom rows (~48px tolerance), then left-to-right columns */
    var items = filtered.map(function (el) {
      var r = el.getBoundingClientRect();
      return { el: el, r: r, cx: r.left + r.width / 2, cy: r.top + r.height / 2 };
    });
    items.sort(function (a, b) {
      if (Math.abs(a.r.top - b.r.top) > 44) return a.r.top - b.r.top;
      return a.r.left - b.r.left;
    });

    /* Assign discrete (row, col) matrix indices */
    var rowIdx = 0, colIdx = 0, lastTop = null;
    items.forEach(function (it) {
      if (lastTop === null || Math.abs(it.r.top - lastTop) > 44) {
        if (lastTop !== null) rowIdx++;
        colIdx = 0;
        lastTop = it.r.top;
      } else {
        colIdx++;
      }
      it.row = rowIdx;
      it.col = colIdx;
    });
    return items;
  }

  function runIosMatrixEnter(scope) {
    if (reduceMotion) return;
    var items = collectVisibleMatrixItems(scope);
    if (!items.length) return;

    var vw = window.innerWidth || 1280;
    var vh = window.innerHeight || 800;
    var midX = vw / 2;
    var midY = vh * 0.46;
    var maxEnd = 0;

    items.forEach(function (it) {
      var el = it.el;
      /* Radial springboard offset: outer tiles close inward from edges + slight depth scale, just like iPhone unlock */
      var dx = Math.round((it.cx - midX) * 0.14);
      var dy = Math.round((it.cy - midY) * 0.14 + 18);
      dx = Math.max(-72, Math.min(72, dx));
      dy = Math.max(-48, Math.min(64, dy));

      var delay = Math.min(310, it.row * 44 + it.col * 36);
      var dur = 390;
      if (delay + dur > maxEnd) maxEnd = delay + dur;

      if (el.animate) {
        var anim = el.animate([
          { opacity: 0, transform: 'translate3d(' + dx + 'px, ' + dy + 'px, 0) scale(0.87)' },
          { opacity: 1, transform: 'translate3d(0px, 0px, 0) scale(1.008)', offset: 0.72 },
          { opacity: 1, transform: 'translate3d(0px, 0px, 0) scale(1)' }
        ], {
          duration: dur,
          delay: delay,
          easing: 'cubic-bezier(0.19, 1, 0.26, 1)',
          fill: 'backwards'
        });
        anim.onfinish = function () { el.style.opacity = ''; el.style.transform = ''; };
      }
    });

    /* Re-align any dynamic SVG connector lines once cards finish settling */
    setTimeout(function () {
      window.dispatchEvent(new Event('resize'));
      if (window.__redrawPillarLines) window.__redrawPillarLines();
    }, maxEnd + 25);
  }

  function runIosMatrixExitAndGo(href) {
    if (reduceMotion) { window.location.href = href; return; }
    var items = collectVisibleMatrixItems(document);
    if (!items.length) { window.location.href = href; return; }

    var vw = window.innerWidth || 1280;
    var vh = window.innerHeight || 800;
    var midX = vw / 2;
    var midY = vh * 0.46;

    items.slice(0, 18).forEach(function (it, idx) {
      var dx = Math.round((it.cx - midX) * 0.09);
      var dy = Math.round((it.cy - midY) * 0.09 - 12);
      var delay = Math.min(85, it.row * 18 + it.col * 14 + idx * 4);
      if (it.el.animate) {
        it.el.animate([
          { opacity: 1, transform: 'translate3d(0,0,0) scale(1)' },
          { opacity: 0, transform: 'translate3d(' + dx + 'px, ' + dy + 'px, 0) scale(0.91)' }
        ], {
          duration: 165,
          delay: delay,
          easing: 'cubic-bezier(0.4, 0, 1, 1)',
          fill: 'forwards'
        });
      }
    });

    setTimeout(function () { window.location.href = href; }, 170);
  }

  /* Intercept internal page links for crisp staggered matrix transition */
  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var link = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!link) return;
    if (link.target === '_blank' || link.hasAttribute('download') || link.hasAttribute('data-no-matrix')) return;
    var rawHref = link.getAttribute('href') || '';
    if (!rawHref || rawHref.charAt(0) === '#' || rawHref.indexOf('javascript:') === 0 || rawHref.indexOf('mailto:') === 0) return;

    var dest;
    try { dest = new URL(link.href, window.location.href); } catch (err) { return; }
    if (dest.origin !== window.location.origin) return;
    if (dest.pathname === window.location.pathname && dest.search === window.location.search) return;

    e.preventDefault();
    runIosMatrixExitAndGo(dest.href);
  });

  window.triggerIosMatrixEnter = runIosMatrixEnter;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      requestAnimationFrame(function () { runIosMatrixEnter(document); });
    });
  } else {
    requestAnimationFrame(function () { runIosMatrixEnter(document); });
  }

  /* Restore clean state if restored from browser Back/Forward cache */
  window.addEventListener('pageshow', function (e) {
    if (e.persisted) {
      document.querySelectorAll(MATRIX_SELECTORS).forEach(function (el) {
        if (el.getAnimations) el.getAnimations().forEach(function (a) { a.cancel(); });
        el.style.opacity = '';
        el.style.transform = '';
      });
      requestAnimationFrame(function () { runIosMatrixEnter(document); });
    }
  });
})();

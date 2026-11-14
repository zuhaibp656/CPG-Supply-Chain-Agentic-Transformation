/* Context-Aware Directional Staggered Transitions across all CPG Portal Pages:
 *  - 'from-right' : Next Slide / Next Pillar / Later Sibling (staggered column-by-column from the right)
 *  - 'from-left'  : Prev Slide / Prev Pillar / Back / Earlier Sibling (staggered column-by-column from the left)
 *  - 'from-down'  : Drill-Down into Pillar, Sub-Pillar Personas, Dossier, or Agent Spec (line-by-line from below)
 *  - 'from-up'    : Return Up to Briefing Map / All Slides Overview (line-by-line from above)
 *  - 'matrix'     : Cold-open of 2D Grid Hubs (index.html & personas/index.html only)
 */
(function () {
  if (window.__CPG_DIR_FLOW_LOADED__) return;
  window.__CPG_DIR_FLOW_LOADED__ = true;

  var STORAGE_KEY = 'cpg-nav-direction';
  var reduceMotion = false;
  try { reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}

  /* Canonical presentation slide order for automatic Next vs Prev inference */
  var SLIDE_ORDER = [
    '00_executive_story.html',
    '01_capital_reality.html',
    '02_value_chain_flows.html',
    '03_swiss_cheese.html',
    '04_talent_velocity_squeeze.html',
    '05_plug_is_an_agent.html',
    'demo_stage.html',
    '06_one_to_many.html',
    'personas/index.html',
    '09_agent_architecture.html',
    '10_surfaces.html',
    '13_proof_and_cases.html'
  ];

  function slideIndexOf(urlPath) {
    var p = String(urlPath || '');
    for (var i = 0; i < SLIDE_ORDER.length; i++) {
      if (p.indexOf(SLIDE_ORDER[i]) >= 0) return i;
    }
    return -1;
  }

  var ITEM_SELECTORS = [
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

  function collectItems(scope) {
    var root = scope || document;
    var raw = [].slice.call(root.querySelectorAll(ITEM_SELECTORS));
    if (!raw.length) return [];

    var set = new Set(raw);
    var filtered = raw.filter(function (el) {
      if (!el || !el.getBoundingClientRect) return false;
      if (el.closest && el.closest('.genie-backdrop')) return false;
      var st = getComputedStyle(el);
      if (st.display === 'none' || st.visibility === 'hidden') return false;
      var r = el.getBoundingClientRect();
      if (r.width < 12 || r.height < 12) return false;
      if (r.top > window.innerHeight * 1.45 || r.bottom < -100) return false;
      var childMatch = el.querySelector && el.querySelector('.tile, .m-card, .flow-card, .slice-card, .per-card, .ag-card, .arch-stage, .ar-lane');
      if (childMatch && set.has(childMatch)) return false;
      return true;
    });

    var items = filtered.map(function (el) {
      var r = el.getBoundingClientRect();
      return { el: el, r: r, cx: r.left + r.width / 2, cy: r.top + r.height / 2 };
    });
    items.sort(function (a, b) {
      if (Math.abs(a.r.top - b.r.top) > 44) return a.r.top - b.r.top;
      return a.r.left - b.r.left;
    });

    var rowIdx = 0, colIdx = 0, lastTop = null, maxCol = 0;
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
      if (colIdx > maxCol) maxCol = colIdx;
    });
    items.forEach(function (it) { it.maxCol = maxCol; });
    return items;
  }

  function inferNavDirection(link, destUrl) {
    var explicit = link.getAttribute('data-nav-dir');
    if (explicit) return explicit;

    var id = (link.id || '').toLowerCase();
    var txt = (link.textContent || '').trim().toLowerCase();
    var dstPath = destUrl.pathname;
    var curPath = window.location.pathname;

    /* Explicit Next / Prev / Back buttons */
    if (id === 'docknext' || txt.indexOf('next ') >= 0 || txt.indexOf('start briefing') >= 0 || txt.indexOf('watch live demo') >= 0) {
      return 'from-right';
    }
    if (id === 'dockprev' || txt.indexOf('prev ') >= 0 || txt.indexOf('←') >= 0 || txt.indexOf('back ') >= 0 || link.textContent.indexOf('\u2190') >= 0 || link.textContent.indexOf('\u25C0') >= 0) {
      return 'from-left';
    }

    /* Returning up to top-level Briefing Map / All Slides */
    if ((dstPath.endsWith('/index.html') || dstPath === '/') && !dstPath.includes('/personas/')) {
      return 'from-up';
    }

    /* Sibling Agent switcher chips on agent_blueprint.html */
    if (link.classList.contains('sw-chip') && curPath.indexOf('agent_blueprint.html') >= 0) {
      var chips = [].slice.call(document.querySelectorAll('.sw-chip'));
      var curChip = document.querySelector('.sw-chip.is-on');
      var curI = chips.indexOf(curChip), nextI = chips.indexOf(link);
      if (curI >= 0 && nextI >= 0 && nextI !== curI) {
        return nextI > curI ? 'from-right' : 'from-left';
      }
    }

    /* Sequential Slide Deck comparison */
    var curS = slideIndexOf(curPath);
    var dstS = slideIndexOf(dstPath);
    if (curS >= 0 && dstS >= 0 && curS !== dstS) {
      return dstS > curS ? 'from-right' : 'from-left';
    }

    /* Drilling down into Pillar, Persona Dossier, or Agent Blueprint */
    if (dstPath.indexOf('pillar.html') >= 0 || dstPath.indexOf('dossier.html') >= 0 || dstPath.indexOf('agent_blueprint.html') >= 0 || dstPath.indexOf('personas/index.html') >= 0) {
      return 'from-down';
    }

    return 'from-right';
  }

  function computeEnterVector(it, mode, vw, vh) {
    if (mode === 'from-right') {
      return {
        dx: 76 + it.col * 10,
        dy: 0,
        scale: 0.985,
        delay: Math.min(280, it.col * 38 + it.row * 24)
      };
    }
    if (mode === 'from-left') {
      var revCol = Math.max(0, it.maxCol - it.col);
      return {
        dx: -(76 + revCol * 10),
        dy: 0,
        scale: 0.985,
        delay: Math.min(280, revCol * 38 + it.row * 24)
      };
    }
    if (mode === 'from-up') {
      return {
        dx: 0,
        dy: -46,
        scale: 0.98,
        delay: Math.min(270, it.row * 42 + it.col * 22)
      };
    }
    if (mode === 'matrix') {
      var midX = vw / 2, midY = vh * 0.46;
      var rx = Math.max(-68, Math.min(68, Math.round((it.cx - midX) * 0.13)));
      var ry = Math.max(-44, Math.min(60, Math.round((it.cy - midY) * 0.13 + 16)));
      return {
        dx: rx,
        dy: ry,
        scale: 0.88,
        delay: Math.min(300, it.row * 42 + it.col * 34)
      };
    }
    /* Default 'from-down': rising cleanly from below line-by-line */
    return {
      dx: 0,
      dy: 50,
      scale: 0.975,
      delay: Math.min(280, it.row * 44 + it.col * 26)
    };
  }

  function computeExitVector(it, mode) {
    /* Outgoing page moves in the natural opposite flow of incoming content */
    if (mode === 'from-right') {
      /* Moving to Next page: current elements glide off to the left */
      return { dx: -64, dy: 0, scale: 0.985, delay: Math.min(75, it.col * 16 + it.row * 12) };
    }
    if (mode === 'from-left') {
      /* Moving to Prev page: current elements glide off to the right */
      var revCol = Math.max(0, it.maxCol - it.col);
      return { dx: 64, dy: 0, scale: 0.985, delay: Math.min(75, revCol * 16 + it.row * 12) };
    }
    if (mode === 'from-up') {
      return { dx: 0, dy: 34, scale: 0.98, delay: Math.min(70, it.row * 16 + it.col * 10) };
    }
    /* Drilling down ('from-down'): current view lifts slightly up as deeper layer rises from below */
    return { dx: 0, dy: -32, scale: 0.98, delay: Math.min(70, it.row * 16 + it.col * 10) };
  }

  function runDirectionalEnter(scope, explicitMode) {
    if (reduceMotion) return;
    var items = collectItems(scope);
    if (!items.length) return;

    var mode = explicitMode;
    if (!mode) {
      try {
        mode = sessionStorage.getItem(STORAGE_KEY) || '';
        sessionStorage.removeItem(STORAGE_KEY);
      } catch (e) {}
    }
    if (!mode) {
      var p = window.location.pathname;
      var is2dGridHub = (p.endsWith('/index.html') || p === '/' || p.indexOf('personas/index.html') >= 0);
      mode = is2dGridHub ? 'matrix' : 'from-down';
    }

    var vw = window.innerWidth || 1280;
    var vh = window.innerHeight || 800;
    var maxEnd = 0;

    items.forEach(function (it) {
      var el = it.el;
      if (el.getAnimations) el.getAnimations().forEach(function (a) { a.cancel(); });
      var v = computeEnterVector(it, mode, vw, vh);
      var dur = 370;
      if (v.delay + dur > maxEnd) maxEnd = v.delay + dur;

      if (el.animate) {
        var anim = el.animate([
          { opacity: 0, transform: 'translate3d(' + v.dx + 'px, ' + v.dy + 'px, 0) scale(' + v.scale + ')' },
          { opacity: 1, transform: 'translate3d(0px, 0px, 0) scale(1)' }
        ], {
          duration: dur,
          delay: v.delay,
          easing: 'cubic-bezier(0.20, 1, 0.30, 1)',
          fill: 'backwards'
        });
        anim.onfinish = function () { el.style.opacity = ''; el.style.transform = ''; };
      }
    });

    setTimeout(function () {
      window.dispatchEvent(new Event('resize'));
      if (window.__redrawPillarLines) window.__redrawPillarLines();
    }, maxEnd + 20);
  }

  function runDirectionalExitAndGo(href, mode) {
    try { sessionStorage.setItem(STORAGE_KEY, mode); } catch (e) {}
    if (reduceMotion) { window.location.href = href; return; }

    var items = collectItems(document);
    if (!items.length) { window.location.href = href; return; }

    items.slice(0, 18).forEach(function (it) {
      var v = computeExitVector(it, mode);
      if (it.el.animate) {
        it.el.animate([
          { opacity: 1, transform: 'translate3d(0,0,0) scale(1)' },
          { opacity: 0, transform: 'translate3d(' + v.dx + 'px, ' + v.dy + 'px, 0) scale(' + v.scale + ')' }
        ], {
          duration: 155,
          delay: v.delay,
          easing: 'cubic-bezier(0.4, 0, 1, 1)',
          fill: 'forwards'
        });
      }
    });

    setTimeout(function () { window.location.href = href; }, 160);
  }

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

    var mode = inferNavDirection(link, dest);
    e.preventDefault();
    runDirectionalExitAndGo(dest.href, mode);
  });

  /* Expose both new directional helper and backward-compatible alias */
  window.triggerDirectionalFlow = runDirectionalEnter;
  window.triggerIosMatrixEnter = function (scope, mode) { runDirectionalEnter(scope, mode || 'from-down'); };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      requestAnimationFrame(function () { runDirectionalEnter(document); });
    });
  } else {
    requestAnimationFrame(function () { runDirectionalEnter(document); });
  }

  window.addEventListener('pageshow', function (e) {
    if (e.persisted) {
      document.querySelectorAll(ITEM_SELECTORS).forEach(function (el) {
        if (el.getAnimations) el.getAnimations().forEach(function (a) { a.cancel(); });
        el.style.opacity = '';
        el.style.transform = '';
      });
      requestAnimationFrame(function () { runDirectionalEnter(document, 'from-left'); });
    }
  });
})();

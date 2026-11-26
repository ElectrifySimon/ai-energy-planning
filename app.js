/* Page behaviour: reveal on scroll, dot field, reading progress.
   Content is visible by default. The hiding class is applied only when the
   observer is available, so a blocked or failed script never blanks the page. */
(function () {
  'use strict';

  /* ---------- reveal ---------- */
  var revealEls = Array.prototype.slice.call(document.querySelectorAll('[data-reveal]'));
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('on');
          io.unobserve(e.target);
        }
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });

    revealEls.forEach(function (el) {
      var top = el.getBoundingClientRect().top;
      if (top > window.innerHeight * 0.9) { el.classList.add('pre'); }
      io.observe(el);
    });

    /* Safety net: anything still hidden after a few seconds is shown. */
    window.setTimeout(function () {
      document.querySelectorAll('.pre:not(.on)').forEach(function (el) {
        el.classList.add('on');
      });
    }, 3000);
  } else {
    revealEls.forEach(function (el) { el.classList.add('on'); });
  }

  /* ---------- dot field: 210 countries, 65 lit ---------- */
  var grid = document.getElementById('leap-grid');
  if (grid && !grid.firstChild) {
    var TOTAL = 210, USED = 65, COLS = 30;
    var svgNS = 'http://www.w3.org/2000/svg';
    var pitch = 30, r = 8.2, pad = 18;
    var rows = Math.ceil(TOTAL / COLS);
    var w = COLS * pitch, h = rows * pitch;
    grid.setAttribute('viewBox', '0 0 ' + (w + pad * 2) + ' ' + (h + pad * 2));
    grid.setAttribute('width', w + pad * 2);
    grid.setAttribute('height', h + pad * 2);

    var frag = document.createDocumentFragment();
    for (var i = 0; i < TOTAL; i++) {
      var c = document.createElementNS(svgNS, 'circle');
      var col = i % COLS, row = Math.floor(i / COLS);
      c.setAttribute('cx', pad + col * pitch + pitch / 2);
      c.setAttribute('cy', pad + row * pitch + pitch / 2);
      c.setAttribute('r', r);
      c.setAttribute('class', i < USED ? 'dot lit' : 'dot');
      c.style.transitionDelay = (i * 7) + 'ms';
      frag.appendChild(c);
    }
    grid.appendChild(frag);
  }

  /* ---------- reading progress ---------- */
  var bar = document.querySelector('.progress i');
  if (bar) {
    var ticking = false;
    var paint = function () {
      var doc = document.documentElement;
      var max = doc.scrollHeight - window.innerHeight;
      var p = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
      bar.style.transform = 'scaleX(' + p + ')';
      ticking = false;
    };
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(paint); }
    }, { passive: true });
    paint();
  }
})();

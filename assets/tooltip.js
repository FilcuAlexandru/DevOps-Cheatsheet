/****************************************************************
 * tooltip.js                                                   *
 *                                                              *
 * A single floating tooltip (position: fixed), reused for      *
 * every command. Positioned in real viewport space on hover —  *
 * prefers the right of the box, falls back to left, then       *
 * below/above, whichever actually has room. Never needs an     *
 * internal scroll and is never constrained by the narrow       *
 * content column.                                              *
 *                                                              *
 * Author: Filcu Alexandru                                      *
 ****************************************************************/

(function () {
  var tip = document.createElement('div');
  tip.id = 'floating-tip';
  tip.setAttribute('role', 'tooltip');
  document.body.appendChild(tip);

  var GAP = 12;
  var current = null;
  var hideTimer = null;

  function place(target) {
    var text = target.getAttribute('data-tip');
    if (!text) return;
    tip.textContent = text;
    tip.classList.add('visible');

    var rect = target.getBoundingClientRect();
    var tipRect = tip.getBoundingClientRect();
    var vw = window.innerWidth;
    var vh = window.innerHeight;

    var left, top;

    if (rect.right + GAP + tipRect.width <= vw) {
      left = rect.right + GAP;
      top = rect.top + rect.height / 2 - tipRect.height / 2;
    } else if (rect.left - GAP - tipRect.width >= 0) {
      left = rect.left - GAP - tipRect.width;
      top = rect.top + rect.height / 2 - tipRect.height / 2;
    } else if (rect.bottom + GAP + tipRect.height <= vh) {
      left = Math.max(8, Math.min(rect.left, vw - tipRect.width - 8));
      top = rect.bottom + GAP;
    } else {
      left = Math.max(8, Math.min(rect.left, vw - tipRect.width - 8));
      top = Math.max(8, rect.top - GAP - tipRect.height);
    }

    top = Math.max(8, Math.min(top, vh - tipRect.height - 8));
    left = Math.max(8, Math.min(left, vw - tipRect.width - 8));

    tip.style.left = left + 'px';
    tip.style.top = top + 'px';
  }

  function show(target) {
    clearTimeout(hideTimer);
    current = target;
    place(target);
  }

  function hide() {
    hideTimer = setTimeout(function () {
      tip.classList.remove('visible');
      current = null;
    }, 60);
  }

  document.querySelectorAll('.cmdline[data-tip]').forEach(function (el) {
    el.addEventListener('mouseenter', function () { show(el); });
    el.addEventListener('mouseleave', hide);
    el.addEventListener('focus', function () { show(el); });
    el.addEventListener('blur', hide);
  });

  window.addEventListener('scroll', function () {
    if (current) place(current);
  }, true);
  window.addEventListener('resize', function () {
    if (current) place(current);
  });
})();

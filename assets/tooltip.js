/****************************************************************
 * tooltip.js                                                   *
 *                                                              *
 * Flips a command's hover tooltip to open above instead of     *
 * below when there isn't enough room in the viewport.          *
 *                                                              *
 * Author: Filcu Alexandru                                      *
 ****************************************************************/

(function () {
  var els = document.querySelectorAll('.cmdline[data-tip]');
  var MIN_SPACE = 160;

  function check(el) {
    var rect = el.getBoundingClientRect();
    var spaceBelow = window.innerHeight - rect.bottom;
    if (spaceBelow < MIN_SPACE && rect.top > MIN_SPACE) {
      el.classList.add('tip-above');
    } else {
      el.classList.remove('tip-above');
    }
  }

  els.forEach(function (el) {
    el.addEventListener('mouseenter', function () { check(el); });
    el.addEventListener('focus', function () { check(el); });
  });
})();

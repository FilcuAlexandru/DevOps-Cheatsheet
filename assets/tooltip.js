/****************************************************************
 * tooltip.js                                                   *
 *                                                              *
 * Flips a command's hover tooltip to open above instead of     *
 * below when there isn't enough room in the viewport.          *
 *                                                              *
 * Author: Filcu Alexandru                                      *
 ****************************************************************/

(function () {
  var boxes = document.querySelectorAll('.cmd-box');
  var MIN_SPACE = 160;

  function check(box, cmd) {
    var rect = box.getBoundingClientRect();
    var spaceAbove = rect.top;
    var spaceBelow = window.innerHeight - rect.bottom;
    if (spaceBelow < MIN_SPACE && spaceAbove > spaceBelow) {
      cmd.classList.add('tip-above');
    } else {
      cmd.classList.remove('tip-above');
    }
  }

  boxes.forEach(function (box) {
    var cmd = box.querySelector('.cmdline[data-tip]');
    if (!cmd) return;
    box.addEventListener('mouseenter', function () { check(box, cmd); });
    box.addEventListener('focusin', function () { check(box, cmd); });
  });
})();

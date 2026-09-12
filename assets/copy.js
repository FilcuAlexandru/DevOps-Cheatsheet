/****************************************************************
 * copy.js                                                      *
 *                                                              *
 * Click-to-copy for every command box.                         *
 *                                                              *
 * Author: Filcu Alexandru                                      *
 ****************************************************************/

(function () {
  document.querySelectorAll('.copy-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var box = btn.closest('.cmd-box');
      var cmd = box.querySelector('.cmdline');
      if (!cmd) return;
      navigator.clipboard.writeText(cmd.textContent).then(function () {
        var original = btn.textContent;
        btn.textContent = 'copied';
        btn.classList.add('copied');
        setTimeout(function () {
          btn.textContent = original;
          btn.classList.remove('copied');
        }, 1200);
      });
    });
  });
})();

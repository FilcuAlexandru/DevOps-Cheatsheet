/****************************************************************
 * search.js                                                    *
 *                                                              *
 * Client-side search over window.SEARCH_INDEX.                 *
 *                                                              *
 * Author: Filcu Alexandru                                      *
 ****************************************************************/

(function () {
  var overlay = document.getElementById('search-overlay');
  var input = document.getElementById('search-input');
  var results = document.getElementById('search-results');
  var trigger = document.getElementById('search-trigger');
  var prefix = trigger ? trigger.getAttribute('data-prefix') : '';
  var index = window.SEARCH_INDEX || [];

  function open() {
    overlay.hidden = false;
    input.value = '';
    input.focus();
    render(index.slice(0, 12));
  }
  function close() {
    overlay.hidden = true;
  }
  function esc(s) {
    return s.replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }
  function render(items) {
    if (!items.length) {
      results.innerHTML = '<div class="search-empty">No matches.</div>';
      return;
    }
    results.innerHTML = items.map(function (it) {
      var href = prefix + it.page + (it.anchor ? '#' + it.anchor : '');
      return '<a class="search-result" href="' + href + '">' +
        '<div class="sr-cmd">' + esc(it.cmd) + '</div>' +
        '<div class="sr-tip">' + esc(it.tip) + '</div>' +
        '<div class="sr-meta">' + esc(it.topic) + ' &rsaquo; ' + esc(it.section) + '</div>' +
        '</a>';
    }).join('');
  }
  function search(q) {
    q = q.trim().toLowerCase();
    if (!q) { render(index.slice(0, 12)); return; }
    var scored = [];
    for (var i = 0; i < index.length; i++) {
      var it = index[i];
      var cmd = it.cmd.toLowerCase();
      var tip = it.tip.toLowerCase();
      var score = -1;
      if (cmd.indexOf(q) === 0) score = 0;
      else if (cmd.indexOf(q) !== -1) score = 1;
      else if (tip.indexOf(q) !== -1) score = 2;
      else if (it.topic.toLowerCase().indexOf(q) !== -1 || it.section.toLowerCase().indexOf(q) !== -1) score = 3;
      if (score !== -1) scored.push([score, it]);
    }
    scored.sort(function (a, b) { return a[0] - b[0]; });
    render(scored.slice(0, 30).map(function (s) { return s[1]; }));
  }

  trigger && trigger.addEventListener('click', open);
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && overlay.hidden && document.activeElement.tagName !== 'INPUT') {
      e.preventDefault();
      open();
    } else if (e.key === 'Escape' && !overlay.hidden) {
      close();
    }
  });
  overlay.addEventListener('click', function (e) {
    if (e.target === overlay) close();
  });
  input && input.addEventListener('input', function () { search(input.value); });
})();

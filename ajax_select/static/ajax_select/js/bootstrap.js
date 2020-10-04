(function(w) {
  /**
   * load jquery and jquery-ui if needed
   */

  function not(thing) {
    return typeof thing === 'undefined';
  }

  function loadJS(src) {
    document.write('<script type="text/javascript"  src="' + src + '"><\/script>');
  }

  function loadCSS(href) {
    var script = document.createElement('link');
    script.href = href;
    script.type = 'text/css';
    script.rel = 'stylesheet';
    document.head.appendChild(script);
  }

  if (not(w.jQuery)) {
    loadJS('//ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js');
  }

  if (not(w.jQuery) || not(w.jQuery.ui) || not(w.jQuery.ui.autocomplete)) {
    loadJS('//code.jquery.com/ui/1.12.1/jquery-ui.js');
    loadCSS('//code.jquery.com/ui/1.12.1/themes/smoothness/jquery-ui.css');
  }
})(window);

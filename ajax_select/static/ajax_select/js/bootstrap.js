// load jquery and jquery-ui if needed
// into window.jQuery
var firstScript = document.getElementsByTagName('script')[0];
if (typeof window.jQuery === 'undefined') {
  var newScript = document.createElement('script');
  newScript.type = 'text/javascript';
  newScript.src = '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js';
  firstScript.parentNode.insertBefore(newScript, firstScript);
}
if (typeof window.jQuery === 'undefined' || typeof window.jQuery.ui === 'undefined' || typeof window.jQuery.ui.autocomplete === 'undefined') {
  var newScript = document.createElement('script');
  newScript.type = 'text/javascript';
  newScript.src = '//code.jquery.com/ui/1.10.3/jquery-ui.js';
  firstScript.parentNode.insertBefore(newScript, firstScript);

  var newLink = document.createElement('link');
  newLink.type = 'text/css';
  newLink.rel = 'stylesheet';
  newLink.href = "//code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css"
  firstScript.parentNode.insertBefore(newLink, firstScript);
}

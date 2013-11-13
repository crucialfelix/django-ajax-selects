// load jquery and jquery-ui if needed
// into window.jQuery
if (typeof window.jQuery === 'undefined') {
  document.write('<script type="text/javascript"  src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"><\/script><script type="text/javascript"  src="//code.jquery.com/ui/1.10.3/jquery-ui.js"><\/script><link type="text/css" rel="stylesheet" href="//code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />');
} else if(typeof window.jQuery.ui === 'undefined' || typeof window.jQuery.ui.autocomplete === 'undefined') {
  document.write('<script type="text/javascript"  src="//code.jquery.com/ui/1.10.3/jquery-ui.js"><\/script><link type="text/css" rel="stylesheet" href="//code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />');
}

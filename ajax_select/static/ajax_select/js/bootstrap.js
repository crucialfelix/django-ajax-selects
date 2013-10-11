// load jquery and jquery-ui if needed
// into window.jQuery
if (typeof window.jQuery === 'undefined') {
	document.write('<script type="text/javascript"  src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"><\/script><script type="text/javascript"  src="//ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js"><\/script><link type="text/css" rel="stylesheet" href="//ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/themes/smoothness/jquery-ui.css" />');
} else if(typeof window.jQuery.ui === 'undefined') {
	document.write('<script type="text/javascript"  src="//ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js"><\/script><link type="text/css" rel="stylesheet" href="//ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/themes/smoothness/jquery-ui.css" />');
}
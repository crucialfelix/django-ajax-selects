
/* requires RelatedObjects.js */

function didAddPopup(win,newId,newRepr) {
    var name = windowname_to_id(win.name);
    $("#"+name).trigger('didAddPopup',[html_unescape(newId),html_unescape(newRepr)]);
    win.close();
}


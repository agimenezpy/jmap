function resizeApp() {
    var offsetTop = 0;
    var mapElem = $("map");
    for (var elem = mapElem; elem; elem = elem.offsetParent)  {
        offsetTop += elem.offsetTop;
    }
    var height = getWindowHeight() - offsetTop - 32;
    if (height >= 0) {
        mapElem.style.height = height + "px";
        $$(".right_page")[0].style.height =(height + 4) + "px";
        $$(".left_sidebar")[0].style.height =(height + 4) + "px";
    }
}

function getWindowHeight() {
    if (window.self && self.innerHeight) {
        return self.innerHeight;
    }
    if (document.documentElement && document.documentElement.clientHeight) {
        return document.documentElement.clientHeight;
    }
    return 0;
}

function highlightFormElements() {
    // add input box highlighting
    addFocusHandlers($$("input"));
    addFocusHandlers($$("textarea"));
}

function addFocusHandlers(elements) {
    for (i=0; i < elements.length; i++) {
        if (elements[i].type != "button" && elements[i].type != "submit" &&
            elements[i].type != "reset" && elements[i].type != "checkbox" && elements[i].type != "radio") {
            if (!elements[i].getAttribute('readonly') && !elements[i].getAttribute('disabled')) {
                elements[i].onfocus=function() {this.style.backgroundColor='#ffd';this.select()};
                elements[i].onmouseover=function() {this.style.backgroundColor='#ffd'};
                elements[i].onblur=function() {this.style.backgroundColor='';}
                elements[i].onmouseout=function() {this.style.backgroundColor='';}
            }
        }
    }
}

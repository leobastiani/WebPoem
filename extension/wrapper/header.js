/******************************************************
 * Inject
 ******************************************************/
var execFunctionGlobal = function execFunctionGlobal(fn) {
    var s = document.createElement('script');
    s.innerHTML = '(' + fn + '());';
    document.children[0].appendChild(s);
};

execFunctionGlobal(function () {
    try {

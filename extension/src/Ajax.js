let { Deferred } = require('./Deferred')

let _XMLHttpRequest = window.XMLHttpRequest
let xhrs = []

class XMLHttpRequest extends Deferred {
    constructor() {
        super()
        this.xhr = new _XMLHttpRequest();
    }

    abort() { return this.xhr.abort(...arguments); }
    getAllResponseHeaders() { return this.xhr.getAllResponseHeaders(...arguments); }
    getResponseHeader() { return this.xhr.getResponseHeader(...arguments); }
    get onabort() { return this.xhr.onabort; }
    get onerror() { return this.xhr.onerror; }
    get onload() { return this.xhr.onload; }
    get onloadend() { return this.xhr.onloadend; }
    get onloadstart() { return this.xhr.onloadstart; }
    get onprogress() { return this.xhr.onprogress; }
    get onreadystatechange() { return this.xhr.onreadystatechange; }
    get ontimeout() { return this.xhr.ontimeout; }
    open() { return this.xhr.open(...arguments); }
    overrideMimeType() { return this.xhr.overrideMimeType(...arguments); }
    get readyState() { return this.xhr.readyState; }
    get response() { return this.xhr.response; }
    get responseText() { return this.xhr.responseText; }
    get responseType() { return this.xhr.responseType; }
    get responseURL() { return this.xhr.responseURL; }
    get responseXML() { return this.xhr.responseXML; }
    setRequestHeader() { return this.xhr.setRequestHeader(...arguments); }
    get status() { return this.xhr.status; }
    get statusText() { return this.xhr.statusText; }
    get timeout() { return this.xhr.timeout; }
    get upload() { return this.xhr.upload; }
    get withCredentials() { return this.xhr.withCredentials; }

    set onabort(val) { this.xhr.onabort = val;                 return this.onabort; }
    set onerror(val) { this.xhr.onerror = val;                 return this.onerror; }
    set onload(val) { this.xhr.onload = val;                   return this.onload; }
    set onloadstart(val) { this.xhr.onloadstart = val;         return this.onloadstart; }
    set onprogress(val) { this.xhr.onprogress = val;           return this.onprogress; }
    set ontimeout(val) { this.xhr.ontimeout = val;             return this.ontimeout; }
    set readyState(val) { this.xhr.readyState = val;           return this.readyState; }
    set response(val) { this.xhr.response = val;               return this.response; }
    set responseText(val) { this.xhr.responseText = val;       return this.responseText; }
    set responseType(val) { this.xhr.responseType = val;       return this.responseType; }
    set responseURL(val) { this.xhr.responseURL = val;         return this.responseURL; }
    set responseXML(val) { this.xhr.responseXML = val;         return this.responseXML; }
    set status(val) { this.xhr.status = val;                   return this.status; }
    set statusText(val) { this.xhr.statusText = val;           return this.statusText; }
    set timeout(val) { this.xhr.timeout = val;                 return this.timeout; }
    set upload(val) { this.xhr.upload = val;                   return this.upload; }
    set withCredentials(val) { this.xhr.withCredentials = val; return this.withCredentials; }

    addEventListener() {
        return this.xhr.addEventListener(...arguments);
    }

    set onreadystatechange(cb) {
        let self = this
        this._onreadstatechange = cb
        this.xhr.onreadystatechange = function () {
            cb && cb.apply(this, arguments);
            if(self.xhr.readyState === XMLHttpRequest.DONE) {
                xhrs.splice(xhrs.indexOf(this), 1);
                self.resolve();
            }
        }
        return this.onreadystatechange
    }

    set onloadend(cb) {
        let self = this
        this._onloadend = cb
        this.xhr.onloadend = function () {
            cb && cb.apply(this, arguments);
            xhrs.splice(xhrs.indexOf(this), 1);
            self.resolve();
        }
        return this.onloadend
    }

    set onload(cb) {
        let self = this
        this._onload = cb
        this.xhr.onload = function () {
            cb && cb.apply(this, arguments);
            xhrs.splice(xhrs.indexOf(this), 1);
            self.resolve();
        }
        return this.onload
    }

    send() {
        let ret = this.xhr.send(...arguments)

        xhrs.push(this);

        return ret
    }
}

XMLHttpRequest.DONE             = _XMLHttpRequest.DONE
XMLHttpRequest.HEADERS_RECEIVED = _XMLHttpRequest.HEADERS_RECEIVED
XMLHttpRequest.LOADING          = _XMLHttpRequest.LOADING
XMLHttpRequest.OPENED           = _XMLHttpRequest.OPENED
XMLHttpRequest.UNSENT           = _XMLHttpRequest.UNSENT

window.XMLHttpRequest = XMLHttpRequest

module.exports = function () {
    // retorna uma copia da lista
    return xhrs.slice();
}
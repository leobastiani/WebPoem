// solução de
// https://stackoverflow.com/questions/858619/viewing-all-the-timeouts-intervals-in-javascript

let Deferred = require('./Deferred')

let Config = require('./Config')

class TimerDeferred extends Deferred {
    constructor(id, delay) {
        super();
        this.id = id;
        this.delay = delay;
    }
}

class TimeoutDeferred extends TimerDeferred { }
class IntervalDeferred extends TimerDeferred { }

let _setTimeout = window.setTimeout;
let _setInterval = window.setInterval;
let _clearInterval = window.clearInterval;
let _clearTimeout = window.clearTimeout;

let timers = {};

window.setTimeout = function(fn, delay) {
    let id = _setTimeout(function() {
        fn && fn();
        removeTimer(id);
    }, delay);
    timers[id] = new TimeoutDeferred(id, delay);
    return id;
};

window.setInterval = function(fn, delay) {
    let id = _setInterval(function() {
        fn && fn();
        if(timers[id]) {
            // ele pode não existir
            // devido a um clearInterval
            // que foi chamado
            // durante a função fn
            timers[id].resolve();

            // fica recriando
            // o promise
            timers[id] = new IntervalDeferred(id, delay);
        }
    }, delay);
    timers[id] = new IntervalDeferred(id, delay);
    return id;
};

window.clearInterval = function(id) {
    _clearInterval(id);
    removeTimer(id);
};

window.clearTimeout = function(id) {
    _clearTimeout(id);
    removeTimer(id);
};


function removeTimer(id) {
    if(id in timers) {
        let d = timers[id]
        delete timers[id];
        d.resolve()
    }
}

module.exports = function () {
    return Object.values(timers);
}

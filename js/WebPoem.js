(function() {

if(typeof window.WebPoem !== "undefined") {
    console.log('WebPoem já está definido');
    return window.WebPoem;
}


var WebPoem = {


    TimeSpent: function() {
        this.started = new Date();

        this.print = function () {
            var elapsed = (new Date() - this.started) / 1000;
            console.log('Tempo gasto de: ' + elapsed + 's');
        }
    },


    getText(e) {
        var res = e.innerText;
        if(res != '') {
            return res;
        }

        // se é vazio, tenta pegar o texto por atributos
        var attrs = ['value', 'placeholder'];
        for(var i=0; i<attrs.length; i++) {
            var attr = attrs[i];
            var res = e.getAttribute(attr);
            if(res) {
                if(res != '') {
                    return res;
                }
            }
        }

        return '';
    },


    stdElementText(e) {
        return WebPoem.stdQuery(this.getText(e));
    },


    stdQuery(query) {
        var query = query.trim().toLowerCase();
        if(query == '') {
            return '';
        }

        // obtém o index da primeira letra
        var cropFirst = query.match(/^\W*\w/);
        if(cropFirst) {
            cropFirst = cropFirst[0].length - 1;
            if(cropFirst) {
                query = query.substr(cropFirst, query.length - cropFirst);
            }
        }

        // obtém o index da última letra
        var lastCharIndex = query.match(/\w\W*$/).index + 1;
        query = query.substr(0, lastCharIndex);

        return query;
    },


    findElement(query) {
        /*
        TODO: Implementar esse caso
         */
        // procuro um elemento com esse ID
        /*var e = document.getElementById(query);
        if(e) {
            return $(e);
        }
        // tenta com name
        e = document.getElementsByName(query);
        if(e.length) {
            return $(e);
        }
        // tenta com o class name
        e = document.getElementsByClassName(query);
        if(e.length) {
            return $(e);
        }
        // tenta com o jquery
        e = $(query);
        if(e.length) {
            return e;
        }
        // tenta pelo valor do input (ou button)
        e = $('[value="'+query+'"]');
        if(e.length) {
            return e;
        }*/
        
        // vou tentar pelo conteúdo agora
        query = WebPoem.stdQuery(query);

        /**
         * Use try catch para obter o retorno
         * dessa função
         */
        function _findElement(els, query) {
            var children = els.children;
            // se não tenho mais filhos, paro por aqui
            if(children.length == 0) {
                return 0;
            }

            // para cada filho, faço de novo
            var maiorDeep = -1;
            for(var i=0; i<children.length; i++) {
                var c = children[i];
                var deep = _findElement(c, query) + 1;
                if(deep > maiorDeep) {
                    maiorDeep = deep;

                    if(deep <= 3) {
                        // faço a verificação do msmo
                        if(WebPoem.stdElementText(c) == query) {
                            throw c;
                        }
                    }
                }
            }

            return maiorDeep;
        }

        try {
            _findElement(document.body, query)
        } catch(e) {
            // encontrei o elemento
            return e;
        }
        return null;
    },

    /**
     * Encontra um input para o determinado elemento
     */
    findInput(e) {
        if(e == null) {
            return null;
        }

        var isInput = function (e) {
            var inputs = ['INPUT', 'SELECT', 'TEXTAREA', 'OPTION', 'BUTTON'];
            for(var i=0; i<inputs.length; i++) {
                if(e.tagName == inputs[i]) {
                    return true;
                }
            }
            return false;
        };

        if(isInput(e)) {
            return e;
        }

        var res = [];

        var _findInput = function (els) {
            for(var i=0; i<els.length; i++) {
                var e = els[i];

                if(isInput(e)) {
                    res.push(e);
                }

                _findInput(e.children);
            }
        };

        var parent = e.parentElement;
        var children = parent.children;

        _findInput(children);
        return res;
    },

    findForm(e) {
        for(var i=0; i<1000; i++) {
            if(e.tagName == 'FORM') {
                return e;
            }
            e = e.parentElement;
        }
        return null;
    },

    // quantidade de requisições e envios
    requests: 0,
    responses: 0,
    callback: null,

    onAjaxStart(method, url) {
        this.requests++;
        console.log('Start');
        console.log("this.requests:", this.requests);
        console.log("arguments:", arguments);
        console.log('');
    },

    onAjaxComplete(xhr) {
        this.responses++;
        console.log('Complete');
        console.log("this.responses:", this.responses);
        console.log("arguments:", arguments);
        console.log('');

        if(this.responses == this.requests) {
            if(this.callback) {
                this.callback();
                this.callback = null;
            }
        }
    },

    waitAjax(callback) {
        if(this.responses == this.requests) {
            // já posso retornar
            callback();
            return ;
        }

        // ele fica no aguardo
        this.callback = callback;
    },
};


var open = XMLHttpRequest.prototype.open;
XMLHttpRequest.prototype.open = function() {
    var ret = open.apply(this, arguments);

    WebPoem.onAjaxStart(arguments[0], arguments[1]);
    return ret;
}

/**
 * interceptação do ajax, no envio e recebimento da informação
 */
var send = XMLHttpRequest.prototype.send;
XMLHttpRequest.prototype.send = function() {
    var onreadystatechange = this.onreadystatechange;

    var xhr = this;
    this.onreadystatechange = function () {
        onreadystatechange.apply(this, arguments);
        if(xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            // o if veio desse site
            // https://developer.mozilla.org/pt-BR/docs/Web/API/XMLHttpRequest/onreadystatechange
            WebPoem.onAjaxComplete(xhr);
        }
    };

    var ret = send.apply(this, arguments);
    return ret;
};


// essa linha é muito importante
window.scrollTo(0, 0);
// pois, quando eu vou para outra pagina
// acontece do scroll mudar num momento em que
// não quero

window.WebPoem = WebPoem;
return WebPoem;


}());
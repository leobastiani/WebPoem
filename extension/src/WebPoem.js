if(typeof window.WebPoem !== "undefined") {
    throw 'WebPoem já está definido'
}

let Config = require('./Config')

let WebPoem = {

    /**
     * funções de temporização
     */
    timers: require('./Timer'),

    /**
     * funções de ajax
     */
    ajaxes: require('./Ajax'),

    Config,

    wait: async function () {
        // faz isso N vezes
        // para os timers que
        // criaram ajaxs
        // e os ajax que criam timers
        for(var i=0; i<Config.WAIT_N; i++) {
            // os ajax criam
            // timers
            let ajaxes = WebPoem.ajaxes()
            await Promise.all(ajaxes.map((a) => a.promise))

            // alguns ajax criam timers
            let timers = WebPoem.timers().filter((t) =>
                // o delay deve ser
                // menor do que o máximo configurado
                t.delay <= Config.MAX_DELAY
            )
            await Promise.all(timers.map((t) => t.promise))
        }
    },


    TimeSpent: function() {
        this.started = new Date()

        this.print = function () {
            let elapsed = (new Date() - this.started) / 1000
            console.log('Tempo gasto de: ' + elapsed + 's')
        }
    },


    getText(e) {
        let res = e.innerText
        if(res != '') {
            return res
        }

        // se é vazio, tenta pegar o texto por atributos
        let attrs = ['value', 'placeholder']
        for(let i=0; i<attrs.length; i++) {
            let attr = attrs[i]
            let res = e.getAttribute(attr)
            if(res) {
                if(res != '') {
                    return res
                }
            }
        }

        // está vazio, não tem jeito
        return ''
    },


    stdElementText(e) {
        return WebPoem.stdQuery(this.getText(e))
    },


    stdQuery(query) {
        if(query == '') {
            return ''
        }

        // faz um trim dos : . \s
        // dos dois lados
        query = query.replace(/^[:\.\s]*(.*?)[:\.\s]*$/, '$1')
        query = query.toLowerCase()

        return query
    },


    findElement(query) {
        // vou tentar pelo conteúdo agora
        query = WebPoem.stdQuery(query)

        /**
         * Use try catch para obter o retorno
         * dessa função
         */
        function _findElement(els, query) {
            let children = els.children
            // se não tenho mais filhos, paro por aqui
            if(children.length == 0) {
                return 0
            }

            // para cada filho, faço de novo
            let maiorDeep = -1
            for(let i=0; i<children.length; i++) {
                let c = children[i]
                let deep = _findElement(c, query) + 1
                if(deep > maiorDeep) {
                    maiorDeep = deep
                }

                if(deep <= 3) {
                    // faço a verificação do msmo
                    if(WebPoem.stdElementText(c) == query) {
                        throw c
                    }
                }
            }

            return maiorDeep
        }

        try {
            _findElement(document.body, query)
        } catch(e) {
            // encontrei o elemento
            return e
        }
        return null
    },

    /**
     * Encontra um input para o determinado elemento
     */
    findInput(e) {
        if(e == null) {
            return null
        }

        let isInput = function (e) {
            let inputs = ['INPUT', 'SELECT', 'TEXTAREA', 'OPTION', 'BUTTON']
            for(let i=0; i<inputs.length; i++) {
                if(e.tagName == inputs[i]) {
                    return true
                }
            }
            return false
        }

        if(isInput(e)) {
            return e
        }

        let res = []

        let _findInput = function (els) {
            for(let i=0; i<els.length; i++) {
                let e = els[i]

                if(isInput(e)) {
                    res.push(e)
                }

                _findInput(e.children)
            }
        }

        let parent = e.parentElement
        let children = parent.children

        _findInput(children)
        return res
    },

    findForm(e) {
        for(let i=0; i<1000; i++) {
            if(e.tagName == 'FORM') {
                return e
            }
            e = e.parentElement
        }
        return null
    },

}


// essa linha é muito importante
window.scrollTo(0, 0)
// pois, quando eu vou para outra pagina
// acontece do scroll mudar num momento em que
// não quero
window.WebPoem = WebPoem
throw WebPoem
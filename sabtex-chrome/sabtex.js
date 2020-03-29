/* TODO:
 * - Make this rely more on jQuery.
 * - Create a function to reverse the effects of wrapUniqueSpan.
 */

var sabtex = {

    extensionURL: 'chrome-extension://pcjgcbkcoaajaeabaebpoaigmiddanph/',

    getStylesheetURL: function(styleName) {
        return sabtex.extensionURL + 'poshytip/src/' + styleName + '/'
            + styleName + '.css';
    },

    wrapUniqueSpan: function(elem, id) {
        var id = id || 0;
        var children = elem.childNodes; 
        for (var i = 0; i < children.length; i++) {
            n = children[i];
            if (n.nodeType == Node.ELEMENT_NODE) {
                id = sabtex.wrapUniqueSpan(n, id);
            } else if (n.nodeType == Node.TEXT_NODE) {
                var tn_span = document.createElement('span');
                tn_span.setAttribute('class', 'sabtex_textnode');
                var words = n.nodeValue.split(' ');
                var paren = n.parentNode;
                paren.replaceChild(tn_span, n);
                for (var j=0; j < words.length; j++) {
                    var w = words[j]
                    if (!w) {
                        tn_span.appendChild(document.createTextNode(' '));
                    } else {
                        var span = document.createElement('span');
                        span.setAttribute('class', 'sabtex_word');
                        span.setAttribute('id', 'word'+id++);
                        var text = document.createTextNode(w);
                        span.appendChild(text);
                        tn_span.appendChild(span);
                        if (j < words.length-1) {
                            tn_span.appendChild(document.createTextNode(' '));
                        }
                    }
                }
            }
        }
        return id;
    },

    getRule: function() {
        var url = document.URL;
        var rules = sabtex.config.rules;
        if (!rules) {
            console.log('Cannot find ruleset.');
            sabtex.currentRule = null;
            return false;
        }
        for (var i = 0; i < rules.length; i++) {
            var r = rules[i];
            var regex = new RegExp(r.url, 'i');
            if (regex.test(url)) {
                sabtex.currentRule = r;
                return true;
            }
        }
        sabtex.currentRule = null;
        return false;
    },

    selCache: {},

    wordCache: {},

    getTranslation: function(updateCallback) {
        var rule = sabtex.currentRule;
        console.log('matched rule: ' + rule.url);
        var sel = window.getSelection();
        var isSel = sel.containsNode(this, true);
        var toTrans = isSel ? sel.toString() : this.textContent;
        console.log('to translate: '+toTrans);
        var cached = sabtex.wordCache[toTrans] || sabtex.selCache[toTrans] || '';
        if (cached) {
            return cached;
        }
        apertium.translate(toTrans, rule.source, rule.target, function(response) {
                //console.log(JSON.stringify(response));
                if (response.error) {
                    var e = response.error;
                    console.log('Error in trying to fetch translation: ' + e.code + ' ' + e.message);
                }
                var trans = response.translation;
                if (!trans) {
                    console.log('Translation is some false value: "' + toTrans + '" -> "' + trans + '"');
                    updateCallback('Could not get translation. Check console for details.');
                } else {
                    if (toTrans[0] == toTrans[0].toLowerCase()) {
                        trans = trans[0].toLowerCase() + trans.slice(1);
                    }
                    if (isSel) {
                        sabtex.selCache[toTrans] = trans;
                    } else {
                        sabtex.wordCache[toTrans] = trans;
                    }
                    updateCallback(trans);
                }
            }, sabtex.config.key);
        return '...';
    },

    handlePage: function(config) {
        sabtex.config = config;
        console.log(config);
        if (!config.isOn) {
            console.log('app is turned off');
            return;
        }
        console.log(sabtex.getStylesheetURL(config.style));
        $('head').append(
            /*$('link')
                .attr('rel', 'stylesheet')
                .attr('type', 'text/css')
                .attr('href', sabtex.getStylesheetURL(config.style))*/
            $('<link rel="stylesheet" type="text/css" href="'+sabtex.getStylesheetURL(config.style)+'">')
        );
        if (sabtex.getRule()) {
            var body = document.getElementsByTagName('body')[0];
            sabtex.wrapUniqueSpan(body);
            $('.sabtex_textnode > .sabtex_word')
                .poshytip({
                    content: sabtex.getTranslation,
                    className: 'tip-skyblue',
                    bgImageFrameSize: 9,
                    showTimeout: config.waitTime
            })
            .mouseover(function(event){
                $(this).poshytip('update', sabtex.getTranslation);
            });
        }
    },

    load: function() {
        chrome.extension.sendMessage({action: 'load_data'}, function(response){
            sabtex.handlePage(response);
        });
    }
};

$(document).ready(sabtex.load);

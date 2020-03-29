/* This is a re-implementation of the library provided by the Apertium people.
 * The main difference is that it doesn't rely on executing code returned by
 * the web service (which seems to disagree with Chrome's security policies
 * for extensions). It also has a few extra features that the official library
 * lacks. */

var apertium = {

    supportedLangPairs: [
        {"source": "ro","target": "es"}, {"source": "es","target": "fr"},
        {"source": "en","target": "gl"}, {"source": "oc","target": "es"},
        {"source": "es","target": "ro"}, {"source": "es","target": "ca_valencia"},
        {"source": "mk","target": "bg"}, {"source": "fr","target": "es"},
        {"source": "oc_aran","target": "ca"}, {"source": "pt","target": "gl"},
        {"source": "en","target": "ca"}, {"source": "an","target": "es"},
        {"source": "eu","target": "es"}, {"source": "es","target": "ca"},
        {"source": "fr","target": "eo"}, {"source": "es","target": "gl"},
        {"source": "ca","target": "pt"}, {"source": "nb","target": "nn_a"},
        {"source": "mk","target": "en"}, {"source": "ca","target": "en_US"},
        {"source": "pt","target": "ca"}, {"source": "is","target": "en"},
        {"source": "fr","target": "ca"}, {"source": "gl","target": "en"},
        {"source": "gl","target": "es"}, {"source": "ca","target": "oc_aran"},
        {"source": "nn","target": "nb"}, {"source": "ca","target": "oc"},
        {"source": "en","target": "es"}, {"source": "es","target": "pt"},
        {"source": "oc_aran","target": "es"}, {"source": "es","target": "eo"},
        {"source": "oc","target": "ca"}, {"source": "cy","target": "en"},
        {"source": "es","target": "en"}, {"source": "ca","target": "fr"},
        {"source": "br","target": "fr"}, {"source": "en","target": "eo"},
        {"source": "bg","target": "mk"}, {"source": "ca","target": "eo"},
        {"source": "ca","target": "en"}, {"source": "es","target": "oc_aran"},
        {"source": "sv","target": "da"}, {"source": "nn","target": "nn_a"},
        {"source": "pt","target": "es"}, {"source": "es","target": "pt_BR"},
        {"source": "es","target": "oc"}, {"source": "es","target": "an"},
        {"source": "da","target": "sv"}, {"source": "it","target": "ca"},
        {"source": "gl","target": "pt"}, {"source": "eo","target": "en"},
        {"source": "ca","target": "es"}, {"source": "es","target": "en_US"},
        {"source": "nn_a","target": "nn"},{"source": "nb","target": "nn"}
    ],

    getPageContent: function(url, callback) {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                if (xhr.status != 200) {
                    console.log('Error fetching url ' + url);
                    console.log('Error: ' + xhr.status + ' ' + xhr.statusText);
                    var error = {
                        status: xhr.status,
                        text: xhr.responseText
                    };
                } else {
                    var error = null;
                }
                callback(xhr.responseText, error);
            }
        };
        xhr.open('GET', url, true);
        xhr.send();
    },

    getTranslateURL: function(content, sourceLang, targLang, key) {
        var base = 'http://api.apertium.org/json/translate?';
        return base+'q='+encodeURIComponent(content)+'&langpair='+sourceLang+'|'+targLang
            + (key ? ('&key=' + key) : '');
    },

    translate: function(content, sourceLang, targLang, callback, key) {
        var url = apertium.getTranslateURL(content, sourceLang, targLang, key);
        console.log(url);
        apertium.getPageContent(url, function(response, error) {
            console.log(response);
            try {
                var jsonObj = JSON.parse(response);
                if (jsonObj.responseStatus != 200) {
                    var responseObj = {
                        translation: jsonObj.responseData.translatedText,
                        error: {
                            code: jsonObj.responseStatus,
                            message: jsonObj.responseDetails
                        }
                    };
                } else {
                    var responseObj = {translation: jsonObj.responseData.translatedText};
                }
            } catch(err) {
                var responseObj = {
                    translation: jsonObj.responseData.translatedText,
                    error: error
                };
            }
            callback(responseObj);
        });
    },

    getSupportedLanguagePairs: function() {
        return apertium.supportedLangPairs;
    },

    getSourceLanguages: function(targLang) {
        var sourceLangs = new Array();
        var all = apertium.supportedLangPairs;
        var added = new Object();
        if (!targLang) {
            for (var i = 0; i < all.length; i++) {
                var s = all[i].source;
                if (!added[s]) {
                    sourceLangs.push(all[i].source);
                    added[s] = true;
                }
            }
        } else {
            for (var i = 0; i < all.length; i++) {
                if (all[i].source == targLang)
                    sourceLangs.push(all[i].target);
            }
        }
        sourceLangs.sort();
        return sourceLangs;
    },

    getTargetLanguages: function(sourceLang) {
        var targLangs = new Array();
        var all = apertium.supportedLangPairs;
        var added = new Object();
        if (!sourceLang) {
            for (var i = 0; i < all.length; i++) {
                var t = all[i].target;
                if (!added[t]) {
                    targLangs.push(all[i].target);
                    added[t] = true;
                }
            }
        } else {
            for (var i = 0; i < all.length; i++) {
                if (all[i].source == sourceLang) {
                    targLangs.push(all[i].target);
                }
            }
        }
        targLangs.sort();
        return targLangs;
    },

    isTranslatablePair: function(sourceLang, targLang) {
        var all = apertium.supportedLangPairs;
        for (var i = 0; i < all.length; i++) {
            pair = all[i]
            if (pair.source == sourceLang && pair.target == targLang) {
                return true;
            }
        }
        return false;
    }
};

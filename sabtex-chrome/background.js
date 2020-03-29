/* This allows us to store user options persistently. */

var background = {

    defaults: {
        isOn: true,
        rules: [],
        waitTime: 1000,
        style: 'tip-skyblue',
        key: 'yuQJMrud/MYzXom0yy7w2sWyQ5M'
    },

    loadData: function() {
        return JSON.parse(localStorage.getItem('sabtex')) || background.defaults;
    },

    saveData: function(data) {
        localStorage.setItem('sabtex', JSON.stringify(data));
    },

    clearData: function() {
        localStorage.setItem('sabtex', '');
    }
};

chrome.extension.onMessage.addListener(
        function(request, sender, sendResponse) {
            console.log('got message '+request);
            if (request.action == 'load_data') {
                var data = background.loadData();
                console.log(data);
                sendResponse(data);
            } else if (request.action == 'save_data') {
                background.saveData(request.data);
            } else if (request.action == 'set_on_off') {
                var config = background.loadData();
                config['onOff'] = request.data;
                background.saveData(config);
            } else if (request.action == 'clear_data') {
                background.clearData();
            }
        });

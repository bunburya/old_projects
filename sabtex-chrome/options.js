optionsPage = {
    
    styles: ['tip-darkgray', 'tip-green', 'tip-skyblue', 'tip-twitter',
        'tip-violet', 'tip-yellow', 'tip-yellowsimple'],

    id: 0,

    rules: [
        {'url': '*', 'source': 'es', 'target': 'en'},
        {'url': 'foo', 'source': 'en', 'target': 'es'}    
    ],

    ruleIsEmpty: function(rule) {
        return (!(rule.url || rule.source || rule.target));
    },

    rulesAreEqual: function(r1, r2) {
        return (
                r1.url == r2.url &&
                r1.source == r2.source &&
                r1.target == r2.target
               );
    },

    deleteRule: function(rule) {
        var rules = optionsPage.rules;
        for (var i = 0; i < rules.length; i++) {
            var r = rules[i];
            if (optionsPage.rulesAreEqual(rule, r)) {
                optionsPage.rules.splice(i, 1);
                return;
            }
        }
    },

    getDropDown: function(srcTarg, filterLang, selectedLang) {
        /* srcTarg: Whether the menu is to select a source language
         *  or target languages. Values are 'source' or 'target'.
         * filterLang: Language which is selected in the other box;
         *  we want to populate the new menu with the source/target
         *  languages for this language.
         * selectedLang: Which language to select by default.
         */
        var menu = $(document.createElement('select'));
        if (srcTarg == 'source') {
            var opts = apertium.getSourceLanguages(filterLang);
            menu.addClass('source_menu');
            menu.change(optionsPage.filterTargets);
        } else if (srcTarg == 'target') {
            var opts = apertium.getTargetLanguages(filterLang);
            menu.addClass('target_menu');
        }
        for (var i = 0; i < opts.length; i++) {
            /* it appears that menu.add here does not actually add the opt */
            //menu.add(opts[i]);
            var o = $(document.createElement('option')).append(opts[i]);
            menu.append(o);
        }
        menu.val(selectedLang);
        return menu;
    },

    filterTargets: function(event) {
        /* Called when a new value is selected in a drop-down menu;
         * changes the other menu on that row so that only the valid
         * source/target languages are selectable. */
        var srcMenu = $(event.target);
        var row = srcMenu.closest('tr');
        var oldMenu = row.find('.target_menu');
        var newMenu = optionsPage.getDropDown('target', srcMenu.val(), oldMenu.val());
        newMenu.attr('name', oldMenu.attr('name'));
        oldMenu.replaceWith(newMenu);
    },
    
    getRuleRow: function(rule) {
        var name = 'langpair_'+optionsPage.id++;
        var row = $(document.createElement('tr'));
        row.attr('name', name);
        
        var urlInput = $(document.createElement('input'));
        urlInput
            .addClass('url_input')
            .attr('type', 'text')
            .attr('name', name)
            .attr('value', rule.url);
        
        var srcMenu = optionsPage.getDropDown('source', rule.target, rule.source);
        var sources = apertium.getSourceLanguages();
        for (var i = 0; i < sources.length; i++) {
            var opt = document.createElement('option');
            $(opt).append(document.createTextNode(sources[i]));
            srcMenu.append(opt);
        }
        srcMenu
            .addClass('source_menu')
            .attr('name', name)
            .val(rule.source);

        var targMenu = optionsPage.getDropDown('target', srcMenu.val(), rule.target);
        var targets = apertium.getTargetLanguages(rule.source);
        for (i = 0; i < targets.length; i++) {
            opt = $(document.createElement('option'));
            opt.append(document.createTextNode(targets[i]));
            targMenu.append(opt);
        }
        targMenu
            .addClass('target_menu')
            .attr('name', name)
            .val(rule.target);

        var button = $(document.createElement('button'));
        if (optionsPage.ruleIsEmpty(rule)) {
            var cls = 'add_button';
            var text = 'Add rule';
        } else {
            row.addClass('has_rule');
            var cls = 'delete_button';
            var text = 'Delete';
        }
        button
            .addClass(cls)
            .attr('name', name)
            .attr('type', 'button')
            .append(text)
            .click(optionsPage.onButtonClick);
        
        var elems = [urlInput, srcMenu, targMenu, button];
        for (var i = 0; i < elems.length; i++) {
            elem = elems[i];
            var cell = $(document.createElement('td'));
            cell.append(elem);
            row.append(cell);
        }
        return row;
    },
    
    removeRow: function(name) {
        $('tr[name='+name+']').remove();
    },

    getRule: function(name) {
        /* This is quite messy and inefficient, try find a better way? */
        var rule = {};
        $(':input[name="'+name+'"]').each(function() {
            var val = $(this).val();
            if ($(this).hasClass('url_input')) {
                rule.url = val;
            } else if ($(this).hasClass('source_menu')) {
                rule.source = val;
            } else if ($(this).hasClass('target_menu')) {
                rule.target = val;
            }
        });
        return rule;
    },
   
    onButtonClick: function(event) {
		event.preventDefault();
		var button = event.target;
        var name = $(button).attr('name');
        var rule = optionsPage.getRule(name);
        if ($(button).hasClass('add_button')) {
            optionsPage.removeRow(name);
            $('#rules_table')
                .append(optionsPage.getRuleRow(rule))
                .append(optionsPage.getRuleRow({}));
        } else if ($(button).hasClass('delete_button')) {
            optionsPage.deleteRule(rule);
            optionsPage.removeRow(name);
        }
    },

    onFormSubmit: function(event) {
        event.preventDefault();
        optionsPage.saveData();
    },

    saveData: function() {
        console.log('saveData entered');
        // Save on-off state
        var isOn = ($('#on_off_checkbox').attr('checked') == 'checked');
        // Save rules
        var rules = [];
        $('.has_rule').each(function(i, elem){
            row = $(elem);
            var rule = {
                url: row.find('.url_input').val(),
                source: row.find('.source_menu').val(),
                target: row.find('.target_menu').val()
            };
            rules.push(rule);
        });
        console.log(rules);
        var waitTime = parseFloat($('#wait_time_field').val());
        // Take the data we loaded at the start, update it and save it.
        // This ensures that data not altered by the options page is not
        // destroyed.
        var data = optionsPage.data;
        data.isOn = isOn;
        data.rules = rules;
        data.waitTime = waitTime;
        chrome.extension.sendMessage({action: 'save_data', data: data});
    },

    loadData: function() {
        console.log('loadData entered');
        chrome.extension.sendMessage({action: 'load_data'}, function(response){
            console.log(response);
            optionsPage.data = response;
            optionsPage.generatePage();
        });

    },

    generatePage: function() {
        var data = optionsPage.data;
        console.log(data);
        $('#on_off_checkbox').attr('checked', optionsPage.data.isOn);
        // Generate rules list
        var rules = data.rules;
        rules.push({});
        for (var r = 0; r < optionsPage.data.rules.length; r++) {
            $('#rules_table').append(optionsPage.getRuleRow(rules[r]));
        }
        
        $('#wait_time_field').val(data.waitTime);
        $('form').submit(optionsPage.onFormSubmit);
        //$('select').change(optionsPage.filterMenuOptions);
    }
}

$(document).ready(optionsPage.loadData);

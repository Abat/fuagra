define([
    'jquery',
    'underscore',
    'marionette',
    'collections',
    'models',
    'text!templates/topView.html',
    'text!templates/userTabView.html',
], function($, _, Marionette, Collections, Models, topT, userT) {

    'use strict';

    var SpecialTopView = Marionette.CompositeView.extend({
        className: 'specialTopContainer',
        template: _.template(topT),

        initialize: function() {
            console.log('Initializing SpecialTopView...');
        },
        events: {
            'click a[name="showMore"]': 'toggleShowMore'
        },
        toggleShowMore: function(e) {
            e.preventDefault();
            $('div#hideThis', this.el).toggle();
            $('div#showMore', this.el).toggle();
        }




    });
    
    var UserTabView = Marionette.ItemView.extend({
        className: 'userTabContainer',
        template: _.template(userT),

    });

    return {
        'SpecialTopView': SpecialTopView,
        'UserTabView': UserTabView
    };
});

define([
    'jquery',
    'underscore',
    'marionette',
    'collections',
    'models',
    'text!templates/topView.html',
], function($, _, Marionette, Collections, Models, topT) {

    'use strict';

    var SpecialTopView = Marionette.CompositeView.extend({
        className: 'specialTopContainer',
        template: _.template(topT),

        initialize: function() {
            console.log('Initializing SpecialTopView...');
        }




    });
    

    return {
        'SpecialTopView': SpecialTopView
    };
});

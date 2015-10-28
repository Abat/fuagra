define([
    'jquery',
    'underscore',
    'marionette',
    'collections',
    'models',
    'text!templates/sideView.html',
], function($, _, Marionette, Collections, Models, sideT) {

    'use strict';

    var SideView = Marionette.CompositeView.extend({
        className: 'sideContainer',
        template: _.template(sideT),

        initialize: function() {
            console.log('Initializing SideView...');
        }




    });


    return {
        'SideView': SideView
    };
});

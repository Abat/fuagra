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

        initialize: function(attr) {
            this.category = attr.category;
            console.log('Initializing SideView...');
        },

        onRender: function() {
            var self = this;

            if (self.category) {
                $('a[name="submitLink"]', self.el).attr('href', "/f/" + self.category + "/submit");
                $('a[name="submitText"]', self.el).attr('href', "/f/" + self.category + "/submitText");
            }


            if (this.category == "Help" || this.category == "Feedback") {
                $('a[name="submitLink"]', self.el).hide();
            }
        }
    });


    return {
        'SideView': SideView
    };
});

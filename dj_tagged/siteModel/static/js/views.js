define(['jquery', 'backbone'], function($, Backbone) {

    var SomeView = Backbone.view.extend({
        el: $('body'),
        render: function() {
            var self = this;
            $(this.el).append("<p> ##### HELLO! #### </p>");
        }
        // more view code
    });

    // export stuff
    return {
        'SomeView': SomeView
    };
});

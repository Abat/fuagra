define([
    'jquery',
    'underscore',
    'backbone',
    'collections',
    'models'
], function($, _, Backbone, Collections, Models) {

    'use strict';
    
    var CommentsItemView = Backbone.View.extend({
        tagName: 'form',
        attributes: function() {
            return {
                action: '#',
                class: 'some_class',
                id: 'some_id'
            }
        },
        initialize: function(){
            _.bindAll(this, 'render');
        },
        render: function(){
            $(this.el).html("<div class='textarea_container'>\
                <div class='textarea'>\
                    <textarea rows='1' cols='1' name='text'> </textarea>\
                </div>\
                <div class='bottom_area'>\
                    <button type='submit'> save </button>\
                </div>\
            </div>");
            return this;
        }
    });

    var CommentsView = Backbone.View.extend({
        el: $('body'),
        initialize: function(){
            _.bindAll(this, 'render');
            
            this.render();
        },
        render: function(){
            var self = this;
            $(self.el).append("<div> hello Derek </div>");
        }
    });

    return {
        'CommentsItemView': CommentsItemView,
        'CommentsView': CommentsView  
    };
});

define([
    'jquery',
    'underscore',
    'backbone',
    'collections',
    'models'
], function($, _, Backbone, Collections, Models) {

    'use strict';
    
    var CommentsItemView = Backbone.View.extend({
        tagName: 'li',
        className: 'commentsItem',
        initialize: function(){
            _.bindAll(this, 'render');
            this.listenTo(this.model, 'change', this.render);
        },
        render: function(){
            $(this.el).html("<div class='comments'>\
                <div class='commentsVote'>\
                    <div class='arrow'> <a href='#'> + </a> </div>\
                    <div class='arrow'> <a href='#'> - </a> </div>\
                </div>\
                <div class='commentsInfo'>\
                    <p class='content'>" + this.model.get('content') + "</p>\
                    <ul class='buttons'>\
                        <li class='comments_button'> <a href='#'> permalink </a> </li>\
                    </ul>\
                </div>\
            </div>");
            return this;
        }
    });

    var CommentsView = Backbone.View.extend({
        el: $('body'),
        initialize: function(attr){
            _.bindAll(this, 'render', 'appendComments');

            this.newsId = attr.newsId;
            this.collection = new Collections.CommentsListCollection([], { newsId: attr.newsId });
            
            this.render();
        },
        render: function(){
            var self = this;
            this.collection.comparator = function(model) {
                return -model.get('date_created');
            }
            this.collection.fetch({ success: function(items, response, options) {

                var csrf = $("input[name='csrfmiddlewaretoken']").val()

                $('#default_container', self.el).append("<form action='/api/comments/" + self.newsId + "/' method='post' enctype='application/json'>\
                    <fieldset><legend> Write a comment </legend>\
                    <textarea name='content'> </textarea>\
                    <input type='hidden' name='news' value='" + self.newsId + "'>\
                    <input type='hidden' name='csrfmiddlewaretoken' value='" + csrf + "'>\
                    <br><br>\
                    <input type='submit' value='Post'></fieldset>\
                    </form>");

                items.forEach(function(element, index, items) {
                    self.appendComments(element);
                });
            } });
        },
        appendComments: function(item){
            var commentsItemView = new CommentsItemView({
                model: item
            });
            $('#default_container', this.el).append(commentsItemView.render().el);
        }
    });

    return {
        'CommentsItemView': CommentsItemView,
        'CommentsView': CommentsView  
    };
});

define([
    'jquery',
    'underscore',
    'backbone',
    'collections',
    'models',
    'routers'
], function($, _, Backbone, Collections, Models, Routers) {

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
        events: {
            'submit form#newComment': 'newComment'
        },
        initialize: function(attr){
            _.bindAll(this, 'render', 'appendComments', 'newComment');

            this.newsId = attr.newsId;
            this.collection = new Collections.CommentsListCollection([], { newsId: attr.newsId });
            this.collection.comparator = function(model) {
                return -model.get('date_created').toString();
            }
            this.collection.sort();


            var self = this;
            this.collection.fetch({ success: function() {
                self.render();    
            } });
        },
        render: function(){
            var self = this;

            $('div#commentsList').empty();

            console.log('Comments view render');

            var csrf = $("input[name='csrfmiddlewaretoken']").val()

            $('div#commentsList', self.el).append("<form action='/api/comments/" + self.newsId + "/' method='post' enctype='application/json' id='newComment'>\
                <fieldset><legend> Write a comment </legend>\
                <textarea name='content'> </textarea>\
                <input type='hidden' name='news' value='" + self.newsId + "'>\
                <input type='hidden' name='csrfmiddlewaretoken' value='" + csrf + "'>\
                <br><br>\
                <input type='submit' value='Post'></fieldset>\
                </form>");

            $('div#commentsList', self.el).append("<div id='topComment'> </div>");

            this.collection.each(function(model) {
                self.appendComments(model);
            });
            App.router.navigate('comments');
        },
        appendComments: function(item){
            var commentsItemView = new CommentsItemView({
                model: item
            });
            $('div#commentsList', this.el).append(commentsItemView.render().el);
        },
        newComment: function(e){
            var self = this;
            e.preventDefault();
            var comment = this.collection.create({
                content: $("textarea[name='content']").val(),
                news: $("input[name='news']").val(),
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                date_created: Date.now()
            }, {
                success: function(resp) {
                    console.log(resp);
                    var newComment = new CommentsItemView({
                        model: comment
                    });
                    $('textarea').val('');
                    $('div#commentsList div#topComment', self.el).prepend(newComment.render().el);
                },
                error: function(err) {
                    console.log(err);
                }
            });
        }
    });

    return {
        'CommentsItemView': CommentsItemView,
        'CommentsView': CommentsView  
    };
});

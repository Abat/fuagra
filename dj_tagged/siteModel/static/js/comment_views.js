define([
    'jquery',
    'underscore',
    'backbone',
    'marionette',
    'collections',
    'models',
    'routers',
    'markdown',
    'text!templates/commentsItemView.html',
    'text!templates/commentsView.html',
], function($, _, Backbone, Marionette, Collections, Models, Routers, Micromarkdown, commentsItemT, commentsT) {

    'use strict';
    
    var CommentsItemView = Marionette.ItemView.extend({
        tagName: 'li',
        className: 'commentsItem',
        template: _.template(commentsItemT),
        
        onRender: function() {
            $('div.content', this.el).html(Micromarkdown.parse(this.model.get('content').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/\r?\n/g, '<br>')));
        },
        
        events: {
            'click a.expand': 'expand'
        },
        modelEvents: {
            'change': 'render'
        },

        expand: function(e){
            e.preventDefault();
            if ($('div.comments', this.el).hasClass('collapsed')) {
                $('div.comments', this.el).removeClass('collapsed');
                $('a.expand', this.el).text("[-]");
            } else {
                $('div.comments', this.el).addClass('collapsed');
                $('a.expand', this.el).text("[+]");
            }
        }
    });

    var CommentsView = Marionette.CompositeView.extend({
        tagName: 'div',
        template: _.template(commentsT),
        templateHelpers: function() {
            return { newsId: this.newsId };
        },

        childView: CommentsItemView,
        childViewContainer: 'ul',

        initialize: function(attr){
            console.log('Initializing CommentsView...');
            this.newsId = attr.newsId;
        },

        events: {
            'submit form#newComment': 'newComment'
        },
        collectionEvents: {
            'add': 'commentAdded'
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
                    $('div#topComment').append('<p> Your comment was posted. </p>').append(newComment.render().el);
                },
                error: function(err) {
                    console.log(err);
                }
            });
        },
        commentAdded: function(){
            console.log('New comments has been added.');
            $('textarea').val('');
            $('div#topComment').empty();
        }
    });

    return {
        'CommentsItemView': CommentsItemView,
        'CommentsView': CommentsView  
    };
});

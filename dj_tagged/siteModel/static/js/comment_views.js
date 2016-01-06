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
    'text!templates/commentsTextareaView.html',
], function($, _, Backbone, Marionette, Collections, Models, Routers, Micromarkdown, commentsItemT, commentsT, commentsTextareaT) {

    'use strict';
    
    var CommentsItemView = Marionette.ItemView.extend({
        tagName: 'li',
        className: 'commentsItem',
        template: _.template(commentsItemT),

        initialize: function(attr) {
            this.collection = attr.collection;
            this.newsId = attr.newsId;
        },
        
        onRender: function() {
            $('div.content', this.el).html(Micromarkdown.parse(this.model.get('content').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/\r?\n/g, '<br>')));
        },
        
        events: {
            'click a.expand': 'expand',
            'click a.reply': 'reply'
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
        },
        reply: function(e) {
            e.preventDefault();
            if (!$('form', this.el)[0]) {
                var commentsTextareaView = new CommentsTextareaView({ newsId: this.newsId, collection: this.collection, parentId: this.model.get('id') });
                $(this.el).append(commentsTextareaView.render().el);
            }
        }
    });

    var CommentsTextareaView = Marionette.ItemView.extend({
        tagName: 'div',
        template: _.template(commentsTextareaT),
        templateHelpers: function() {
            return { newsId: this.newsId };
        },

        initialize: function(attr){
            console.log('Initializing CommentsTextareaView...');
            this.newsId = attr.newsId;
            this.parentId = attr.parentId;
        },

        events: {
            'submit form#newComment': 'newComment',
            'click span.help a': 'toggleHelp'
        },

        newComment: function(e){
            var self = this;
            e.preventDefault();
            var comment = this.collection.create({
                content: $("textarea[name='content']", this.el).val(),
                news: $("input[name='news']", this.el).val(),
                "parent": this.parentId,
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']", this.el).val(),
                date_created: Date.now()
            }, {
                success: function(resp) {
                    console.log(resp);
                    var newComment = new CommentsItemView({
                        model: comment
                    });
                    $('form#newComment', self.el).remove();
                    $('div#topComment', self.el).empty();
                    $('div#topComment', self.el).append('<br><p><b>Your comment was posted. </b></p>').append(newComment.render().el);
                },
                error: function(err) {
                    console.log(err);
                }
            });
        },
        toggleHelp: function(e) {
            var self = this;
            e.preventDefault();
            $('div.markhelp', this.el).toggle();
        }
    });

    var CommentsView = Marionette.CompositeView.extend({
        tagName: 'div',
        template: _.template(commentsT),

        childView: CommentsItemView,
        childViewContainer: 'ul#comments',
        childViewOptions: function(model, index) {
            return {
                collection: this.collection,
                newsId: this.newsId
            }
        },

        onRender: function() {
            console.log('CommentsView onRender...');
            var commentsTextareaView = new CommentsTextareaView({ newsId: this.newsId, collection: this.collection });
            $(this.el).prepend(commentsTextareaView.render().el);
        },

        initialize: function(attr){
            this.newsId = attr.newsId;
            console.log('Initializing CommentsView...');
        },
    });

    return {
        'CommentsItemView': CommentsItemView,
        'CommentsTextareaView': CommentsTextareaView,
        'CommentsView': CommentsView  
    };
});

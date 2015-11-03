define([
    'jquery',
    'underscore',
    'backbone',
    'marionette',
    'collections',
    'models',
    'comment_views',
    'text!templates/newsView.html',
    'text!templates/newsItemView.html',
], function($, _, Backbone, Marionette, Collections, Models, Comment_Views, newsT, newsItemT) {

    'use strict';

    var parseUrl = (function () {
        var a = document.createElement('a');
        return function (url) {
            a.href = url;
            return {
                host: a.host,
                hostname: a.hostname,
                pathname: a.pathname,
                port: a.port,
                protocol: a.protocol,
                search: a.search,
                hash: a.hash
            };
        }
    })();

    var NewsItemView = Marionette.ItemView.extend({
        tagName: 'li',
        className: 'newsItem',
        template: _.template(newsItemT),
        templateHelpers: function() {
            return { urlParsed: parseUrl(this.model.get('url')) };
        },
        events: {
            'click a.up': 'upvote',
            'click a.down': 'downvote',
            'click a.comments': 'comments'
        },
        modelEvents: {
            'change': 'render'
        },
        upvote: function(e) {
            e.preventDefault();
            this.model.save({upvotes: this.model.get('upvotes') + 1}, {
                success: function(model, response, options) {
                    console.log(response);
                    console.log(model);
                },
                error: function(model, xhr, options) {
                    console.log(xhr);
                }
            });
        },
        downvote: function(e) {
            e.preventDefault();
            this.model.save({downvotes: this.model.get('downvotes') + 1}, {
                success: function(model, response, options) {
                    console.log(response);
                },
                error: function(model, xhr, options) {
                    console.log(xhr);
                }
            });
        },
        comments: function(e) {
            var self = this;
            e.preventDefault();
            console.log('comments view triggered');
            App.router.navigate('comments/' + self.model.get('id'), {trigger: true});
            /*
            var comments = new Collections.CommentsListCollection([], { newsId: this.model.get('id') });
            comments.fetch({ success: function(items, response, options) {
                var commentsView = new Comment_Views.CommentsView({ newsId: self.model.get('id'), collection: items }); 
                commentsView.render();
            }});*/
        }
    });

    var NewsView = Marionette.CompositeView.extend({
        tagName: 'div',
        template: _.template(newsT),

        childView: NewsItemView,
        childViewContainer: 'ul',

        initialize: function() {
            console.log('Initializing NewsView...');
            this.pageNum = 1;
        },

        events: {
            'click a#nextPage': 'nextPage',
            'click a#prevPage': 'prevPage'
        },
        collectionEvents: {
            "sync": 'newsSync'
        },

        newsSync: function() {
            console.log('News collection synced');    
        },
        nextPage: function(e) {
            e.preventDefault();
            this.pageNum += 1;
            this.fetch();
        },
        prevPage: function(e) {
            e.preventDefault();
            this.pageNum -= 1;
            this.fetch();
        },
        fetch: function() {
            var self = this;
            this.collection.fetch({data: {page: this.pageNum},  success: function(items, response, options) {
                console.log('success: ', response);
            }, error: function(collection, response, options) {
                console.log('error: ', response);
                self.pageNum = 1;
            }});
        }
    });

    // export stuff
    return {
        'NewsView': NewsView,
        'NewsItemView': NewsItemView
    };
});

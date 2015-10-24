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
        }
    });

    /*
    var NewsItemView = Backbone.View.extend({
        tagName: 'li',
        className: 'newsItem',
        events: {
            'click a.up': 'upvote',
            'click a.down': 'downvote',
            'click a.comments': 'comments'
        },
        initialize: function(){
            _.bindAll(this, 'render', 'upvote', 'downvote', 'comments');
            this.listenTo(this.model, 'change', this.render);
        },
        render: function(){
            this.url = parseUrl(this.model.get('url'));

            var score = this.model.get('upvotes') - this.model.get('downvotes');

            $(this.el).html("<div class='news'>\
                <div class='newsVote'>\
                    <div class='arrow'> <a href='#' class='up'> + </a> </div>\
                    <div class='score'>" + score + "</div>\
                    <div class='arrow'> <a href='#' class='down'> - </a> </div>\
                </div>\
                <div class='newsInfo'>\
                    <p class='title'>\
                        <a target='_blank' href='" + this.model.get('url') + "'>" + this.model.get('title') + "</a>\
                        <span class='source'> <a target='_blank' href='http://" + this.url.hostname + "'> ( " + this.url.hostname + " ) </a> </span>\
                    </p>\
                    <ul class='buttons'>\
                        <li class='comments_button'> <a href='/api/comments/" + this.model.get('id') + "' class='comments'> comments </a> </li>\
                    </ul>\
                </div>\
            </div>");
            return this;
        },
        upvote: function(e) {
            e.preventDefault();
            this.model.save({upvotes: this.model.get('upvotes') + 1}, {
                success: function(model, response, options) {
                    console.log(response);
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
            e.preventDefault();
            console.log('comments view triggered');
            $('ul#newsList').empty();
            var commentsView = new Comment_Views.CommentsView({ newsId: this.model.get('id') }); 
        }
    });
    */

    var NewsView = Marionette.CompositeView.extend({
        el: '#commentsList',
        tagName: 'div',
        template: _.template(newsT),

        childView: NewsItemView,
        childViewContainer: 'ul',

        collectionEvents: {
            "sync": 'newsSync'
        },

        modelEvents: {
            change: 'render'
        },

        initialize: function() {
            console.log('Initializing NewsView...');
        },

        newsSync: function() {
            console.log('Collection synced');    
        }
    });

    /*
    var NewsView = Backbone.View.extend({
        el: $('body'),
        events: {
            'click a#nextPage': 'nextPage',
            'click a#prevPage': 'prevPage'
        },
        initialize: function(){
            _.bindAll(this, 'render', 'appendNews', 'nextPage', 'prevPage');
            
            this.collection = new Collections.NewsListCollection();

            this.nextPage = 1;
            this.prevPage = 1;
            this.render(1);
        },
        render: function(pageNum){

            console.log("newsview render");

            var self = this;
            this.collection.comparator = function(model) {
                return -model.get('date_created');
            }
            this.collection.sort();
            this.collection.fetch({data: {page: pageNum},  success: function(items, response, options) {
                $('div.container a#nextPage', self.el).remove();
                $('div.container a#prevPage', self.el).remove();
                $('ul#newsList', self.el).empty();

                items.forEach(function(element, index, items) {
                    self.appendNews(element);
                });

                if (response.previous) {
                    if (response.previous.match(/\d+/)) {
                        self.prevPage = response.previous.match(/\d+$/)[0];
                        $('span#newsListNav', self.el).append("<a href='#' id='prevPage'> <--Previous-- </a>");
                    }
                }

                if (response.next) {
                    if (response.next.match(/\d+$/)) {
                        self.nextPage = response.next.match(/\d+$/)[0];
                        $('span#newsListNav', self.el).append("<a href='#' id='nextPage'> --Next--> </a>");
                    }
                }

                App.router.navigate('');
            } });
        },
        appendNews: function(item){
            var newsItemView = new NewsItemView({
                model: item
            });
            $('ul#newsList', this.el).append(newsItemView.render().el);
        },
        nextPage: function(){
            this.render(this.nextPage);
        },
        prevPage: function(){
            this.render(this.prevPage);
        }
    });
    */

    // export stuff
    return {
        'NewsView': NewsView,
        'NewsItemView': NewsItemView
    };
});

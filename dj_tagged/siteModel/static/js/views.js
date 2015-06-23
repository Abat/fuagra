define([
    'jquery',
    'underscore',
    'backbone',
    'collections',
    'models'
], function($, _, Backbone, Collections, Models) {

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

    var NewsItemView = Backbone.View.extend({
        tagName: 'li',
        events: {
            'click a.up': 'upvote',
            'click a.down': 'downvote'
        },
        initialize: function(){
            _.bindAll(this, 'render', 'upvote', 'downvote');
            this.listenTo(this.model, 'change', this.render);
        },
        render: function(){
            this.url = parseUrl(this.model.get('url'));

            $(this.el).html("<div class='news'>\
                <div class='newsVote'>\
                    <div class='arrow'> <a href='#' class='up'> + </a> </div>\
                    <div class='score'>" + this.model.get('likes') + "</div>\
                    <div class='arrow'> <a href='#' class='down'> - </a> </div>\
                </div>\
                <div class='newsInfo'>\
                    <p class='title'>\
                        <a target='_blank' href='" + this.model.get('url') + "'>" + this.model.get('title') + "</a>\
                        <span class='source'> <a target='_blank' href='http://" + this.url.hostname + "'> ( " + this.url.hostname + " ) </a> </span>\
                    </p>\
                    <ul class='buttons'>\
                        <li class='comments_button'> <a href='comments'> comments </a> </li>\
                    </ul>\
                </div>\
            </div>");
            return this;
        },
        upvote: function(e) {
            e.preventDefault();
            this.model.save({likes: this.model.get('likes') + 1}, {
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
            this.model.save({likes: this.model.get('likes') - 1}, {
                success: function(model, response, options) {
                    console.log(response);
                },
                error: function(model, xhr, options) {
                    console.log(xhr);
                }
            });
        }
    });

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

    // export stuff
    return {
        'NewsView': NewsView,
        'NewsItemView': NewsItemView
    };
});

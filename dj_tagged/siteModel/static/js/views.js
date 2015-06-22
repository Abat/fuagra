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
        initialize: function(){
            _.bindAll(this, 'render');
        },
        render: function(){
            this.url = parseUrl(this.model.get('url'));

            $(this.el).html("<div class='news'>\
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
        }
    });

    var NewsView = Backbone.View.extend({
        el: $('body'),
        events: {
            'click a#nextPage': 'nextPage'
        },
        initialize: function(){
            _.bindAll(this, 'render', 'appendNews', 'nextPage');
            
            this.collection = new Collections.NewsListCollection();

            this.nextPage = 1;
            this.prevPage = 1;
            this.render();
        },
        render: function(){
            var self = this;
            this.collection.comparator = function(model) {
                return model.get('date_created');
            }
            this.collection.sort();
            this.collection.fetch({data: {page: this.nextPage},  success: function(items, response, options) {
                var matches = response.next.match(/\d+$/);
                if (matches) {
                    self.nextPage = matches[0];
                }
        
                $('.container', self.el).append("<a href='#' id='nextPage'> Next </a>");
                items.forEach(function(element, index, items) {
                    self.appendNews(element);
                });
            } });
        },
        appendNews: function(item){
            var newsItemView = new NewsItemView({
                model: item
            });
            $('ul#newsList', this.el).append(newsItemView.render().el);
        },
        nextPage: function(){
            $('div.container a#nextPage', this.el).remove();
            $('ul#newsList', this.el).empty();
            this.render();
        }
    });

    // export stuff
    return {
        'NewsView': NewsView,
        'NewsItemView': NewsItemView
    };
});

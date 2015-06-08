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
        initialize: function(){
            _.bindAll(this, 'render', 'appendNews');
            
            this.collection = new Collections.NewsListCollection();

            this.render();
        },
        render: function(){
            var self = this;
            this.collection.comparator = function(model) {
                return model.get('date_created');
            }
            this.collection.sort();
            this.collection.fetch({ success: function(items, response, options) {
                $('.container', self.el).append("<a href='" + response.next + "'> Next </a>");
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
        }
    });

    // export stuff
    return {
        'NewsView': NewsView,
        'NewsItemView': NewsItemView
    };
});

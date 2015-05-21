$(document).ready(function() {

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
    
    (function($){

        var NewsItem = Backbone.Model.extend({
            defaults: {
                title: '',
                date_created: '2015-03-22',
                date_updated: '2015-03-22',
                likes: 0,
                views: 0,
                url: '#',
                num_comments: 0                
            }
        });

        var NewsList = Backbone.Collection.extend({
            model: NewsItem,
            url: '/api/news'
        });


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
                            <li class='comments_button'> <a href='#'> comments </a> </li>\
                        </ul>\
                    </div>\
                </div>");
                return this;
            }
        });

        var NewsView = Backbone.View.extend({
            el: $('body'),
            events: {
                'click button#add': 'addNews'
            },
            initialize: function(){
                _.bindAll(this, 'render', 'addNews', 'appendNews');
                
                this.collection = new NewsList();
                this.collection.bind('add', this.appendNews);

                this.counter = 0;
                this.render();
            },
            render: function(){
                var self = this;
                $(this.el).append("<button id='add'> Add news </button>");
                this.collection.fetch({ success: function(items) {
                    items.each(function(item){
                        self.appendNews(item);
                    });
                } });
            },
            addNews: function(){
                this.counter++;
                var newsItem = new NewsItem();
                newsItem.set({
                    title: newsItem.get('title') + this.counter
                });
                this.collection.add(newsItem);
            },
            appendNews: function(item){
                var newsItemView = new NewsItemView({
                    model: item
                });
                $('ul#newsList', this.el).append(newsItemView.render().el);
            }
        });

        var newsView = new NewsView();
    })(jQuery);
});

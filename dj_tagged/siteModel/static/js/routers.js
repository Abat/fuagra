define([
    'jquery',
    'underscore',
    'backbone',
    'marionette',
    'collections',
    'models',
    'views',
    'comment_views',
    'side_views',
    'top_views',
], function($, _, Backbone, Marionette, Collections, Models, Views, Comment_Views, Side_Views, Top_Views) {

    'use strict';

    var MyRouter = Marionette.AppRouter.extend({
        appRoutes: {

        },

        routes: {
            "": "home",
            "comments/:newsId": "comments",
            "*nomatch": "notFound"
        },

        home: function() {
            console.log("home route triggered");
            var news = new Collections.NewsListCollection();
            var sideView = new Side_Views.SideView();
            var specialTopView = new Top_Views.SpecialTopView();
            news.fetch({ success: function(items, response, options) {
                var newsView = new Views.NewsView({ collection: items });
                App.rootLayout.getRegion('content').show(newsView);
                App.rootLayout.getRegion('side').show(sideView);
                App.rootLayout.getRegion('special_top').show(specialTopView);
            }});
        },

        comments: function(newsId) {
            console.log("comments route triggered: ", newsId);
            var comments = new Collections.CommentsListCollection([], { newsId: newsId });
            var news = new Collections.NewsListCollection();
            news.fetch({ success: function(items, response, options) {
                var newsModel = items.get(newsId);
                App.rootLayout.getRegion('special_top').show(new Views.NewsItemView({model: newsModel}));  
                comments.fetch({ success: function(items, response, options) {
                    var commentsView = new Comment_Views.CommentsView({ newsId: newsId, collection: items }); 
                    App.rootLayout.getRegion('content').show(commentsView);
                }});
            }});
        },
        notFound: function() {
            console.log("Route not found: ", arguments);
        }
    });

    return {
        'MyRouter': MyRouter
    };
});

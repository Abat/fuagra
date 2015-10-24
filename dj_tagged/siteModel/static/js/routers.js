define([
    'jquery',
    'underscore',
    'backbone',
    'marionette',
    'collections',
    'views',
    'comment_views',
], function($, _, Backbone, Marionette, Collections, Views, Comment_Views) {

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
            news.fetch({ success: function(items, response, options) {
                var newsView = new Views.NewsView({ collection: items });
                newsView.render();
            }});
        },

        comments: function(newsId) {
            console.log("comments route triggered: ", newsId);
            var commentsView = new Comment_Views.CommentsView({ newsId: newsId });
        },
        notFound: function() {
            console.log("Route not found: ", arguments);
        }
    });

    return {
        'MyRouter': MyRouter
    };
});

define([
    'jquery',
    'underscore',
    'backbone',
    'marionette',
    'url',
    'collections',
    'models',
    'views',
    'comment_views',
    'side_views',
    'top_views',
], function($, _, Backbone, Marionette, Url, Collections, Models, Views, Comment_Views, Side_Views, Top_Views) {

    'use strict';

    var MyRouter = Marionette.AppRouter.extend({
        appRoutes: {

        },

        routes: {
            "": "home",

            "submit": "submit",
            "submitText": "submitText",
            "f/:category/submit": "submit",
            "f/:category/submitText": "submitText",

            "f/:category": "subfuas",
            "comments/:newsId": "comments",
            "administer": "administer",
            "*nomatch": "notFound"
        },

        home: function() {
            var sort_sort = url('?sort') ? url('?sort') : 'None';

            var sideView = new Side_Views.SideView();
            var specialTopView = new Top_Views.SpecialTopView();
            App.news.fetch({ data: $.param({ sort: sort_sort }), success: function(items, response, options) {
                var newsView = new Views.NewsView({ collection: items });
                App.rootLayout.getRegion('content').show(newsView);
                App.rootLayout.getRegion('side').show(sideView);
                App.rootLayout.getRegion('special_top').show(specialTopView);
            }});
        },
        submit: function(category) {
            console.log("submit route triggered...");
            var news = new Collections.NewsListCollection();
            var specialTopView = new Top_Views.SpecialTopView();
            var submitLinkView = new Views.SubmitLinkView({ collection: news, category: category });
            App.rootLayout.getRegion('content').show(submitLinkView);
            App.rootLayout.getRegion('special_top').show(specialTopView);
        },
        submitText: function(category) {
            console.log("submitText route triggered...");
            var news = new Collections.NewsListCollection();
            var specialTopView = new Top_Views.SpecialTopView();
            var submitTextView = new Views.SubmitTextView({ collection: news, category: category });
            App.rootLayout.getRegion('content').show(submitTextView);
            App.rootLayout.getRegion('special_top').show(specialTopView);
        },
        subfuas: function(category) {
            var sort_sort = url('?sort') ? url('?sort') : 'None';

            var sideView = new Side_Views.SideView({ category: category });
            var specialTopView = new Top_Views.SpecialTopView();
            App.news.fetch({ data: $.param({ category: category, sort: sort_sort }), success: function(items, response, options) {
                var newsView = new Views.NewsView({ collection: items, category: category, sort: sort_sort });
                App.rootLayout.getRegion('content').show(newsView);
                App.rootLayout.getRegion('side').show(sideView);
                App.rootLayout.getRegion('special_top').show(specialTopView);
            }});
        },
        comments: function(newsId) {
            console.log("comments route triggered: ", newsId);
            var comments = new Collections.CommentsListCollection([], { newsId: newsId });
            var newsModel = new Models.NewsItemModel({ id: newsId });
            newsModel.fetch({ success: function(model, response, options) {
                App.rootLayout.getRegion('special_top').show(new Views.NewsItemView({model: model, textPost: model.get('content')}));  
                comments.fetch({ success: function(items, response, options) {
                    var commentsView = new Comment_Views.CommentsView({ newsId: newsId, collection: items }); 
                    App.rootLayout.getRegion('content').show(commentsView);
                }});
            }});
        },
        administer: function() {
            console.log("administer route triggered...");
            var administerView = new Views.AdministerView();
            App.rootLayout.getRegion('content').show(administerView);
        },
        notFound: function() {
            console.log("Route not found: ", arguments);
        }
    });

    return {
        'MyRouter': MyRouter
    };
});

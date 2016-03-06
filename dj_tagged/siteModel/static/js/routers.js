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

        // order matters, be careful when changing
        routes: {

            "submit": "submit",
            "submitText": "submitText",
            "f/:category/submit": "submit",
            "f/:category/submitText": "submitText",

            "f/:category/administer": "administer",

            "f/:category": "subfuas",
            "f/:category/:sort": "subfuas",

            "comments/:newsId": "comments",

            "(:sort)": "home",
            "*nomatch": "notFound"
        },

        home: function(sort) {
            var sort_sort = sort || 'None';
            var page = url('?page') ? url('?page') : 1;

            var sideView = new Side_Views.SideView();
            var specialTopView = new Top_Views.SpecialTopView();
            App.news.fetch({ data: $.param({ sort: sort_sort, page: page }), success: function(items, response, options) {
                var newsView = new Views.NewsView({ collection: items, sort: sort_sort, page: page, fetchResponse: response });
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
        subfuas: function(category, sort) {
            var sort_sort = sort || 'None';
            var page = url('?page') ? url('?page') : 1;

            $.ajax({
                type: 'GET',
                url: "/api/users/" + category,
                success: function(data) {
                    var sideView = new Side_Views.SideView({ category: category, permission: data.permission });
                    var specialTopView = new Top_Views.SpecialTopView();
                    App.news.fetch({ data: $.param({ category: category, sort: sort_sort, page: page }), success: function(items, response, options) {
                        var newsView = new Views.NewsView({ page: page, collection: items, category: category, sort: sort_sort, permission: data.permission, fetchResponse: response });
                        App.rootLayout.getRegion('content').show(newsView);
                        App.rootLayout.getRegion('side').show(sideView);
                        App.rootLayout.getRegion('special_top').show(specialTopView);
                    }});
                }
            });
        },
        comments: function(newsId) {
            console.log("comments route triggered: ", newsId);
            var comments = new Collections.CommentsListCollection([], { newsId: newsId });
            var newsModel = new Models.NewsItemModel({ id: newsId });
            newsModel.fetch({ success: function(model, response, options) {
                App.rootLayout.getRegion('special_top').show(new Views.NewsItemView({model: model, textPost: model.get('content')}));  
                comments.fetch({ success: function(items, response, options) {
				
					console.log("items: ", items);
					
					var new_items = items;
					console.log("new items: ", new_items);
					
					//create leveled lists
					var i;
					var j;
					
					var level0list = [];
					for(i = 0; i < new_items.length; i ++) {
						if (new_items.models[i].attributes.parent == null) {
							level0list.push(new_items.models[i]);
							new_items.remove(new_items.models[i]);
							i --;
						}
					}
					
					var levelLists = [];
					var prevlevellist = level0list;
					while(new_items.length > 0) {
						console.log("new_items.length", new_items.length);
						console.log("prevlevellist", prevlevellist);
						var curlevellist = [];
						for(i = 0; i < new_items.length; i ++) {
							var flag = false;
							for(j = 0; j < prevlevellist.length; j ++) {
								if (new_items.models[i].attributes.parent == prevlevellist[j].attributes.id)
									flag = true;
							}
							if(flag) {
								curlevellist.push(new_items.models[i]);
								new_items.remove(new_items.models[i]);
								i --;
							}
						}
                        if(curlevellist.length == 0) break;
						levelLists.push(curlevellist);
						prevlevellist = curlevellist;
					}
					
					var lv0 = new Collections.CommentsListCollection([], { newsId: newsId });
					lv0.add(level0list);

                    $.ajax({
                        type: 'GET',
                        url: "/api/users/" + model.get('category'),
                        success: function(data) {
                            var commentsView = new Comment_Views.CommentsView({ newsId: newsId, collection: lv0, permission: data.permission });
                            
                            commentsView.childCollection = levelLists;
                            //var commentsView = new Comment_Views.CommentsView({ newsId: newsId, collection: items});
                            App.rootLayout.getRegion('content').show(commentsView);			
                        }
                    });
                }});
            }});
        },
        administer: function(category) {
            console.log("administer route triggered...");
            var administerView = new Views.AdministerView({ category: category });
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

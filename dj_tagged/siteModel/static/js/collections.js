// collesctions
define([
    'jquery',
    'underscore',
    'backbone',
    'models'
], function($, _, Backbone, Models){
    
    'use strict';

    var NewsList = Backbone.Collection.extend({
        model: Models.NewsItemModel,
        url: '/api/news/',
        parse: function(response) {
            return response;
        }
    });

    var CommentsList = Backbone.Collection.extend({
        initialize: function(models, options) {
            this.options=options;
        },
        model: Models.CommentsItemModel,
        url: function() { return '/api/comments/' + this.options.newsId + '/'; },
        parse: function(response) {
            return response;
        } 
    });

    var UserCommentsList = Backbone.Collection.extend({
        initialize: function(models, options) {
            this.options=options;
        },
        model: Models.CommentsItemModel,
        url: '/api/comments',
        parse: function(response) {
            return response;
        }
    });

    return {
        'NewsListCollection': NewsList,
        'CommentsListCollection': CommentsList,
        'UserCommentsListCollection': UserCommentsList
    };   
});

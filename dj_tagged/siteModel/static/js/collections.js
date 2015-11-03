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
            return response.results;
        }
    });

    var CommentsList = Backbone.Collection.extend({
        initialize: function(models, options) {
            this.options=options;
        },
        model: Models.CommentsItemModel,
        comparator: function(model) {
            return model.get('-date_created');
        },
        url: function() { return '/api/comments/' + this.options.newsId + '/'; },
        parse: function(response) {
            return response.results;
        } 
    });

    return {
        'NewsListCollection': NewsList,
        'CommentsListCollection': CommentsList
    };   
});

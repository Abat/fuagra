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
        model: Models.CommentsItemModel,
        url: '/api/comments/' + '1',
        parse: function(response) {
            return response.results;
        } 
    });

    return {
        'NewsListCollection': NewsList,
        'CommentsListCollection': CommentsList
    };   
});

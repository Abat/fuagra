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

    return {
        'NewsListCollection': NewsList
    };   
});

// models
define([
    'jquery',
    'underscore',
    'backbone'
], function($, _, Backbone){
    
    'use strict';

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

    return {
        'NewsItemModel': NewsItem
    };
});

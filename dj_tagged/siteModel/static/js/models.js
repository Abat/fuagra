// models
define([
    'jquery',
    'underscore',
    'backbone'
], function($, _, Backbone){
    
    'use strict';

    var NewsItem = Backbone.Model.extend({

    });

    var CommentsItem = Backbone.Model.extend({

    });

    return {
        'NewsItemModel': NewsItem,
        'CommentsItemModel': CommentsItem
    };
});

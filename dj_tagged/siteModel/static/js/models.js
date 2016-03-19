// models
define([
    'jquery',
    'underscore',
    'backbone'
], function($, _, Backbone){
    
    'use strict';

    var NewsItem = Backbone.Model.extend({
        urlRoot: '/api/news/',
        defaults: {
            "upvotes": 0,
            "downvotes": 0, 
            "thumbnail_image": '#',
            'title': 'unknown',
            'date_created': '3182016',
            'username': 'unknown',
            'category': 'Test',
            'id': 0,
            'num_comments': 0,
        }
    });

    var CommentsItem = Backbone.Model.extend({

    });

    var UserProfileItem = Backbone.Model.extend({
        idAttribute: 'username',
        urlRoot: '/api/users/'
    });

    var VoteItem = Backbone.Model.extend({
        urlRoot: function() { return this.get('url_created') },
    });

    var CommentVoteItem = Backbone.Model.extend({
        urlRoot: function() { return this.get('url_created') },
    });

    var UserRoleItem = Backbone.Model.extend({
        urlRoot: '/api/permissions/'
    });

    return {
        'NewsItemModel': NewsItem,
        'CommentsItemModel': CommentsItem,
        'UserProfileItemModel': UserProfileItem,
        'VoteItemModel': VoteItem,
        'CommentVoteItemModel': CommentVoteItem,
        'UserRoleItemModel': UserRoleItem
    };
});

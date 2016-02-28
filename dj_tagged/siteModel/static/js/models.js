// models
define([
    'jquery',
    'underscore',
    'backbone'
], function($, _, Backbone){
    
    'use strict';

    var NewsItem = Backbone.Model.extend({
        urlRoot: '/api/news/'        
    });

    var CommentsItem = Backbone.Model.extend({

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
        'VoteItemModel': VoteItem,
        'CommentVoteItemModel': CommentVoteItem,
        'UserRoleItemModel': UserRoleItem
    };
});

define([
    'jquery',
    'underscore',
    'backbone',
    'marionette',
    'collections',
    'models',
    'comment_views',
    'text!templates/newsView.html',
    'text!templates/newsItemView.html',
    'text!templates/submitLinkView.html',
    'text!templates/administerView.html',
], function($, _, Backbone, Marionette, Collections, Models, Comment_Views, newsT, newsItemT, submitLinkT, administerT) {

    'use strict';

    var parseUrl = (function () {
        var a = document.createElement('a');
        return function (url) {
            a.href = url;
            return {
                host: a.host,
                hostname: a.hostname,
                pathname: a.pathname,
                port: a.port,
                protocol: a.protocol,
                search: a.search,
                hash: a.hash
            };
        }
    })();
    var VoteItem = Backbone.Model.extend({
        urlRoot: function() { return this.get('url_created') },
    });
    var NewsItemView = Marionette.ItemView.extend({
        tagName: 'li',
        className: 'newsItem',
        template: _.template(newsItemT),
        templateHelpers: function() {
            return { urlParsed: parseUrl(this.model.get('url')) };
        },
        events: {
            'click a.up': 'upvote',
            'click a.down': 'downvote',
            'click a.comments': 'comments'
        },
        modelEvents: {
            'change': 'render'
        },
        upvote: function(e) {
            e.preventDefault();
            var self = this;
            var vote = new VoteItem({'url_created': '/api/news/' + this.model.id + '/upvote/'});

            vote.save({news:this.model.id}, {
                success: function(model, response, options){
                    var upvoteDelta = parseInt(response.upvote);
                    var downvoteDelta = 0;
                    if (response.downvote) {
                        downvoteDelta = parseInt(response.downvote);
                    }
                    console.log('News have been upvoted: ', self.model.id);
                    self.model.set({upvotes: self.model.get('upvotes') + upvoteDelta, downvotes: self.model.get('downvotes') + downvoteDelta})
                    $('div.score', self.el).css({"color" : "green", "font-weight" : "bold"});
                },
                error: function(model, xhr, options){
                    console.log('Upvote error: ', xhr);
                }
            });
        },
        downvote: function(e) {
            e.preventDefault();
            var self = this;
            var vote = new VoteItem({'url_created': '/api/news/' + this.model.id + '/downvote/'});

            vote.save({news:this.model.id}, {
                success: function(model, response, options){
                    var downvoteDelta = parseInt(response.downvote);
                    var upvoteDelta = 0;
                    if (response.upvote) {
                        upvoteDelta = parseInt(response.upvote);
                    }
                    console.log('News have been downvoted: ', self.model.id);
                    self.model.set({downvotes: self.model.get('downvotes') + downvoteDelta, upvotes: self.model.get('upvotes') + upvoteDelta})
                    $('div.score', self.el).css({"color" : "red", "font-weight" : "bold"});
                },
                error: function(model, xhr, options){
                    console.log('Downvote error: ', xhr);
                }
            });
        },
        comments: function(e) {
            var self = this;
            e.preventDefault();
            console.log('comments view triggered');
            App.router.navigate('comments/' + self.model.get('id'), {trigger: true});
        }
    });

    var SubmitLinkView = Marionette.ItemView.extend({
        tagName: 'div',
        className: 'submitLinkView',
        template: _.template(submitLinkT),
        initialize: function() {
            console.log('Initializing SubmitLinkView...');
        },
        onBeforeRender: function() {
            var self = this;
            $.ajax({
                type: 'GET',
                url: "/api/categories",
                success: function(data) {
                    $('select[name="category"] option').remove();
                    $.each(data, function(index, item) {
                        $('select[name="category"]').append(
                            $("<option></option>")
                                .text(item.title)
                                .val(item.title)
                        );
                    });
                }
            });
        },
        events: {
            'submit form#newPost': 'newPost'
        },
        newPost: function(e) {
            var self = this;
            e.preventDefault();
            console.log('New link post...');
            var post = this.collection.create({
                title: $("input[name='title']", this.el).val(),
                url: $("input[name='url']", this.el).val(),
                category: $("select[name='category']", this.el).val(),
            }, {
                success: function(resp) {
                    console.log("Success, a new link post: ", resp);
                    $(self.el).empty().append('<br><p><b>Thanks for your link!</b></p>');
                },
                error: function(err) {
                    console.log("Error: ", err);
                    $(self.el).empty().append('<br><p><b>Something went wrong...</b></p>');
                }
            });
        }
    });

    var AdministerView = Marionette.ItemView.extend({
        tagName: 'div',
        className: 'administerView',
        template: _.template(administerT),
        initialize: function() {
            console.log('Initializing AdministerView...');
        },
        onBeforeRender: function() {
            var self = this;
            $.ajax({
                type: 'GET',
                url: "/api/categories",
                success: function(data) {
                    $('select[name="category"] option').remove();
                    $.each(data, function(index, item) {
                        $('select[name="category"]').append(
                            $("<option></option>")
                                .text(item.title)
                                .val(item.title)
                            );
                    });
                }
            });
        }
    });

    var NewsView = Marionette.CompositeView.extend({
        tagName: 'div',
        template: _.template(newsT),

        childView: NewsItemView,
        childViewContainer: 'ul',

        initialize: function() {
            console.log('Initializing NewsView...');
            this.pageNum = 1;
        },

        events: {
            'click a#nextPage': 'nextPage',
            'click a#prevPage': 'prevPage'
        },
        collectionEvents: {
            "sync": 'newsSync'
        },

        newsSync: function() {
            console.log('News collection synced');    
        },
        nextPage: function(e) {
            e.preventDefault();
            this.pageNum += 1;
            this.fetch();
        },
        prevPage: function(e) {
            e.preventDefault();
            this.pageNum -= 1;
            this.fetch();
        },
        fetch: function() {
            var self = this;
            this.collection.fetch({data: {page: this.pageNum},  success: function(items, response, options) {
                console.log('success: ', response);
            }, error: function(collection, response, options) {
                console.log('error: ', response);
                self.pageNum = 1;
            }});
        }
    });

    // export stuff
    return {
        'NewsView': NewsView,
        'NewsItemView': NewsItemView,
        'SubmitLinkView': SubmitLinkView,
        'AdministerView': AdministerView
    };
});

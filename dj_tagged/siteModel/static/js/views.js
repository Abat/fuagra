define([
    'jquery',
    'underscore',
    'backbone',
    'marionette',
    'bootstrap',
    'collections',
    'models',
    'comment_views',
    'marked',
    'timeago',
    'text!templates/newsView.html',
    'text!templates/newsItemView.html',
    'text!templates/submitLinkView.html',
    'text!templates/submitTextView.html',
    'text!templates/administerView.html',
], function($, _, Backbone, Marionette, Bootstrap, Collections, Models, Comment_Views, Marked, Timeago, newsT, newsItemT, submitLinkT, submitTextT, administerT) {

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

    var NewsItemView = Marionette.ItemView.extend({
        tagName: 'li',
        className: 'newsItem',
        template: _.template(newsItemT),
        templateHelpers: function() {
            return { urlParsed: parseUrl(this.model.get('url')), textPost: this.textPost, moderating: this.moderating };
        },
        initialize: function(attr) {
            this.textPost = attr.textPost;
            this.moderating = attr.moderating;
        },
        events: {
            'click a.up': 'upvote',
            'click a.down': 'downvote',
            'click a.comments': 'comments',
            'click a[name="delete_news"]': 'delete_news',
        },
        modelEvents: {
            'change': 'render'
        },
        onRender: function() {
            var self = this;
            // vote coloring
            if (this.model.get('has_voted') == 1) {
                $('div.score', self.el).css({"color" : "green", "font-weight" : "bold"});
            } else if (this.model.get('has_voted') == -1) {
                $('div.score', self.el).css({"color" : "red", "font-weight" : "bold"});
            } else {
                $('div.score', self.el).css({"color" : "black"});
            }
            // show text post
            if (this.textPost) {
                $('p.textPost', self.el).html(Marked(self.textPost));
            }
            // convert to timeago
            $('time.timeago', self.el).text($.timeago($('time.timeago', self.el)));
            // show moderating buttons
            if (this.moderating) {
                $('ul.buttons', this.el).append("<li class='comments_buttons'><a href='#' class='moderating' name='delete_news'> delete </a></li>");
            }
            // show media
            if (this.model.get('thumbnail_image')) {
                $('div.newsMedia', this.el).removeClass('hidden');
            }
        },
        upvote: function(e) {
            e.preventDefault();
            var self = this;
            var vote = new Models.VoteItemModel({'url_created': '/api/news/' + this.model.id + '/upvote/'});

            vote.save({news:this.model.id}, {
                success: function(model, response, options){
                    console.log('News have been upvoted: ', self.model.id);
                    self.model.fetch();
                },
                error: function(model, xhr, options){
                    if (xhr.responseJSON.reason) {
                        self.dialog('Upvote error:', xhr.responseJSON.reason); 
                    } else if (xhr.responseJSON.detail) {
                        self.dialog('Upvote error:', xhr.responseJSON.detail); 
                    } else {
                        console.log(xhr);
                    }
                }
            });
        },
        downvote: function(e) {
            e.preventDefault();
            var self = this;
            var vote = new Models.VoteItemModel({'url_created': '/api/news/' + this.model.id + '/downvote/'});

            vote.save({news:this.model.id}, {
                success: function(model, response, options){
                    console.log('News have been downvoted: ', self.model.id);
                    self.model.fetch();
                },
                error: function(model, xhr, options){
                    if (xhr.responseJSON.reason) {
                        self.dialog('Downvote error:', xhr.responseJSON.reason); 
                    } else if (xhr.responseJSON.detail) {
                        self.dialog('Downvote error:', xhr.responseJSON.detail); 
                    } else {
                        console.log(xhr);
                    }
                }
            });
        },
        comments: function(e) {
            var self = this;
            e.preventDefault();
            console.log('comments view triggered');
            App.router.navigate('comments/' + self.model.get('id'), {trigger: true});
        },
        delete_news: function(e) {
            var self = this;
            e.preventDefault();
            var newsId = this.model.get('id');
            var newsTitle = this.model.get('title');
            
            this.model.destroy({ 
                success: function() {
                    self.dialog('News deleted:', newsTitle); 
                },
                error: function(model, xhr, options) {
                    self.dialog('Error:', xhr.responseJSON.reason); 
                }
            });
        },
        dialog: function(title, body) {
            console.log('News Dialog:', title, body);
            $('#myModal .modal-title').text(title);
            $('#myModal .modal-body').text(body);
            $('#myModal').modal({ show: true });
        }
    });

    var SubmitLinkView = Marionette.ItemView.extend({
        tagName: 'div',
        className: 'submitLinkView',
        template: _.template(submitLinkT),
        initialize: function(attr) {
            console.log('Initializing SubmitLinkView...');
            this.category = attr.category;
        },
        onBeforeRender: function() {
            if (!this.category) { 
                $.ajax({
                    type: 'GET',
                    url: "/api/categories",
                    success: function(data) {
                        $('select[name="category"] option').remove();
                        $.each(data, function(index, item) {
                            if (item.title != "Help" && item.title != "Feedback") {
                                $('select[name="category"]').append(
                                    $("<option></option>")
                                        .text(item.title)
                                        .val(item.title)
                                );
                            }
                        });
                    }
                });
            } 
        },
        onRender: function() {
            var self = this;
            if (self.category) {
                $('select[name="category"] option', self.el).remove();
                $('select[name="category"]', self.el).append(
                    $("<option></option>")
                        .text(self.category)
                        .val(self.category)
                );
                $('div#top a[name="' + this.category + '"]').css({ "color": "red" });
            }
        },
        events: {
            'submit form#newLinkPost': 'newPost',
            'click button#suggest_title': 'suggestTitle'
        },
        newPost: function(e) {
            var self = this;
            e.preventDefault();
            var post = this.collection.create({
                title: $("input[name='title']", this.el).val(),
                url: $("input[name='url']", this.el).val(),
                category: $("select[name='category']", this.el).val(),
            }, {
                success: function(resp) {
                    console.log("Success, a new link post: ", resp);
                    $(self.el).empty().append('<br><p><b>Thanks for your link!</b></p>');
                },
                error: function(model, xhr, options) {
                    $('form', self.el)[0].reset(); 
                    if (xhr.responseJSON) {
                        self.dialog('Something went wrong:', xhr.responseJSON.reason); 
                    } else {
                        console.log("Error: ", xhr);
                        $(self.el).append('<br><p><b>Something went wrong... Did you login?</b></p>');
                    }
                }
            });
        },
        suggestTitle: function(e) {
            var url = $("input[name='url']", this.el).val();
            var self = this;
            $('#title_status').text('Loading...');
            $('#title_status').show();
            $.ajax({
                type: 'GET',
                url: "/api/news/suggest_title/",
                data: {url: encodeURI(url)},
                success: function(data) {
                    var title = data.title;
                    console.log(title);
                    $("input[name='title']", this.el).val(title);
                    $('#title_status').hide();
                },
                error: function(response, options) {
                    $('#title_status').text(response.responseJSON.reason);
                    console.log(response.responseJSON.reason);
                    $('#title_status').show();
                }

            });
        },
        dialog: function(title, body) {
            console.log('Submit link Dialog:', title, body);
            $('#myModal .modal-title').text(title);
            $('#myModal .modal-body').text(body);
            $('#myModal').modal({ show: true });
        }
    });

    var SubmitTextView = Marionette.ItemView.extend({
        tagName: 'div',
        className: 'submitTextView',
        template: _.template(submitTextT),
        initialize: function(attr) {
            console.log('Initializing SubmitTextView...');
            this.category = attr.category;
        },
        onBeforeRender: function() {
            if (!this.category) {
                $.ajax({
                    type: 'GET',
                    url: "/api/categories",
                    success: function(data) {
                        $('select[name="category"] option').remove();
                        $.each(data, function(index, item) {
                            if (item.title != "Help" && item.title != "Feedback") {
                                $('select[name="category"]').append(
                                    $("<option></option>")
                                        .text(item.title)
                                        .val(item.title)
                                );
                            }
                        });
                    }
                });
            }
        },
        onRender: function() {
            var self = this;
            if (self.category) {
                $('select[name="category"] option', self.el).remove();
                $('select[name="category"]', self.el).append(
                    $("<option></option>")
                        .text(self.category)
                        .val(self.category)
                );
                $('div#top a[name="' + this.category + '"]').css({ "color": "red" });
            }
        },
        events: {
            'submit form#newTextPost': 'newPost'
        },
        newPost: function(e) {
            var self = this;
            e.preventDefault();
            console.log('New text post...');
            var post = this.collection.create({
                title: $("input[name='title']", this.el).val(),
                content: $("textarea[name='content']", this.el).val(),
                category: $("select[name='category']", this.el).val(),
            }, {
                success: function(resp) {
                    console.log("Success, a new text post: ", resp);
                    $(self.el).empty().append('<br><p><b>Thanks for your post!</b></p>');
                },
                error: function(model, xhr, options) {
                    $('form', self.el)[0].reset(); 
                    if (xhr.responseJSON) {
                        self.dialog('Something went wrong:', xhr.responseJSON.reason); 
                    } else {
                        console.log("Error: ", xhr);
                        $(self.el).append('<br><p><b>Something went wrong... Did you login?</b></p>');
                    }
                }
            });
        },
        dialog: function(title, body) {
            console.log('Submit text Dialog:', title, body);
            $('#myModal .modal-title').text(title);
            $('#myModal .modal-body').text(body);
            $('#myModal').modal({ show: true });
        }
    });

    var AdministerView = Marionette.ItemView.extend({
        tagName: 'div',
        className: 'administerView',
        template: _.template(administerT),
        initialize: function(attr) {
            console.log('Initializing AdministerView...');
            this.category = attr.category;
        },
        events: {
            'submit form#changeUserRole': 'modify'
        },
        onBeforeRender: function() {
            var self = this;
            $.ajax({
                type: 'GET',
                url: "/api/users/permissions/" + self.category,
                success: function(data) {
                    // show Administer link for moderators and admins
                    if (data.permission == "Admin") {
                        $('select[name="role"]', self.el).append(
                            $('<option></option>').text("Moderator").val("Moderator")
                        );
                    }
                }
            });
            
        },
        onRender: function() {
            $('select[name="category"] option', this.el).remove();
            $('select[name="category"]', this.el).append(
                $("<option></option>").text(this.category).val(this.category)
            );
            $('div#top a[name="' + this.category + '"]').css({ "color": "red" });
        },
        modify: function(e) {
            var self = this;
            e.preventDefault();
            console.log('Changing user role...');
            var userRole = new Models.UserRoleItemModel({
                username: $("input[name='username']", this.el).val(),
                role: $("select[name='role']", this.el).val(),
                category: $("select[name='category']", this.el).val(),
            });
            
            userRole.save({}, {
                success: function(model, response, options) {
                    console.log("Succes, user role has changed: ", response);
                    $('form#changeUserRole', self.el)[0].reset();
                    $(self.el).append('<br><b> Success, ' + model.attributes.username + '\'s role has changed</b>');
                },
                error: function(model, response, options) {
                    console.log("Error: ", response);
                    $(self.el).append('<br><b> Error: ' + response.responseJSON.reason + '</b>');
                }
            });
             
        }
    });

    var BaseNewsView = Marionette.CompositeView.extend({
        tagName: 'div',
        template: _.template(newsT),

        childView: NewsItemView,
        childViewContainer: 'ul',
        childViewOptions: function() {
            return {
                moderating: this.moderating
            }
        },

        initialize: function(attr) {
            this.pageNum = parseInt(attr.page) || 1;
            console.log('Initializing BaseNewsView...', this.pageNum);
            this.category = attr.category;
            this.sort = attr.sort;
            this.fetchResponse = attr.fetchResponse;
            if (attr.permission == "Admin" || attr.permission == "Moderator") {
                this.moderating = true;
            }
        },
        onRender: function() {
            var self = this;
            if (this.category && this.category != "None" && this.category != undefined) {
                $('div#bottom a[name="Hot"]').attr('href', "/f/" + this.category + "/Hot");
                $('div#bottom a[name="Newest"]').attr('href', "/f/" + this.category + "/Newest");
                $('div#top a[name="' + this.category + '"]').css({ "color": "red" });
            } else {
                $('div#top a').removeAttr('style');
            }
            $('a#prevPage', self.el).attr('href', '?page=' + (this.pageNum - 1));
            $('a#nextPage', self.el).attr('href', '?page=' + (this.pageNum + 1));
            if (this.pageNum == 1) {
                $('a#prevPage', self.el).hide();
            } else {
                $('a#prevPage', self.el).show();
            }
            if (this.fetchResponse.next == null) {
                $('a#nextPage', self.el).hide();
            } else {
                $('a#nextPage', self.el).show();
            }
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
            this.pageNum += 1;
            this.fetch();
        },
        prevPage: function(e) {
            this.pageNum -= 1;
            this.fetch();
        },
        fetch: function() {
            var self = this;
            this.collection.fetch({data: $.param({page: this.pageNum, category: self.category, sort: self.sort }),  success: function(items, response, options) {
                console.log('success: ', response);
                self.fetchResponse = response;
            }, error: function(collection, response, options) {
                console.log('error: ', response);
                self.pageNum = 1;
            }});
        }
    });

    var NewsView = BaseNewsView.extend({ 
        onRender: function() {
            if (this.sort == "Newest") {
                $('div#bottom a[name="Newest"]').css({ "color": "red" });
            } else {
                $('div#bottom a[name="Hot"]').css({ "color": "red" });
            }
            BaseNewsView.prototype.onRender.apply(this);
        }
    });

    var UserNewsView = BaseNewsView.extend({

    });

    // export stuff
    return {
        'NewsView': NewsView,
        'UserNewsView': UserNewsView,
        'NewsItemView': NewsItemView,
        'SubmitLinkView': SubmitLinkView,
        'SubmitTextView': SubmitTextView,
        'AdministerView': AdministerView
    };
});

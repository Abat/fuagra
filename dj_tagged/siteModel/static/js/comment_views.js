define([
    'jquery',
    'underscore',
    'backbone',
    'marionette',
    'collections',
    'models',
    'routers',
    'marked',
    'timeago',
    'text!templates/commentsItemView.html',
    'text!templates/commentsView.html',
    'text!templates/commentsTextareaView.html',
], function($, _, Backbone, Marionette, Collections, Models, Routers, Marked, Timeago, commentsItemT, commentsT, commentsTextareaT) {

    'use strict';
    
    var CommentsItemView = Marionette.CompositeView.extend({
        tagName: 'li',
        className: 'commentsItem',
        template: _.template(commentsItemT),
		
		//helper data
		childCollection: [],
		
        childViewOptions: function(model, index) {
			//console.log("CommentsItemView pass to child", this.childCollection);
			
			var new_items = new Collections.CommentsListCollection([], { newsId: this.newsId });
			
			var i = 0;
			
			if((this.childCollection != null) && this.childCollection.length > 0)
				for(i = 0; i < this.childCollection[0].length; i ++) {
					if(this.childCollection[0][i].attributes.parent == model.id) {
						new_items.add(this.childCollection[0][i]);
					}
				}
			
			//console.log("new_items", new_items);
			
			//filter out first level of child collection
			var childcoll = null;
			if(this.childCollection != null) {
				childcoll = this.childCollection.slice();
				childcoll.splice(0,1);
			}
            return {
                collection: new_items,
                newsId: this.newsId, 
				childColl: childcoll,
                moderating: this.moderating,
            }
        },

        initialize: function(attr) {
			
			console.log("CommentsItemView_attr", attr);
			
            this.collection = attr.collection;			
			
            this.newsId = attr.newsId;
			if(attr.childColl != null)
				this.childCollection = attr.childColl;
            this.moderating = attr.moderating;
			
			console.log("This collection", this.collection);
			
			//console.log("this.childCollection", this.childCollection);
			//console.log("CommentsItemView_initialize_collection...", this.collection);
        },
        
        onRenderTemplate: function() {
            var self = this;
			//console.log("CommentsItemView_render...", this.model);
            if (self.model.get('content') != '[deleted]') {
                $('div.content', this.el).html(Marked(self.model.get('content')));
                if (this.model.get('is_op')) {
                    $('a#comment_author', this.el).css("font-weight", "bold").append('[S]'); 
                }
                if (this.model.get('submitter_role') == 'MD') {
                    $('a#comment_author', this.el).css("color", "purple").append('[M]'); 
                } else if (this.model.get('submitter_role') == 'AD') {
                    $('a#comment_author', this.el).css("color", "red").append('[A]'); 
                }
                // delete button for Moderators and Admins
                if (this.moderating) {
                    $('ul.comments_buttons', this.el).append("<li class='comments_buttons'><a href='#' class='moderating' name='delete_comment'> delete </a></li>");
                }
            } else {
                $('div.commentsVote', this.el).css('visibility', 'hidden'); 
                $('ul.comments_buttons', this.el).css('display', 'none');
                $('a#comment_author', this.el).css('display', 'none');
            }
            $('time.timeago', self.el).text($.timeago($('time.timeago', self.el)));
        },
        
        events: {
            'click a.expand': 'expand',
            'click a.reply': 'reply',
            'click a[name="delete_comment"]': 'delete_comment',
        },
        modelEvents: {
            'change': 'render',
        },

        expand: function(e){
			//console.log("e: ", e);
            e.preventDefault();
			e.stopImmediatePropagation();
            if ($('div.comments', this.el).hasClass('collapsed')) {
                $('div.comments', this.el).removeClass('collapsed');
                $('a.expand', this.el).text("[-]");
            } else {
                $('div.comments', this.el).addClass('collapsed');
                $('a.expand', this.el).text("[+]");
            }
			
        },
        reply: function(e) {
            e.preventDefault();
			e.stopImmediatePropagation();
            if (!$('form', this.el)[0]) {
                var commentsTextareaView = new CommentsTextareaView({ newsId: this.newsId, collection: this.collection, parentId: this.model.get('id'), reply: true });
                $(this.el).append(commentsTextareaView.render().el);
            }
        },
        delete_comment: function(e) {
            e.preventDefault();
			e.stopImmediatePropagation();
            var commentId = this.model.get('id');
            var newsTitle = this.model.get('content');

            this.model.destroy({
                success: function(model, response, options) {
                    console.log('Successfully deleted comment:', commentId);
                },
                error: function(model, response, options) {
                    console.log('Error:', response);
                }
            });
        }
    });

	
    var CommentsTextareaView = Marionette.ItemView.extend({
        tagName: 'div',
        template: _.template(commentsTextareaT),
        templateHelpers: function() {
            return { newsId: this.newsId };
        },

        initialize: function(attr){
            console.log('Initializing CommentsTextareaView...');
            this.newsId = attr.newsId;
            this.parentId = attr.parentId;
            this.reply = attr.reply;
        },

        events: {
            'submit form#newComment': 'newComment',
            'click span.help a': 'toggleHelp'
        },

        newComment: function(e){
            var self = this;
            e.preventDefault();
            var comment = this.collection.create({
                content: $("textarea[name='content']", this.el).val(),
                news: $("input[name='news']", this.el).val(),
                "parent": this.parentId,
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']", this.el).val(),
                date_created: Date.now()
            }, {
                success: function(resp) {
                    console.log(resp);
                    if (self.reply) {
                        $('form#newComment', self.el)[0].remove();
                    } else {
                        $('form#newComment', self.el)[0].reset();
                    }
                    $('div#topComment', self.el).append('<br><p><b>Your comment was posted. </b></p>');
                },
                error: function(err) {
                    console.log(err);
                }
            });
        },
        toggleHelp: function(e) {
            var self = this;
            e.preventDefault();
            $('div.markhelp', this.el).toggle();
        }
    });

    var CommentsView = Marionette.CompositeView.extend({
        tagName: 'div',
        template: _.template(commentsT),
		
		childCollection: [],

        childView: CommentsItemView,
        childViewContainer: 'ul#comments',
        childViewOptions: function(model, index) {
			//console.log("pass to child", model);
			console.log("pass to child", this.collection);
			var comments = new Collections.CommentsListCollection([], { newsId: this.newsId });
            var new_items = new Collections.CommentsListCollection([], { newsId: this.newsId });
			//var new_items = $.extend(true, {}, this.collection);
			
			console.log("pass to child2", new_items);
			
			
			
			var i = 0;
			
			if(this.childCollection.length > 0)
				for(i = 0; i < this.childCollection[0].length; i ++) {
					if(this.childCollection[0][i].attributes.parent == model.id) {
						new_items.add(this.childCollection[0][i]);
					}
				}
			
			//console.log("new_items", new_items);
			
			//filter out first level of child collection
			var childcoll = this.childCollection.slice();
			childcoll.splice(0,1);
			
			//console.log("childcoll", childcoll);
			
            return {
                collection: new_items,
                newsId: this.newsId,
                moderating: this.moderating,
				childColl: childcoll,
            }
        },
		itemView: CommentsItemView,

        onRender: function() {
            console.log('CommentsView onRender...');
            var commentsTextareaView = new CommentsTextareaView({ newsId: this.newsId, collection: this.collection });
            $(this.el).prepend(commentsTextareaView.render().el);
        },
        onShow: function() {
            if (window.location.hash) {
                $("body, html").animate({ scrollTop: $(window.location.hash + "").offset().top }, 600);
            }

        },
        initialize: function(attr){			
            console.log('Initializing CommentsView...');
            this.newsId = attr.newsId;
            if (attr.permission == "Admin" || attr.permission == "Moderator") {
                this.moderating = true;
            }
            $("html, body").animate({ scrollTop: 0 }, 0);
        },
    });
	



    return {
        'CommentsItemView': CommentsItemView,
        'CommentsTextareaView': CommentsTextareaView,
        'CommentsView': CommentsView,
    };
});

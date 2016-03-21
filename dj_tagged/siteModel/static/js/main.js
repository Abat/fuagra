requirejs.config({
    'baseUrl': '/static',
    'paths': {
        'app': 'js',
        'text': 'js/text',
        'marked': 'js/marked/marked',
        'jquery': 'js/jquery/jquery-2.1.3.min',
        'underscore': 'js/underscore/underscore-min',
        'backbone': 'js/backbone/backbone-min',
        'marionette': 'js/marionette/backbone.marionette.min',
        'bootstrap': 'js/bootstrap/bootstrap.min',
        'url': 'js/url/url.min',
        'timeago': 'js/timeago/timeago',
        'models': 'js/models',
        'collections': 'js/collections',
        'views': 'js/views',
        'comment_views': 'js/comment_views',
        'side_views': 'js/side_views',
        'top_views': 'js/top_views',
        'routers': 'js/routers',
        'polyglot': 'js/polyglot/polyglot.min',
    }
});

require(['app/taggednews'], function(App) {
    // App starts here
    window.App = App;
    var locale = localStorage.getItem('locale') || 'kk';
    $.getJSON('/locale/' + locale, function(data) {
        console.log(data);
        // Instantiates polyglot with phrases.
        var phrases = data["phrases"];
        window.App.start(phrases);
    });
});

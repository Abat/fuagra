requirejs.config({
    'baseUrl': '/static',
    'paths': {
        'app': 'js',
        'text': 'js/text',
        'jquery': 'js/jquery/jquery-2.1.3.min',
        'underscore': 'js/underscore/underscore-min',
        'backbone': 'js/backbone/backbone-min',
        'marionette': 'js/marionette/backbone.marionette.min',
        'bootstrap': 'js/bootstrap/bootstrap.min',
        'models': 'js/models',
        'collections': 'js/collections',
        'views': 'js/views',
        'comment_views': 'js/comment_views',
        'side_views': 'js/side_views',
        'top_views': 'js/top_views',
        'routers': 'js/routers'
    }
});

require(['app/taggednews'], function(App) {
    // App starts here
    window.App = App;
    window.App.start();
});

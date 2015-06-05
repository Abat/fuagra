requirejs.config({
    'baseUrl': '/static',
    'paths': {
        'app': 'js',
        'jquery': 'js/jquery/jquery-2.1.3.min',
        'underscore': 'js/underscore/underscore-min',
        'backbone': 'js/backbone/backbone-min',
        'bootstrap': 'js/bootstrap/bootstrap.min',
    }
});

require(['app/taggednews'], function(Application) {
    // App starts here
});

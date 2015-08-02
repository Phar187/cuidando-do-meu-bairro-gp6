// Place third party dependencies in the lib folder
//
// Configure loading modules from the lib directory,
// except 'app' ones,
requirejs.config({
    baseUrl: "static/js",
    urlArgs: "bust=" + (new Date()).getTime(),
    paths: {
        bootstrap: "bower_components/bootstrap/dist/js/bootstrap",
        highcharts: "bower_components/highcharts/highcharts",
        // hcd: "bower_components/highcharts/highcharts-more",
        hcd: "bower_components/highcharts/modules/data",
        hce: "bower_components/highcharts/modules/exporting",
        jquery: "bower_components/jquery/dist/jquery.min",
        leaflet: "bower_components/leaflet/dist/leaflet",
        mapcluster: "leaflet.markercluster",
        pubsub: '../vendor/pubsub-js/js/pubsub',
        mapquest: "mq-map",
        handlebars: "handlebars",
        datatables: 'bower_components/datatables/media/js/jquery.dataTables.min',
        requirejs: '../vendor/requirejs/js/require',
        base64: 'bower_components/base64/base64',
        // jwtdecode: "jwt-decode.min",
        // base64: 'bower_components/requirejs-base64/base64.min'
    },
    shim: {
        // 'leaflet': {
        //     exports: 'L'
        // },
        mapcluster: ['leaflet', 'mapquest'],
        mapquest: ['leaflet'],
        datatables: ['jquery'],
        highcharts: ['jquery'],
        bootstrap: ['jquery'],
        hcd: ['highcharts'],
        hce: ['highcharts']
    }
})

// Load the main app module to start the app
requirejs(["app/main"])

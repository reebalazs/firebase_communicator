
var collect = require('grunt-collection-helper');

module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    copy: {
      'default': {
        files: {
          'app/dist/': [
            collect.bower('jquery').path('jquery.js'),
            collect.bower('angular').path('angular.js'),
            collect.bower('angular-cookies').path('angular-cookies.js'),
            collect.bower('angular-elastic').path('elastic.js'),
            collect.bower('angularFire').path('angularFire.js')
          ]
        }
      }
    },
    uglify: {
      'default': {
        files: {
          'app/dist/angular.min.js': [
            collect.bower('angular').path('angular.js')
          ],
          'app/dist/angular-cookies.min.js': [
            collect.bower('angular-cookies').path('angular-cookies.js')
          ],
          'app/dist/angular-elastic.min.js': [
              collect.bower('angular-elastic').path('elastic.js')
          ],
          'app/dist/jquery.min.js': [
            collect.bower('jquery').path('jquery.js')
          ]

        }
      }
    },
    watch: {
      options: {
        debounceDelay: 250
      },
      'default': {
        files: [
          collect.bower('jquery').path('jquery.js'),
          collect.bower('angular').path('angular.js'),
          collect.bower('angular-cookies').path('angular-cookies.js'),
          collect.bower('angular-elastic').path('elastic.js'),
          collect.bower('angularFire').path('angularFire.js')
        ],
        tasks: ['copy:default', 'uglify:default']
      }
    }
  });

  // Load the task plugins.
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-watch');

  // Default task(s).
  grunt.registerTask('default', ['copy:default', 'uglify:default']);

};

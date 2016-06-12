'use strict';

module.exports = function ( grunt ) {
  // load all grunt tasks
  grunt.loadNpmTasks( 'grunt-contrib-less' );
  grunt.loadNpmTasks( 'grunt-postcss' );
  grunt.loadNpmTasks( 'grunt-contrib-uglify' );
  grunt.loadNpmTasks( 'grunt-contrib-watch' );

  grunt.initConfig( {
    watch: {
      // if any .less file changes in directory "public/css/" run the "less"-task.
      files: "assets/less/*.less",
      tasks: [ "less" ]
    },
    // "less"-task configuration
    less: {
      // production config is also available
      development: {
        options: {
          // Specifies directories to scan for @import directives when parsing.
          // Default value is the directory of the source, which is probably what you want.
          paths: [ "less/" ],
        },
        files: {
          // compilation.css  :  source.less
          "assets/css/reset.css": "bower_components/blankslate/reset.less",
          "assets/css/main.css": "assets/less/main.less"
        }
      },
    },
    postcss: {
      options: {
        map: false, // inline sourcemaps
        processors: [
          require( 'autoprefixer' )( { browsers: 'last 2 versions' } ),
          require( 'cssnano' )()
        ]
      },
      dist: {
        src: 'assets/css/*.css'
      }
    },
    uglify: {
      options: {
        mangle: false // set to false if you want to rename your variables on deployment - my personal feelings are that you shouldn't as that's not the nature of the web
      },
      build: {
        files: {
          'assets/js/init.min.js': [ 'assets/js/init.js' ]
        }
      }
    }
  });
  // the default task (running "grunt" in console) is "watch"
  grunt.registerTask( 'default', [ 'watch', 'less', 'postcss', 'uglify' ] );
  grunt.registerTask( 'build', [ 'less', 'postcss', 'uglify' ] );
};

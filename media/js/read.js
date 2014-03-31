
/*
 * jQuery File Upload Plugin Angular JS Example 1.2.1
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2013, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */

/* jshint nomen:false */
/* global window, angular */

(function () {
    'use strict';

	var url = 'upload_pdf_file/'

    angular.module('bbsparse', [
        'blueimp.fileupload'
    ])
        .config([
            '$httpProvider', 'fileUploadProvider',
            function ($httpProvider, fileUploadProvider) {
                delete $httpProvider.defaults.headers.common['X-Requested-With'];
                //fileUploadProvider.defaults.redirect = window.location.href.replace(
                //    /\/[^\/]*$/,
                //    '/cors/result.html?%s'
               // );

            }
        ])

        .controller('file_upload_controller', [
            '$scope', '$http', '$filter', '$window',
            function ($scope, $http) {
                $scope.options = {
                    url: url
                };

				$scope.loadingFiles = false;

            }
        ])

        .controller('file_destroy_controller', [
            '$scope', '$http',
            function ($scope, $http) {
                var file = $scope.file,
                    state;
				file.$cancel = function () {
                        $scope.clear(file);
                    };
 
            }
        ])
        
        .controller('list_book_controller', [
            '$scope', '$http',
            function ($scope, $http) {
                $scope.init = function(){
                    $http.get('booksubs.json').success(function (data) { 
                        $scope.booksubs = data; 
                    }); 
                }
            }
        ]);

}());


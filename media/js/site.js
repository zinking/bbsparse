 angular.module('redditApp', [])
    .controller('FeedListCtrl', function ($scope,$http) {
        $http.get('content/linkbyschools.json').success(function (data) { 
            $scope.linkbyschools = data; 
            
        }); 
    });



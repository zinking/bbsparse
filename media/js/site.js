angular.module('bbsparse', [])
	.controller('FeedListCtrl', function ($scope,$http) {
		$scope.loading = true;
		$http.get('content/linkbyschools.json').success(function (data) { 
			$scope.linkbyschools = data; 
			$scope.loading = false;
		}); 
	})
	.directive('showParentHover',function() {
		  return {
			 link : function(scope, element, attrs) {
				element.hide();
				element.parent().bind('mouseenter', function() {
					element.show();
				});
				element.parent().bind('mouseleave', function() {
					 element.hide();
				});
		   }
	   };
	})
	.directive('hideParentHover',function() {
		  return {
			 link : function(scope, element, attrs) {
				
				element.parent().bind('mouseenter', function() {
					element.hide();
				});
				element.parent().bind('mouseleave', function() {
					 element.show();
				});
		   }
	   };
	});



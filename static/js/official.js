angular.module('p1', ['ngRoute'])
  .config(function ($routeProvider) {
     $routeProvider
        .when('/locations', {
           templateUrl: '/locations.html',
           controller: 'LocationListCtrl',
           controllerAs: 'locations'
        })
        .otherwise({
           redirectTo: '/locations'
        });
  }).factory('LocationsFactory', function LocationsFactory ($http) {
     var exports = {};
     exports.get_locations = function () {
        return $http.post('api/locations')
           .error(function (data) {
              console.log('Failed to get locations!', data)
        })
     }
     exports.filter_locations = function(f) {
       return $http.post('api/filter_loc', f)
        .error(function (data) {
          console.log('Failed to save location!', data)
        })
     }
     return exports
  }).controller('LocationListCtrl', function($scope, LocationsFactory) {
    $scope.non_opt = [{"id": '-', "name": "Not selected"}]
    
    $scope.states = $scope.non_opt.concat([{"id": 0, "name": "Georgia"}, 
      {"id": 1, "name": "Alaska"}])
    $scope.cities = $scope.non_opt.concat([{"id": 0, "name":"Atlanta"}, 
      {"id": 1, "name":"Smyrna"}])
    
    $scope.locations = $scope.non_opt
    $scope.f = {'flagged': false, 'name': $scope.non_opt[0].id, 
      'city': $scope.non_opt[0].id, 'state': $scope.non_opt[0].id}
    $scope.filtered = []
    
    LocationsFactory.get_locations().success(function(data, status) {
      if(data.succ == 0) $scope.locations = $scope.non_opt.concat(data.c)
    })
    $scope.filter = function() {
      LocationsFactory.filter_locations(this.f).success(function(data, status) {
        console.log("filter_loc response: ", data, status)
        if(data.succ == 0) $scope.filtered = data.c
      })
    }
  })

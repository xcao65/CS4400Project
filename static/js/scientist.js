angular.module('p2', ['ngRoute'])
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

     exports.get_types = function () {
        return $http.get('api/types')
           .error(function (data) {
              console.log('Failed to get types!', data)
        })
     }
     exports.get_locations = function () {
        return $http.get('api/locations')
           .error(function (data) {
              console.log('Failed to get locations!', data)
        })
     }
     exports.put_point = function(p) {
       return $http.put('api/points', p)
        .error(function (data) {
          console.log('Failed to save point!', data)
        })
     }
     exports.put_loc = function(l) {
       return $http.put('api/locations', l)
        .error(function (data) {
          console.log('Failed to save location!', data)
        })
     }
     return exports
  }).controller('LocationListCtrl', function($scope, LocationsFactory) {
     $scope.p = {'ts': new Date()}
     $scope.l = {'city': 0, 'state': 0}
     $scope.m = true // true for adding point, false for adding location
     $scope.switch = function() {
       this.m = !this.m 
     }
     
     $scope.states = [{"id": 0, "name": "Georgia"}, {"id": 0, "name": "Georgia"}]
     $scope.cities = [{"id": 0, "name":"Atlanta"}, {"id": 0, "name":"Smyrna"}]
     $scope.save_point = function() {
       LocationsFactory.put_point(this.p)
        .success(function(data, status) {
          console.log("Successfully saved point: ", status, data)
        })
     }
     $scope.save_loc = function() {
       LocationsFactory.put_loc(this.l).success(function(data, status) {
         console.log("Successfully saved location: ", status, data)
         $scope.locations.push(data.data)
       })
     }
     LocationsFactory.get_types()
        .success(function(jsonData, statusCode) {
           console.log('Successfully got types!', statusCode, jsonData)
           // Now add the Email messages to the controller's scope
           $scope.types = jsonData
           $scope.p.type = jsonData[0].id
     })
     LocationsFactory.get_locations()
        .success(function(jsonData, statusCode) {
           console.log('Successfuly got locations!', statusCode, jsonData)
           // Now add the Email messages to the controller's scope
           $scope.locations = jsonData
           $scope.p.loc = jsonData[0].id
     })
  })

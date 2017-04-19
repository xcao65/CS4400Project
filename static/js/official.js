angular.module('p1', ['ngRoute'])
  .config(function ($routeProvider) {
     $routeProvider
        .when('/locations', {
           templateUrl: '/locations.html',
           controller: 'LocationListCtrl',
           controllerAs: 'locations'
        }).when('/locations/:id/:name', {
           'templateUrl': '/detail.html'
          ,'controller': 'DetailController'
          ,'controllerAs': 'detail'
        }).when('/report', {
          templateUrl:'/report.html',
          controller: 'ReportCtrl',
          controllerAs: 'report'
        }).otherwise({
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
  }).controller('LocationListCtrl', function($scope, $location, LocationsFactory) {
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
    $scope.reset = function() {
      this.filtered = []
      var none = $scope.non_opt[0].id
      this.f = {'flagged': false, 'name': none, 'city': none, 'state': none }
    }
    $scope.inspect = function(id) {
      console.log("switch to detial - ", id)
    }
    $scope.goto = function(view){
      $location.path(view); // path not hash
    }
  }).factory('DetailFactory', function DetailFactory($http){
    var exports = {}
    exports.filter_points = function(f) {
      return $http.post('api/filter_points', f).error(function(data) {
        console.log('Failed to filter points! ', data)
      })
    }
    exports.get_types = function () {
      return $http.get('api/types')
         .error(function (data) {
            console.log('Failed to get types!', data)
      })
    }
    return exports
  }).controller('DetailController', function($scope, $routeParams, $location, 
      DetailFactory) {
    $scope.f = {'loc': $routeParams.id, 'name': $routeParams.name}
    $scope.non_opt = [{"id": '-', "name": "Not selected"}]
    $scope.goto = function(view){
      $location.path(view); // path not hash
    }
    DetailFactory.get_types().success(function(data, status) {
       console.log('Successfully got types!', status, data)
       if(data.succ != 0) return
       $scope.types = $scope.non_opt.concat(data.c)
    })
    $scope.filter = function() {
      DetailFactory.filter_points(this.f).success(function(data, stataus) {
        console.log('Successfully got filtred points response', status, data)
        if(data.succ != 0) return
        $scope.filtered = data.c
      })
    }
    $scope.reset = function() {
      this.f.from = 0
      this.f.to = 10000
      this.filtered = []
      this.f.type = $scope.non_opt[0].id
    }
    $scope.reset()
  })

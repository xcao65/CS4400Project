angular.module('p2', ['ngRoute'])
  .config(function ($routeProvider) {
     $routeProvider.when('/add_loc', {
          'templateUrl': '/add_location.html'
          , 'controller': 'AddLocationCtrl'
          , 'controllerAs': 'add_loc'
        }).when('/add_point', {
          'templateUrl': '/add_point.html'
          , 'controller': 'AddDataPointCtrl'
          , 'controllerAs': 'add_point'
        })
        .otherwise({
           redirectTo: '/add_point'
        });
  }).factory('Commons', function Commons ($http, $location) {
     var exports = {};
     
     exports.goto = function(view) {
       $location.path(view); // path not hash
     }
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
  }).controller('AddLocationCtrl', function($scope, Commons) {
    $scope.l = {'city': 0, 'state': 0}
    $scope.states = [{"id": 0, "name": "Georgia"}, {"id": 1, "name": "Alaska"}]
    $scope.cities = [{"id": 0, "name":"Atlanta"}, {"id": 1, "name":"Smyrna"}]
    
    $scope.save_loc = function() {
      Commons.put_loc(this.l).success(function(data, status) {
        console.log("Successfully saved location: ", status, data)
        if(data.succ == 0) alert("Success!")
      })
    }
  }).controller('NavCtrl', function($scope, Commons) {
    $scope.goto = Commons.goto
  }).controller('AddDataPointCtrl', function($scope, Commons) {
    $scope.goto = Commons.goto
    $scope.p = {'ts': "2017-03-19T16:00"}
    
    Commons.get_types().success(function(data, statusCode) {
      console.log('Successfully got types!', statusCode, data)
      if(data.succ != 0) return
      $scope.types = data.c
      $scope.p.attr = data.c[0]
    })
    Commons.get_locations().success(function(data, statusCode) {
      console.log('Successfuly got locations!', statusCode, data)
      if(data.succ != 0) return
      $scope.locations = data.c
      $scope.p.loc = data.c[0].id
    })
    
    $scope.save_point = function() {
      Commons.put_point(this.p).success(function(data, status) {
        console.log("Successfully saved point: ", status, data)
        if(data.succ == 0) alert("Success!")
      })
    }
  })

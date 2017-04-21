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
     exports.get_city_state = function() {
       return $http.post('api/city_state').error(function(data) {
         console.log('Failed to fectch city_state!', data)
       })
     }
     return exports
  }).controller('AddLocationCtrl', function($scope, Commons) {
    $scope.l = {} // the data model for new city
    $scope.states = []
    $scope.cities = []
    
    var non = "- Please Select", c2s = {}, s2c = {}
    c2s[non] = [non], s2c[non] = [non]
    Commons.get_city_state().success(function(data, status) {
      console.log("Successfully got city_state: ", status, data)
      if(data.succ != 0) return
      data.c.forEach(function(d) {
        if(!(d.c in c2s)) {
          c2s[d.c] = [non]
          s2c[non].push(d.c)
        }
        if(!(d.s in s2c)) {
          s2c[d.s] = [non]
          c2s[non].push(d.s)
        }
        c2s[d.c].push(d.s)
        s2c[d.s].push(d.c)
      })
      $scope.states = c2s[non]
      $scope.cities = s2c[non]
      $scope.l.city = $scope.cities[0]
      $scope.l.state = $scope.states[0]
    })
    
    $scope.opt_states = function() { $scope.states = c2s[$scope.l.city] }
    $scope.opt_cities = function() { $scope.cities = s2c[$scope.l.state] }
    
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

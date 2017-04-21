angular.module('p4', ['ngRoute'])
  .config(function ($routeProvider) {
     $routeProvider.when('/default', {
          'templateUrl': '/default.html'
          , 'controller': 'LoginCtrl'
          , 'controllerAs': 'default'
        }).when('/register', {
          'templateUrl': '/register.html'
          , 'controller': 'RegisterCtrl'
          , 'controllerAs': 'register'
        })
        .otherwise({
           redirectTo: '/default'
        });
  }).factory('Commons', function Commons ($http, $location) {
     var exports = {};
     
     exports.goto = function(view) {
       $location.path(view); // path not hash
     }
     exports.put_user = function(u) {
       return $http.put('api/accounts', u)
        .error(function (data) {
          console.log('Failed to create new user!', data)
        })
     }
     exports.get_city_state = function() {
       return $http.post('api/city_state').error(function(data) {
         console.log('Failed to fectch city_state!', data)
       })
     }
     return exports
  }).controller('LoginCtrl', function($scope, $timeout, Commons) {
    $scope.goto = Commons.goto
  }).controller('RegisterCtrl', function($scope, $timeout, Commons) {
    $scope.goto = Commons.goto
    $scope.succ = null
    $scope.u = {}
    
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
    
    var void_msg = function() { $scope.msg = $scope.succ = null }
    
    $scope.save_user = function() {
      Commons.put_user(this.u).success(function(data, status) {
        console.log("Successfully saved point: ", status, data)
        $scope.succ = data.succ
        $scope.msg = data.succ == 0? "Success!" : ("Failed:( succ = " + data.succ)
        $timeout(void_msg, 3000)
      }).error(function(error, status) {
        $scope.succ = 1000
        $scope.msg = 'Error with status code [' + status + ']'
        $timeout(void_msg, 3000)
      })
    }
  })

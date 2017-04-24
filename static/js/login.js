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
       return $http.post('api/register', u)
        .error(function (data) {
          console.log('Failed to create new user!', data)
        })
     }
     exports.check_availability = function(name) {
       return $http.get('api/register', {'username': name})
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

    $scope.states = []
    $scope.cities = []
    $scope.acc_types = [
      {'v': 'scientist', 'n': 'Scientist'}
    , {'v': 'official', 'n': 'City Official'}
    ]
    $scope.u = {'type': $scope.acc_types[0].v, 'password':'', 'conf_pwd': ''}

    var non = "- Please Select", c2s = {}, s2c = {}
    c2s[non] = [non], s2c[non] = [non]
    Commons.get_city_state().success(function(data, status) {
      console.log("Successfully got city_state: ", status, data)
      if(data.succ != 0) return
      data.c.forEach(function(d) {
        if(!(d.City in c2s)) {
          c2s[d.City] = [non]
          s2c[non].push(d.City)
        }
        if(!(d.State in s2c)) {
          s2c[d.State] = [non]
          c2s[non].push(d.State)
        }
        c2s[d.City].push(d.State)
        s2c[d.State].push(d.City)
      })
      $scope.states = c2s[non]
      $scope.cities = s2c[non]
      $scope.u.city = $scope.cities[0]
      $scope.u.state = $scope.states[0]
    })

    $scope.opt_states = function() { $scope.states = c2s[$scope.u.city] }
    $scope.opt_cities = function() { $scope.cities = s2c[$scope.u.state] }

    var void_msg = function() { $scope.msg = $scope.succ = null }

    $scope.save_user = function() {
      Commons.put_user(this.u).success(function(data, status) {
        console.log("Successfully saved point: ", status, data)
        $scope.succ = data.succ
        if(data.succ == 0) {
          $scope.msg = "You have successfully registered! "
          if(data.c.type == "official")
            $scope.msg += " Waiting administrative review..."
        } else {
          $scope.msg = "Failed to register!"
        }
        $timeout(void_msg, 3000)
        $timeout(function() { Commons.goto('/') }, 3000)
      }).error(function(error, status) {
        $scope.succ = 1000
        $scope.msg = 'Error with status code [' + status + ']'
        $timeout(void_msg, 3000)
      })
    }

    $scope.validate = function() { // not called yet, need timeout/promise/delay
      Commons.check_availability(this.u.username).success(function(data,
          status) {
        console.log("Successfully validated username: ", status, data)
      })
    }
  })

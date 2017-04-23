angular.module('p4', ['ngRoute'])
  .config(function ($routeProvider) {
     $routeProvider.when('/default', {
          'templateUrl': '/default.html'
          , 'controller': 'ErrorCtrl'
          , 'controllerAs': 'default'
        }).when('/login', {
          'templateUrl': '/login.html'
          , 'controller': 'registerCtrl'
          , 'controllerAs': 'login'
        })
        .otherwise({
           redirectTo: '/default'
        });
  }).factory('Commons', function Commons ($http, $location) {
     var exports = {};

     exports.goto = function(view) {
       $location.path(view); // path not hash
       console.log("haha",  $location.path(view))
     }
     return exports
  }).controller('ErrorCtrl', function($scope, $timeout, Commons) {
    $scope.goto = Commons.goto
    console.log("commons.goto is ",  Commons.goto)
  })

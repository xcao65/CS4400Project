angular.module('p0', ['ngRoute'])
  .config(function ($routeProvider) {
     $routeProvider
        .when('/points', {
           templateUrl: '/points.html',
           controller: 'PointListCtrl',
           controllerAs: 'points'
        }).when('/officials', {
          templateUrl:'/officials.html',
          controller: 'OfficialAccountCtrl',
          controllerAs: 'officials'
        }).otherwise({
           redirectTo: '/points'
        });
  }).factory('Commons', function Commons($location){
    var exports = {'id2p': {}, 'id2a': {}}
    exports.goto = function(view) {
      $location.path(view); // path not hash
    }
    exports.index_points = function(arr) {
      var dict = {}
      arr.forEach(function(d) { dict[d.id] = d })
      exports['id2p'] = dict
    }
    exports.update_point = function(incoming) {
      if(!(incoming.id in exports.id2p)) return
      var t = exports.id2p[incoming.id]
      for(var k in incoming) t[k] = incoming[k]
    }
    exports.index_accounts = function(arr) {
      exports['id2a'] = {}
      arr.forEach(function(d) { exports['id2a'][d.id] = d })
    }
    exports.update_account = function(incoming) {
      if(!(incoming.id in exports.id2a)) return
      var t = exports.id2a[incoming.id]
      for(var k in incoming) t[k] = incoming[k]
    }
    return exports
  }).controller('PointListCtrl', function($scope, $location, $http, 
      Commons) {
    $scope.points = []
    
    $scope.get_points = function() {
      $http.post('api/points').error(function(data) {
        console.log('Failed to get pending points! ', data)
      }).success(function(data, status) {
        console.log('Successfully get pending points', status, data)
        if(data.succ != 0) return
        $scope.points = data.c
        Commons.index_points(data.c)
      })
    }
    $scope.get_points()
    
    $scope.mark = function(p, acc) {
      p.status = -2 /* hide buttons, before new status arrives*/
      var payload = {'id': p.id, 'status': acc? 1 : 0}
      $http.put('api/points', payload).error(function(data) {
        console.log('Failed to mark point! ', data)
        p.status = -1 /* restore on failure */
      }).success(function(data, status) {
        console.log('Successfully marked point', status, data)
        if(data.succ != 0) return
        Commons.update_point(data.c)
      })
    }
        
  }).controller('NavCtrl', function($scope, Commons) {
    $scope.goto = Commons.goto
  }).controller('OfficialAccountCtrl', function($scope, $location, $http, 
                                                Commons) {
    $scope.accounts = []
    $scope.get_accounts = function() {
      $http.post('api/gov_accounts').error(function(data) {
        console.log('Failed to get pending city official accounts! ', data)
      }).success(function(data, status) {
        console.log('Successfully get pending city official accounts', status, data)
        if(data.succ != 0) return
        $scope.accounts = data.c
        Commons.index_accounts(data.c)
      })
    }
    $scope.get_accounts()
    
    $scope.mark = function(p, acc) {
      p.status = -2 /* hide buttons, before new status arrives*/
      var payload = {'id': p.id, 'status': acc? 1 : 0}
      $http.put('api/accounts', payload).error(function(data) {
        console.log('Failed to mark account! ', data)
        p.status = -1 /* restore on failure */
      }).success(function(data, status) {
        console.log('Successfully marked account', status, data)
        if(data.succ != 0) return
        Commons.update_account(data.c)
      })
    }
  })

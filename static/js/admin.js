angular.module('p0', ['ngRoute'])
  .config(function ($routeProvider) {
     $routeProvider
        .when('/points', {
           templateUrl: '/points.html',
           controller: 'PointListCtrl',
           controllerAs: 'points'
        }).when('/pt2', {
         'templateUrl': '/point_alt.html'
        ,'controller': 'PointListCtrl'
        , 'controllerAs': 'pt2'
        }).when('/officials', {
          templateUrl:'/officials.html',
          controller: 'OfficialAccountCtrl',
          controllerAs: 'officials'
        }).otherwise({
           redirectTo: '/pt2'
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
    $scope.sort_field = 'ts4sort'
    $scope.sort_reverse = false

    $scope.switch_sort = function(field_name) {
      if($scope.sort_field == field_name) {
        $scope.sort_reverse = !$scope.sort_reverse
      } else {
        $scope.sort_field = field_name
        $scope.sort_reverse = true
      }
    }
    var bin2clz = ['arrow-non', 'arrow-non', 'arrow-up', 'arrow-down']
    $scope.eval_sc = function(name) {
      return bin2clz[+(this.sort_field == name) * 2 + (+this.sort_reverse)]
    }

    var reshape = function(d) {
      d.ts4sort = new Date(d.DateTime)
      d.id = d.LocName + '_' + d.DateTime
    }

    $scope.get_points = function() {
      $http.post('api/points').error(function(data) {
        console.log('Failed to get pending points! ', data)
      }).success(function(data, status) {
        console.log('Successfully get pending points', status, data)
        if(data.succ != 0) return
        $scope.points = data.c
        $scope.points.forEach(reshape)
        Commons.index_points(data.c)
      })
    }
    $scope.get_points()

    $scope.all_mark = false
    $scope.select_all = function() {
      if($scope.points.length < 1) return
      $scope.points.forEach(function(d) { d.marked = $scope.all_mark })
    }

    $scope.mark = function(p, acc) {
      p.Status = -2 /* hide buttons, before new status arrives*/
      var payload = {'id': p.id, 'status': acc? 1 : 0, 'datetime': p.DateTime, 'loc': p.LocName}
      $http.put('api/points', payload).error(function(data) {
        console.log('Failed to mark point! ', data)
        p.Status = -1 /* restore on failure */
      }).success(function(data, status) {
        console.log('Successfully marked point', status, data)
        if(data.succ != 0) return
        Commons.update_point(data.c)
      })
    }

    $scope.mark_selected = function(acc) {
      var selected = $scope.points.filter(function(d) { return d.marked }).map(
          function(d) { return {'LocName': d.LocName, 'DateTime': d.DateTime} })
      var payload = {'acc': acc, 'keys': selected}
      console.log("payload ", payload)
      $http.post('api/mark_points', payload).error(function(error, status) {
        console.log("Failed to batch mark!", error, status)
      }).success(function(data, status) {
        console.log('Successfully marked point', status, data)
        $scope.get_points() // Refresh!
      })
    }

  }).controller('NavCtrl', function($scope, Commons) {
    $scope.goto = Commons.goto
  }).controller('OfficialAccountCtrl', function($scope, $location, $http,
                                                Commons) {
    $scope.accounts = []
    $scope.get_official_accounts = function() {
      $http.post('api/accounts', {'type': 1}).error(function(data) {
        console.log('Failed to get pending city official accounts! ', data)
      }).success(function(data, status) {
        console.log('Successfully get pending city official accounts', status, data)
        if(data.succ != 0) return
        $scope.accounts = data.c
        Commons.index_accounts(data.c)
      })
    }
    $scope.get_official_accounts()

    $scope.mark = function(p, acc) {
      p.Status = -2 /* hide buttons, before new status arrives*/
      var payload = {'id': p.id, 'status': acc? 1 : 0, 'email': p.EmailAddress}
      $http.put('api/accounts', payload).error(function(data) {
        console.log('Failed to mark account! ', data)
        p.Status = -1 /* restore on failure */
      }).success(function(data, status) {
        console.log('Successfully marked account', status, data)
        if(data.succ != 0) return
        Commons.update_account(data.c)
        $scope.get_official_accounts() // Refresh!
      })
    }
  })

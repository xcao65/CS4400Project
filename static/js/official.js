angular.module('p1', ['ngRoute'])
  .config(function ($routeProvider) {
     $routeProvider
        .when('/locations', {
           templateUrl: '/locations.html',
           controller: 'LocationListCtrl',
           controllerAs: 'locations'
        }).when('/locations/:id', {
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
  }).factory('SharedData', function SharedData(){
    return { }
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
  }).controller('LocationListCtrl', function($scope, $location, 
      LocationsFactory, SharedData) {
    $scope.non_opt = [{"id": '-', "name": "Not selected"}]
    
    $scope.states = $scope.non_opt.concat([{"id": 0, "name": "Georgia"}, 
      {"id": 1, "name": "Alaska"}])
    $scope.cities = $scope.non_opt.concat([{"id": 0, "name":"Atlanta"}, 
      {"id": 1, "name":"Smyrna"}])
      
    $scope.id2city = function(id) {
      return "[Not implemented] Map id to city: " + id
    }  
    $scope.id2state = function(id) {
      return "[Not implemented] Map id to state: " + id
    }
    
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
    $scope.inspect = function(obj) {
      console.log("switch to detial - ", obj)
      SharedData.target = obj
      $scope.goto('/locations/' + obj.id)
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
    exports.flag = function(obj) {
      return $http.put('api/flag', obj).error(function(data) {
        console.log('Failed to toggle flag ', data)
      })
    }
    return exports
  }).controller('DetailController', function($scope, $routeParams, $location, 
                                              DetailFactory, SharedData) {
    if(!SharedData || !('target' in SharedData) || !SharedData.target || 
        !'id' in SharedData.target || SharedData.target.id != $routeParams.id)
      $scope.f = {'loc': '-', 'name': 'unknown', 'flag': null}
    else 
      $scope.f = {'loc': SharedData.target.id, 'name': SharedData.target.name, 
        'flag': SharedData.target.flag}
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
      this.f.attr = $scope.non_opt[0].id
    }
    $scope.reset()
    
    $scope.flag = function() {
      DetailFactory.flag(this.f).success(function(data, status) {
        console.log('Successfully got flag response', status, data)
        if(data.succ != 0) return
        $scope.f.flag = data.c.flag
      })
    }
  }).controller('NavCtrl', function($scope, $location, $http) {
    $scope.goto = function(view) {
      $location.path(view); // path not hash
    }
  }).controller('ReportCtrl', function($scope, $location, $http) {
      $scope.items = []
      $scope.generate_report = function(){
        $http.post('api/report').error(function(data) {
          console.log('Failed to get report! ', data)
        }).success(function(data, status) {
          console.log('Successfully get report', status, data)
          if(data.succ != 0) return
          $scope.items = data.c
        })
      }
      $scope.generate_report()
  })

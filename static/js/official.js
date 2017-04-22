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
     exports.get_city_state = function() {
       return $http.post('api/city_state').error(function(data) {
         console.log('Failed to fectch city_state!', data)
       })
     }
     return exports
  }).controller('LocationListCtrl', function($scope, $location,
      LocationsFactory, SharedData) {
    //$scope.non_opt = [{"id": '-', "name": "Not selected"}]
    $scope.non_opt = [{"id": '- Please Select', "name": "Not selected"}]
    $scope.f = {}
    //$scope.states = $scope.non_opt.concat([{"id": 0, "name": "Georgia"},
    //  {"id": 1, "name": "Alaska"}])
    //$scope.cities = $scope.non_opt.concat([{"id": 0, "name":"Atlanta"},
    //      {"id": 1, "name":"Smyrna"}])
    $scope.states = []
    $scope.cities = []
    //$scope.locations = $scope.non_opt
    var non = "- Please Select", c2s = {}, s2c = {}, get_loc = []
    c2s[non] = [non], s2c[non] = [non], get_loc.push({"LocationName": non})

    LocationsFactory.get_locations().success(function(data, status) {
      console.log("Successfully got locations: ", status, data)
      if(data.succ != 0) return
      data.c.forEach(function(d) {
        if(!(d in get_loc)) {
          get_loc.push(d)
        }
      })
      //$scope.locations = $scope.non_opt.concat(data.c)
      $scope.locations = get_loc
      $scope.f.name = $scope.locations[0].LocationName
      console.log("get_loc is  ", get_loc)
      console.log("locations are: ", data.c)
    })

    LocationsFactory.get_city_state().success(function(data, status) {
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
      $scope.f.city = $scope.cities[0]
      $scope.f.state = $scope.states[0]
    })

    $scope.id2state = function() { $scope.states = c2s[$scope.f.city] }
    $scope.id2city = function() { $scope.cities = s2c[$scope.f.state] }
/*
    $scope.id2city = function(id) {
      return "[Not implemented] Map id to city: " + id
    }
    $scope.id2state = function(id) {
      return "[Not implemented] Map id to state: " + id
    }
*/

    console.log("before, scope non_opts are: ", $scope.non_opt)
    //$scope.f = {'flagged': false, 'name': '-', 'city': '-', 'state': '-'}
    //$scope.f = {}


    $scope.filter = function() {
    LocationsFactory.filter_locations(this.f).success(function(data, status) {
        console.log("filter_loc response: ", data, status)
        if(data.succ == 0) {
            $scope.filtered = data.c
            //$scope.filtered = $scope.locations
        }
      })
    }
    $scope.reset = function() {
      this.filtered = []
      //console.log("$scope.non_opt[0] is ", $scope.non_opt[0])
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
      //console.log("current scope.nonopt[0] is ", $scope.non_opt[0])
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

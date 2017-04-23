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
    var all_cities = [], all_states = []

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
      all_states = c2s[non]
      all_cities = s2c[non]
    })

    $scope.id2state = function() { $scope.states = c2s[$scope.f.city] }
    $scope.id2city = function() { $scope.cities = s2c[$scope.f.state] }

    $scope.id_city = function(id) {
      return id
    }
    $scope.id_state = function(id) {
      return id
    }

    console.log("before, scope non_opts are: ", $scope.non_opt)
    //$scope.f = {'flagged': false, 'name': '-', 'city': '-', 'state': '-'}
    //$scope.f = {}


    $scope.filter = function() {
    LocationsFactory.filter_locations(this.f).success(function(data, status) {
        console.log("filter_loc response: ", data, status)
        if(data.succ == 0) {
            $scope.filtered = data.c
            //$scope.filtered = $scope.locations
            console.log("filtered are : ", $scope.filtered)
        }
      })
    }
    $scope.reset = function() {
      this.filtered = []
      $scope.filtered = []
      var none = $scope.non_opt[0].id
      this.f = {'flagged': false, 'name': none, 'city': none, 'state': none }
      $scope.states = all_states
      $scope.cities = all_cities
      console.log("after reset f is ", this.f)
      console.log("filtered are : ", $scope.filtered)
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
      $scope.f = {'loc': '-', 'name': 'unknown', 'flag': null, 'flagged': 0}
    else
      $scope.f = {'loc': SharedData.target.id, 'name': SharedData.target.name,
        'flag': SharedData.target.flag, 'flagged': SharedData.target.flagged}
    $scope.non_opt = [{"id": '-', "name": "Not selected"}]
    $scope.goto = function(view){
      $location.path(view); // path not hash
    }
    DetailFactory.get_types().success(function(data, status) {
       console.log('Successfully got types!', status, data)
       if(data.succ != 0) return
       $scope.types = data.c
       //console.log("types"data.c)
       //$scope.f.attr = $scope.types[]
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
      $scope.f.start = null
      $scope.f.end = null
    }
    $scope.reset()

    $scope.flag = function() {
      DetailFactory.flag(this.f).success(function(data, status) {
        console.log('Successfully got flag response', status, data)
        if(data.succ != 0) return
        $scope.f.flag = data.c.flag
        $scope.f.flagged = data.c.flagged
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

      $scope.sort_field = 'name'
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
  })

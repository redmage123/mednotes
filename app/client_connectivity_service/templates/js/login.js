app.controller('loginCtrl', function($scope, $http) {
  $scope.login = function() {
    $http.post('/api/login/', {
      'username': $scope.username,
      'password': $scope.password
    }).then(function successCallback(response) {
      window.location.href = "/dashboard";
    }, function errorCallback(response) {
      alert("Invalid username or password.");
    });
  };
});


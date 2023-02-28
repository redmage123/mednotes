angular.module('mednotesApp')
  .controller('registerController', function($scope, $http) {
    $scope.submitRegistration = function() {
      var data = {
        username: $scope.username,
        email: $scope.email,
        password: $scope.password,
        confirm_password: $scope.confirm_password
      };

      $http.post('/api/register', data)
        .then(function(response) {
          // handle success
          console.log(response);
        })
        .catch(function(error) {
          // handle error
          console.log(error);
        });
    };
  });


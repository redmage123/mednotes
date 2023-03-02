// Define the indexController
app.controller("indexController", function($scope, $http, $location) {
  // Define the submitLoginForm function
  $scope.submitLoginForm = function() {
    // Define the data object
    var data = {
      "username": $scope.username,
      "password": $scope.password
    };
    
    // Make a POST request to the login endpoint
    $http.post("/login/", data).then(function(response) {
      // Redirect to the dashboard on success
      $location.path("/dashboard/");
    }, function(error) {
      // Display an error message on failure
      alert("Invalid username or password");
    });
  };
  
  // Define the submitRegisterForm function
  $scope.submitRegisterForm = function() {
    // Define the data object
    var data = {
      "username": $scope.username,
      "email": $scope.email,
      "password": $scope.password,
      "confirm_password": $scope.confirm_password
    };
    
    // Make a POST request to the register endpoint
    $http.post("/register/", data).then(function(response) {
      // Redirect to the dashboard on success
      $location.path("/dashboard/");
    }, function(error) {
      // Display an error message on failure
      alert("Registration failed");
    });
  };
});


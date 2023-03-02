angular.module('mednotesApp')
  .controller('dashboardController', function($scope, $http) {
    
    // Fetch data from the backend API
    $http.get('/api/dashboard')
      .then(function(response) {
        $scope.data = response.data;
      })
      .catch(function(error) {
        console.error('Error fetching data:', error);
      });
      
    // Handle form submission
    $scope.submitForm = function() {
      var data = {
        name: $scope.name,
        email: $scope.email,
        message: $scope.message
      };
      
      $http.post('/api/contact', data)
        .then(function(response) {
          $scope.messageSent = true;
        })
        .catch(function(error) {
          console.error('Error sending message:', error);
        });
    };
    
  });


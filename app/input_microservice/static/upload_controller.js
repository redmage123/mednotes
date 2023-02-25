var app = angular.module('mednotesApp', []);

app.controller('fileUploadController', ['$scope', '$http', function($scope, $http) {
    $scope.uploadFile = function() {
        var file = $scope.myFile;
        var uploadUrl = "/upload_file";
        var fd = new FormData();
        fd.append('file', file);
        $http.post(uploadUrl, fd, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        })
        .success(function(data) {
            console.log(data


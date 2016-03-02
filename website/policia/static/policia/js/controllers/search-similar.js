/*globals angular, console */
var policia = angular.module('policia', []);

policia.controller('searchSimilar', function ($scope, $http) {
    'use strict';

    $scope.searchUsername = '';
    $scope.searchLanguage = 'es';
    $scope.searchMax = 100;
    $scope.searchBy = 'topic';
    $scope.searchIn = 'all';
    $scope.similarUsers = [];

    $scope.checkUsername = function () {
        return true;

    };

    $scope.search = function () {

        var endpoint = '/api/buscar/similares/';
        var params = {
            'search-username': $scope.searchUsername,
            'search-language': $scope.searchLanguage,
            'search-max': $scope.searchMax,
            'search-by': $scope.searchBy,
            'search-in': $scope.searchIn
        };

        $http.get(endpoint, { 'params': params }).success(function (data) {
            console.log('respuesta api');
            console.log(data);
            if (data === "missing_params") {

            } else if (data === "no_results") {

            } else if (data === "downloading") {

            } else {
                $scope.similarUsers = data.users;
            }
        });
    };
});

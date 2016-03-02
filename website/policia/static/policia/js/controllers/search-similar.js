var policia = angular.module('policia', []);

policia.controller('searchSimilar', function ($scope, $http) {
    'use strict';
    $scope.searchUsername = '';
    $scope.searchLanguage = 'es';
    $scope.searchMax = 100;
    $scope.searchBy = 'topic';
    $scope.searchIn = 'all';

    function checkUsername() {
        $http.get('https://twitter.com/' + $scope.searchUsername)
            .success(
                
            )
            .error(

            );
    }


    function checkForm() {
        checkUsername();
    }

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

            if (data == "missing_params") {

            } else if (data == "no_results") {

            } else if ("downloading"){

            } else {

            }
        });
    };
});

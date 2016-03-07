/*globals angular, console */
var policia = angular.module('policia', []);

policia.controller('searchSimilar', function ($scope, $http) {
    'use strict';

    // Modelos de datos
    $scope.searchUsername = '';
    $scope.searchLanguage = 'es';
    $scope.searchMax = 100;
    $scope.searchBy = 'topic';
    $scope.searchIn = 'all';
    $scope.similarUsers = [];
    $scope.error = "";

    // Clases
    $scope.searchUsernameClass = "";

    // Shows
    $scope.searchSpinnerVisible = false;
    $scope.searchButtonVisible = true;
    $scope.errorVisible = false;

    // Flags
    var validSearchUsername = false;

    $scope.checkUsername = function () {
        var username = $scope.searchUsername;

        if (username[0] === '@') {
            username = username.substring(1);
        }

        if (username.length === 0) {
            validSearchUsername = false;
            return $scope.searchUsernameClass = "has-error";
        }

        $http.get('/api/validar/usuario/' + username + '/')
            .success(function(data) {
                if (data == "invalid") {
                    validSearchUsername = false;
                    $scope.searchUsernameClass = "has-error"
                } else {
                    validSearchUsername = true;
                    $scope.searchUsernameClass = ""
                }
            });
    };

    $scope.search = function () {

        var endpoint = '/api/buscar/similares/';
        var params = {
            'search-username': $scope.searchUsername,
            'search-language': $scope.searchLanguage,
            'search-max': $scope.searchMax,
            'search-by': $scope.searchBy,
            'search-in': $scope.searchIn,
            'r':  Math.floor(Math.random() * (9999 - 0))
        };

        $scope.searchSpinnerVisible = true;
        $scope.searchButtonVisible = false;
        $scope.errorVisible = false;

        $http.get(endpoint, { 'params': params })
            .success(function (data) {
                if (data.status === "missing_params") {
                    $scope.similarUsers = [];
                    $scope.error = "Falta algún parámetro de búsqueda.";
                    $scope.errorVisible = true;
                } else if (data.status === "no_results" || data === "db_error") {
                    $scope.similarUsers = [];
                    $scope.error = "No se encontraron usuarios similares. " +
                                    "Compruebe que el nombre de usuario esté " +
                                    "escrito correctamente.";

                    $scope.errorVisible = true;
                } else if (data.status === "downloading") {
                    $scope.similarUsers = [];
                    Custombox.open({
                        target: '#custom-modal',
                        effect: 'blur',
                        speed: 100
                    });
                } else if (data.status = "done"){
                    $scope.similarUsers = data.users;
                }
                $scope.searchSpinnerVisible = false;
                $scope.searchButtonVisible = true;
            })
            .error(function (data) {
                console.log('Error searching similar user.');
                console.log(data);
                $scope.searchSpinnerVisible = false;
                $scope.searchButtonVisible = true;
            });
    };
});

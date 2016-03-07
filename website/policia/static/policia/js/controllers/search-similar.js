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

    var currentTaskId = 0;

    $scope.notifyByEmail = function () {
        $http.get('/api/notificar/' + currentTaskId + '/')
            .success(function (data) {
                console.log('Notified!');
                console.log(data);
            })
            .error(function (err) {
                console.log('Error notifying by email: ' + err);
            });
            $scope.closeModal();
    };

    $scope.closeModal = function () {
        Custombox.close();
    };

    $scope.checkUsername = function () {
        var username = $scope.searchUsername;

        if (username[0] === '@') {
            username = username.substring(1);
        }

        if (username.length === 0) {
            $scope.searchUsernameClass = "has-error";
            return;
        }

        $http.get('/api/validar/usuario/' + username + '/')
            .success(function (data) {
                if (data === "invalid") {
                    $scope.searchUsernameClass = "has-error";
                } else {
                    $scope.searchUsernameClass = "";
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
            'r':  Math.floor(Math.random() * (9999))
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
                    currentTaskId = data.taskId;
                    Custombox.open({
                        target: '#custom-modal',
                        effect: 'blur',
                        speed: 100
                    });
                } else if (data.status === "ready") {
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

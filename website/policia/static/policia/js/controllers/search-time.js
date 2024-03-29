/*globals angular, console, window, Custombox */
var policia = angular.module('policia', []);

policia.config(['$compileProvider', function ($compileProvider) {
    'use strict';
    $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|data):/);
}]);

policia.controller('searchSimilar', ['$scope', '$http', 'CSVConverter', function ($scope, $http, CSVConverter) {

    'use strict';

    var currentTaskId = 0;

    // Modelos de datos
    $scope.searchUsername = '';
    $scope.searchLanguage = 'es';
    $scope.searchMax = 100;
    $scope.searchIn = 'all';
    $scope.error = '';
    $scope.similarUsers = [];
    $scope.resultsDataURI = '';

    // Classes
    $scope.usernameValidationClass = "text-danger large md md-close";

    // Shows
    $scope.searchSpinnerVisible = false;
    $scope.searchButtonVisible = true;
    $scope.errorVisible = false;
    $scope.successVisible = false;
    $scope.downloadVisible = false;

    $scope.downloadDataInternetExplorer = function () {
        CSVConverter.downloadDataInternetExplorer($scope.similarUsers);
    };

    function getQueryParam(sParam) {
        var sPageURL = decodeURIComponent(window.location.search.substring(1)),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            j;

        for (j = 0; j < sURLVariables.length; j += 1) {
            sParameterName = sURLVariables[j].split('=');

            if (sParameterName[0] === sParam) {
                return sParameterName[1] === undefined ? true : sParameterName[1];
            }
        }
    }

    $scope.updateSearchParams = function () {
        var taskId = -1;
        $scope.searchUsername = getQueryParam('username') || $scope.searchUsername;
        $scope.searchLanguage =  getQueryParam('idioma') || $scope.searchLanguage;
        $scope.searchMax = parseInt(getQueryParam('max'), 10) || $scope.searchMax;
        $scope.searchIn = getQueryParam('in') || $scope.searchIn;
        $scope.taskId = getQueryParam('id') || taskId;
        
        $scope.checkUsername();
        if ($scope.searchUsername.length > 0) {
            $scope.search();
        }
    };

    $scope.notifyByEmail = function () {
        $http.get('/api/tarea/notificar/' + currentTaskId + '/')
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
            $scope.usernameValidationClass = "text-danger large md md-close";
            return;
        }

        $http.get('/api/validar/usuario/' + username + '/')
            .success(function (data) {
                if (data === "invalid") {
                    $scope.usernameValidationClass = "text-danger large md md-close";
                } else {
                    $scope.usernameValidationClass = "text-success large md md-check";
                }
            });
    };

    $scope.search = function () {

        var endpoint = '/api/buscar/tiempo/',
            params = {
                'search-username': $scope.searchUsername,
                'search-language': $scope.searchLanguage,
                'search-max': $scope.searchMax,
                'search-in': $scope.searchIn,
                'r':  Math.floor(Math.random() * (9999))
            };
        if ($scope.taskId != -1){
            endpoint = '/api/buscar/tiempo/',
                params = {
                    'search-username': $scope.searchUsername,
                    'search-language': $scope.searchLanguage,
                    'search-max': $scope.searchMax,
                    'search-in': $scope.searchIn,
                    'id': $scope.taskId,
                    'r':  Math.floor(Math.random() * (9999))
                };
        }

        $scope.searchSpinnerVisible = true;
        $scope.searchButtonVisible = false;
        $scope.errorVisible = false;
        $scope.successVisible = false;
        $scope.downloadVisible = false;

        console.log('Querying ' + endpoint);
        console.log('With params:');
        console.log(params);

        $http.get(endpoint, { 'params': params })
            .success(function (data) {
                if (data.status === "missing_params") {

                    $scope.similarUsers = [];
                    $scope.error = "Falta algún parámetro de búsqueda.";
                    $scope.errorVisible = true;
                    $scope.downloadVisible = false;

                } else if (data.status === "no_results" || data === "db_error") {

                    $scope.similarUsers = [];
                    $scope.error = "No se encontraron usuarios similares. " +
                                    "Compruebe que el nombre de usuario esté " +
                                    "escrito correctamente.";

                    $scope.errorVisible = true;
                    $scope.downloadVisible = false;


                } else if (data.status === "downloading") {

                    $scope.similarUsers = [];
                    currentTaskId = data.taskId;
                    Custombox.open({
                        target: '#custom-modal',
                        effect: 'blur',
                        speed: 100
                    });
                    $scope.successVisible = true;
                    $scope.downloadVisible = false;

                } else if (data.status === "ready") {

                    $scope.similarUsers = data.users;
                    $scope.resultsDataURI = CSVConverter.getDataURI(data.users);
                    $scope.downloadVisible = true;

                }
                $scope.searchSpinnerVisible = false;
                $scope.searchButtonVisible = true;
            })
            .error(function (data) {
                console.log('Error searching similar user.');
                console.log(data);
                $scope.searchSpinnerVisible = false;
                $scope.searchButtonVisible = true;
                $scope.downloadVisible = false;

            });
    };
}]);

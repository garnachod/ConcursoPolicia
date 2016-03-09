/*globals angular, console, window, Custombox, $ */
var policia = angular.module('policia', []);

policia.config(['$httpProvider', function ($httpProvider) {
    'use strict';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

policia.controller('searchText', function ($scope, $http) {
    'use strict';

    // Modelos de datos
    $scope.searchText = '';
    $scope.searchLanguage = 'es';
    $scope.searchMax = 100;
    $scope.searchBy = 'topic';
    $scope.similarUsers = [];
    $scope.error = "";

    // Shows
    $scope.searchSpinnerVisible = false;
    $scope.searchButtonVisible = true;
    $scope.errorVisible = false;

    var currentTaskId = 0;

    function getQueryParam(sParam) {
        var sPageURL = decodeURIComponent(window.location.search.substring(1)),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;

        for (i = 0; i < sURLVariables.length; i += 1) {
            sParameterName = sURLVariables[i].split('=');

            if (sParameterName[0] === sParam) {
                return sParameterName[1] === undefined ? true : sParameterName[1];
            }
        }
    }

    function updateSearchText(taskId) {

        $http.get('/api/tarea/texto/' + taskId + '/')
            .success(function (data) {
                $scope.searchText = data;
                if (data.length > 0) {
                    $scope.search();
                }
            });
    }

    $scope.updateSearchParams = function () {
        var taskId = -1;
        $scope.searchLanguage =  getQueryParam('idioma') || $scope.searchLanguage;
        $scope.searchMax = parseInt(getQueryParam('max'), 10) || $scope.searchMax;
        $scope.searchBy = getQueryParam('by') || $scope.searchBy;
        taskId = getQueryParam('id') || taskId;
        if (taskId !== -1) {
            updateSearchText(taskId);
        }
    };

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

    $scope.search = function () {

        var endpoint = '/api/buscar/texto/',
            params = {
                'search-text': $scope.searchText,
                'search-language': $scope.searchLanguage,
                'search-max': $scope.searchMax,
                'search-by': $scope.searchBy,
                'r':  Math.floor(Math.random() * (9999))
            },
            transform;

        $scope.searchSpinnerVisible = true;
        $scope.searchButtonVisible = false;
        $scope.errorVisible = false;

        transform = function (data) {
            return $.param(data);
        };

        $http.post(endpoint, params, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
            transformRequest: transform
        }).success(function (data) {

            if (data.status === "missing_params") {
                $scope.similarUsers = [];
                $scope.error = "Falta algún parámetro de búsqueda.";
                $scope.errorVisible = true;
            } else if (data.status === "no_results" || data === "db_error") {
                $scope.similarUsers = [];
                $scope.error = "No se encontraron usuarios relacionados " +
                                "con el texto introducido. " +
                                "Pruebe con menos términos.";

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

        }).error(function (data) {
            console.log('Error searching similar user.');
            console.log(data);
            $scope.searchSpinnerVisible = false;
            $scope.searchButtonVisible = true;
        });
    };
});

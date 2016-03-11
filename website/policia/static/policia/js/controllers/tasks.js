/*globals angular, console, window, Custombox */
var policia = angular.module('policia', []);

policia.controller('tasks', function ($scope, $http) {
    'use strict';

    $scope.deleteTask = function (taskId) {
        $http.get('/api/tarea/eliminar/' + taskId + '/')
            .success(function () {
                console.log('Tarea eliminada');
            })
            .error(function (data) {
                console.error('Error eliminando tarea');
                console.error(data);
            });
    };
});

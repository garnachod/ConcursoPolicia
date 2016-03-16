/*globals angular, console, window, Custombox, location */
var policia = angular.module('policia', []);

policia.controller('tasks', function ($scope, $http) {

    'use strict';

    var updateInterval = 15000;

    function update() {
        location.reload();
    }

    setInterval(update, updateInterval);
    
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

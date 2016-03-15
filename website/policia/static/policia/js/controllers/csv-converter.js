/*globals policia, angular, navigator, Blob */
var policia = policia || angular.module('policia', []);

policia.config(['$provide', function ($provide) {
    'use strict';

    $provide.factory('CSVConverter', function () {

        function getCSV(usersArray) {
            var csv = 'Username;Nombre;Fecha de creación;Ubicación;Siguiendo;Seguidores\r\n';
            usersArray.forEach(function (user) {
                csv += user.screen_name + ";";
                csv += user.name + ";";
                csv += user.created_at + ";";
                csv += user.location + ";";
                csv += user.following + ";";
                csv += user.followers + "\r\n";
            });
            return csv;
        }

        function getDataURI(usersArray) {
            var urlEncodedCSV = '',
                dataURI = 'data:application/csv;charset=utf-8,';
            urlEncodedCSV = encodeURIComponent(getCSV(usersArray));
            dataURI += urlEncodedCSV;
            return dataURI;
        }

        function downloadDataInternetExplorer(usersArray) {
            if (navigator.msSaveBlob == true) {
                var csvContent = getCSV(usersArray),
                    blob = new Blob([csvContent], {
                        type: "text/csv;charset=utf-8;"
                    });
                navigator.msSaveBlob(blob, "resultados.csv");
            }
        }

        return {
            getDataURI: getDataURI,
            downloadDataInternetExplorer: downloadDataInternetExplorer
        };
    });
}]);

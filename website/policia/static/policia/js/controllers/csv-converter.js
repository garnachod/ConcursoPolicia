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

            //http://stackoverflow.com/questions/7405345/data-uri-scheme-and-internet-explorer-9-errors
            if (window.navigator.msSaveOrOpenBlob) {
                var csvContent = getCSV(usersArray),
                    blobObject = new Blob([csvContent]);
                window.navigator.msSaveOrOpenBlob(blobObject, 'resultados.csv');
            }

            if (document.execCommand) {
                var IEwindow = window.open();
                IEwindow.document.write('sep=,\r\n' + CSV);
                IEwindow.document.close();
                IEwindow.document.execCommand('SaveAs', true, fileName + ".csv");
                IEwindow.close();
            }
        }

        return {
            getDataURI: getDataURI,
            downloadDataInternetExplorer: downloadDataInternetExplorer
        };
    });
}]);

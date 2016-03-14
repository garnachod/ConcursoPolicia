var policia = policia || angular.module('policia', []);

policia.config(['$provide', function($provide) {
  $provide.factory('CSVConverter', function() {
      function getDataURI(usersArray) {
          var csv = '',
              urlEncodedCSV = '',
              dataURI = 'data:application/csv;charset=utf-8,';

          csv += 'Username;Nombre;Fecha de creación;Ubicación;Siguiendo;Seguidores\r\n';

          usersArray.forEach(function (user) {
              csv += user.screen_name + ";";
              csv += user.name + ";";
              csv += user.created_at + ";";
              csv += user.location + ";";
              csv += user.following + ";";
              csv += user.followers + "\r\n";
          });

          urlEncodedCSV = encodeURIComponent(csv);
          dataURI += urlEncodedCSV;
          return dataURI;
      }

      return {
          getDataURI: getDataURI,
      };
  });
}]);

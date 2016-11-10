/* This file is part of Plugin openzwave for jeedom.
 *
 * Plugin openzwave for jeedom is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Plugin openzwave for jeedom is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Plugin openzwave for jeedom. If not, see <http://www.gnu.org/licenses/>.
 */

 $('#bt_createBackup').off().on('click', function (event) {
    bootbox.confirm('{{Etes-vous sûr de vouloir créer un backup ? Une fois lancée cette opération ne peut être annulée.}}',
        function (result) {
            if (result) {
                jeedom.openzwave.backup.do({
                    error: function (error) {
                        $('#div_backupAlert').showAlert({message: error.message, level: 'danger'});
                    },
                    success: function () {
                        $('#div_backupAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
                        updateListBackup();
                    }
                });
            }
        });
});

 $('#bt_removeBackup').off().on('click', function (event) {
    bootbox.confirm('{{Etes-vous sûr de vouloir supprimer le backup suivant }} <b>' + $('#sel_restoreBackup option:selected').text() + '</b> ? {{Une fois lancée cette opération ne peut être annulée.}}',
        function (result) {
            if (result) {
              jeedom.openzwave.backup.delete({
                backup : $('#sel_restoreBackup option:selected').text(),
                error: function (error) {
                    $('#div_backupAlert').showAlert({message: error.message, level: 'danger'});
                },
                success: function () {
                    $('#div_backupAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
                    updateListBackup();
                }
            });
          }
      });
});

 $('#bt_restoreBackup').off().on('click', function (event) {
    bootbox.confirm('{{Etes-vous sûr de vouloir restaurer Openzwave avec }} <b>' + $('#sel_restoreBackup option:selected').text() + '</b> ? {{Une fois lancée cette opération ne peut être annulée et redémarrera le moteur OpenZwave.}}',
        function (result) {
            if (result) {
                jeedom.openzwave.backup.restore({
                    backup : $('#sel_restoreBackup option:selected').text(),
                    error: function (error) {
                        $('#div_backupAlert').showAlert({message: error.message, level: 'danger'});
                    },
                    success: function () {
                        $('#div_backupAlert').showAlert({message: '{{Restauration réussie. Redémarrage d\'OpenZwave en cours.}}', level: 'success'});
                    }
                });
            }
        });
});

 function updateListBackup() {
   jeedom.openzwave.backup.list({
    error: function (error) {
        $('#div_backupAlert').showAlert({message: error.message, level: 'danger'});
    },
    success: function (backups) {
      var options = '';
      for (i in backups) {
        options += '<option value="' + i + '">' + backups[i] + '</option>';
    }
    $('#sel_restoreBackup').html(options);
}
});
}

updateListBackup();
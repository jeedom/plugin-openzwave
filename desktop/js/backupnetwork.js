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

 $('.bt_backupNetwork').off().on('click', function (event) {
    bootbox.confirm('{{Etes-vous sûr de vouloir créer un backup du réseau ? Une fois lancée cette opération ne peut être annulée.}}',
        function (result) {
            if (result) {
                jeedom.openzwave.netbackup.do({
                    name : $('.backName').value(),
                    port : $('.zwavePort option:selected').value(),
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

 $('#bt_removeNetBackup').off().on('click', function (event) {
    bootbox.confirm('{{Etes-vous sûr de vouloir supprimer le backup suivant }} <b>' + $('#sel_restoreNetBackup option:selected').text() + '</b> ? {{Une fois lancée cette opération ne peut être annulée.}}',
        function (result) {
            if (result) {
              jeedom.openzwave.netbackup.delete({
                backup : $('#sel_restoreNetBackup option:selected').text(),
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

 $('#bt_restoreNetBackup').off().on('click', function (event) {
    bootbox.confirm('{{Etes-vous sûr de vouloir restaurer la clé avec }} <b>' + $('#sel_restoreNetBackup option:selected').text() + '</b> ? {{Une fois lancée cette opération ne peut être annulée et redémarrera le moteur OpenZwave !!!! Attention cela écrasera tout réseau présent sur la clé <b>' + $('.zwavePort option:selected').text() +'</b> }}',
        function (result) {
            if (result) {
                jeedom.openzwave.netbackup.restore({
					name : $('#sel_restoreNetBackup option:selected').value(),
                    port : $('.zwavePort option:selected').value(),
                    backup : $('#sel_restoreNetBackup option:selected').text(),
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

$('#bt_downloadNetBackup').on('click', function() {
  window.open('core/php/downloadFile.php?pathfile=' + $('#sel_restoreNetBackup').value(), "_blank", null)
})

$('#bt_uploadNetBackup').fileupload({
  dataType: 'json',
  replaceFileInput: false,
  done: function(e, data) {
    if (data.result.state != 'ok') {
      $('#div_backupAlert').showAlert({message: data.result.result, level: 'danger'})
      return;
    }
    updateListBackup();
    $('#div_backupAlert').showAlert({message: '{{Fichier(s) ajouté(s) avec succès}}', level: 'success'})
  }
})

$("#bt_removeBackup").on('click', function(event) {
  var el = $(this)
  bootbox.confirm('{{Êtes-vous sûr de vouloir supprimer la sauvegarde}} <b>' + $('#sel_restoreBackup option:selected').text() + '</b> ?', function(result) {
    if (result) {
      el.find('.fa-sync').show()
      jeedom.backup.remove({
        backup: $('#sel_restoreBackup').value(),
        error: function(error) {
          $('#div_backupAlert').showAlert({message: error.message, level: 'danger'})
        },
        success: function() {
          updateListBackup()
          $('#div_backupAlert').showAlert({message: '{{Sauvegarde supprimée avec succès}}', level: 'success'})
        }
      })
    }
  })
})

 function updateListBackup() {
   jeedom.openzwave.netbackup.list({
    error: function (error) {
        $('#div_backupAlert').showAlert({message: error.message, level: 'danger'});
    },
    success: function (backups) {
      var options = '';
      for (i in backups) {
        options += '<option value="' + backups[i]['folder'] + '">' + backups[i]['name'] + '</option>';
    }
    $('#sel_restoreNetBackup').html(options);
}
});
}

$('body').on('openzwave::backup', function (_event,_options) {
	if (_options==1){
		$('#div_backupProgress').empty().append('<div class="alert alert-info">{{Un backup ou une restauration est en cours}}</div>');
	} else {
		$('#div_backupProgress').empty().append('<div class="alert alert-info">{{Opération terminée}}</div>');
		updateListBackup();
	}
});

updateListBackup();
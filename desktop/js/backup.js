$('#bt_createBackup').off().on('click', function (event) {
    bootbox.confirm('{{Etes-vous sûr de vouloir créer un backup ? Une fois lancée cette opération ne peut être annulée.}}',
        function (result) {
            if (result) {
                $.ajax({
                    url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=/ZWaveAPI/Run/network.ManualBackup()",
                    dataType: 'json',
                    async: true,
                    error: function (request, status, error) {
                        handleAjaxError(request, status, error, $('#div_backupAlert'));
                    },
                    success: function (data) {
                        updateListBackup();
                        if (data['result'] == true) {
                            $('#div_backupAlert').showAlert({message: '{{Sauvegarde réussie}}', level: 'success'});
                        } else {
                            $('#div_backupAlert').showAlert({message: '{{Echec}} :' + data.data, level: 'danger'});
                        }
                    }
                });
            }
        });
});

$('#bt_removeBackup').off().on('click', function (event) {
    bootbox.confirm('{{Etes-vous sûr de vouloir supprimer le backup suivant }} <b>' + $('#sel_restoreBackup option:selected').text() + '</b> ? {{Une fois lancée cette opération ne peut être annulée.}}',
        function (result) {
            if (result) {
                $.ajax({
                    url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=/ZWaveAPI/Run/network.DeleteBackup(" + $('#sel_restoreBackup option:selected').text() + ")",
                    dataType: 'json',
                    async: true,
                    error: function (request, status, error) {
                        handleAjaxError(request, status, error, $('#div_backupAlert'));
                    },
                    success: function (data) {
                        updateListBackup();
                        if (data['result'] == true) {
                            $('#div_backupAlert').showAlert({message: '{{Suppression réussie}}', level: 'success'});
                        } else {
                            $('#div_backupAlert').showAlert({message: '{{Echec}} :' + data.data, level: 'danger'});
                        }
                    }
                });
            }
        });
});

$('#bt_restoreBackup').off().on('click', function (event) {
    bootbox.confirm('{{Etes-vous sûr de vouloir restaurer Openzwave avec }} <b>' + $('#sel_restoreBackup option:selected').text() + '</b> ? {{Une fois lancée cette opération ne peut être annulée et redémarrera le moteur OpenZwave.}}',
        function (result) {
            if (result) {
                $.ajax({
                    url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=/ZWaveAPI/Run/network.RestoreBackup(" + $('#sel_restoreBackup option:selected').text() + ")",
                    dataType: 'json',
                    async: true,
                    error: function (request, status, error) {
                        handleAjaxError(request, status, error, $('#div_backupAlert'));
                    },
                    success: function (data) {
                        if (data['result'] == true) {
                            $('#div_backupAlert').showAlert({
                                message: '{{Restauration réussie. Redémarrage d\'OpenZwave en cours.}}',
                                level: 'success'
                            });
                        } else {
                            $('#div_backupAlert').showAlert({message: '{{Echec}} :' + data.data, level: 'danger'});
                        }
                    }
                });
            }
        });
});

function updateListBackup() {
    $.ajax({
        url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=/ZWaveAPI/Run/network.GetOZBackups()",
        dataType: 'json',
        async: true,
        error: function (request, status, error) {
            handleAjaxError(request, status, error, $('#div_backupAlert'));
        },
        success: function (data) {
            var options = '';
            backups = data['Backups'];
            for (i in backups) {
                options += '<option value="' + i + '">' + backups[i] + '</option>';
            }
            $('#sel_restoreBackup').html(options);

        }
    });
}
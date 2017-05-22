<?php
/* This file is part of Jeedom.
 *
 * Jeedom is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Jeedom is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Jeedom. If not, see <http://www.gnu.org/licenses/>.
 */

if (!isConnect('admin')) {
	throw new Exception('401 Unauthorized');
}
?>
<div class="col-sm-6">
<legend><i class="fa fa-folder-open"></i>  {{Icônes locales}}</legend>
            <form class="form-horizontal">
                <fieldset>
                    <div class="form-group">
                        <label class="col-sm-4 col-xs-6 control-label">{{Icônes disponibles}}</label>
                        <select id="sel_item3">
						</select>
                    </div>
                    <div class="form-group">
                        <label class="col-sm-4 col-xs-6 control-label">{{Supprimer l'icône}}</label>
                        <div class="col-sm-4 col-xs-6">
                            <a class="btn btn-danger" id="bt_removeIcon"><i class="fa fa-trash-o"></i> {{Supprimer}}</a>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="col-sm-4 col-xs-6 control-label">{{Envoyer une Icône}}</label>
                        <div class="col-sm-8 col-xs-6">
                            <span class="btn btn-default btn-file">
                                <i class="fa fa-cloud-upload"></i> {{Envoyer}}<input id="bt_uploadIcon" type="file" name="file" data-url="plugins/openzwave/core/ajax/openzwave.ajax.php?action=iconUpload&jeedom_token=<?php echo ajax::getToken(); ?>">
                            </span>
                        </div>
                    </div>
                </fieldset>
            </form>
</div>
<div class="col-sm-6">
<legend><i class="fa fa-picture-o"></i>  {{Icône}}</legend>
<div style="text-align: center">
    <img class="dahsicon" name="icon_visuC" src="" style="width:300px"/>
</div>

<script>
updateListIcon();
$("#sel_item3").on('change', function () {
    loadIcon();
});

$("#bt_removeIcon").on('click', function () {
	bootbox.confirm('{{Etes-vous sûr de vouloir supprimer l\'icône suivante }} <b>' + $('#sel_item3 option:selected').text() + '</b> ?',
        function (result) {
            if (result) {
				$.ajax({// fonction permettant de faire de l'ajax
					type: "POST", // methode de transmission des données au fichier php
					url: "plugins/openzwave/core/ajax/openzwave.ajax.php", // url du fichier php
					data: {
						action: "removeIcon",
						icon: $("#sel_item3").value()
					},
					dataType: 'json',
					error: function(request, status, error) {
						handleAjaxError(request, status, error);
					},
					success: function(data) { // si l'appel a bien fonctionné
						if (data.state != 'ok') {
							$('#div_alert').showAlert({message:  data.result,level: 'danger'});
							return;
						}
						modifyWithoutSave=false;
						updateListIcon();
					}
				});
			}
		}
	);
});

$("#bt_uploadIcon").on('click', function () {
    loadIcon();
});

$('#bt_uploadIcon').fileupload({
    dataType: 'json',
    replaceFileInput: false,
    done: function (e, data) {
        if (data.result.state != 'ok') {
            $('#div_alert').showAlert({message: data.result.result, level: 'danger'});
            return;
        }
        updateListIcon();
        $('#div_alert').showAlert({message: '{{Fichier(s) ajouté(s) avec succès}}', level: 'success'});
    }
});

function loadIcon(){
	$(".dahsicon").attr("src",$("#sel_item3").value());
}
function updateListIcon() {
    $.ajax({
        url: "plugins/openzwave/core/ajax/openzwave.ajax.php",
        dataType: 'json',
        data: {
			action: "listIcon"
		},
        error: function (request, status, error) {
            handleAjaxError(request, status, error, $('#div_backupAlert'));
        },
        success: function (data) {
            var options = '';
			list = data['result'];
            for (i in list) {
                options += '<option value="' + list[i][0] + '">' + list[i][1] + '</option>';
            }
            $('#sel_item3').html(options);
			loadIcon();
        }
    });
}
</script>
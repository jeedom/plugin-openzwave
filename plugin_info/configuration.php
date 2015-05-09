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

require_once dirname(__FILE__) . '/../../../core/php/core.inc.php';
include_file('core', 'authentification', 'php');
if (!isConnect()) {
	include_file('desktop', '404', 'php');
	die();
}
$port = config::byKey('port', 'openzwave');
$deamonRunningMaster = openzwave::deamonRunning();
$deamonRunningSlave = array();
if (config::byKey('jeeNetwork::mode') == 'master') {
	foreach (jeeNetwork::byPlugin('openzwave') as $jeeNetwork) {
		try {
			$deamonRunningSlave[$jeeNetwork->getName()] = $jeeNetwork->sendRawRequest('deamonRunning', array('plugin' => 'openzwave'));
		} catch (Exception $e) {
			$deamonRunningSlave[$jeeNetwork->getName()] = false;
		}
	}
}
?>
<form class="form-horizontal">
	<fieldset>
		<?php
echo '<div class="form-group">';
echo '<label class="col-sm-4 control-label">{{Démon local}}</label>';
if (!$deamonRunningMaster) {
	echo '<div class="col-sm-1"><span class="label label-danger tooltips" title="{{Peut être normale si vous etes en deporté}}">NOK</span></div>';
} else {
	echo '<div class="col-sm-1"><span class="label label-success">OK</span></div>';
}
echo '</div>';
foreach ($deamonRunningSlave as $name => $status) {
	echo ' <div class="form-group"><label class="col-sm-4 control-label">{{Sur l\'esclave}} ' . $name . '</label>';
	if (!$status) {
		echo '<div class="col-sm-1"><span class="label label-danger">NOK</span></div>';
	} else {
		echo '<div class="col-sm-1"><span class="label label-success">OK</span></div>';
	}
	echo '</div>';
}
?>
	</fieldset>
</form>

<form class="form-horizontal">
	<fieldset>
		<legend>{{Démon local}}</legend>
		<?php
if (exec('sudo cat /etc/sudoers') != "") {
	echo '<div class="form-group">
			<label class="col-lg-4 control-label">{{Installer/Mettre à jour OpenZwave en local}}</label>
			<div class="col-lg-3">
				<a class="btn btn-danger" id="bt_installDeps"><i class="fa fa-check"></i> {{Lancer}}</a>
			</div>
		</div>';
} else {
	echo '<div class="form-group">
		<label class="col-lg-4 control-label">{{Installation automatique impossible}}</label>
		<div class="col-lg-8">
			{{Veuillez lancer la commande suivante :}} wget http://127.0.0.1/jeedom/plugins/openzwave/ressources/install.sh -v -O install.sh; ./install.sh
		</div>
	</div>';
}
?>
<div class="form-group">
	<label class="col-sm-4 control-label">{{Port clé Z-Wave}}</label>
	<div class="col-sm-4">
		<select class="configKey form-control" data-l1key="port">
			<option value="none">{{Aucun}}</option>
			<?php
foreach (jeedom::getUsbMapping() as $name => $value) {
	echo '<option value="' . $name . '">' . $name . ' (' . $value . ')</option>';
}
foreach (ls('/dev/', 'tty*') as $value) {
	echo '<option value="/dev/' . $value . '">/dev/' . $value . '</option>';
}
?>
		</select>
	</div>
</div>
<div class="form-group">
	<label class="col-sm-4 control-label">{{Port du Serveur (laisser vide par défault)}}</label>
	<div class="col-sm-2">
		<input class="configKey form-control" data-l1key="port_server" placeholder="8083" />
	</div>
</div>
<div class="form-group">
	<label class="col-sm-4 control-label">{{Mode Debug (cela peut ralentir le systeme)}}</label>
	<div class="col-sm-2">
		<input type="checkbox" class="configKey" data-l1key="enableLogging" />
	</div>
</div>
<div class="form-group">
	<label class="col-sm-4 control-label">{{Gestion du démon}}</label>
	<div class="col-sm-8">
		<a class="btn btn-success" id="bt_startopenZwaveDemon"><i class='fa fa-play'></i> {{(Re)démarrer}}</a>
		<a class="btn btn-danger" id="bt_stopopenZwaveDemon"><i class='fa fa-stop'></i> {{Arrêter}}</a>
	</div>
</div>
</fieldset>
</form>
<?php
if (config::byKey('jeeNetwork::mode') == 'master') {
	foreach (jeeNetwork::byPlugin('openzwave') as $jeeNetwork) {
		?>
		<form class="form-horizontal slaveConfig" data-slave_id="<?php echo $jeeNetwork->getId();?>">
			<fieldset>
				<legend>{{Démon sur l'esclave}} <?php echo $jeeNetwork->getName()?></legend>
				<div class="form-group">
					<label class="col-lg-4 control-label">{{Port clé Z-Wave}}</label>
					<div class="col-lg-4">
						<select class="slaveConfigKey form-control" data-l1key="port">
							<option value="none">{{Aucun}}</option>
							<option value="auto">{{Auto}}</option>
							<?php
foreach ($jeeNetwork->sendRawRequest('jeedom::getUsbMapping') as $name => $value) {
			echo '<option value="' . $name . '">' . $name . ' (' . $value . ')</option>';
		}
		?>
						</select>
					</div>
				</div>

				<div class="form-group">
					<label class="col-sm-4 control-label">{{Port du Serveur (laisser vide par défault)}}</label>
					<div class="col-sm-2">
						<input class="slaveConfigKey form-control" data-l1key="port_server" placeholder="8083" />
					</div>
				</div>

				<div class="form-group">
					<label class="col-sm-4 control-label">{{Mode Debug (cela peut ralentir le systeme)}}</label>
					<div class="col-sm-2">
						<input type="checkbox" class="slaveConfigKey" data-l1key="enableLogging" />
					</div>
				</div>

				<div class="form-group">
					<label class="col-lg-4 control-label">{{Gestion du démon}}</label>
					<div class="col-lg-8">
						<a class="btn btn-success bt_restartOpenZwaveDeamon"><i class='fa fa-play'></i> {{(Re)démarrer}}</a>
						<a class="btn btn-danger bt_stopZwaveDeamon"><i class='fa fa-stop'></i> {{Arrêter}}</a>
					</div>
				</div>
			</fieldset>
		</form>
		<?php
}
}
?>

<script>
	$('#bt_installDeps').on('click',function(){
		bootbox.confirm('{{Etes-vous sûr de vouloir installer/mettre à jour Openzwave ? }}', function (result) {
			if (result) {
				$('#md_modal').dialog({title: "{{Installation / Mise à jour}}"});
				$('#md_modal').load('index.php?v=d&plugin=openzwave&modal=update.openzwave').dialog('open');
			}
		});
	});

	$('#bt_stopopenZwaveDemon').on('click', function() {
		stopopenZwaveDemon('local',0);
	});

	$('#bt_startopenZwaveDemon').on('click', function() {
		startopenZwaveDemon('local',0);
	});
	$('.bt_restartOpenZwaveDeamon').on('click', function() {
		startopenZwaveDemon('remote',$(this).closest('.slaveConfig').attr('data-slave_id'));
	});

	$('.bt_stopZwaveDeamon').on('click', function() {
		stopopenZwaveDemon('remote',$(this).closest('.slaveConfig').attr('data-slave_id'));
	});

	function stopopenZwaveDemon(type,id) {
	    $.ajax({// fonction permettant de faire de l'ajax
	        type: "POST", // methode de transmission des données au fichier php
	        url: "plugins/openzwave/core/ajax/openzwave.ajax.php", // url du fichier php
	        data: {
	        	action: "stopDeamon",
	        	type: type,
	        	id: id
	        },
	        dataType: 'json',
	        error: function(request, status, error) {
	        	handleAjaxError(request, status, error);
	        },
	        success: function(data) { // si l'appel a bien fonctionné
	        if (data.state != 'ok') {
	        	$('#div_alert').showAlert({message: data.result, level: 'danger'});
	        	return;
	        }
	        $('#div_alert').showAlert({message: 'Le démon a été correctement arreté', level: 'success'});
	        $('#ul_plugin .li_plugin[data-plugin_id=openzwave]').click();
	    }
	});

	}

	function startopenZwaveDemon(type,id) {
	    $.ajax({// fonction permettant de faire de l'ajax
	        type: "POST", // methode de transmission des données au fichier php
	        url: "plugins/openzwave/core/ajax/openzwave.ajax.php", // url du fichier php
	        data: {
	        	action: "startDeamon",
	        	type: type,
	        	id: id
	        },
	        dataType: 'json',
	        error: function(request, status, error) {
	        	handleAjaxError(request, status, error);
	        },
	        success: function(data) { // si l'appel a bien fonctionné
	        if (data.state != 'ok') {
	        	$('#div_alert').showAlert({message: data.result, level: 'danger'});
	        	return;
	        }
	        $('#div_alert').showAlert({message: 'Le démon a été correctement lancé', level: 'success'});
	        $('#ul_plugin .li_plugin[data-plugin_id=openzwave]').click();
	    }
	});

	}
</script>

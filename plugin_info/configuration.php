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
$deamonRunningMaster = openzwave::deamonRunning();
$deamonRunningSlave = array();
$deamonSlaveVersion = array();
if (config::byKey('jeeNetwork::mode') == 'master') {
	foreach (jeeNetwork::byPlugin('openzwave') as $jeeNetwork) {
		$deamonSlaveVersion[$jeeNetwork->getName()] = array('openzwave' => 0, 'python-openzwave' => 0);
		$deamonRunningSlave[$jeeNetwork->getName()] = false;
		try {
			$deamonRunningSlave[$jeeNetwork->getName()] = $jeeNetwork->sendRawRequest('deamonRunning', array('plugin' => 'openzwave'));
			$deamonSlaveVersion[$jeeNetwork->getName()]['openzwave'] = $jeeNetwork->sendRawRequest('getVersion', array('plugin' => 'openzwave', 'module' => 'openzwave'));
			$deamonSlaveVersion[$jeeNetwork->getName()]['compilation'] = $jeeNetwork->sendRawRequest('compilationOk', array('plugin' => 'openzwave'));
		} catch (Exception $e) {

		}
	}
}

$urlMasterLocal = false;
try {
	$request_http = new com_http(network::getNetworkAccess('internal', 'proto:127.0.0.1:port:comp') . '/plugins/openzwave/core/php/jeeZwave.php?apikey=' . config::byKey('api') . '&test=1');
	$request_http->setNoSslCheck(false);
	if ($request_http->exec(1, 1) == 'OK') {
		$urlMasterLocal = true;
	}
} catch (Exception $e) {

}
$urlMasterDistant = false;
try {
	$request_http = new com_http(network::getNetworkAccess('internal', 'proto:ip:port:comp') . '/plugins/openzwave/core/php/jeeZwave.php?apikey=' . config::byKey('api') . '&test=1');
	$request_http->setNoSslCheck(false);
	if ($request_http->exec(1, 1) == 'OK') {
		$urlMasterDistant = true;
	}
} catch (Exception $e) {

}
?>
<form class="form-horizontal">
	<fieldset>
		<?php
echo '<div class="form-group">';
echo '<label class="col-sm-4 control-label">{{Retour local}}</label>';
if (!$urlMasterLocal) {
	echo '<div class="col-sm-1"><span class="label label-danger tooltips" style="font-size : 1em;" title="{{Vérifiez votre configuration sur la page de configuration réseaux, celle-ci est incorrecte et le démon ne pourra communiquer avec Jeedom}}">NOK</span></div>';
} else {
	echo '<div class="col-sm-1"><span class="label label-success" style="font-size : 1em;">OK</span></div>';
}
echo '<label class="col-sm-1 control-label">{{Retour distant}}</label>';
if (!$urlMasterDistant) {
	echo '<div class="col-sm-1"><span class="label label-danger tooltips" style="font-size : 1em;" title="{{Vérifiez votre configuration sur la page de configuration réseaux, celle-ci est incorrecte et le démon ne pourra communiquer avec Jeedom}}">NOK</span></div>';
} else {
	echo '<div class="col-sm-1"><span class="label label-success" style="font-size : 1em;">OK</span></div>';
}
echo '<label class="col-sm-2 control-label">{{OpenZwave}} (' . openzwave::getVersion('openzwave') . ')</label>';
if (version_compare(config::byKey('openzwave_version', 'openzwave'), openzwave::getVersion('openzwave'), '>')) {
	echo '<div class="col-sm-1"><span class="label label-danger" style="font-size : 1em;">NOK</span></div>';
} else {
	echo '<div class="col-sm-1"><span class="label label-success" style="font-size : 1em;">OK</span></div>';
}
echo '<label class="col-sm-1 control-label">{{Compilation}}</label>';
if (openzwave::compilationOk()) {
	echo '<div class="col-sm-1"><span class="label label-success" style="font-size : 1em;">OK</span></div>';
} else {
	echo '<div class="col-sm-1"><span class="label label-danger" style="font-size : 1em;">NOK</span></div>';
}
echo '</div>';

echo '<div class="form-group">';
echo '<label class="col-sm-4 control-label">{{Démon local}}</label>';
if (!$deamonRunningMaster) {
	echo '<div class="col-sm-1"><span class="label label-danger tooltips" style="font-size : 1em;" title="{{Peut être normale si vous etes en deporté}}">NOK</span></div>';
} else {
	echo '<div class="col-sm-1"><span class="label label-success" style="font-size : 1em;">OK</span></div>';
}

echo '</div>';
foreach ($deamonRunningSlave as $name => $status) {
	echo ' <div class="form-group"><label class="col-sm-4 control-label">{{Sur l\'esclave}} ' . $name . '</label>';
	if (!$status) {
		echo '<div class="col-sm-1"><span class="label label-danger" style="font-size : 1em;">NOK</span></div>';
	} else {
		echo '<div class="col-sm-1"><span class="label label-success" style="font-size : 1em;">OK</span></div>';
	}
	echo '<label class="col-sm-3 control-label">{{OpenZwave}} (' . $deamonSlaveVersion[$name]['openzwave'] . ')</label>';
	if (version_compare(config::byKey('openzwave_version', 'openzwave'), $deamonSlaveVersion[$name]['openzwave'], '>')) {
		echo '<div class="col-sm-1"><span class="label label-danger" style="font-size : 1em;">NOK</span></div>';
	} else {
		echo '<div class="col-sm-1"><span class="label label-success" style="font-size : 1em;">OK</span></div>';
	}
	echo '<label class="col-sm-1 control-label">{{Compilation}}</label>';
	if ($deamonSlaveVersion[$name]['compilation']) {
		echo '<div class="col-sm-1"><span class="label label-success" style="font-size : 1em;">OK</span></div>';
	} else {
		echo '<div class="col-sm-1"><span class="label label-danger" style="font-size : 1em;">NOK</span></div>';
	}
	echo '</div>';
}
?>
	</fieldset>
</form>

<form class="form-horizontal">
	<fieldset>
		<legend><i class="fa fa-list-alt"></i> {{Général}}</legend>
		<?php if (config::byKey('jeeNetwork::mode') == 'master') {?>
			<div class="form-group">
				<label class="col-lg-4 control-label">{{Supprimer automatiquement les périphériques exclus}}</label>
				<div class="col-lg-3">
					<input type="checkbox" class="configKey bootstrapSwitch" data-l1key="autoRemoveExcludeDevice" />
				</div>
			</div>
			<div class="form-group">
				<label class="col-lg-4 control-label">{{Soigner le réseau automatiquement 2 fois par semaine}}</label>
				<div class="col-lg-3">
					<input type="checkbox" class="configKey bootstrapSwitch" data-l1key="auto_health" />
				</div>
			</div>
			<legend><i class="fa fa-cog"></i>  {{Gestion avancée}}</legend>
			<div class="form-group">
				<label class="col-lg-4 control-label">{{Options avancées}}</label>
				<div class="col-lg-5">
					<a class="btn btn-success" id="bt_consoleZwave"><i class="fa fa-terminal"></i> {{Console}}</a>
					<a class="btn btn-warning" id="bt_backupsZwave"><i class="fa fa-floppy-o"></i> {{Backups}}</a>
					<a class="btn btn-danger" id="bt_fileconfigZwave"><i class="fa fa-file-o"></i> {{Configuration}}</a>
				</div>
			</div>
			<?php }
if (config::byKey('jeeNetwork::mode') == 'master' && count(eqLogic::byType('zwave')) > 0) {?>
			<div class="form-group">
				<label class="col-lg-4 control-label">{{Migration des équipements zwave}}</label>
				<div class="col-lg-3">
					<a class="btn btn-warning" id="bt_migrateZwave"><i class="fa fa-ship"></i> {{Migrer}}</a>
				</div>
			</div>
			<?php }
?>
		</fieldset>
	</form>
	<form class="form-horizontal">
		<fieldset>
			<legend><i class="icon loisir-darth"></i>  {{Démon local}}</legend>
			<?php
if (jeedom::isCapable('sudo')) {
	echo '<div class="form-group">
				<label class="col-lg-4 control-label">{{Dépendance OpenZwave locale}}</label>
				<div class="col-lg-3">
					<a class="btn btn-warning bt_installDeps"><i class="fa fa-check"></i> {{Installer/Mettre à jour}}</a>
				</div>
			</div>';
} else {
	echo '<div class="alert alert danger">{{Jeedom n\'a pas les droits sudo sur votre système, il faut lui ajouter pour qu\'il puisse installer le démon openzwave, voir <a target="_blank" href="https://jeedom.fr/doc/documentation/installation/fr_FR/doc-installation.html#autre">ici</a> partie 1.7.4}}</div>';
}
?>
		<div class="form-group">
			<label class="col-sm-4 control-label">{{Port clé Z-Wave}}</label>
			<div class="col-sm-4">
				<select class="configKey form-control" data-l1key="port">
					<option value="none">{{Aucun}}</option>
					<?php
foreach (jeedom::getUsbMapping('', true) as $name => $value) {
	echo '<option value="' . $name . '">' . $name . ' (' . $value . ')</option>';
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
			<label class="col-sm-4 control-label">{{Mode "direct push" (recommandé)}}</label>
			<div class="col-sm-2">
				<input type="checkbox" class="configKey bootstrapSwitch" data-l1key="directPush" />
			</div>
		</div>
		<div class="form-group">
			<label class="col-sm-4 control-label">{{Gestion du démon}}</label>
			<div class="col-sm-8">
				<a class="btn btn-success" id="bt_startopenZwaveDemon"><i class='fa fa-play'></i> {{(Re)démarrer}}</a>
				<a class="btn btn-danger" id="bt_stopopenZwaveDemon"><i class='fa fa-stop'></i> {{Arrêter}}</a>
				<a class="btn btn-warning" id="bt_launchOpenZwaveInDebug"><i class="fa fa-exclamation-triangle"></i> {{Lancer en mode debug}}</a>
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
							<?php
foreach ($jeeNetwork->sendRawRequest('jeedom::getUsbMapping', array('gpio' => true)) as $name => $value) {
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
					<label class="col-sm-4 control-label">{{Mode "direct push" (recommandé)}}</label>
					<div class="col-sm-2">
						<input type="checkbox" class="slaveConfigKey bootstrapSwitch" data-l1key="directPush" />
					</div>
				</div>
				<div class="form-group">
					<label class="col-lg-4 control-label">{{Gestion du démon}}</label>
					<div class="col-lg-8">
						<a class="btn btn-success bt_restartOpenZwaveDeamon"><i class='fa fa-play'></i> {{(Re)démarrer}}</a>
						<a class="btn btn-danger bt_stopZwaveDeamon"><i class='fa fa-stop'></i> {{Arrêter}}</a>
						<a class="btn btn-warning bt_launchOpenZwaveInDebug"><i class="fa fa-exclamation-triangle"></i> {{Lancer en mode debug}}</a>
					</div>
				</div>
			</fieldset>
		</form>
		<?php
}
}
?>

<script>
	$('.bt_installDeps').on('click',function(){
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

	$('.bt_launchOpenZwaveInDebug').on('click', function () {
		var slave_id = $(this).closest('.slaveConfig').attr('data-slave_id');
		bootbox.confirm('{{Etes-vous sur de vouloir lancer le démon en mode debug ? N\'oubliez pas de le relancer en mode normale une fois terminé}}', function (result) {
			if (result) {
				$('#md_modal').dialog({title: "{{Openzwave en mode debug}}"});
				$('#md_modal').load('index.php?v=d&plugin=openzwave&modal=show.debug&slave_id='+slave_id).dialog('open');
			}
		});
	});

	$('#bt_launchOpenZwaveInDebug').on('click', function () {
		bootbox.confirm('{{Etes-vous sûr de vouloir lancer le démon en mode debug ? N\'oubliez pas d\'arrêter/redémarrer le démon une fois terminé}}', function (result) {
			if (result) {
				$('#md_modal').dialog({title: "{{Openzwave en mode debug}}"});
				$('#md_modal').load('index.php?v=d&plugin=openzwave&modal=show.debug').dialog('open');
			}
		});
	});

	$('#bt_migrateZwave').on('click', function () {
		bootbox.confirm('{{Etes-vous sûr de vouloir lancer la migration cette opération est irreversible}}', function (result) {
			if (result) {
				$('#md_modal').dialog({title: "{{Openzwave migration}}"});
				$('#md_modal').load('index.php?v=d&plugin=openzwave&modal=migrate.zwave').dialog('open');
			}
		});
	});

	$('#bt_backupsZwave').on('click', function () {
		$('#md_modal').dialog({title: "{{Backups}}"});
		$('#md_modal').load('index.php?v=d&plugin=openzwave&modal=backup').dialog('open');
	});

	$('#bt_fileconfigZwave').on('click', function () {
		$('#md_modal').dialog({title: "{{Configuration}}"});
		$('#md_modal').load('index.php?v=d&plugin=openzwave&modal=config').dialog('open');
	});

	$('#bt_consoleZwave').on('click', function () {
		$('#md_modal').dialog({title: "{{Console}}"});
		$('#md_modal').load('index.php?v=d&plugin=openzwave&modal=console').dialog('open');
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

	function openzwave_postSaveConfiguration(){
		startopenZwaveDemon('local',0);
		  $.ajax({// fonction permettant de faire de l'ajax
	        type: "POST", // methode de transmission des données au fichier php
	        url: "plugins/openzwave/core/ajax/openzwave.ajax.php", // url du fichier php
	        data: {
	        	action: "rewriteNginxAndRestartCron",
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
	    }
	});
		}

		function openzwave_postSaveSlaveConfiguration(_slave_id){
			startopenZwaveDemon('remote',_slave_id);
		}
	</script>

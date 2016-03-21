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
?>
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
					<a class="btn btn-danger" id="bt_fileconfigZwave"><i class="fa fa-file-o"></i> {{Zwcfg}}</a>
					<a class="btn btn-success" id="bt_syncconfigZwave"><i class="fa fa-refresh"></i> {{Configs modules}}</a>
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
				<label class="col-sm-4 control-label">{{Mettre à jour la configuration des modules automatiquement}}</label>
				<div class="col-sm-2">
					<input type="checkbox" class="configKey bootstrapSwitch" data-l1key="auto_updateConf" checked/>
				</div>
			</div>
		</fieldset>
	</form>
	<?php
if (config::byKey('jeeNetwork::mode') == 'master') {
	foreach (jeeNetwork::byPlugin('openzwave') as $jeeNetwork) {
		?>
			<form class="form-horizontal slaveConfig" data-slave_id="<?php echo $jeeNetwork->getId(); ?>">
				<fieldset>
					<legend>{{Démon sur l'esclave}} <?php echo $jeeNetwork->getName() ?></legend>
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
				<label class="col-sm-4 control-label">{{Mettre à jour la configuration des modules automatiquement}}</label>
				<div class="col-sm-2">
					<input type="checkbox" class="slaveConfigKey bootstrapSwitch" data-l1key="auto_updateConf" checked/>
				</div>
			</div>
				</fieldset>
			</form>
			<?php
}
}
?>

	<script>
		$('#bt_migrateZwave').on('click', function () {
			bootbox.confirm('{{Etes-vous sûr de vouloir lancer la migration cette opération est irreversible}}', function (result) {
				if (result) {
					$('#md_modal2').dialog({title: "{{Openzwave migration}}"});
					$('#md_modal2').load('index.php?v=d&plugin=openzwave&modal=migrate.zwave').dialog('open');
				}
			});
		});

		$('#bt_backupsZwave').on('click', function () {
			$('#md_modal2').dialog({title: "{{Backups}}"});
			$('#md_modal2').load('index.php?v=d&plugin=openzwave&modal=backup').dialog('open');
		});

		$('#bt_fileconfigZwave').on('click', function () {
			$('#md_modal2').dialog({title: "{{Configuration}}"});
			$('#md_modal2').load('index.php?v=d&plugin=openzwave&modal=config').dialog('open');
		});

		$('#bt_consoleZwave').on('click', function () {
			$('#md_modal2').dialog({title: "{{Console}}"});
			$('#md_modal2').load('index.php?v=d&plugin=openzwave&modal=console').dialog('open');
		});

		$('#bt_syncconfigZwave').on('click',function(){
			bootbox.confirm('{{Etes-vous sûr de vouloir télécharger les dernières configurations des modules ?}}', function (result) {
				if (result) {
					$('#md_modal2').dialog({title: "{{Téléchargement des configurations}}"});
					$('#md_modal2').load('index.php?v=d&plugin=openzwave&modal=syncconf.openzwave').dialog('open');
				}
			});
		});
	</script>

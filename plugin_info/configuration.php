<?php
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

require_once dirname(__FILE__) . '/../../../core/php/core.inc.php';
include_file('core', 'authentification', 'php');
if (!isConnect('admin')) {
	throw new Exception('{{401 - Accès non autorisé}}');
}
?>
<form class="form-horizontal">
	<fieldset>
		<legend><i class="fas fa-list-alt"></i> {{Général}}</legend>

		<div class="form-group">
			<label class="col-lg-4 control-label">{{Supprimer automatiquement les périphériques exclus}}</label>
			<div class="col-lg-3">
				<input type="checkbox" class="configKey" data-l1key="autoRemoveExcludeDevice" />
			</div>
		</div>
		<div class="form-group">
			<label class="col-sm-4 control-label">{{Appliquer le jeu de configuration recommandée à l'inclusion}}</label>
			<div class="col-sm-2">
				<input type="checkbox" class="configKey" data-l1key="auto_applyRecommended" checked/>
			</div>
		</div>
		<div class="form-group">
			<label class="col-sm-4 control-label">{{Désactiver l'actualisation en arrière-plan des variateurs}}</label>
			<div class="col-sm-2">
				<input type="checkbox" class="configKey" data-l1key="suppress_refresh" checked/>
			</div>
		</div>
		<div class="form-group">
			<label class="col-sm-4 control-label">{{Cycle (s)}}</label>
			<div class="col-sm-2">
				<input class="configKey form-control" data-l1key="cycle" />
			</div>
		</div>
		<div class="form-group">
			<label class="col-sm-4 control-label">{{Port clé Z-Wave}}</label>
			<div class="col-sm-2">
				<select class="configKey form-control" data-l1key="port">
					<option value="none">{{Aucun}}</option>
					<option value="auto">{{Auto}}</option>
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
			<label class="col-lg-4 control-label">{{Options avancées}}</label>
			<div class="col-lg-5">
				<a class="btn btn-warning" id="bt_backupsZwave"><i class="fa fa-floppy-o"></i> {{Backups}}</a>
				<a class="btn btn-warning" id="bt_syncconfigZwave"><i class="fas fa-sync-alt"></i> {{Configs modules}}</a>
			</div>
		</div>
	</fieldset>
</form>

<script>
	$('#bt_backupsZwave').on('click', function () {
		$('#md_modal2').dialog({title: "{{Backups}}"});
		$('#md_modal2').load('index.php?v=d&plugin=openzwave&modal=backup').dialog('open');
	});
	$('#bt_syncconfigZwave').on('click',function(){
		bootbox.confirm('{{Etes-vous sûr de vouloir télécharger les dernières configurations des modules ? Ceci relancera le plugin OpenZwave.}}', function (result) {
			if (result) {
				$('#md_modal2').dialog({title: "{{Téléchargement des configurations}}"});
				$('#md_modal2').load('index.php?v=d&plugin=openzwave&modal=syncconf.openzwave').dialog('open');
			}
		});
	});
</script>

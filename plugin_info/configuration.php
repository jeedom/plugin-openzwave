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
		<div class="form-group">
			<label class="col-md-4 control-label">{{Appliquer la configuration recommandée lors de l'inclusion}}
				<sup><i class="fas fa-question-circle tooltips" title="{{Cocher la case pour appliquer le jeu de configuration spécialement recommandé pour votre module par l'équipe Jeedom}}"></i></sup>
			</label>
			<div class="col-md-1">
				<input type="checkbox" class="configKey" data-l1key="auto_applyRecommended" checked/>
			</div>
			<label class="col-md-4 control-label">{{Suppression automatique des périphériques exclus}}
				<sup><i class="fas fa-question-circle tooltips" title="{{Cocher la case pour supprimer automatiquement les équipements Jeedom correspondant à des périphériques exclus du contrôleur}}"></i></sup>
			</label>
			<div class="col-md-1">
				<input type="checkbox" class="configKey" data-l1key="autoRemoveExcludeDevice" />
			</div>
		</div>
		<div class="form-group">
			<label class="col-md-4 control-label">{{Désactiver l'actualisation en arrière-plan des variateurs}}
				<sup><i class="fas fa-question-circle tooltips" title="{{Cocher la case pour empêcher le rafraîchissement des variateurs en arrière-plan}}"></i></sup>
			</label>
			<div class="col-md-1">
				<input type="checkbox" class="configKey" data-l1key="suppress_refresh" checked/>
			</div>
			<label class="col-md-4 control-label">{{Désactiver la gestion automatique des processus USB}} <sub>(socat)</sub>
				<sup><i class="fas fa-question-circle tooltips" title="{{Cocher la case pour empêcher l'arrêt du processus socat lors du redémarrage du démon. Peut être utile en cas d'utilisation d'un contrôleur sur un port USB distant}}"></i></sup>
			</label>
			<div class="col-md-1">
				<input type="checkbox" class="configKey" data-l1key="socat"/>
			</div>
		</div>
		<br>
		<div class="form-group">
			<label class="col-md-4 control-label">{{Cycle de rafraîchissement}} <sub>({{secondes}})</sub>
				<sup><i class="fas fa-question-circle tooltips" title="{{Fréquence de mise à jour des données Zwave en secondes}}"></i></sup>
			</label>
			<div class="col-md-6">
				<input type="number" class="configKey form-control" data-l1key="cycle" />
			</div>
		</div>
		<div class="form-group">
			<label class="col-md-4 control-label">{{Port du contrôleur Zwave}}
				<sup><i class="fas fa-question-circle tooltips" title="{{Renseigner le port utilisé par le contrôleur Zwave. Pour les contrôleurs branchés en USB, il est possible de découvrir automatiquement le port en sélectionnant Auto}}"></i></sup>
			</label>
			<div class="col-md-6">
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
			<label class="col-md-4 control-label">{{Port du Serveur}}
				<sup><i class="fas fa-question-circle tooltips" title="{{Permet de modifier le port de communication interne du démon. Réservé aux utilisateurs avancés}}"></i></sup>
			</label>
			<div class="col-md-6">
				<input class="configKey form-control" data-l1key="host_server" placeholder="127.0.0.1" />
			</div>
			<div class="col-md-6">
				<input class="configKey form-control" data-l1key="port_server" placeholder="8083" />
			</div>
		</div>
		<br>
		<div class="form-group">
			<label class="col-md-4 control-label">{{Options avancées}}</label>
			<div class="col-md-6">
				<a class="btn btn-warning" id="bt_backupsZwave"><i class="fas fa-save"></i> {{Backups Openzwave}}</a>
				<a class="btn btn-warning" id="bt_backupsNetwork"><i class="fas fa-random"></i> {{Backups Réseau}}</a>
				<a class="btn btn-warning" id="bt_syncconfigZwave" title="Cliquer sur le bouton pour récupérer manuellement les derniers fichiers de configuration OpenZwave à jour"><i class="fas fa-sync-alt"></i> {{Configuration des modules}}</a>
			</div>
		</div>
	</fieldset>
</form>

<script>
$('#bt_backupsZwave').on('click', function () {
	$('#md_modal2').dialog({title: "{{Backups Openzwave}}"});
	$('#md_modal2').load('index.php?v=d&plugin=openzwave&modal=backup').dialog('open');
});
$('#bt_backupsNetwork').on('click', function () {
	$('#md_modal2').dialog({title: "{{Backups Réseau}}"});
	$('#md_modal2').load('index.php?v=d&plugin=openzwave&modal=backupnetwork').dialog('open');
});
$('#bt_syncconfigZwave').on('click',function(){
	bootbox.confirm('{{Etes-vous sûr de vouloir télécharger les dernières configurations de modules ? Le plugin sera redémarré suite à cette action.}}', function (result) {
		if (result) {
			$('#md_modal2').dialog({title: "{{Téléchargement des configurations}}"});
			$('#md_modal2').load('index.php?v=d&plugin=openzwave&modal=syncconf.openzwave').dialog('open');
		}
	});
});
</script>

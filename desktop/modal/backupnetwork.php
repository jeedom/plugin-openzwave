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

if (!isConnect('admin')) {
	throw new Exception('401 Unauthorized');
}
?>
<span class="pull-left alert" id="span_state" style="background-color : #dff0d8;color : #3c763d;height:35px;border-color:#d6e9c6;display:none;margin-bottom:0px;"><span style="position:relative; top : -7px;">{{Demande envoyée}}</span></span>
<br/><br/>

<div id='div_backupAlert' style="display: none;"></div>
<div class="alert alert-danger">{{Un backup réseau d'un contrôleur Zwave n'est pas une chose anodine. Soyez bien sûr du port et de l'ordre dans lequel vous faites les choses. Jeedom ne pourra être tenu responsable d'une perte de votre contrôleur. 
								Smart : Odroid C2 (/dev/ttyS1) / Atlas : Jeedom Atlas (/dev/ttyS2) / Dongle : (/dev/ttyACM0).}}</div>
				</div>
<div id='div_backupProgress'>
<?php
if (config::byKey('backupInProgress', 'openzwave',0) ==1){
	echo '<div class="alert alert-info">{{Un backup ou une restauration est en cours}}</div>';
}
?>
</div>
<form class="form-horizontal">
    <fieldset>
	<div class="row">
		<div class="col-lg-12 col-sm-12">
			<div class="row">
				<div class="col-sm-12">
					<div class="panel panel-primary">
						<div class="panel-heading">
							<h3 class="panel-title"><i class="fas fa-folder-open"></i> {{Sauvegardes}}</h3>
						</div>
						<div class="panel-body">
							<form class="form-horizontal">
								<fieldset>
									<div class="form-group">
										<label class="col-sm-6 col-xs-6 control-label">{{Nom du backup}}</label>
										<div class="col-sm-6 col-xs-6">
											<input type="text" class="backName form-control"/>
										</div>
									</div>
									<div class="form-group">
										<label class="col-sm-6 control-label">{{Port clé Z-Wave}}</label>
										<div class="col-sm-6">
											<select class="zwavePort form-control">
												<option value="none">{{Aucun}}</option>
												<?php
													foreach (jeedom::getUsbMapping('', true) as $name => $value) {
															echo '<option value="' . $value . '">' . $name . ' (' . $value . ')</option>';
													}
												?>
											</select>
										</div>
									</div>
									<div class="form-group">
										<div class="col-sm-6 col-xs-6"></div>
										<div class="col-sm-6 col-xs-6">
											<a class="btn btn-success bt_backupNetwork" style="width:100%;"><i class="fas fa-sync fa-spin" style="display:none;"></i> <i class="fas fa-save"></i> {{Lancer une sauvegarde}}</a>
										</div>
									</div>

									<div class="form-group">
										<label class="col-xs-12"><i class="fas fa-tape"></i> {{Sauvegardes disponibles}}</label>
										<div class="col-xs-12">
											<select class="form-control" id="sel_restoreNetBackup"> </select>
										</div>
									</div>
									<div class="form-group">
										<div class="col-sm-6 col-xs-12">
											<a class="btn btn-danger" id="bt_removeNetBackup" style="width:100%;"><i class="far fa-trash-alt"></i> {{Supprimer la sauvegarde}}</a>
										</div>
										<div class="col-sm-6 col-xs-12">
											<a class="btn btn-warning" id="bt_restoreNetBackup" style="width:100%;"><i class="fas fa-sync fa-spin" style="display:none;"></i> <i class="far fa-file"></i> {{Restaurer la sauvegarde}}</a>
										</div>
									</div>
									<div class="form-group">
										<div class="col-sm-6 col-xs-12">
											<a class="btn btn-success" id="bt_downloadNetBackup" style="width:100%;"><i class="fas fa-cloud-download-alt"></i> {{Télécharger la sauvegarde}}</a>
										</div>
										<div class="col-sm-6 col-xs-12">
											<span class="btn btn-default btn-file" style="width:100%;">
												<i class="fas fa-cloud-upload-alt"></i> {{Ajouter une sauvegarde}}<input id="bt_uploadNetBackup" type="file" name="file" data-url="plugins/openzwave/core/ajax/openzwave.ajax.php?action=fileupload">
											</span>
										</div>
									</div>
								</fieldset>
							</form>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
   </fieldset>
    </form>
</div>
<?php include_file('core', 'openzwave', 'class.js', 'openzwave');?>
<?php include_file('desktop', 'backupnetwork', 'js', 'openzwave');?>

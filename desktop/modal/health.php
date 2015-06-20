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
<span class="pull-left alert" id="span_state" style="background-color : #dff0d8;color : #3c763d;height:35px;border-color:#d6e9c6;display:none;margin-bottom:0px;"><span style="position:relative; top : -7px;">{{Demande envoyée}}</span></span>
<span class='pull-right'>
	<select class="form-control expertModeVisible" style="width : 200px;" id="sel_zwaveHealthServerId">
		<?php
foreach (openzwave::listServerZwave() as $id => $server) {
	if (isset($server['name'])) {
		echo '<option value="' . $id . '" data-path="' . $server['path'] . '">' . $server['name'] . '</option>';
	}
}
?>
	</select>
</span>

<br/><br/>

<div id='div_networkHealthAlert' style="display: none;"></div>
<table class="table table-condensed tablesorter" id="table_healthNetwork">
	<thead>
		<tr>
			<th>{{Module}}</th>
			<th>{{ID}}</th>
			<th>{{Notification}}</th>
			<th>{{Groupe}}</th>
			<th>{{Constructeur}}</th>
			<th>{{Voisin}}</th>
			<th>{{Statut}}</th>
			<th>{{Batterie}}</th>
			<th>{{Wakeup time}}</th>
			<th>{{Paquet total}}</th>
			<th>{{% OK}}</th>
			<th>{{Temporisation}}</th>
			<th>{{Dernière communication}}</th>
			<th>{{Ping}}</th>
		</tr>
	</thead>
	<tbody>

	</tbody>
</table>
<?php include_file('desktop', 'health', 'js', 'openzwave');?>
<script>
	var path = $('#sel_zwaveHealthServerId option:selected').attr('data-path')+'/';
	$("#sel_zwaveHealthServerId").on("change",function() {
		path = $('#sel_zwaveHealthServerId option:selected').attr('data-path')+'/';
		window["app_health"].init();
		window["app_health"].show();
	});
	var nodes = {};
	if (window["app_health"]!=undefined){
		window["app_health"].init();
		window["app_health"].show();
	}
	$('.tab-pane').height($('#md_modal').height() - 50);
	$('.tab-pane').css('overflow','scroll');
</script>
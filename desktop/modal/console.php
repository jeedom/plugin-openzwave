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
<span class='pull-right'>
	<select class="form-control expertModeVisible" style="width : 200px;" id="sel_zwaveNetworkServerId">
		<?php
foreach (openzwave::listServerZwave() as $id => $server) {
	if (isset($server['name'])) {
		echo '<option value="' . $id . '" data-path="' . $server['path'] . '">' . $server['name'] . '</option>';
	}
}
?>
	</select>
</span>

<style>
#log {
    width:100%;
    height:700px;
    margin:0px;
    padding:0px;
    font-size:16px;
    color:#fff;
    background-color:#300a24;
    overflow: scroll;
    overflow-x: hidden;
    font-size:16px;
}

.console-out {
    padding-left:20px;
    padding-top:20px;
}
</style>
<div id='div_consoleOpenzwaveAlert' style="display: none;"></div>
<button type="button" id="startLiveLog" class="btn btn-success pull-left"><i class="fa fa-play"></i> {{Reprendre}}</button>
<button type="button" id="stopLiveLog" class="btn btn-warning pull-left"><i class="fa fa-pause"></i> {{Pause}}</button>
<pre id="log"><div class="console-out"></div></pre>

<?php include_file('desktop', 'console', 'js', 'openzwave');?>
<script>
var path = $('#sel_zwaveNetworkServerId option:selected').attr('data-path')+'/';
$("#sel_zwaveNetworkServerId").on("change",function() {
	path = $('#sel_zwaveNetworkServerId option:selected').attr('data-path')+'/';
    window["app_console"].init();
	window["app_console"].show();
});
	var nodes = {};
	if (window["app_console"]!=undefined){
		window["app_console"].init();
		window["app_console"].show();
	}
	$('.tab-pane').height($('#md_modal').height() - 100);
	$('.tab-pane').css('overflow','scroll');
</script>
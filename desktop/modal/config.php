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
<style media="screen" type="text/css">
    .noscrolling {
        width: 99%;
        overflow: hidden;
    }

    .table-striped {
        width: 90%;
    }

    .node-item {
        border: 1px solid;
    }

    .modal-dialog-center {
        margin: 0;
        position: absolute;
        top: 0%;
        left: 0%;
    }

    .greeniconcolor {
        color: green;
    }

    .yellowiconcolor {
        color: #FFD700;
    }

    .rediconcolor {
        color: red;
    }
</style>

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
    .bound-config {
        width: 100%;
        margin: 0px;
        padding: 0px;
    }

    textarea {
        width: 100%;
        margin: 0px;
        padding: 20px;
        height: 700px;
        font-size: 14px;

    }
</style>
<div id='div_configOpenzwaveAlert' style="display: none;"></div>
<button id="saveconf" class="btn btn-success pull-left"><i class="fa fa-floppy-o"></i> {{Sauvegarder les changements}}
</button><br/>
<br/>
<div class="bound-config">
    <textarea id="zwcfgfile" class="boxsizingborder"></textarea>
</div>

<?php include_file('desktop', 'config', 'js', 'openzwave');?>
<script>
    var path = $('#sel_zwaveNetworkServerId option:selected').attr('data-path') + '/';
    $("#sel_zwaveNetworkServerId").on("change", function () {
        path = $('#sel_zwaveNetworkServerId option:selected').attr('data-path') + '/';
        window["app_config"].init();
        window["app_config"].show();
    });
    var nodes = {};
    if (window["app_config"] != undefined) {
        window["app_config"].init();
        window["app_config"].show();
    }
</script>
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
sendVarToJs('debugMode_slaveId', init('slave_id'));
echo '<div class="alert alert-warning">{{Attention le lancement en mode debug est très consommateur en ressources et en log, pensez bien à relancer le démon une fois l\'analyse terminée.}}</div>';
?>
<div id='div_openzwaveShowDebug' style="display: none;"></div>
<a class="btn btn-warning pull-right" data-state="1" id="bt_openzwaveLogStopStart"><i class="fa fa-pause"></i> {{Pause}}</a>
<input class="form-control pull-right" id="in_openzwaveLogSearch" style="width : 300px;" placeholder="{{Rechercher}}" />
<br/><br/><br/>
<pre id='pre_openzwavelog' style='overflow: auto; height: 80%;with:90%;'></pre>


<script>
    $('#bt_openzwaveLogStopStart').on('click',function(){
        if($(this).attr('data-state') == 1){
            $(this).attr('data-state',0);
            $(this).removeClass('btn-warning').addClass('btn-success');
            $(this).html('<i class="fa fa-play"></i> {{Reprise}}');

        }else{
            $(this).removeClass('btn-success').addClass('btn-warning');
            $(this).html('<i class="fa fa-pause"></i> {{Pause}}');
            $(this).attr('data-state',1);
            jeedom.log.autoupdate({
                log : 'openzwave',
                slaveId : debugMode_slaveId,
                display : $('#pre_openzwavelog'),
                search : $('#in_openzwaveLogSearch'),
                control : $('#bt_openzwaveLogStopStart'),
            });
        }
    });


    if(debugMode_slaveId != ''){
 $.ajax({// fonction permettant de faire de l'ajax
            type: "POST", // methode de transmission des données au fichier php
            url: "plugins/openzwave/core/ajax/openzwave.ajax.php", // url du fichier php
            data: {
                action: "startDeamon",
                type : 'remote',
                id : debugMode_slaveId,
                debug : 1
            },
            dataType: 'json',
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_openzwaveShowDebug'));
            },
            success: function (data) { // si l'appel a bien fonctionné
            if (data.state != 'ok') {
                $('#div_openzwaveShowDebug').showAlert({message: data.result, level: 'danger'});
                return;
            }
            jeedom.log.autoupdate({
                log : 'openzwave',
                slaveId : debugMode_slaveId,
                display : $('#pre_openzwavelog'),
                search : $('#in_openzwaveLogSearch'),
                control : $('#bt_openzwaveLogStopStart'),
            });
        }
    });

}else{
    $.ajax({
        type: 'POST',
        url: "plugins/openzwave/core/ajax/openzwave.ajax.php", // url du fichier php
        data: {
            action: 'startDeamon',
            debug : 1
        },
        dataType: 'json',
        error: function (request, status, error) {
            handleAjaxError(request, status, error, $('#div_openzwaveShowDebug'));
        },
        success: function (data) {
            if (data.state != 'ok') {
                $('#div_openzwaveShowDebug').showAlert({message: data.result, level: 'danger'});
                return;
            }

            jeedom.log.autoupdate({
               log : 'openzwave',
               display : $('#pre_openzwavelog'),
               search : $('#in_openzwaveLogSearch'),
               control : $('#bt_openzwaveLogStopStart'),
           });
        }
    });

}
</script>

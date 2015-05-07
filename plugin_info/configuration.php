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

if (exec('sudo cat /etc/sudoers')<>"") {

    echo '<form class="form-horizontal">
<fieldset><div class="form-group">
        <label class="col-lg-4 control-label">{{Installer/Mettre à jour OpenZwave en local}}</label>
        <div class="col-lg-3">
            <a class="btn btn-danger" id="bt_installDeps"><i class="fa fa-check"></i> {{Lancer}}</a>
        </div>
    </div></fieldset></form>';
    }else{
    echo '<form class="form-horizontal">
<fieldset><div class="form-group">
        <label class="col-lg-4 control-label">{{Installation automatique impossible}}</label>
        <div class="col-lg-8">
            {{Veuillez lancer la commande suivante :}} wget http://127.0.0.1/jeedom/plugins/openzwave/ressources/install.sh -v -O install.sh; ./install.sh
        </div>
    </div></fieldset></form>';
    }

if (config::byKey('jeeNetwork::mode') == 'slave') {
		echo '<div class="alert alert-danger"><b>{{La configuration du plugin se fait uniquement sur le Jeedom principal}}</b></div>';
	} else {
echo '<form class="form-horizontal">
    <fieldset>
    	<u>Configuration locale</u>
        <div class="form-group">
            <label class="col-lg-4 control-label">Port Clé Zwave</label>
            <div class="col-lg-4">
                <select class="configKey form-control" data-l1key="port">
                    <option value="">Aucun</option>';
                    foreach (jeedom::getUsbMapping() as $name => $value) {
                        echo '<option value="' . $name . '">' . $name . ' (' . $value . ')</option>';
                    }
					foreach (ls('/dev/', 'tty*') as $value) {
                        echo '<option value="/dev/' . $value . '">/dev/' . $value . '</option>';
                    }
               echo '</select>
            </div>
        </div>
         <div class="form-group">
            <label class="col-lg-4 control-label">Port du Serveur (laisser vide par défault)</label>
            <div class="col-lg-4">
                <input type="text" class="configKey form-control" data-l1key="port_server">
                   
            </div>
        </div>
        <div class="form-group">
            <label class="col-lg-4 control-label">Mode Debug, cela peut ralentir le systeme</label>
            <div class="col-lg-4">
                <input type="checkbox" class="configKey" data-l1key="enableLogging" />
            </div>
        </div>
        <div class="form-group">
	        <div class="col-lg-8 center">';

	        $statuslocal = openzwave::deamonRunning();
			if ($statuslocal==1) {
	            echo "<a class='btn btn-default btn-sm tooltips' id='bt_stopopenZwaveDemon' title=\"Le démon est démarré. Forcer l'arret du démon openZwave\"><i class='fa fa-stop' style='color : red;'></i> {{Arreter openZwave}}</a>";
	        }else{
	        	echo "<a class='btn btn-default btn-sm tooltips' id='bt_startopenZwaveDemon' title=\"Le démon est arreté.\"><i class='fa fa-play' style='color : green;'></i> {{Démarrer openZwave}}</a>";
	        }

	        echo '</div>
        </div>
    </fieldset>
</form>

<form class="form-horizontal">
    <fieldset>';

 
    foreach (jeeNetwork::byPlugin('openzwave') as $jeeNetwork) {
    					$id_sat=$jeeNetwork->getId();
						$jsonrpc = $jeeNetwork->getJsonRpc();
						if (!$jsonrpc->sendRequest('deamonRunning', array('plugin' => 'openzwave'))) {
							throw new Exception($jsonrpc->getError(), $jsonrpc->getErrorCode());
						}
						$statusremote = $jsonrpc->getResult();
						echo '<div class="config-remote" id='.$jeeNetwork->getId().'>';
						echo '<u>Configuration pour le serveur distant : <b>'.$jeeNetwork->getName().'</b></u>';
						echo '<div class="form-group">
					            <label class="col-lg-4 control-label">Port Clé Zwave</label>
					            <div class="col-lg-4">
					                <select class="configKey form-control portusb" data-l1key="port'.$id_sat.'">
					                    <option value="">Aucun</option>';	
									
									foreach ($jeeNetwork->sendRawRequest('jeedom::getUsbMapping') as $name => $value) {
				                        echo '<option value="' . $name . '">' . $name . ' (' . $value . ')</option>';
				                    }
						echo '</select>
			            </div>
			        </div>
			         <div class="form-group">
			            <label class="col-lg-4 control-label">Port du Serveur (laisser vide par défault)</label>
			            <div class="col-lg-4">
			                <input type="text" class="configKey form-control portserver" data-l1key="port_server'.$id_sat.'">
			                   
			            </div>
			        </div>
			        <div class="form-group">
			            <label class="col-lg-4 control-label">Mode Debug, cela peut ralentir le systeme</label>
			            <div class="col-lg-4">
			                <input type="checkbox" class="configKey debug" data-l1key="enableLogging'.$id_sat.'" />
			            </div>
			        </div>
			        <div class="form-group">
				        <div class="col-lg-8 center">';
						if ($statusremote==1) {
				            echo "<a class='btn btn-default btn-sm tooltips stopdemon' id='bt_stopopenZwaveDemon".$id_sat."' title=\"Le démon est démarré. Forcer l'arret du démon openZwave\"><i class='fa fa-stop' style='color : red;'></i> {{Arreter openZwave}}</a>";
				        }else{
				        	echo "<a class='btn btn-default btn-sm tooltips startdemon' id='bt_startopenZwaveDemon".$id_sat."' title=\"Le démon est arreté.\"><i class='fa fa-play' style='color : green;'></i> {{Démarrer openZwave}}</a>";
				        }
						
						echo '</div>
						</div>';
						if (!$jsonrpc->sendRequest('getConfig', array('plugin' => 'openzwave'))) {
							throw new Exception($jsonrpc->getError(), $jsonrpc->getErrorCode());
						}
						$config = $jsonrpc->getResult();
						//echo 'config port'.json_encode($config);
						echo '</div>';
	}	
    

	echo '    </fieldset>
</form>';
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
		$('.stopdemon').on('click', function() {
			var id=$(this).attr('id').substring(21);
			stopopenZwaveDemon('remote',id);
		});
		
		$('.startdemon').on('click', function() {
			var id=$(this).attr('id').substring(22);
		    startopenZwaveDemon('remote',id);
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
		$('.config-remote').each(function(index, value) { 
		var idsat=$(this).attr('id');
		var port_usb=$(this).find('.portusb').val();
		var port_server=$(this).find('.portserver').val();
		var debug=0;
		if($(this).find('.debug').is(":checked")){
			debug=1;
		}else{
			debug=0;
		}
    $.ajax({// fonction permettant de faire de l'ajax
            type: "POST", // methode de transmission des données au fichier php
            url: "plugins/openzwave/core/ajax/openzwave.ajax.php", // url du fichier php
            data: {
                action: "postSave",
                type: "remote",
                id: idsat,
                port_usb: port_usb,
                port_server: port_server,
                debug: debug
            },
            dataType: 'json',
            error: function (request, status, error) {
                handleAjaxError(request, status, error);
            },
            success: function (data) { // si l'appel a bien fonctionné
            if (data.state != 'ok') {
                $('#div_alert').showAlert({message: data.result, level: 'danger'});
                return;
            }
            $('#ul_plugin .li_plugin[data-plugin_id=openzwave]').click();
        }
    });	

});
		}			
			
				
			</script>

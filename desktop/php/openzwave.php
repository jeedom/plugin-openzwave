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
	throw new Exception('{{401 - Accès non autorisé}}');
}
$plugin = plugin::byId('openzwave');
sendVarToJS('eqType', $plugin->getId());
$eqLogics = eqLogic::byType($plugin->getId());
echo '<div id="div_inclusionAlert"></div>';
$controllerMode = 0;
$networkState = 10;
try {
	$result = openzwave::callOpenzwave('/network?type=info&info=getStatus');
	if (isset($result['result'])) {
		if (isset($result['result']['state'])) {
			$networkState = $result['result']['state'];
		}
		if (isset($result['result']['mode'])) {
			$controllerMode = $result['result']['mode'];
		}
	}
} catch (Exception $e) {
	$controllerMode = null;
}
switch ($networkState) {
	case 0: # STATE_STOPPED = 0
		event::add('jeedom::alert', array(
			'level' => 'danger',
			'page' => 'openzwave',
			'message' => __('Le réseau Z-Wave est arreté sur le serveur', __FILE__),
		));
		break;
	case 1: # STATE_FAILED = 1
		event::add('jeedom::alert', array(
			'level' => 'danger',
			'page' => 'openzwave',
			'message' => __('Le réseau Z-Wave est en erreur sur le serveur', __FILE__),
		));
		break;
	case 3: # STATE_RESET = 3
		event::add('jeedom::alert', array(
			'level' => 'danger',
			'page' => 'openzwave',
			'message' => __('Le réseau Z-Wave est remis à zéro sur le serveur', __FILE__),
		));
		break;
	case 5: # STATE_STARTED = 5
		event::add('jeedom::alert', array(
			'level' => 'warning',
			'page' => 'openzwave',
			'message' => __('Le réseau Z-Wave est en cours de démarrage sur le serveur', __FILE__),
		));
		break;
}
if ($controllerMode === 0) {
	echo '<div id="div_inclusionAlert"></div>';
}
if ($controllerMode === 1) {
	echo '<div class="alert jqAlert alert-warning" id="div_inclusionAlert" style="margin : 0px 5px 15px 15px; padding : 7px 35px 7px 15px;">{{Vous êtes en mode inclusion. Cliquez à nouveau sur le bouton d\'inclusion pour sortir de ce mode}}</div>';
}
if ($controllerMode === 5) {
	echo '<div class="alert jqAlert alert-warning" id="div_inclusionAlert" style="margin : 0px 5px 15px 15px; padding : 7px 35px 7px 15px;">{{Vous êtes en mode exclusion. Cliquez à nouveau sur le bouton d\'exclusion pour sortir de ce mode}}</div>';
}
if ($controllerMode === null) {
	event::add('jeedom::alert', array(
		'level' => 'danger',
		'page' => 'openzwave',
		'message' => __('Impossible de contacter le serveur Z-wave', __FILE__),
	));
}
$tags = array();
if (is_array($eqLogics)) {
	foreach ($eqLogics as $eqLogic) {
		$tags[$eqLogic->getLogicalId()] = $eqLogic->getHumanName(true);
	}
}
sendVarTojs('eqLogic_human_name', $tags);
?>
<div class="row row-overflow">
    <div class="col-lg-2 col-md-3 col-sm-4">
        <div class="bs-sidebar">
            <ul id="ul_eqLogic" class="nav nav-list bs-sidenav">
                <?php
if ($controllerMode == 1) {
	echo ' <a class="btn btn-success changeIncludeState" title="{{Inclure périphérique Z-Wave}}" data-mode="1" data-state="0" style="width : 100%;margin-bottom : 5px;"><i class="fa fa-sign-in fa-rotate-90"></i> {{Arrêter inclusion}}</a>';
} else {
	echo ' <a class="btn btn-default changeIncludeState" title="{{Inclure périphérique Z-Wave}}" data-mode="1" data-state="1" style="width : 100%;margin-bottom : 5px;"><i class="fa fa-sign-in fa-rotate-90"></i> {{Mode inclusion}}</a>';
}
if ($controllerMode == 5) {
	echo ' <a class="btn btn-danger changeIncludeState" title="{{Exclure périphérique Z-Wave}}" data-mode="0" data-state="0" style="width : 100%;margin-bottom : 5px;"><i class="fa fa-sign-out fa-rotate-90"></i> {{Arrêter exclusion}}</a>';
} else {
	echo ' <a class="btn btn-default changeIncludeState" title="{{Exclure périphérique Z-Wave}}" data-mode="0" data-state="1" style="width : 100%;margin-bottom : 5px;"><i class="fa fa-sign-out fa-rotate-90"></i> {{Mode exclusion}}</a>';
}
?>
               <li class="filter" style="margin-bottom: 5px;"><input class="filter form-control input-sm" placeholder="Rechercher" style="width: 100%"/>
               </li>
               <?php
foreach ($eqLogics as $eqLogic) {
	$opacity = ($eqLogic->getIsEnable()) ? '' : jeedom::getConfiguration('eqLogic:style:noactive');
	echo '<li class="cursor li_eqLogic" data-eqLogic_id="' . $eqLogic->getId() . '" data-assistant="' . $eqLogic->getAssistantFilePath() . '" style="' . $opacity . '"><a>' . $eqLogic->getHumanName(true);
	echo '</a></li>';
}
?>
           </ul>
       </div>
   </div>
   <div class="col-lg-10 col-md-9 col-sm-8 eqLogicThumbnailDisplay" style="border-left: solid 1px #EEE; padding-left: 25px;">
    <legend><i class="fa fa-cog"></i> {{Gestion}}</legend>
    <div class="eqLogicThumbnailContainer">
        <?php
if ($controllerMode == 1) {
	echo '<div class="cursor changeIncludeState card" data-mode="1" data-state="0" style="background-color : #8000FF; height : 140px;margin-bottom : 10px;padding : 5px;border-radius: 2px;width : 160px;margin-left : 10px;" >';
	echo '<center>';
	echo '<i class="fa fa-sign-in fa-rotate-90" style="font-size : 6em;color:#94ca02;"></i>';
	echo '</center>';
	echo '<span style="font-size : 1.1em;position:relative; top : 23px;word-break: break-all;white-space: pre-wrap;word-wrap: break-word;color:#94ca02"><center>{{Arrêter inclusion}}</center></span>';
	echo '</div>';
} else {
	echo '<div class="cursor changeIncludeState card" data-mode="1" data-state="1" style="background-color : #ffffff; height : 140px;margin-bottom : 10px;padding : 5px;border-radius: 2px;width : 160px;margin-left : 10px;" >';
	echo '<center>';
	echo '<i class="fa fa-sign-in fa-rotate-90" style="font-size : 6em;color:#94ca02;"></i>';
	echo '</center>';
	echo '<span style="font-size : 1.1em;position:relative; top : 23px;word-break: break-all;white-space: pre-wrap;word-wrap: break-word;color:#94ca02"><center>{{Mode inclusion}}</center></span>';
	echo '</div>';
}
if ($controllerMode == 5) {
	echo '<div class="cursor changeIncludeState card" data-mode="0" data-state="0" style="background-color : #8000FF; height : 140px;margin-bottom : 10px;padding : 5px;border-radius: 2px;width : 160px;margin-left : 10px;" >';
	echo '<center>';
	echo '<i class="fa fa-sign-out fa-rotate-90" style="font-size : 6em;color:#FA5858;"></i>';
	echo '</center>';
	echo '<span style="font-size : 1.1em;position:relative; top : 23px;word-break: break-all;white-space: pre-wrap;word-wrap: break-word;color:#FA5858"><center>{{Arrêter exclusion}}</center></span>';
	echo '</div>';
} else {
	echo '<div class="cursor changeIncludeState card" data-mode="0" data-state="1" style="background-color : #ffffff; height : 140px;margin-bottom : 10px;padding : 5px;border-radius: 2px;width : 160px;margin-left : 10px;" >';
	echo '<center>';
	echo '<i class="fa fa-sign-out fa-rotate-90" style="font-size : 6em;color:#FA5858;"></i>';
	echo '</center>';
	echo '<span style="font-size : 1.1em;position:relative; top : 23px;word-break: break-all;white-space: pre-wrap;word-wrap: break-word;color:#FA5858"><center>{{Mode exclusion}}</center></span>';
	echo '</div>';
}
?>
       <div class="cursor eqLogicAction" data-action="gotoPluginConf" style="background-color : #ffffff; height : 140px;margin-bottom : 10px;padding : 5px;border-radius: 2px;width : 160px;margin-left : 10px;">
        <center>
            <i class="fa fa-wrench" style="font-size : 6em;color:#767676;"></i>
        </center>
        <span style="font-size : 1.1em;position:relative; top : 23px;word-break: break-all;white-space: pre-wrap;word-wrap: break-word;color:#767676"><center>{{Configuration}}</center></span>
    </div>
    <div class="cursor" id="bt_syncEqLogic" style="background-color : #ffffff; height : 140px;margin-bottom : 10px;padding : 5px;border-radius: 2px;width : 160px;margin-left : 10px;">
        <center>
            <i class="fa fa-refresh" style="font-size : 6em;color:#767676;"></i>
        </center>
        <span style="font-size : 1.1em;position:relative; top : 23px;word-break: break-all;white-space: pre-wrap;word-wrap: break-word;color:#767676"><center>{{Synchroniser}}</center></span>
    </div>
    <div class="cursor" id="bt_zwaveNetwork" style="background-color : #ffffff; height : 140px;margin-bottom : 10px;padding : 5px;border-radius: 2px;width : 160px;margin-left : 10px;">
        <center>
            <i class="fa fa-sitemap" style="font-size : 6em;color:#767676;"></i>
        </center>
        <span style="font-size : 1.1em;position:relative; top : 23px;word-break: break-all;white-space: pre-wrap;word-wrap: break-word;color:#767676"><center>{{Réseau Zwave}}</center></span>
    </div>
    <div class="cursor" id="bt_zwaveHealth" style="background-color : #ffffff; height : 140px;margin-bottom : 10px;padding : 5px;border-radius: 2px;width : 160px;margin-left : 10px;">
        <center>
            <i class="fa fa-medkit" style="font-size : 6em;color:#767676;"></i>
        </center>
        <span style="font-size : 1.1em;position:relative; top : 23px;word-break: break-all;white-space: pre-wrap;word-wrap: break-word;color:#767676"><center>{{Santé}}</center></span>
    </div>
</div>
<legend><i class="fa fa-table"></i> {{Mes équipements Z-Wave}}</legend>
<input class="form-control" placeholder="{{Rechercher}}" style="margin-bottom:4px;" id="in_searchEqlogic" />
<div class="eqLogicThumbnailContainer">
    <?php
foreach ($eqLogics as $eqLogic) {
	$opacity = ($eqLogic->getIsEnable()) ? '' : jeedom::getConfiguration('eqLogic:style:noactive');
	echo '<div class="eqLogicDisplayCard cursor" data-logical-id="' . $eqLogic->getLogicalId() . '" data-eqLogic_id="' . $eqLogic->getId() . '" style="background-color : #ffffff; height : 200px;margin-bottom : 10px;padding : 5px;border-radius: 2px;width : 160px;margin-left : 10px;' . $opacity . '" >';
	echo "<center>";
	if ($eqLogic->getImgFilePath() !== false) {
		echo '<img class="lazy" src="plugins/openzwave/core/config/devices/' . $eqLogic->getImgFilePath() . '" height="105" width="95" />';
	} else {
		echo '<img src="' . $plugin->getPathImgIcon() . '" height="105" width="95" />';
	}
	echo "</center>";
	echo '<span class="name" style="font-size : 1.1em;position:relative; top : 15px;word-break: break-all;white-space: pre-wrap;word-wrap: break-word;"><center>' . $eqLogic->getHumanName(true, true) . '</center></span>';
	echo '</div>';
}
?>
</div>
</div>
<div class="col-lg-10 col-md-9 col-sm-8 eqLogic" style="border-left: solid 1px #EEE; padding-left: 25px;display: none;">
    <a class="btn btn-success eqLogicAction pull-right" data-action="save"><i class="fa fa-check-circle"></i> {{Sauvegarder}}</a>
    <a class="btn btn-danger eqLogicAction pull-right" data-action="remove"><i class="fa fa-minus-circle"></i> {{Supprimer}}</a>
    <a class="btn btn-default eqLogicAction pull-right" data-action="configure"><i class="fa fa-cogs"></i> {{Configuration avancée}}</a>
    <ul class="nav nav-tabs" role="tablist">
       <li role="presentation"><a class="eqLogicAction cursor" aria-controls="home" role="tab" data-action="returnToThumbnailDisplay"><i class="fa fa-arrow-circle-left"></i></a></li>
       <li role="presentation" class="active"><a href="#eqlogictab" aria-controls="home" role="tab" data-toggle="tab"><i class="fa fa-tachometer"></i> {{Equipement}}</a></li>
       <li role="presentation"><a href="#commandtab" aria-controls="profile" role="tab" data-toggle="tab"><i class="fa fa-list-alt"></i> {{Commandes}}</a></li>
   </ul>
   <div class="tab-content" style="height:calc(100% - 50px);overflow:auto;overflow-x: hidden;">
    <div role="tabpanel" class="tab-pane active" id="eqlogictab">
      <br/>
      <div class="row">
        <div class="col-sm-7">
            <form class="form-horizontal">
                <fieldset>
                    <div class="form-group">
                        <label class="col-sm-4 control-label">{{Nom de l'équipement}}</label>
                        <div class="col-sm-6">
                            <input type="text" class="eqLogicAttr form-control" data-l1key="id" style="display : none;"/>
                            <input type="text" class="eqLogicAttr form-control" data-l1key="name" placeholder="{{Nom de l'équipement}}"/>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="col-sm-4 control-label">{{Objet parent}}</label>
                        <div class="col-sm-6">
                            <select class="eqLogicAttr form-control" data-l1key="object_id">
                                <option value="">{{Aucun}}</option>
                                <?php
foreach (object::all() as $object) {
	echo '<option value="' . $object->getId() . '">' . $object->getName() . '</option>';
}
?>
                           </select>
                       </div>
                   </div>
                   <div class="form-group">
                    <label class="col-sm-4 control-label">{{Catégorie}}</label>
                    <div class="col-sm-8">
                        <?php
foreach (jeedom::getConfiguration('eqLogic:category') as $key => $value) {
	echo '<label class="checkbox-inline">';
	echo '<input type="checkbox" class="eqLogicAttr" data-l1key="category" data-l2key="' . $key . '" />' . $value['name'];
	echo '</label>';
}
?>
                   </div>
               </div>
               <div class="form-group">
                <label class="col-sm-4 control-label"></label>
                <div class="col-sm-8">
                    <label class="checkbox-inline"><input type="checkbox" class="eqLogicAttr" data-l1key="isEnable" checked/>{{Activer}}</label>
                    <label class="checkbox-inline"><input type="checkbox" class="eqLogicAttr" data-l1key="isVisible" checked/>{{Visible}}</label>
                </div>
            </div>
            <div class="form-group">
                <label class="col-sm-4 control-label">{{Node ID}}</label>
                <div class="col-sm-2">
                    <input type="text" class="eqLogicAttr form-control" data-l1key="logicalId"/>
                </div>
            </div>
        </fieldset>
    </form>
</div>
<div class="col-sm-5">
    <form class="form-horizontal">
        <fieldset>
            <div class="form-group">
                <label class="col-sm-2 control-label">{{Informations}}</label>
                <div class="col-sm-8">
                    <a id="bt_autoDetectModule" class="btn btn-danger"><i class="fa fa-search"></i> {{Recharger configuration}}</a>
                    <a id="bt_displayZwaveData" class="btn btn-default"><i class="fa fa-tree"></i> {{Arbre Z-Wave}}</a>
                    <span class="label label-warning isPending" style="font-size:0.6em;cursor:default;position:relative;top:-4px;left:20px;" title="{{Il faut réveiller le module s'il est sur batterie ou vérifier le paramétrage}}"></span>
                </div>
            </div>
            <div class="form-group">
                <label class="col-sm-2 control-label">{{Type}}</label>
                <div class="col-sm-8">
                    <select class="eqLogicAttr form-control" data-l1key="configuration" data-l2key="fileconf"></select>
                </div>
            </div>
            <div class="form-group">
                <label class="col-sm-2 control-label">{{Modèle}}</label>
                <div class="col-sm-10">
                  <span class="label label-default" style='font-size : 1em;'>
                    <span class="eqLogicAttr" data-l1key="configuration" data-l2key="product_name"></span>
                    <span class="eqLogicAttr" data-l1key="configuration" data-l2key="conf_version" title="{{Version de la configuration}}"></span>
                </span>
            <img src="core/img/no_image.gif" data-original=".jpg" id="img_device" class="img-responsive" style="max-height : 120px;margin-top: 10px"/>
            </div>
			
               
        </div>
        <div class="form-group">
            <label class="col-sm-2 control-label">{{Paramètres}}</label>
            <div class="col-sm-10">
                <a class="btn btn-primary" id="bt_configureDevice" title='{{Configurer}}'><i class="fa fa-wrench"></i> {{Configuration}}</a>
                <a class="btn btn-info" id="bt_deviceAssistant" title='{{Assistant de configuration spécifique}}' style="display:none;"><i class="fa fa-magic"></i> {{Assistant}}</a>
                <a class="btn btn-default" id="bt_deviceDocumentation" title='{{Documentation du module}}' target="_blank" style="display:none;"><i class="fa fa-book"></i>{{Documentation}} </a>
                <a class="btn btn-warning" id="bt_deviceRecommended" title="{{Appliquer le jeu de configuration recommandée par l'équipe Jeedom}}" style="display:none;"><i class="fa fa-thumbs-up"></i> {{Configuration recommandée}}</a>
            </div>
        </div>
        
    </fieldset>
</form>
</div>
</div>

</div>
<div role="tabpanel" class="tab-pane" id="commandtab">
    <a class="btn btn-success btn-sm cmdAction pull-right" data-action="add" style="margin-top:5px;"> <i class="fa fa-plus-circle"></i> {{Commandes}}</a>
    <br/><br/>
    <table id="table_cmd" class="table table-bordered table-condensed">
        <thead>
            <tr>
                <th style="width: 300px;">{{Nom}}</th>
                <th style="width: 130px;">{{Type}}</th>
                <th>{{Instance}}</th>
                <th>{{Classe}}</th>
                <th>{{Index}}</th>
                <th>{{Commande}}</th>
                <th style="width: 200px;">{{Paramètres}}</th>
                <th style="width: 100px;">{{Options}}</th>
                <th></th>
            </tr>
        </thead>
        <tbody>
        </tbody>
    </table>
</div>
</div>
</div>
</div>
<?php include_file('core', 'openzwave', 'class.js', 'openzwave');?>
<?php include_file('desktop', 'openzwave', 'js', 'openzwave');?>
<?php include_file('core', 'plugin.template', 'js');?>

<?php
if (!isConnect('admin')) {
	throw new Exception('{{401 - Accès non autorisé}}');
}
include_file('3rdparty', 'jquery.fileupload/jquery.ui.widget', 'js');
include_file('3rdparty', 'jquery.fileupload/jquery.iframe-transport', 'js');
include_file('3rdparty', 'jquery.fileupload/jquery.fileupload', 'js');
sendVarToJS('eqType', 'openzwave');
sendVarToJS('marketAddr', config::byKey('market::address'));
sendVarToJS('listServerZwave', openzwave::listServerZwave());
echo '<div id="div_inclusionAlert"></div>';
$controlerState = 0;
$state = 10;
foreach (openzwave::listServerZwave() as $id => $server) {
	if (isset($server['name'])) {
		try {
			$controlerState = openzwave::callOpenzwave('/ZWaveAPI/Run/network.GetControllerStatus()', $id);
			if (isset($controlerState['result']['data'])) {
				$state = $controlerState['result']['data']['networkstate']['value'];
				$controlerState = $controlerState['result']['data']['mode']['value'];
			}
		} catch (Exception $e) {
			$controlerState = null;
		}
		if ($state < 7) {
			echo '<div class="alert jqAlert alert-warning" id="div_inclusionAlert' . $id . '" style="margin : 0px 5px 15px 15px; padding : 7px 35px 7px 15px;">{{Openzwave est en cours de démarrage sur ' . $server['name'] . '.}}</div>';
		}
		if ($controlerState === 0) {
			echo '<div id="div_inclusionAlert' . $id . '"></div>';
		}
		if ($controlerState === 1) {
			echo '<div class="alert jqAlert alert-warning" id="div_inclusionAlert' . $id . '" style="margin : 0px 5px 15px 15px; padding : 7px 35px 7px 15px;">{{Vous êtes en mode inclusion sur ' . $server['name'] . '. Cliquez à nouveau sur le bouton d\'inclusion pour sortir de ce mode}}</div>';
		}
		if ($controlerState === 5) {
			echo '<div class="alert jqAlert alert-warning" id="div_inclusionAlert' . $id . '" style="margin : 0px 5px 15px 15px; padding : 7px 35px 7px 15px;">{{Vous êtes en mode exclusion sur ' . $server['name'] . '. Cliquez à nouveau sur le bouton d\'exclusion pour sortir de ce mode}}</div>';
		}
		if ($controlerState === null) {
			echo '<div class="alert jqAlert alert-danger" style="margin : 0px 5px 15px 15px; padding : 7px 35px 7px 15px;">{{Impossible de contacter le serveur Z-wave ' . $server['name'] . '.}}</div>';
		}
	}
}

$eqLogics = eqLogic::byType('openzwave');
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
if ($controlerState == 1) {
	echo ' <a class="btn btn-success tooltips changeIncludeState" title="{{Inclure périphérique Z-Wave}}" data-mode="1" data-state="0" style="width : 100%;margin-bottom : 5px;"><i class="fa fa-sign-in fa-rotate-90"></i> {{Arrêter inclusion}}</a>';
} else {
	echo ' <a class="btn btn-default tooltips changeIncludeState" title="{{Inclure périphérique Z-Wave}}" data-mode="1" data-state="1" style="width : 100%;margin-bottom : 5px;"><i class="fa fa-sign-in fa-rotate-90"></i> {{Mode inclusion}}</a>';
}
if ($controlerState == 5) {
	echo ' <a class="btn btn-danger tooltips changeIncludeState" title="{{Exclure périphérique Z-Wave}}" data-mode="0" data-state="0" style="width : 100%;margin-bottom : 5px;"><i class="fa fa-sign-out fa-rotate-90"></i> {{Arrêter exclusion}}</a>';
} else {
	echo ' <a class="btn btn-default tooltips changeIncludeState" title="{{Exclure périphérique Z-Wave}}" data-mode="0" data-state="1" style="width : 100%;margin-bottom : 5px;"><i class="fa fa-sign-out fa-rotate-90"></i> {{Mode exclusion}}</a>';
}
?>
       <li class="filter" style="margin-bottom: 5px;"><input class="filter form-control input-sm" placeholder="Rechercher" style="width: 100%"/></li>
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
   <legend>{{Gestion}}</legend>
   <div class="eqLogicThumbnailContainer">
     <?php
if ($controlerState == 1) {
	echo '<div class="cursor changeIncludeState card" data-mode="1" data-state="0" style="background-color : #8000FF; height : 140px;margin-bottom : 10px;padding : 5px;border-radius: 2px;width : 160px;margin-left : 10px;" >';
	echo '<center>';
	echo '<i class="fa fa-sign-in fa-rotate-90" style="font-size : 5em;color:#94ca02;"></i>';
	echo '</center>';
	echo '<span style="font-size : 1.1em;position:relative; top : 23px;word-break: break-all;white-space: pre-wrap;word-wrap: break-word;color:#94ca02"><center>{{Arrêter inclusion}}</center></span>';
	echo '</div>';
} else {
	echo '<div class="cursor changeIncludeState card" data-mode="1" data-state="1" style="background-color : #ffffff; height : 140px;margin-bottom : 10px;padding : 5px;border-radius: 2px;width : 160px;margin-left : 10px;" >';
	echo '<center>';
	echo '<i class="fa fa-sign-in fa-rotate-90" style="font-size : 5em;color:#94ca02;"></i>';
	echo '</center>';
	echo '<span style="font-size : 1.1em;position:relative; top : 23px;word-break: break-all;white-space: pre-wrap;word-wrap: break-word;color:#94ca02"><center>{{Mode inclusion}}</center></span>';
	echo '</div>';
}
if ($controlerState == 5) {
	echo '<div class="cursor changeIncludeState card" data-mode="0" data-state="0" style="background-color : #8000FF; height : 140px;margin-bottom : 10px;padding : 5px;border-radius: 2px;width : 160px;margin-left : 10px;" >';
	echo '<center>';
	echo '<i class="fa fa-sign-out fa-rotate-90" style="font-size : 5em;color:#FA5858;"></i>';
	echo '</center>';
	echo '<span style="font-size : 1.1em;position:relative; top : 23px;word-break: break-all;white-space: pre-wrap;word-wrap: break-word;color:#FA5858"><center>{{Arrêter exclusion}}</center></span>';
	echo '</div>';
} else {
	echo '<div class="cursor changeIncludeState card" data-mode="0" data-state="1" style="background-color : #ffffff; height : 140px;margin-bottom : 10px;padding : 5px;border-radius: 2px;width : 160px;margin-left : 10px;" >';
	echo '<center>';
	echo '<i class="fa fa-sign-out fa-rotate-90" style="font-size : 5em;color:#FA5858;"></i>';
	echo '</center>';
	echo '<span style="font-size : 1.1em;position:relative; top : 23px;word-break: break-all;white-space: pre-wrap;word-wrap: break-word;color:#FA5858"><center>{{Mode exclusion}}</center></span>';
	echo '</div>';
}
?>
     <div class="cursor expertModeVisible" id="bt_syncEqLogic" style="background-color : #ffffff; height : 140px;margin-bottom : 10px;padding : 5px;border-radius: 2px;width : 160px;margin-left : 10px;" >
      <center>
        <i class="fa fa-refresh" style="font-size : 5em;color:#767676;"></i>
      </center>
      <span style="font-size : 1.1em;position:relative; top : 23px;word-break: break-all;white-space: pre-wrap;word-wrap: break-word;color:#767676"><center>{{Synchroniser}}</center></span>
    </div>

    <div class="cursor expertModeVisible" id="bt_zwaveNetwork" style="background-color : #ffffff; height : 140px;margin-bottom : 10px;padding : 5px;border-radius: 2px;width : 160px;margin-left : 10px;" >
      <center>
        <i class="fa fa-sitemap" style="font-size : 5em;color:#767676;"></i>
      </center>
      <span style="font-size : 1.1em;position:relative; top : 23px;word-break: break-all;white-space: pre-wrap;word-wrap: break-word;color:#767676"><center>{{Reseaux Zwave}}</center></span>
    </div>

    <div class="cursor expertModeVisible" id="bt_zwaveHealth" style="background-color : #ffffff; height : 140px;margin-bottom : 10px;padding : 5px;border-radius: 2px;width : 160px;margin-left : 10px;" >
      <center>
        <i class="fa fa-medkit" style="font-size : 5em;color:#767676;"></i>
      </center>
      <span style="font-size : 1.1em;position:relative; top : 23px;word-break: break-all;white-space: pre-wrap;word-wrap: break-word;color:#767676"><center>{{Santé}}</center></span>
    </div>
  </div>
  <legend>{{Mes équipements Z-Wave}}</legend>
  <div class="eqLogicThumbnailContainer">

    <?php
foreach ($eqLogics as $eqLogic) {
	$opacity = ($eqLogic->getIsEnable()) ? '' : jeedom::getConfiguration('eqLogic:style:noactive');
	echo '<div class="eqLogicDisplayCard cursor" data-logical-id="' . $eqLogic->getLogicalId() . '" data-server-id="' . $eqLogic->getConfiguration('serverID', 0) . '" data-eqLogic_id="' . $eqLogic->getId() . '" style="background-color : #ffffff; height : 200px;margin-bottom : 10px;padding : 5px;border-radius: 2px;width : 160px;margin-left : 10px;' . $opacity . '" >';
	echo "<center>";
	if ($eqLogic->getImgFilePath() !== false) {
		echo '<img class="lazy" src="plugins/openzwave/core/config/devices/' . $eqLogic->getImgFilePath() . '" height="105" width="95" />';
	} else {
		echo '<img class="lazy" src="plugins/openzwave/doc/images/openzwave_icon.png" height="105" width="95" />';
	}
	echo "</center>";
	echo '<span style="font-size : 1.1em;position:relative; top : 15px;word-break: break-all;white-space: pre-wrap;word-wrap: break-word;"><center>' . $eqLogic->getHumanName(true, true) . '</center></span>';
	echo '</div>';
}
?>
</div>
</div>

<div class="col-lg-10 col-md-9 col-sm-8 eqLogic" style="border-left: solid 1px #EEE; padding-left: 25px;display: none;">
  <div class="row">
    <div class="col-sm-7">
      <form class="form-horizontal">
        <fieldset>
          <legend><i class="fa fa-arrow-circle-left eqLogicAction cursor" data-action="returnToThumbnailDisplay"></i> {{Général}} <i class='fa fa-cogs eqLogicAction pull-right cursor expertModeVisible' data-action='configure'></i></legend>
          <div class="form-group">
            <label class="col-sm-4 control-label">{{Nom de l'équipement}}</label>
            <div class="col-sm-6">
              <input type="text" class="eqLogicAttr form-control" data-l1key="id" style="display : none;" />
              <input type="text" class="eqLogicAttr form-control" data-l1key="name" placeholder="{{Nom de l'équipement}}"/>
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-4 control-label" >{{Objet parent}}</label>
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
          <input type="checkbox" class="eqLogicAttr bootstrapSwitch" data-label-text="{{Activer}}" data-l1key="isEnable" checked/>
          <input type="checkbox" class="eqLogicAttr bootstrapSwitch" data-label-text="{{Visible}}" data-l1key="isVisible" checked/>
        </div>
      </div>
      <div class="form-group expertModeVisible">
        <label class="col-sm-4 control-label">{{Node ID}}</label>
        <div class="col-sm-2">
          <input type="text" class="eqLogicAttr form-control" data-l1key="logicalId" />
        </div>
      </div>
      <div class="form-group expertModeVisible">
        <label class="col-sm-4 control-label">{{Serveur}}</label>
        <div class="col-sm-4">
         <select class="form-control eqLogicAttr" data-l1key="configuration" data-l2key="serverID">
          <?php
foreach (openzwave::listServerZwave() as $id => $server) {
	if (isset($server['name'])) {
		echo '<option value="' . $id . '">' . $server['name'] . '</option>';
	}
}
?>
      </select>
    </div>
  </div>
  <div class="form-group expertModeVisible">
    <label class="col-sm-4 control-label">{{Délai maximum autorisé entre 2 messages (min)}}</label>
    <div class="col-sm-4">
      <input class="eqLogicAttr form-control" data-l1key="timeout" />
    </div>
  </div>
</fieldset>
</form>
</div>
<div class="col-sm-5">
  <form class="form-horizontal">
    <fieldset>
      <legend>{{Informations}}
       <i id="bt_autoDetectModule" class="fa fa-search expertModeVisible pull-right tooltips cursor" title="{{Detecter automatiquement le modele du module}}"></i>
       <i id="bt_displayZwaveData" title="{{Voir l'arbre Z-Wave}}" class="fa fa-tree expertModeVisible pull-right tooltips cursor"></i>
     </legend>

     <div class="form-group">
      <label class="col-sm-2 control-label">{{Type}}</label>
      <div class="col-sm-8">
       <select class="eqLogicAttr form-control" data-l1key="configuration" data-l2key="fileconf" ></select>
     </div>
   </div>

   <div class="form-group">
    <label class="col-sm-2 control-label">{{Marque}}</label>
    <div class="col-sm-10">
      <span class="tooltips label label-default" style='font-size : 1em;'>
        <span class="eqLogicAttr" data-l1key="configuration" data-l2key="product_name"></span>
        <span class="eqLogicAttr tooltips" data-l1key="configuration" data-l2key="conf_version" title="{{Version de la configuration}}"></span>
      </span>
    </div>
  </div>

  <div class="form-group">
    <label class="col-sm-2 control-label">{{Paramètres}}</label>
    <div class="col-sm-10">
      <a class="btn btn-primary" id="bt_configureDevice" title='{{Configurer}}'><i class="fa fa-wrench"></i> {{Configuration}}</a>
      <a class="btn btn-info" id="bt_deviceAssistant" title='{{Assistant de configuration spécifique}}' style="display:none;"><i class="fa fa-question-circle"></i> {{Assistant}}</a>
      <a class="btn btn-default" id="bt_deviceDocumentation" title='{{Documentation du module}}' target="_blank" style="display:none;"><i class="fa fa-book"></i> {{Documentation}}</a>
    </div>
  </div>
  <center>
    <img src="core/img/no_image.gif" data-original=".jpg" id="img_device" class="img-responsive" style="max-height : 250px;"/>
  </center>
  <br/>
  <div class="form-group">
    <label class="col-sm-2 control-label">{{Commentaire}}</label>
    <div class="col-sm-10">
      <textarea class="eqLogicAttr form-control" data-l1key="configuration" data-l2key="commentaire" ></textarea>
    </div>
  </div>
</fieldset>
</form>
</div>
</div>

<legend>Commandes</legend>
<a class="btn btn-success btn-sm cmdAction expertModeVisible" data-action="add"><i class="fa fa-plus-circle"></i> {{Commandes}}</a><br/><br/>
<table id="table_cmd" class="table table-bordered table-condensed">
  <thead>
    <tr>
      <th style="width: 300px;">{{Nom}}</th>
      <th style="width: 130px;" class="expertModeVisible">{{Type}}</th>
      <th class="expertModeVisible">{{Instance ID}}</th>
      <th class="expertModeVisible">{{Classe}}</th>
      <th class="expertModeVisible">{{Commande}}</th>
      <th style="width: 100px;">{{Paramètres}}</th>
      <th style="width: 100px;">{{Options}}</th>
      <th></th>
    </tr>
  </thead>
  <tbody>

  </tbody>
</table>

<form class="form-horizontal">
  <fieldset>
    <div class="form-actions">
      <a class="btn btn-danger eqLogicAction" data-action="remove"><i class="fa fa-minus-circle"></i> {{Supprimer}}</a>
      <a class="btn btn-success eqLogicAction" data-action="save"><i class="fa fa-check-circle"></i> {{Sauvegarder}}</a>
    </div>
  </fieldset>
</form>

</div>
</div>
<?php include_file('desktop', 'openzwave', 'js', 'openzwave');?>
<?php include_file('core', 'plugin.template', 'js');?>

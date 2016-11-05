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
sendVarToJs('node_id', init('id'));
?>
<style media="screen" type="text/css">
    .noscrolling {
        width: 99%;
        overflow: hidden;
    }
    .node-item {
        border: 1px solid;
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
    .pendingcolor {
        color: #FFD700
    }
    .rejectcolor {
        color: #e74c3c
    }
    .table-striped > tbody > tr.yellowrow > td {
        background-color: #FFD700;
    }
    .table-striped > tbody > tr.redrow > td {
        background-color: #e74c3c;
    }
</style>
<div id='div_nodeConfigureOpenzwaveAlert' style="display: none;"></div>
<div class="modal fade modal-dialog-center" id="paramsModal" tabindex="-1" role="dialog" data-backdrop="false">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <a class="close" data-dismiss="modal" aria-label="Close"><span>&times;</span></a>
                <h4 class="modal-title" id="exampleModalLabel">Nouveau message</h4>
            </div>
            <div class="modal-body">
                <div id="modalparamname"></div>
            </div>
            <div class="modal-footer">
                <a class="btn btn-default" data-dismiss="modal">{{Annuler}}</a>
                <a class="btn btn-primary" id="saveParam">{{Appliquer}}</a>
            </div>
        </div>
    </div>
</div>
<div class="modal fade modal-dialog-center" id="valuesModal" tabindex="-1" role="dialog" data-backdrop="false">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <a class="close" data-dismiss="modal" aria-label="Close"><span>&times;</span></a>
                <h4 class="modal-title" id="valueModalLabel">Nouveau message</h4>
            </div>
            <div class="modal-body">
                <div id="modalvaluename"></div>
            </div>
            <div class="modal-footer">
                <a class="btn btn-default" data-dismiss="modal">{{Annuler}}</a>
                <a class="btn btn-primary" id="applyValue">{{Appliquer}}</a>
            </div>
        </div>
    </div>
</div>
<div class="modal fade modal-dialog-center" id="pollingModal" tabindex="-1" role="dialog" data-backdrop="false">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <a class="close" data-dismiss="modal" aria-label="Close"><span>&times;</span></a>
                <h4 class="modal-title" id="pollingModalLabel">Nouveau message</h4>
            </div>
            <div class="modal-body">
                <div id="modalpolling"></div>
            </div>
            <div class="modal-footer">
                <a class="btn btn-default" data-dismiss="modal">{{Annuler}}</a>
                <a class="btn btn-primary" id="savePolling">{{Appliquer}}</a>
            </div>
        </div>
    </div>
</div>
<div class="modal fade modal-dialog-center" id="copyParamsModal" tabindex="-1" role="dialog" data-backdrop="false">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <a class="close" data-dismiss="modal" aria-label="Close"><span>&times;</span></a>
                <h4 class="modal-title" id="copyParamsModalLabel">Nouveau message</h4>
            </div>
            <div class="modal-body">
                <div id="modalcopyParams"></div>
            </div>
            <div class="modal-footer">
                <a class="btn btn-default" data-dismiss="modal">{{Annuler}}</a>
                <a class="btn btn-primary" id="saveCopyParams">{{Appliquer les paramètres}}</a>
            </div>
        </div>
    </div>
</div>
<div class="modal fade modal-dialog-center" id="copyToParamsModal" tabindex="-1" role="dialog" data-backdrop="false">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <a class="close" data-dismiss="modal" aria-label="Close"><span>&times;</span></a>
                <h4 class="modal-title" id="copyToParamsModalLabel">Nouveau message</h4>
            </div>
            <div class="modal-body">
                <div id="modalcopyToParams"></div>
            </div>
            <div class="modal-footer">
                <a class="btn btn-default" data-dismiss="modal">{{Annuler}}</a>
                <a class="btn btn-primary" id="saveCopyToParams">{{Appliquer les paramètres}}</a>
            </div>
        </div>
    </div>
</div>
<div class="modal fade modal-dialog-center" id="groupsModal" tabindex="-1" role="dialog" data-backdrop="false">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <a class="close" data-dismiss="modal" aria-label="Close"><span>&times;</span></a>
                <h4 class="modal-title" id="groupsModalLabel">Nouveau message</h4>
            </div>
            <div class="modal-body">
                <div id="modalgroups"></div>
            </div>
            <div class="modal-footer">
                <a class="btn btn-default" data-dismiss="modal">{{Annuler}}</a>
                <a class="btn btn-primary" id="saveGroups">{{Appliquer}}</a>
            </div>
        </div>
    </div>
</div>
<div class='node' nid='' id="div_nodeConfigure">
    <div id="template-node">
        <div class="container-fluid">
            <div id="content">
                <ul id="tabs" class="nav nav-tabs" data-tabs="tabs">
                    <li id="tab-summary" class="active">
                        <a href="#summary" data-toggle="tab"><i class="fa fa-tachometer"></i> {{Résumé}}</a>
                    </li>
                    <li id="tab-values">
                        <a href="#values" data-toggle="tab"><i class="fa fa-tag"></i> {{Valeurs}}</a>
                    </li>
                    <li id="tab-parameters">
                        <a href="#parameters" data-toggle="tab"><i class="fa fa-wrench"></i> {{Paramètres}}</a>
                    </li>
                    <li id="tab-groups">
                        <a href="#groups" data-toggle="tab"><i class="fa fa-users"></i> {{Associations}}</a>
                    </li>
                    <li id="tab-systems">
                        <a href="#systems" data-toggle="tab"><i class="fa fa-cogs"></i> {{Systèmes}}</a>
                    </li>
                    <li id="tab-actions">
                        <a href="#actions" data-toggle="tab"><i class="fa fa-sliders"></i> {{Actions}}</a>
                    </li>
                    <li id="tab-stats">
                        <a href="#statistics" data-toggle="tab"><i class="fa fa-bar-chart"></i> {{Statistiques}}</a>
                    </li>
                    <li id="li_state" class="pull-right alert" style="background-color : #dff0d8;color : #3c763d;height:35px;border-color:#d6e9c6;display:none;">
                        <span style="position:relative; top : -7px;">{{Envoi OK}}</span>
                    </li>
                </ul>
                <div id="my-tab-content" class="tab-content">
                    <div class="tab-pane active" id="summary">
                        <br>
                        <div id="panel-danger" class="panel panel-danger template">
                            <div class="panel-heading">
                                <h4 class="panel-title"><i class="fa fa-exclamation-circle"></i> {{Attention}}</h4>
                            </div>
                            <div class="panel-body">
                                <p><span class="zwaveNodeAttr" data-l1key="warning"></span></p>
                            </div>
                        </div>
                        <div class="panel panel-primary template">
                            <div class="panel-heading">
                                <h4 class="panel-title"><i class="fa fa-info-circle"></i> {{Informations Noeud}}</h4>
                            </div>
                            <div class="panel-body">
                                <p>{{Objet parent :}} <b><span class="zwaveNodeAttr label label-default" data-l1key="location" data-l2key="value" style="font-size : 1em;"></span></b></p>
                                <p>{{Nom de l'équipement :}}
                                <b><span class="zwaveNodeAttr label label-default" data-l1key="name" data-l2key="value" style="font-size : 1em;"></span></b>
                                </p>
                                <p>{{Modèle :}}
                                    <b><span class="zwaveNodeAttr label label-default" data-l1key="product_name" data-l2key="value" style="font-size : 1em;"></span></b>
                                    <b><span class="node-zwaveplus label label-info" data-l1key="location" data-l2key="value" style="font-size:1em;"></span></b>
                                    <b><span class="node-isSecured label label-success" data-l1key="location" data-l2key="value" style="font-size:1em;"></span></b>
                                </p>
                                <p>{{Fabricant :}}
                                    <b><span class="zwaveNodeAttr label label-default" data-l1key="vendorString" data-l2key="value" style="font-size : 1em;"></span></b>
                                </p>
                                <p>
                                    <span class="zwaveNodeAttr" data-l1key="zwave_id"></span></p>
                                    <p>{{Etat des demandes :}}
                                        <b><span class="zwaveNodeAttr label label-default" data-l1key="queryStage" style="font-size : 1em;"></span></b>
                                    </p>
                                    <p>{{Etat :}} <b><span class="node-sleep label label-default" data-l1key="location" data-l2key="value" style="font-size : 1em;"></span></b>
                                        <span class="node-battery-span">{{Batterie : }} <b><span class="zwaveNodeAttr label label-default" data-l1key="battery_level" data-l2key="value" style="font-size : 1em;"></span>%</b></span>
                                    </p>
                                    <p>{{Dernier message :}}
                                        <b><span class="zwaveNodeAttr label label-default" data-l1key="lastReceived" data-l2key="updateTime" style="font-size : 1em;"></span></b>
                                        <span class="node-next-wakeup-span">{{Prochain réveil : }}
                                            <b><span class="zwaveNodeAttr label label-default" data-l1key="last_notification" data-l2key="next_wakeup" style="font-size : 1em;"></span></b>
                                        </span>
                                    </p>
                                    <p>{{Voisins : }} <span class="node-neighbours label label-default" data-l1key="location" data-l2key="value" style="font-size : 1em;"></span></p>
                                </div>
                            </div>
                            <div class="panel panel-primary template">
                                <div class="panel-heading">
                                    <h4 class="panel-title"><i class="fa fa-info-circle"></i> {{Classe du module}}</h4>
                                </div>
                                <div class="panel-body">
                                    {{Basique :}} <b><span class="zwaveNodeAttr label label-default" data-l1key="basicDeviceClassDescription"></span></b><br/>
                                    {{Générique :}} <b><span class="zwaveNodeAttr label label-default" data-l1key="genericDeviceClassDescription"></span></b><br/>
                                    {{Spécifique :}} <b><span class="zwaveNodeAttr label label-default" data-l1key="type" data-l2key="value"></span></b></p>
                                </div>
                            </div>
                            <div class="panel panel-primary template">
                                <div class="panel-heading">
                                    <h4 class="panel-title"><i class="fa fa-info-circle"></i> {{Informations Protocole}}
                                    </h4>
                                </div>
                                <div class="panel-body">
                                    <p>{{Vitesse maximale de communication du module :}}<b><span class="zwaveNodeAttr" data-l1key="maxBaudRate" data-l2key="value"></span></b> {{bit/sec}}</p>
                                    <b><span class="node-routing" data-l1key="location" data-l2key="value"></span></b>
                                    <b><span class="node-isSecurity" data-l1key="location" data-l2key="value"></span></b>
                                    <b><span class="node-listening" data-l1key="location" data-l2key="value"></span></b>
                                    <b><span class="node-isFrequentListening" data-l1key="location" data-l2key="value"></span></b>
                                    <b><span class="node-isBeaming" data-l1key="location" data-l2key="value"></span></b>
                                    <br/>
                                    <p><b><span class="node-security"></span></b></p>
                                </div>
                            </div>
                        </div>
                        <div class="tab-pane" id="values">
                            <table class="table table-striped">
                                <tr>
                                    <th>{{Nom}}</th>
                                    <th>{{Valeur}}</th>
                                    <th>{{Classe}}</th>
                                    <th>{{Instance}}</th>
                                    <th>{{Index}}</th>
                                    <th>{{Type}}</th>
                                    <th>{{Rafraichissement}}</th>
                                    <th>{{Forcer la mise à jour}}</th>
                                    <th>{{Date de mise à jour}}</th>
                                </tr>
                                <tr id="template-variable" style="display:none">
                                    <td key="variable-name"></td>
                                    <td key="variable-value"></td>
                                    <td key="variable-cc"></td>
                                    <td key="variable-instance"></td>
                                    <td key="variable-index"></td>
                                    <td key="variable-type"></td>
                                    <td key="variable-polling"></td>
                                    <td key="variable-refresh"></td>
                                    <td key="variable-updatetime"></td>
                                </tr>
                                <tbody class="variables"></tbody>
                            </table>
                        </div>
                        <div class="tab-pane" id="parameters">
                            <div style="overflow: scroll;height : 100%;max-height: 96%;">
                                <table class="table table-striped">
                                    <tr>
                                        <th>{{Index}}</th>
                                        <th>{{Nom}}</th>
                                        <th>{{Type}}</th>
                                        <th>{{Valeur}}</th>
                                        <th>{{Modifier}}</th>
                                        <th>{{Aide}}
                                            <div class="btn-group pull-right">
                                                <a id="refreshParams" class="btn btn-info btn-sm refreshParams">
                                                    <i class="fa fa-refresh"></i> {{Actualiser les paramètres}}
                                                </a>
                                            </div>
                                            <div class="btn-group pull-right">
                                                <a id="copyToParams" class="btn btn-info btn-sm copyToParams">
                                                    <i class="fa fa-copy"></i> {{Appliquer sur...}}
                                                </a>
                                            </div>
                                            <div class="btn-group pull-right">
                                                <a id="copyParams" class="btn btn-info btn-sm copyParams">
                                                    <i class="fa fa-paste"></i> {{Reprendre de...}}
                                                </a>
                                            </div>
                                        </th>
                                    </tr>
                                    <tr id="template-parameter" style="display:none">
                                        <td key="parameter-index"></td>
                                        <td key="parameter-name"></td>
                                        <td key="parameter-type"></td>
                                        <td key="parameter-value"></td>
                                        <td key="parameter-edit"></td>
                                        <td key="parameter-help"></td>
                                    </tr>
                                    <tbody class="parameters"></tbody>
                                </table>
                            </div>
                        </div>
                        <div class="tab-pane" id="groups">
                            <a id="addGroup" class="btn btn-primary addGroup"><i class="fa fa-plus"></i>
                                {{Ajouter une association}}
                            </a>
                            <br>
                            <table class="table table-striped">
                                <tr>
                                    <th>{{ID du groupe}}</th>
                                    <th>{{ID de noeud}}</th>
                                    <th></th>
                                </tr>
                                <tr id="template-group" style="display:none">
                                    <td key="group-groupeindex"></td>
                                    <td key="group-nodeindex"></td>
                                    <td key="group-delete"></td>
                                </tr>
                                <tbody class="groups"></tbody>
                            </table>
                        </div>
                        <div class="tab-pane" id="systems">
                            <table class="table table-striped">
                                <tr>
                                    <th>{{Nom}}</th>
                                    <th>{{Valeur}}</th>
                                    <th>{{Modifier}}</th>
                                    <th>{{Classe de la commande}}</th>
                                    <th>{{Instance}}</th>
                                    <th>{{Index}}</th>
                                    <th>{{Type}}</th>
                                    <th>{{Date de mise à jour}}</th>
                                </tr>
                                <tr id="template-system" style="display:none">
                                    <td key="system-name"></td>
                                    <td key="system-value"></td>
                                    <td key="system-edit"></td>
                                    <td key="system-cc"></td>
                                    <td key="system-instance"></td>
                                    <td key="system-index"></td>
                                    <td key="system-type"></td>
                                    <td key="system-updatetime"></td>
                                </tr>
                                <tbody class="system_variables"></tbody>

                            </table>
                        </div>
                        <div class="tab-pane" id="actions">
                            <table class="table table-striped">
                                <tr>
                                    <td><a data-action="requestNodeNeighboursUpdate" class="btn btn-primary node_action"><i class="fa fa-sitemap"></i> {{Mise à jour des nœuds voisins}}</a></td>
                                    <td>{{Force la mise à jour de la liste des nœuds voisins.}}</td>
                                </tr>
                                <tr>
                                    <td><a data-action="healNode" class="btn btn-success node_action"><i class="fa fa-medkit"></i> {{Soigner le nœud}}</a></td>
                                    <td>{{Soigner le nœud au sein du réseau.}}</td>
                                </tr>
                                <tr>
                                    <td><a data-action="assignReturnRoute" class="btn btn-success node_action"><i class="fa fa-road""></i> {{Mise à jour de la route de retour au contrôleur}}</a></td>
                                    <td>{{Demandez la mise à jour de la route de retour au contrôleur.}}</td>
                                </tr>
                                <tr>
                                    <td><a data-action="testNode" class="btn btn-info node_action"><i class="fa fa-check-square-o"></i> {{Tester le nœud}}</a></td>
                                    <td>{{Envoyer une série de message à un noeud pour le tester s'il répond.}}</td>
                                </tr>
                                <tr>
                                    <td><a data-action="refreshNodeValues" class="btn btn-success node_action"><i class="fa fa-refresh"></i> {{Rafraîchir les valeurs du nœud}}</a></td>
                                    <td>{{Demande l'actualisation de l'ensemble des valeurs du nœud.}}</td>
                                </tr>
                                <tr>
                                    <td><a data-action="requestNodeDynamic" class="btn btn-success node_action"><i class="fa fa-refresh"></i> {{Récupère les CC dynamiques}}</a></td>
                                    <td>{{Récupère les données de commande classe dynamiques du nœud.}}</td>
                                </tr>
                                <tr>
                                    <td><a data-action="refreshNodeInfo" class="btn btn-success node_action"><i class="fa fa-retweet"></i> {{Rafraîchir infos du nœud}}</a></td>
                                    <td>{{Déclencher l'obtention des informations du nœud.}} <br>{{Les données du nœud sont obtenues du réseau Z-Wave de la même façon que s'il venait d'être ajouté.}}</td>
                                </tr>
                                <tr>
                                    <td><a data-action="hasNodeFailed" class="btn btn-primary node_action"><i class="fa fa-heartbeat"></i> {{Nœud en échec ?}}</a></td>
                                    <td>{{Vérifie si le nœud est dans la liste des nœuds en erreur.}}</td>
                                </tr>
                                <tr>
                                    <td><a data-action="removeFailedNode" class="btn btn-danger node_action"><i class="fa fa-times"></i> {{Supprimer le nœud en échec}}</a></td>
                                    <td>{{Permet de supprimer un nœud marqué comme défaillant par le contrôleur.}}<br>{{Le nœud doit être en échec.}}</td>
                                </tr>
                                <tr>
                                    <td><a id="replaceFailedNode" class="btn btn-warning"><i class="fa fa-chain-broken"></i> {{Remplacer nœud en échec}}</a></td>
                                    <td>{{Remplace un module en échec par un autre. Si le nœud n'est pas dans la liste des nœuds en échec sur le contrôleur, ou que le nœud répond, la commande va échouer.}}</td>
                                </tr>
                                <tr>
                                    <td><a data-action="sendNodeInformation" class="btn btn-info node_action"><i class="fa fa-info-circle"></i> {{Envoi infos du nœud}}</a></td>
                                    <td>{{Envoi une trame d'info au noeud (NIF).}}</td>
                                </tr>
                                <tr>
                                    <td><a id="regenerateNodeCfgFile" class="btn btn-warning node_action"><i class="fa fa-search"></i> {{Régénérer la détection du nœud}}</a></td>
                                    <td>{{Supprime les informations du noeud dans le fichier de config afin qu'il soit à nouveau détecté.}}<br>{{(Attention : Relance le réseau)}}</td>
                                </tr>
                                <tr>
                                    <td><a data-action="removeGhostNode" class="btn btn-warning node_action"><i class="fa fa-bug"></i> {{Suppression automatique du nœud fantôme}}</a></td>
                                    <td>{{Permet de supprimer un nœud sur pile qui n'est plus accessible sur le réseau.}}<br>{{Le nœud sera automatiquement supprimé dans les 5 à 15 minutes suivant le redémarrage du réseau}}<br>{{(Attention : Relance le réseau)}}</td>
                                </tr>
                            </table>
                        </div>
                        <div class="tab-pane" id="statistics">
                            <table class="table table-striped table-condensed">
                                <tr>
                                    <td><b>{{Temps de demande moyen (ms) :}}</b></td>
                                    <td><span class="zwaveStatsAttr" data-l1key="statistics" data-l2key="averageRequestRTT"></span></td>
                                </tr>
                                <tr>
                                    <td><b>{{Temps de réponse moyen (ms) :}}</b></td>
                                    <td><span class="zwaveStatsAttr" data-l1key="statistics" data-l2key="averageResponseRTT"></span></td>
                                </tr>
                                <tr>
                                    <td><b>{{Dernier message de réponse RTT:}}</b></td>
                                    <td><span class="zwaveStatsAttr" data-l1key="statistics" data-l2key="lastRequestRTT"></span></td>
                                </tr>
                                <tr>
                                    <td><b>{{Dernière réponse RTT :}}</b></td>
                                    <td><span class="zwaveStatsAttr" data-l1key="statistics" data-l2key="lastResponseRTT"></span></td>
                                </tr>
                                <tr>
                                    <td><b>{{Qualité de la communication avec ce noeud :}}</b></td>
                                    <td><span class="zwaveStatsAttr" data-l1key="statistics" data-l2key="quality"></span></td>
                                </tr>
                                <tr>
                                    <td><b>{{Nombre de messages reçus par ce noeud :}}</b></td>
                                    <td><span class="zwaveStatsAttr" data-l1key="statistics" data-l2key="receivedCnt"></span></td>
                                </tr>
                                <tr>
                                    <td><b>{{Nombre de messages reçus en double :}}</b></td>
                                    <td><span class="zwaveStatsAttr" data-l1key="statistics" data-l2key="receivedDups"></span></td>
                                </tr>
                                <tr>
                                    <td><b>{{Heure du dernier message reçu :}}</b></td>
                                    <td><span class="zwaveStatsAttr" data-l1key="statistics" data-l2key="receivedTS"></span></td>
                                </tr>
                                <tr>
                                    <td><b>{{Nombre de messages reçus spontanément :}}</b></td>
                                    <td><span class="zwaveStatsAttr" data-l1key="statistics" data-l2key="receivedUnsolicited"></span></td>
                                </tr>
                                <tr>
                                    <td><b>{{Nombre de tentatives d'envoi :}}</b></td>
                                    <td><span class="zwaveStatsAttr" data-l1key="statistics" data-l2key="retries"></span></td>
                                </tr>
                                <tr>
                                    <td><b>{{Nombre de messages envoyés par ce noeud :}}</b></td>
                                    <td><span class="zwaveStatsAttr" data-l1key="statistics" data-l2key="sentCnt"></span></td>
                                </tr>
                                <tr>
                                    <td><b>{{Nombre de messages envoyés en erreur :}}</b></td>
                                    <td><span class="zwaveStatsAttr" data-l1key="statistics" data-l2key="sentFailed"></span></td>
                                </tr>
                                <tr>
                                    <td><b>{{Heure du dernier message envoyé :}}</b></td>
                                    <td><span class="zwaveStatsAttr" data-l1key="statistics" data-l2key="sentTS"></span></td>
                                </tr>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <?php include_file('desktop', 'nodes', 'js', 'openzwave');?>

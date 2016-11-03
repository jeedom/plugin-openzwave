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
<script type="text/javascript" src="plugins/openzwave/3rdparty/vivagraph/vivagraph.min.js"></script>
<style media="screen" type="text/css">
    #graph_network {
        height: 80%;
        width: 90%;
        position: absolute;
    }
    #graph_network > svg {
        height: 100%;
        width: 100%
    }
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
    .node-primary-controller-color{
        color: #a65ba6;
    }
    .node-direct-link-color {
        color: #7BCC7B;
    }
    .node-remote-control-color {
        color: #00a2e8;
    }
    .node-more-of-one-up-color {
        color: #E5E500;
    }
    .node-more-of-two-up-color {
        color: #FFAA00;
    }
    .node-interview-not-completed-color {
        color: #979797;
    }
    .node-no-neighbourhood-color {
        color: #d20606;
    }
    .node-na-color {
        color: white;
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
    #log {
        width: 100%;
        height: 700px;
        margin: 0px;
        padding: 0px;
        font-size: 16px;
        color: #fff;
        background-color: #300a24;
        overflow: scroll;
        overflow-x: hidden;
        font-size: 16px;
    }
    .console-out {
        padding-left: 20px;
        padding-top: 20px;
    }
    .bound-config {
        width: 100%;
        margin: 0px;
        padding: 0px;
    }
    .bound-config textarea {
        width: 100%;
        margin: 0px;
        padding: 20px;
        height: 700px;
        font-size: 14px;

    }
</style>
<div id='div_networkOpenzwaveAlert' style="display: none;"></div>
<div id="confirmModal" class="modal fade modal-dialog-center" tabindex="-1" role="dialog" aria-labelledby="myModalLabel"
aria-hidden="true" data-backdrop="false">
<div class="modal-dialog">
    <div class="modal-content">
        <div class="modal-header">
            <a class="close" data-dismiss="modal" aria-hidden="true">×</a>
            <h3 id="myModalLabel">{{Confirmation}}</h3>
        </div>
        <div class="modal-body">
            <b>{{Remettre à zéro le contrôleur et effacer ses paramètres de configuration réseau.}}</b>
            <br>{{Le contrôleur devient un contrôleur primaire, prêt pour ajouter des modules sur un nouveau réseau.}}
            <div class="form-group">
                <label>{{Veuillez confirmer la remise à zéro en tapant YES}}</label>
                <input class="form-control required" id="confirm_text" data-placement="top" data-trigger="manual" type="text">
            </div>
        </div>
        <div class="modal-footer">
            <a type="submit" id="confirm_reset" class="btn btn-success">{{Confirmer la remise à zéro}}</a>
            <a class="btn btn-danger" data-dismiss="modal" aria-hidden="true">{{Annuler}}</a>
        </div>
    </div>
</div>
</div>
<div class='network' nid='' id="div_templateNetwork">
    <div class="container-fluid">
        <div id="content">
            <ul id="tabs_network" class="nav nav-tabs" data-tabs="tabs">
                <li class="active"><a href="#summary_network" data-toggle="tab"><i class="fa fa-tachometer"></i> {{Résumé}}</a></li>
                <li><a href="#notifications" data-toggle="tab"><i class="fa fa-bell-o"></i> {{Notifications}}</a> </li>
                <li><a href="#actions_network" data-toggle="tab"><i class="fa fa-sliders"></i> {{Actions}}</a></li>
                <li><a href="#statistics_network" data-toggle="tab"><i class="fa fa-bar-chart"></i> {{Statistiques}}</a></li>
                <li id="tab_graph"><a href="#graph_network" data-toggle="tab"><i class="fa fa-picture-o"></i> {{Graphique du réseau}}</a></li>
                <li id="tab_route"><a href="#route_network" data-toggle="tab"><i class="fa fa-table"></i> {{Table de routage}}</a></li>
                <li id="li_state" class="pull-right alert" style="background-color : #dff0d8;color : #3c763d;height:35px;border-color:#d6e9c6;display:none;"><span style="position:relative; top : -7px;">{{Demande envoyée}}</span></li>
            </ul>
            <div id="network-tab-content" class="tab-content">
                <div class="tab-pane active" id="summary_network">
                    <br>
                    <div class="panel panel-primary">
                        <div class="panel-heading"><h4 class="panel-title">{{Informations}}</h4></div>
                        <div class="panel-body">
                            <p>{{Réseau démarré le}} <span class="network-startTime label label-default" style="font-size : 1em;"></span> <span class="network-awakedTime label label-default" style="font-size : 1em;"></span></p>
                            <p>{{Le réseau contient}} <b><span class="network-nodes-count"></span></b> {{noeuds, actuellement}} <b><span class="network-sleeping-nodes-count"></span> </b>{{dorment}}</p>
                            <p>{{Intervalle des demandes :}}<span class="network-poll-interval label label-default" style="font-size : 1em;"></span></p>
                            <p>{{Voisins :}}<span class="network-node-neighbours label label-default" style="font-size : 1em;"></span></p>
                        </div>
                    </div>
                    <div class="panel panel-primary">
                        <div class="panel-heading"><h4 class="panel-title">{{Etat}}</h4></div>
                        <div class="panel-body">
                            <p><span class="network-state-led"></span> {{Etat actuel :}} <span class="network-state-description label label-default" style="font-size : 1em;"></span></p>
                            <p><span class="network-outgoing-send-queueWarning"></span> {{Queue sortante :}} <span class="network-outgoing-send-queue label label-default" style="font-size : 1em;"></span></p>
                        </div>
                    </div>
                    <div class="panel panel-primary">
                        <div class="panel-heading"><h4 class="panel-title">{{Capacités}}</h4></div>
                        <div class="panel-body"><lu class="network-controller-node-capabilities" style="font-size : 1em;"></lu></div>
                    </div>
                    <div class="panel panel-primary">
                        <div class="panel-heading"><h4 class="panel-title">{{Système}}</h4></div>
                        <div class="panel-body">
                            <p>{{Chemin du contrôleur Z-Wave :}} <span class="network-device-path label label-default" style="font-size : 1em;"></span></p>
                            <p>{{Version de la librairie OpenZwave :}}<span class="network-oz-library-version label label-default" style="font-size : 1em;"></span></p>
                            <p>{{Version de la librairie Python-OpenZwave :}} <span class="network-poz-library-version label label-default" style="font-size : 1em;"></span></p>
                        </div>
                    </div>
                </div>
                <div class="tab-pane" id="notifications">
                    <br>
                    <table class="table table-striped">
                        <tr>
                            <th>{{Reçu}}</th>
                            <th>{{Détails}}</th>
                            <th>{{Erreur}}</th>
                        </tr>
                        <tbody class="notification_variables"></tbody>
                    </table>
                </div>
                <div id="graph_network" class="tab-pane">
                    <table class="table table-bordered table-condensed" style="width: 350px;position:fixed;margin-top : 25px;">
                        <thead><tr><th colspan="2">{{Légende}}</th></tr></thead>
                        <tbody>
                            <tr>
                                <td class="node-primary-controller-color" style="width: 35px"><i class="fa fa-square fa-2x"></i></td>
                                <td>{{Contrôleur Primaire}}</td>
                            </tr>
                            <tr>
                                <td class="node-direct-link-color" style="width: 35px"><i class="fa fa-square fa-2x"></i></td>
                                <td>{{Communication directe}}</td>
                            </tr>
                            <tr>
                                <td class="node-remote-control-color"><i class="fa fa-square fa-2x"></i></td>
                                <td>{{Virtuellement associé au contrôleur primaire}}</td>
                            </tr>
                            <tr>
                                <td class="node-more-of-one-up-color"><i class="fa fa-square fa-2x"></i></td>
                                <td>{{Toutes les routes ont plus d'un saut}}</td>
                            </tr>
                            <tr>
                                <td class="node-interview-not-completed-color"><i class="fa fa-square fa-2x"></i></td>
                                <td>{{Interview non completé}}</td>
                            </tr>
                            <tr>
                                <td class="node-no-neighbourhood-color"><i class="fa fa-square fa-2x"></i></td>
                                <td>{{Présumé mort ou Pas de voisin}}</td>
                            </tr>
                        </tbody>
                    </table>
                    <div id="graph-node-name"></div>
                </div>
                <div id="route_network" class="tab-pane">
                    <br/>
                    <div id="div_routingTable"></div>
                    <table class="table table-bordered table-condensed" style="width: 500px;">
                        <thead><tr><th colspan="2">{{Légende}}</th></tr></thead>
                        <tbody>
                            <tr>
                                <td colspan="2">{{Nombre de [routes directes / avec 1 saut / 2 sauts]}}</td>
                            </tr>
                            <tr>
                                <td class="node-direct-link-color" style="width: 35px"><i class="fa fa-square fa-2x"></i></td>
                                <td>{{Communication directe}}</td>
                            </tr>
                            <tr>
                                <td class="node-remote-control-color"><i class="fa fa-square fa-2x"></i></td>
                                <td>{{Au moins 2 routes avec un saut}}</td>
                            </tr>
                            <tr>
                                <td class="node-more-of-one-up-color"><i class="fa fa-square fa-2x"></i></td>
                                <td>{{Moins de 2 routes avec un saut}}</td>
                            </tr>
                            <tr>
                                <td class="node-more-of-two-up-color"><i class="fa fa-square fa-2x"></i></td>
                                <td>{{Toutes les routes ont plus d'un saut}}</td>
                            </tr>
                            <tr>
                                <td class="node-interview-not-completed-color"><i class="fa fa-square fa-2x"></i></td>
                                <td>{{Interview non completé}}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="tab-pane" id="actions_network">
                    <table class="table">
                        <tr>
                            <td><a id="addDevice" class="btn btn-success"><i class="fa fa-plus-circle"></i> {{Ajouter module (inclusion)}}</a></td>
                            <td>{{Ajouter un nouveau module au réseau Z-Wave.}}</td>
                        </tr>
                        <tr>
                            <td><a id="addDeviceSecure" class="btn btn-warning"><i class="fa fa-plus-circle"></i> {{Ajouter module en mode sécurisé (inclusion)}}</a></td>
                            <td>{{Ajouter un nouveau module au réseau Z-Wave en mode sécurisé (peut ne pas marcher si le module ne le supporte pas bien).}}</td>
                        </tr>
                        <tr>
                            <td><a id="removeDevice" class="btn btn-danger"><i class="fa fa-minus-circle"></i> {{Supprimer module (Exclusion)}}</a></td>
                            <td>{{Supprimer un module du réseau Z-Wave.}}</td>
                        </tr>
                        <tr>
                            <td><a data-action="cancelCommand" class="btn btn-warning controller_action"><i class="fa fa-times"></i> {{Annuler commande}}</a></td>
                            <td>{{Annule toutes les commandes en cours sur le contrôleur.}}</td>
                        </tr>
                        <tr>
                            <td><a data-action="testNetwork" class="btn btn-primary controller_action"><i class="fa fa-check-square-o"></i> {{Test du réseau}}</a></td>
                            <td>{{Envoie une série de messages sur le réseau pour le tester.}}</td>
                        </tr>
                        <tr>
                            <td><a data-action="healNetwork" class="btn btn-success controller_action"><i class="fa fa-medkit"></i> {{Soigner le réseau}}</a></td>
                            <td>{{Soigner le réseau Z-Wave noeud par noeud.}}<br>{{Essaie de soigner tous les noeuds (un par un) en mettant à jour la liste des voisins et les routes optionnelles.}}</td>
                        </tr>
                        <tr>
                            <td><a data-action="createNewPrimary" class="btn btn-danger controller_action"><i class="fa fa-file"></i> {{Créer un nouveau noeud primaire}}</a></td>
                            <td>{{Mettez le contrôleur cible en mode de réception de configuration.}}<br>{{Le contrôleur cible doit être moins de 2m du contrôleur primaire. Nécessite SUC.}}</td>
                        </tr>
                        <tr>
                        <td><a data-action="receiveConfiguration" class="btn btn-danger controller_action"><i class="fa fa-file"></i> {{Receive Configuration}}</a></td>
                            <td>{{Transfert de la configuration réseau à partir d'un autre contrôleur.}}<br><i>{{Approcher l'autre contrôleur à moins de 2m du contrôleur primaire .}}</i></td>
                        </tr>
                        <tr>
                            <td><a data-action="transferPrimaryRole" class="btn btn-primary controller_action"><i class="fa fa-external-link"></i> {{Transférer le rôle primaire}}</a></td>
                            <td>{{Changer de contrôleur primaire. Le contrôleur primaire existant devient contrôleur secondaire.}}<br><i>{{Approcher l'autre contrôleur à moins de 2m du contrôleur primaire.}}</i></td>
                        </tr>
                        <tr>
                            <td><a id="writeconfigfile" class="btn btn-info"><i class="fa fa-pencil"></i> {{Ecrire le fichier de configuration}}</a></td>
                            <td>{{Ecrit le fichier de configuration OpenZwave.}}</td>
                        </tr>
                        <tr>
                            <td><a id="regenerateNodesCfgFile" class="btn btn-warning"><i class="fa fa-repeat"></i> {{Régénérer la détection des noeuds inconnus}}</a></td>
                            <td>{{Supprime les informations des noeuds inconnus dans le fichier de config afin qu'il soit régénéré.}}<br><i>{{(Attention : Relance du réseau)}}</i></td>
                        </tr>
                        <tr>
                            <td><a data-action="softReset" class="btn btn-warning controller_action"><i class="fa fa-times"></i>{{Redémarrage}}</a></td>
                            <td>{{Redémarre le contrôleur sans effacer les paramètres de sa configuration réseau.}}</td>
                        </tr>
                        <tr>
                            <td><a data-action="hardReset" class="btn btn-danger controller_action"><i class="fa fa-eraser"></i>{{Remise à zéro}}</a></td>
                            <td>{{Remise à zéro du contrôleur.}} <b>{{Remet à zéro un contrôleur et efface ses paramètres de configuration réseau.}}</b><br>{{Le contrôleur devient un contrôleur primaire, prêt pour ajouter de nouveaux modules à un nouveau réseau.}}</td>
                        </tr>
                    </table>
                </div>
                <div class="tab-pane" id="statistics_network">
                    <table class="table table-condensed table-striped">
                        <tr>
                            <td><b>{{Nombre d'émissions lues :}}</b></td>
                            <td><span class="stats_broadcastReadCnt"></span></td>
                        </tr>
                        <tr>
                            <td><b>{{Nombre d'émissions envoyées :}}</b></td>
                            <td><span class="stats_broadcastWriteCnt"></span></td>
                        </tr>
                        <tr>
                            <td><b>{{Nombre de bits ACK reçus :}}</b></td>
                            <td><span class="stats_ACKCnt"></span></td>
                        </tr>
                        <tr>
                            <td><b>{{Nombre de messages non-sollicités alors qu'en attente d'ACK :}}</b></td>
                            <td><span class="stats_ACKWaiting"></span></td>
                        </tr>
                        <tr>
                            <td><b>{{Nombre de bits CAN reçus :}}</b></td>
                            <td><span class="stats_CANCnt"></span></td>
                        </tr>
                        <tr>
                            <td><b>{{Nombre de bits NAK reçus :}}</b></td>
                            <td><span class="stats_NAKCnt"></span></td>
                        </tr>
                        <tr>
                            <td><b>{{Nombre de bits jamais arrivés :}}</b></td>
                            <td><span class="stats_OOFCnt"></span></td>
                        </tr>
                        <tr>
                            <td><b>{{Nombre de bits SOF reçus :}}</b></td>
                            <td><span class="stats_SOFCnt"></span></td>
                        </tr>
                        <tr>
                            <td><b>{{Nombre de mauvais checksums :}}</b></td>
                            <td><span class="stats_badChecksum"></span></td>
                        </tr>
                        <tr>
                            <td><b>{{Nombre de retours inattendus :}}</b></td>
                            <td><span class="stats_callbacks"></span></td>
                        </tr>
                        <tr>
                            <td><b>{{Nombre de ACK retournés en erreur :}}</b></td>
                            <td><span class="stats_noack"></span></td>
                        </tr>
                        <tr>
                            <td><b>{{Nombre de lectures en échec dues au timeout :}}</b></td>
                            <td><span class="stats_readAborts"></span></td>
                        </tr>
                        <tr>
                            <td><b>{{Nombre de messages d'échec dus au réseau occupé :}}</b></td>
                            <td><span class="stats_netbusy"></span></td>
                        </tr>
                        <tr>
                            <td><b>{{Nombre de messages correctement reçus :}}</b></td>
                            <td><span class="stats_readCnt"></span></td>
                        </tr>
                        <tr>
                            <td><b>{{Nombre de messages correctement envoyés :}}</b></td>
                            <td><span class="stats_writeCnt"></span></td>
                        </tr>
                        <tr>
                            <td><b>{{Nombre de messages non remis au réseau :}}</b></td>
                            <td><span class="stats_nondelivery"></span></td>
                        </tr>
                        <tr>
                            <td><b>{{Nombre de messages jetés ou non délivrés :}}</b></td>
                            <td><span class="stats_dropped"></span></td>
                        </tr>
                        <tr>
                            <td><b>{{Nombre de messages en échec à cause d'un mauvais routage :}}</b></td>
                            <td><span class="stats_badroutes"></span></td>
                        </tr>
                        <tr>
                            <td><b>{{Nombre de messages retransmis :}}</b></td>
                            <td><span class="stats_retries"></span></td>
                        </tr>
                        <tr>
                            <td><b>{{Nombre de messages reçus avec statut de routage occupé :}}</b></td>
                            <td><span class="stats_routedbusy"></span></td>
                        </tr>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
</div>
<?php include_file('desktop', 'network', 'js', 'openzwave');?>

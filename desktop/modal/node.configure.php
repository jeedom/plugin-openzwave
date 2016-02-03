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
sendVarToJs('node_id', init('id'));
$listServerZwave = openzwave::listServerZwave();
sendVarToJs('path', $listServerZwave[init('serverId')]['path'] . '/');
?>
<style media="screen" type="text/css">
	.noscrolling{
		width:99%;
		overflow: hidden;
	}
	.node-item{
		border: 1px solid;
	}
	.greeniconcolor {color:green;}
	.yellowiconcolor {color:#FFD700;}
	.rediconcolor {color:red;}
	.modal-dialog-center {
		margin: 0;
		position: absolute;
		top: 0%;
		left: 0%;
	}
	.table-striped>tbody>tr.yellowrow>td {
		background-color: #FFD700;
	}
	.table-striped>tbody>tr.redrow>td {
		background-color: #e74c3c;
	}
	.table-striped>tbody>tr.greenrow>td {
		/*background-color: #2ecc71;*/
	}
</style>
<div id='div_nodeConfigureOpenzwaveAlert' style="display: none;"></div>
<div class="modal fade modal-dialog-center" id="paramsModal" tabindex="-1" role="dialog" aria-hidden="true" data-backdrop="false">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
				<h4 class="modal-title" id="exampleModalLabel">Nouveau message</h4>
			</div>
			<div class="modal-body">
				<div id="modalparamname"></div>
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-default" data-dismiss="modal">Fermer</button>
				<button type="button" class="btn btn-primary" id="saveParam">Sauvegarder</button>
			</div>
		</div>
	</div>
</div>
<div class="modal fade modal-dialog-center" id="valuesModal" tabindex="-1" role="dialog" aria-hidden="true" data-backdrop="false">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
				<h4 class="modal-title" id="valueModalLabel">Nouveau message</h4>
			</div>
			<div class="modal-body">
				<div id="modalvaluename"></div>
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-default" data-dismiss="modal">Fermer</button>
				<button type="button" class="btn btn-primary" id="applyValue">Appliquer</button>
			</div>
		</div>
	</div>
</div>
<div class="modal fade modal-dialog-center" id="pollingModal" tabindex="-1" role="dialog" aria-hidden="true" data-backdrop="false">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
				<h4 class="modal-title" id="pollingModalLabel">Nouveau message</h4>
			</div>
			<div class="modal-body">
				<div id="modalpolling"></div>
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-default" data-dismiss="modal">Fermer</button>
				<button type="button" class="btn btn-primary" id="savePolling">Sauvegarder</button>
			</div>
		</div>
	</div>
</div>
<div class="modal fade modal-dialog-center" id="copyParamsModal" tabindex="-1" role="dialog" aria-hidden="true" data-backdrop="false">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
				<h4 class="modal-title" id="copyParamsModalLabel">Nouveau message</h4>
			</div>
			<div class="modal-body">
				<div id="modalcopyParams"></div>
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-default" data-dismiss="modal">Fermer</button>
				<button type="button" class="btn btn-primary" id="saveCopyParams">Copier les paramètres</button>
			</div>
		</div>
	</div>
</div>
<div class="modal fade modal-dialog-center" id="groupsModal" tabindex="-1" role="dialog" aria-hidden="true" data-backdrop="false">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
				<h4 class="modal-title" id="groupsModalLabel">Nouveau message</h4>
			</div>
			<div class="modal-body">
				<div id="modalgroups"></div>
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-default" data-dismiss="modal">Fermer</button>
				<button type="button" class="btn btn-primary" id="saveGroups">Sauvegarder</button>
			</div>
		</div>
	</div>
</div>
<div class='node' nid='' >
	<div id="template-node" >

		<center><h3><span class="node-productname fixed">{{inconnu}}</span> - <span class="node-name fixed">{{inconnu}}</span> - {{Node Id:}} <span class="node-id">{{inconnu}}</span></h3></center>
		<div class="container-fluid">
			<div id="content">

				<ul id="tabs" class="nav nav-tabs" data-tabs="tabs">
					<li id="tab-summary" class="active"><a href="#summary" data-toggle="tab"><i class="fa fa-tachometer"></i> {{Résumé}}</a></li>
					<li id="tab-values"><a href="#values" data-toggle="tab"><i class="fa fa-tag"></i> {{Valeurs}}</a></li>
					<li id="tab-parameters"><a href="#parameters" data-toggle="tab"><i class="fa fa-wrench"></i> {{Paramètres}}</a></li>
					<li id="tab-groups"><a href="#groups" data-toggle="tab"><i class="fa fa-users"></i> {{Associations}}</a></li>
					<li id="tab-systems"><a href="#systems" data-toggle="tab"><i class="fa fa-cogs"></i> {{Systèmes}}</a></li>
					<li id="tab-actions"><a href="#actions" data-toggle="tab"><i class="fa fa-sliders"></i> {{Actions}}</a></li>
					<li id="tab-stats"><a href="#statistics" data-toggle="tab"><i class="fa fa-bar-chart"></i> {{Statistiques}}</a></li>

					<li id="li_state" class="pull-right alert" style="background-color : #dff0d8;color : #3c763d;height:35px;border-color:#d6e9c6;display:none;"><span style="position:relative; top : -7px;">{{Envoi OK}}</span></li>
				</ul>
				<div id="my-tab-content" class="tab-content">
					<div class="tab-pane active" id="summary">
						<br>
						<div id="panel-danger" class="panel panel-danger template">
							<div class="panel-heading">
								<h4 class="panel-title"><i class="fa fa-exclamation-circle"></i> {{Attention}}</h4>
							</div>
							<div class="panel-body">
								<p><span class="node-warning">{{inconnu}}</span></p>
							</div>
						</div>
						<div class="panel panel-primary template">
							<div class="panel-heading">
								<h4 class="panel-title"><i class="fa fa-info-circle"></i> {{Informations Noeud}}</h4>
							</div>
							<div class="panel-body">
								<p>{{Objet parent :}} <b><span class="node-location label label-default" style="font-size : 1em;">{{inconnu}}</span></b></p>
								<p>{{Nom de l'équipement :}} <b><span class="node-name label label-default" style="font-size : 1em;">{{inconnu}}</span></b></p>
								<p>{{Modèle :}} <b><span class="node-productname label label-default" style="font-size : 1em;">{{inconnu}}</span></b></p>
								<p>{{Fabricant :}} <b><span class="node-vendor label label-default" style="font-size : 1em;">{{inconnu}}</span></b></p>
								<p><span class="node-zwave-id default">{{inconnu}}</span></p>
								<p>{{Etat des demandes :}} <b><span class="node-queryStage label label-default" style="font-size : 1em;">{{inconnu}}</span></b>  <i class="fa fa-info-circle" id="node-queryStageDescrition"></i></p>
								<p>{{Etat :}} <b><span class="node-sleep label label-default" style="font-size : 1em;">{{inconnu}}</span></b> <span class="node-battery-span">{{Batterie : }} <b><span class="node-battery label label-default" style="font-size : 1em;">{{inconnu}}</span></b></span></p>
								<p>{{Dernier message :}} <b><span class="node-lastSeen label label-default" style="font-size : 1em;">{{inconnu}}</span></b> <span class="node-next-wakeup-span">{{Prochain réveil : }} <b><span class="node-next-wakeup label label-default" style="font-size : 1em;">{{inconnu}}</span></b></span></p>
								<p>{{Voisins : }} <span class="node-neighbours label label-default" style="font-size : 1em;">{{inconnu}}</span></p>
							</div>
						</div>
						<div class="panel panel-primary template">
							<div class="panel-heading">
								<h4 class="panel-title"><i class="fa fa-info-circle"></i> {{Classe du module}}</h4>
							</div>
							<div class="panel-body">
								{{Basique :}} <b><span class="node-basic label label-default">{{inconnu}}</span></b>
								<br/>
								{{Générique :}} <b><span class="node-generic label label-default">{{inconnu}}</span></b>
								<br/>
								{{Spécifique :}} <b><span class="node-specific label label-default">{{inconnu}}</span></b></p>
							</div>
						</div>


						<div class="panel panel-primary template">
							<div class="panel-heading">
								<h4 class="panel-title"><i class="fa fa-info-circle"></i> {{Informations Protocole}}</h4>
							</div>
							<div class="panel-body">
								<p>{{Vitesse maximale de communication du module :}}<b><span class="node-maxBaudRate"></span></b> {{bit/sec}}</p>
								<b><span class="node-routing"></span></b>
								<b><span class="node-isSecurity"></span></b>
								<b><span class="node-listening"></span></b>
								<b><span class="node-isFrequentListening"></span></b>
								<b><span class="node-isBeaming"></span></b>
								<br/>
								<p><b><span class="node-security"></span></b></p>
							</div>
						</div>

						<!--
                            <p>Id: <b><span class="node-id label label-default"></span></b></p>
                            <p>Product Name: <b><span class="node-name label label-default">undefined</span></b></p>
                            <p>Manufacturer: <b><span class="node-vendor label label-default">undefined</span></b></p>
                            <p>Type: <b><span class="node-type label label-default">undefined</span></b></p>
                            <p>Basic: <b><span class="node-basic label label-default">undefined</span></b> Generic: <b><span class="node-generic label label-default">undefined</span></b> Specific: <b><span class="node-specific label label-default">undefined</span></b></p>
                            <p><b><span class="node-sleep label label-default">undefined</span></b></p>
                            <p><b><span class="node-isFailed label label-default">undefined</span></b></p>
                            <p>Query stage: <b><span class="node-queryStage label label-default">undefined</span></b>  <i class="fa fa-info-circle" id="node-queryStageDescrition"></i></p>
                            <p>Is Locked : <b><span class="node-isLocked label label-default">undefined</span></b></p>
                            <p>Neighbours: <span class="node-neighbours label label-default">undefined</span></p>
                            <div class="panel panel-primary template">
                              <div class="panel-heading">
                                <h4 class="panel-title">Protocol Informations</h4>
                              </div>
                              <div class="panel-body">
                                <p>Maximum baud rate at which this device can communicate: <b><span class="node-maxBaudRate"></span></b> bit/sec</p>
                                <p><b><span class="node-routing"></span></b></p>
                                <p><b><span class="node-isSecurity"></span></b></p>
                                <p><b><span class="node-listening"></span></b></p>
                                <p><b><span class="node-isFrequentListening"></span></b></p>
                                <p><b><span class="node-isBeaming"></span></b></p>
                                <p><b><span class="node-security"></span></b></p>
                              </div>
                            </div>
                        -->

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
											<a id="refreshParams" class="btn btn-info btn-sm refreshParams"><i class="fa fa-refresh"></i> {{Actualiser les paramètres}}</a>
										</div>
										<div class="btn-group pull-right">
											<a id="copyParams" class="btn btn-info btn-sm copyParams"><i class="fa fa-copy"></i> {{Copier les paramètres d'un node existant}}</a>
										</div></th>
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
						<button type="button" id="addGroup" class="btn btn-primary addGroup"><i class="fa fa-plus"></i> {{Ajouter une association}}</button>
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
								<td><button type="button" id="requestNodeNeighboursUpdate" class="btn btn-primary requestNodeNeighboursUpdate"><i class="fa fa-sitemap"></i> {{Mise à jour des nœud voisins}}</button></td>
								<td>{{Force la mise à jour de la liste des nœuds voisins.}}</td>
							</tr>
							<tr>
								<td><button type="button" id="healNode" class="btn btn-success healNode"><i class="fa fa-medkit"></i> {{Soigner le nœud}}</button></td>
								<td>{{Soigner le nœud au sein du réseau.}}</td>
							</tr>
							<tr>
								<td><button type="button" id="testNode" class="btn btn-info testNode"><i class="fa fa-check-square-o"></i> {{Tester le nœud}}</button></td>
								<td>{{Envoyer une série de message à un noeud pour le tester s'il répond.}}</td>
							</tr>
							<tr>
								<td><button type="button" id="refreshNodeValues" class="btn btn-success"><i class="fa fa-refresh"></i> {{Rafraîchir les valeurs du nœud}}</button></td>
								<td>{{Demande l'actualisation de l'ensemble des valeurs du nœud.}}</td>
							</tr>
							<tr>
								<td><button type="button" id="requestNodeDynamic" class="btn btn-success"><i class="fa fa-refresh"></i> {{Récupère les CC dynamique}}</button></td>
								<td>{{Récupère les données de commande classe dynamiques du nœud.}}</td>
							</tr>
							<tr>
								<td><button type="button" id="refreshNodeInfo" class="btn btn-success refreshNodeInfo"><i class="fa fa-retweet"></i> {{Rafraîchir infos du nœud}}</button></td>
								<td>{{Déclencher l'obtention des information du nœud.}} <br>{{Les données du nœud sont obtenues du réseau Z-Wave de la même façon que s'il venait d'être ajouté.}}</td>
							</tr>
							<tr>
								<td><button type="button" id="hasNodeFailed" class="btn btn-primary hasNodeFailed"><i class="fa fa-question"></i> {{Nœud en échec ?}}</button></td>
								<td>{{Vérifie si le nœud est dans la liste des nœuds en erreur.}}</td>
							</tr>
							<tr>
								<td><button type="button" id="removeFailedNode" class="btn btn-danger"><i class="fa fa-times"></i> {{Supprimer le nœud en échec}}</button></td>
								<td>{{Permet de supprimer un nœud marqué comme défaillant par le contrôleur.}}<br>{{Le nœud doit être en échec.}}</td>
							</tr>
							<tr>
								<td><button type="button" id="replaceFailedNode" class="btn btn-warning"><i class="fa fa-repeat"></i> {{Remplacer nœud en échec}}</button></td>
								<td>{{Remplace un module en échec par un autre. Si le nœud n'est pas dans la liste des nœuds en échec sur le contrôleur, ou que le nœud répond, la commande va échouer.}}</td>
							</tr>
							<tr>
								<td><button type="button" id="sendNodeInformation" class="btn btn-info"><i class="fa fa-info-circle"></i> {{Envoi infos du nœud}}</button></td>
								<td>{{Envoi une trame d'info au noeud (NIF).}}</td>
							</tr>
							<tr>
								<td><button type="button" id="regenerateNodeCfgFile" class="btn btn-warning"><i class="fa fa-repeat"></i> {{Regénérer la détection du nœud}}</button></td>
								<td>{{Supprime les informations du noeud dans le fichier de config afin qu'il soit à nouveau détecté.}}<br>
									{{Le noeud sera automatiquement supprimé dans les 5 minutes suivant le redémarrage du réseau}}
									{{(Attention : Relance le réseau)}}</td>
							</tr>
							<tr>
								<td><button type="button" id="removeGhostNode" class="btn btn-warning"><i class="fa fa-repeat"></i> {{Suppression automatique du nœud fantôme}}</button></td>
								<td>{{Permet de supprimer un nœud sur pile qui n'est plus accessible sur le réseau.}}<br>
									{{Le nœud sera automatiquement supprimé dans les 5 minutes suivant le redémarrage du réseau}}
									{{(Attention : Relance le réseau)}}
								</td>
							</tr>
						</table>
					</div>
					<div class="tab-pane" id="statistics">
						<!--
                        Statistics:
                        cdef struct NodeData:
                                * sentCnt                  # Number of messages sent from this node.
                                * sentFailed               # Number of sent messages failed
                                * retries                  # Number of message retries
                                * receivedCnt              # Number of messages received from this node.
                                * receivedDups             # Number of duplicated messages received;
                                * receivedUnsolicited      # Number of messages received unsolicited
                                * sentTS                   # Last message sent time
                                * receivedTS               # Last message received time
                                * lastRequestRTT           # Last message request RTT
                                * averageRequestRTT        # Average Request Round Trip Time (ms).
                                * lastResponseRTT          # Last message response RTT
                                * averageResponseRTT       # Average Reponse round trip time.
                                * quality                  # Node quality measure
                                * lastReceivedMessage      # Place to hold last received message
                            -->
						<table class="table table-striped table-condensed">
							<tr>
								<td><b>{{Temps de demande moyen (ms) :}}</b></td><td><span class="stats_av_req_rtt"></span></td>
							</tr><tr>
								<td><b>{{Temps de réponse moyen (ms) :}}</b></td><td><span class="stats_av_res_rtt"></span></td>
							</tr><tr>
								<td><b>{{Dernier message de réponse RTT:}}</b></td><td><span class="stats_la_req_rtt"></span></td>
							</tr><tr>
								<td><b>{{Dernière réponse RTT :}}</b></td><td><span class="stats_la_res_rtt"></span></td>
							</tr><tr>
								<td><b>{{Qualité de la communication avec ce noeud :}}</b></td><td><span class="stats_quality"></span></td>
							</tr><tr>
								<td><b>{{Nombre de messages reçus par ce noeud :}}</b></td><td><span class="stats_rec_cnt"></span></td>
							</tr><tr>
								<td><b>{{Nombre de messages reçus en double :}}</b></td><td><span class="stats_rec_dups"></span></td>
							</tr><tr>
								<td><b>{{Heure du dernier message reçu :}}</b></td><td><span class="stats_rec_ts"></span></td>
							</tr><tr>
								<td><b>{{Nombre de messages reçus spontanément :}}</b></td><td><span class="stats_rec_uns"></span></td>
							</tr><tr>
								<td><b>{{Nombre de tentatives d'envoi :}}</b></td><td><span class="stats_retries"></span></td>
							</tr><tr>
								<td><b>{{Nombre de messages envoyés par ce noeud :}}</b></td><td><span class="stats_sen_cnt"></span></td>
							</tr><tr>
								<td><b>{{Nombre de messages envoyés en erreur :}}</b></td><td><span class="stats_sen_failed"></span></td>
							</tr><tr>
								<td><b>{{Heure du dernier message envoyé :}}</b></td><td><span class="stats_sen_ts"></span></td>
							</tr>
						</table>
					</div>
				</div>
			</div>
		</div>

	</div>

</div>
<?php include_file('desktop', 'nodes', 'js', 'openzwave');?>
<script>
	var nodes = {};
	if (window["app_nodes"]!=undefined){
		window["app_nodes"].init();
		window["app_nodes"].show();
	}
	$('.tab-pane').height($('#md_modal').height() - 100);
	$('.tab-pane').css('overflow','scroll');
</script>
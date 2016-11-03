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

 $('.controller_action').on('click',function(){
    jeedom.openzwave.controller.action({
        action : $(this).data('action'),
        error: function (error) {
            $('#div_networkOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
        },
        success: function () {
           $('#li_state').show();
           setTimeout(function () {
            $('#li_state').hide();
        }, 3000);
       }
   });
});

 $("#tab_graph").off("click").on("click", function () {
    network_load_data();
});

 $("#tab_route").off("click").on("click", function () {
     jeedom.openzwave.network.info({
        info : 'getNeighbours',
        error: function (request, status, error) {
            handleAjaxError(request, status, error, $('#div_networkOpenzwaveAlert'));
        },
        success: function (data) { 
            devicesRouting = data.devices;
            var skipPortableAndVirtual = true; 
            var routingTable = '';
            var routingTableHeader = '';
            const queryStageNeighbors = 13;
            $.each(devicesRouting, function (nodeId, node) {
                if (nodeId == 255) {
                    return;
                }
                if (skipPortableAndVirtual && node.data.type.basic == 1) {
                    return;
                }
                var routesCount = getRoutesCount(nodeId);

                if (node.data.type.basic != 2) {
                    var link = 'index.php?v=d&p=openzwave&m=openzwave&logical_id=' + nodeId;
                } else {
                    var link = '#';
                }
                if (node.data.name.value != '') {
                    routingTableHeader += '<th title="' + node.data.location.value + ' ' + node.data.name.value + '" >' + nodeId + '</th>';
                    if (isset(eqLogic_human_name[nodeId])) {
                        var name = '<span class="nodeConfiguration cursor" data-node-id="' + nodeId + '">' + nodeId + ' ' + eqLogic_human_name[nodeId] + '</span>';
                    } else {
                        var name = '<span class="nodeConfiguration cursor" data-node-id="' + nodeId + '"><span class="label label-primary">' + node.data.location.value + '</span> ' + node.data.name.value + '</span>';
                    }
                } else {
                    routingTableHeader += '<th title="' + node.data.product_name.valuee + '" >' + nodeId + '</th>';
                    var name = '<span class="nodeConfiguration cursor" data-node-id="' + nodeId + '">' + node.data.product_name.value + '</span>';
                }
                routingTable += '<tr><td style="width: 500px">' + name;
                if (node.data.isDead.value) {
                    routingTable += '  <i class="fa fa-exclamation-triangle fa-lg" style="color:red; text-align:right"  title="{{Présumé mort}}"></i>';
                }
                routingTable += '</td><td style="width: 35px">' + nodeId + '</td>';
                $.each(devicesRouting, function (nnodeId, nnode) {
                    if (nnodeId == 255)
                        return;
                    if (skipPortableAndVirtual && nnode.data.type.basic == 1)
                        return;
                    var rtClass;
                    if (!routesCount[nnodeId])
                        routesCount[nnodeId] = new Array(); 
                    var routeHops = (routesCount[nnodeId][0] || '0') + "/";
                    routeHops += (routesCount[nnodeId][1] || '0') + "/";
                    routeHops += (routesCount[nnodeId][2] || '0');
                    if (nodeId == nnodeId || node.data.type.basic == 1 || nnode.data.type.basic == 1) {
                        rtClass = 'node-na-color';
                        routeHops = '';
                    } else if (nnode.data.state.value <= queryStageNeighbors || node.data.state.value <= queryStageNeighbors) {
                        rtClass = 'node-interview-not-completed-color';
                    } else if ($.inArray(parseInt(nnodeId, 10), node.data.neighbours.value) != -1)
                    rtClass = 'node-direct-link-color';
                    else if (routesCount[nnodeId] && routesCount[nnodeId][1] > 1)
                        rtClass = 'node-remote-control-color';
                    else if (routesCount[nnodeId] && routesCount[nnodeId][1] == 1)
                        rtClass = 'node-more-of-one-up-color';
                    else
                        rtClass = 'node-more-of-two-up-color';
                    routingTable += '<td class=' + rtClass + ' style="width: 35px"><i class="fa fa-square fa-2x" title="' + routeHops + '"></i></td>';
                });
                routingTable += '</td><td><button type="button" id="requestNodeNeighboursUpdate" data-nodeid="' + nodeId + '" class="btn btn-xs btn-primary requestNodeNeighboursUpdate" title="{{Mise à jour des noeuds voisins}}"><i class="fa fa-refresh"></i></button></td></tr>';
            });
            $('#div_routingTable').html('<table class="table table-bordered table-condensed"><thead><tr><th>{{Nom}}</th><th>ID</th>' + routingTableHeader + '<th><button type="button" id="healNetwork2" class="btn btn-xs btn-success healNetwork2" title="{{Soigner le réseau}}"><i class="fa fa-medkit"></i></button></th></tr></thead><tbody>' + routingTable + '</tbody></table>');
        }
    });
});

$("#addDevice").off("click").on("click", function () {
 jeedom.openzwave.controller.addNodeToNetwork({
    secure : 0,
    dataType: 'json',
    error: function (request, status, error) {
        handleAjaxError(request, status, error, $('#div_networkOpenzwaveAlert'));
    },
    success: function (data) {
        if (data['result'] == true) {
            $('#li_state').show();
            setTimeout(function () {
                $('#li_state').hide();
            }, 3000);
        } else {
            $('#div_networkOpenzwaveAlert').showAlert({message: '{{Echec}} :' + data.data, level: 'danger'});
        }
    }
});
});

$("#addDeviceSecure").off("click").on("click", function () {
  jeedom.openzwave.controller.addNodeToNetwork({
    secure : 1,
    error: function (request, status, error) {
        handleAjaxError(request, status, error, $('#div_networkOpenzwaveAlert'));
    },
    success: function (data) {
        if (data['result'] == true) {
         $('#li_state').show();
         setTimeout(function () {
            $('#li_state').hide();
        }, 3000);
     } else {
        $('#div_networkOpenzwaveAlert').showAlert({message: '{{Echec}} :' + data.data, level: 'danger'});
    }
}
});
});

$("#removeDevice").off("click").on("click", function () {
   jeedom.openzwave.controller.removeNodeFromNetwork({
    error: function (request, status, error) {
        handleAjaxError(request, status, error, $('#div_networkOpenzwaveAlert'));
    },
    success: function (data) {
        if (data['result'] == true) {
            $('#li_state').show();
            setTimeout(function () {
                $('#li_state').hide();
            }, 3000);
        } else {
            $('#div_networkOpenzwaveAlert').showAlert({message: '{{Echec}} :' + data.data, level: 'danger'});
        }
    }
});
});

$("#replicationSend").off("click").on("click", function () {
    return;
    jeedom.openzwave.controller.replicationSend({
        bridge_controller_id : bridge_controller_id,
        error: function (request, status, error) {
            handleAjaxError(request, status, error, $('#div_networkOpenzwaveAlert'));
        },
        success: function (data) {
            $('#li_state').show();
            setTimeout(function () {
                $('#li_state').hide();
            }, 3000);
        }
    });
});

$("#regenerateNodesCfgFile").off("click").on("click", function () {
    bootbox.confirm("Etes-vous sûr ? Cela va redémarrer votre réseau", function (result) {
      if (result) {
          jeedom.openzwave.network.action({
            action:'removeUnknownsDevicesZWConfig',
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_networkOpenzwaveAlert'));
            },
            success: function (data) {
             $('#li_state').show();
             setTimeout(function () {
                $('#li_state').hide();
            }, 3000);
         }
     });
      }
  });
});
$("body").off("click", ".requestNodeNeighboursUpdate").on("click", ".requestNodeNeighboursUpdate", function (e) {
 $.ajax({
    url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + $(this).attr('data-nodeid') + "].RequestNodeNeighbourUpdate()",
    dataType: 'json',
    error: function (request, status, error) {
        handleAjaxError(request, status, error, $('#div_networkOpenzwaveAlert'));
    },
    success: function (data) {
        if (data['result'] == true) {
         $('#li_state').show();
         setTimeout(function () {
            $('#li_state').hide();
        }, 3000);
         network_load_data();
         app_network.displayRoutingTable();
     } else {
        $('#div_networkOpenzwaveAlert').showAlert({message: '{{Echec}} :' + data.data, level: 'danger'});
    }
}
});
});

function network_load_data(){
    $('#graph_network svg').remove();
    jeedom.openzwave.network.info({
        info:'getNeighbours',
        error: function (request, status, error) {
            handleAjaxError(request, status, error, $('#div_networkOpenzwaveAlert'));
        },
        success: function (data) {
            nodes = data['devices'];
            var graph = Viva.Graph.graph();
            var controllerId = 1;
            for (z in nodes) {
                if (nodes[z].data.isPrimaryController.value == true){
                    controllerId = parseInt(z);
                    break;
                }
            }
            const queryStageNeighbors = 13;
            for (z in nodes) {
                if (nodes[z].data.name.value != '') {
                    if (isset(eqLogic_human_name[z])) {
                        graph.addNode(z, {
                            'name': eqLogic_human_name[z],
                            'neighbours': nodes[z].data.neighbours.value,
                            'enabled': nodes[z].data.neighbours.enabled,
                            'interview': parseInt(nodes[z].data.state.value)
                        });
                    } else {
                        graph.addNode(z, {
                            'name': '<span class="label label-primary">' + nodes[z].data.location.value + '</span> ' + nodes[z].data.name.value,
                            'neighbours': nodes[z].data.neighbours.value,
                            'enabled': nodes[z].data.neighbours.enabled,
                            'interview': parseInt(nodes[z].data.state.value)
                        });
                    }
                } else {
                    graph.addNode(z, {
                        'name': nodes[z].data.product_name.value,
                        'neighbours': nodes[z].data.neighbours.value,
                        'enabled': nodes[z].data.neighbours.enabled,
                        'interview': parseInt(nodes[z].data.state.value)
                    });
                }
                if (nodes[z].data.neighbours.value.length < 1 && nodes[z].data.neighbours.enabled != 1) {
                    if (typeof nodes[controllerId] != 'undefined') {
                        graph.addLink(z, controllerId, {isdash: 1, lengthfactor: 0.6});
                    }
                } else {
                    for (neighbour in nodes[z].data.neighbours.value) {
                        neighbourid = nodes[z].data.neighbours.value[neighbour];
                        if (typeof nodes[neighbourid] != 'undefined') {
                            graph.addLink(z, neighbourid, {isdash: 0, lengthfactor: 0});
                        }
                    }
                }
            }
            var graphics = Viva.Graph.View.svgGraphics(),
            nodeSize = 24,
            highlightRelatedNodes = function (nodeId, isOn) {
                graph.forEachLinkedNode(nodeId, function (node, link) {
                    var linkUI = graphics.getLinkUI(link.id);
                    if (linkUI) {
                        linkUI.attr('stroke', isOn ? '#FF0000' : '#B7B7B7');
                    }
                });
            };
            graphics.node(function (node) {
                if (typeof node.data == 'undefined') {
                    graph.removeNode(node.id);
                }
                nodecolor = '#7BCC7B';
                var nodesize = 10;
                const nodeshape = 'rect';
                if (node.id == controllerId) {
                    nodecolor = '#a65ba6'; 
                    nodesize = 16;
                } else if (node.data.enabled == false) {
                    nodecolor = '#00a2e8'; 
                } else if (node.data.neighbours.length < 1 && node.id != controllerId && node.data.interview >= queryStageNeighbors) {
                    nodecolor = '#d20606'; 
                } else if (node.data.neighbours.indexOf(controllerId) == -1 && node.id != controllerId && node.data.interview >= queryStageNeighbors) {
                    nodecolor = '#E5E500'; 
                } else if (node.data.interview < queryStageNeighbors) {
                    nodecolor = '#979797'; 
                }
                var ui = Viva.Graph.svg('g'),
                svgText = Viva.Graph.svg('text').attr('y', '0px').text(node.id),
                img = Viva.Graph.svg(nodeshape)
                .attr("width", nodesize)
                .attr("height", nodesize)
                .attr("fill", nodecolor);
                ui.append(svgText);
                ui.append(img);
                $(ui).hover(function () {
                    var link = 'index.php?v=d&p=openzwave&m=openzwave&logical_id=' + node.id;
                    numneighbours = node.data.neighbours.length;
                    interview = node.data.interview;
                    if (numneighbours < 1 && interview >= queryStageNeighbors) {
                        if (node.data.enabled) {
                            sentenceneighbours = '{{Pas de voisins}}';
                        } else {
                            sentenceneighbours = '{{Télécommande}}'
                        }
                    } else if (interview >= queryStageNeighbors) {
                        sentenceneighbours = numneighbours + ' {{voisins}} [' + node.data.neighbours + ']';
                    } else {
                        sentenceneighbours = '{{Interview incomplet}}';
                    }
                    if (node.id != controllerId) {
                        linkname = '<a href="' + link + '">' + node.data.name + '</a>'
                    } else {
                        linkname = node.data.name
                    }
                    $('#graph-node-name').html(linkname + ' : ' + sentenceneighbours);
                    highlightRelatedNodes(node.id, true);
                }, function () {
                    highlightRelatedNodes(node.id, false);
                });
                return ui;
            }).placeNode(function (nodeUI, pos) {
                nodeUI.attr('transform',
                    'translate(' +
                    (pos.x - nodeSize / 3) + ',' + (pos.y - nodeSize / 2.5) +
                    ')');
            });
            var middle = graph.getNode(controllerId);
            if (typeof middle !== 'undefined') {
                middle.isPinned = true;
            }
            var idealLength = 200;
            var layout = Viva.Graph.Layout.forceDirected(graph, {
                springLength: idealLength,
                stableThreshold: 0.9,
                dragCoeff: 0.01,
                springCoeff: 0.0004,
                gravity: -20,
                springTransform: function (link, spring) {
                    spring.length = idealLength * (1 - link.data.lengthfactor);
                }
            });
            graphics.link(function (link) {
                dashvalue = '5, 0';
                if (link.data.isdash == 1) {
                    dashvalue = '5, 2';
                }
                return Viva.Graph.svg('line').attr('stroke', '#B7B7B7').attr('stroke-dasharray', dashvalue).attr('stroke-width', '0.4px');
            });
            var renderer = Viva.Graph.View.renderer(graph, {
                layout: layout,
                graphics: graphics,
                prerender: 10,
                renderLinks: true,
                container: document.getElementById('graph_network')
            });
            renderer.run();
            setTimeout(function () {
                renderer.pause();
                renderer.reset();
            }, 200);
        }
    });
}


function network_load_info(){
    jeedom.openzwave.network.info({
        info : 'getStatus',
        global:false,
        error: function (request, status, error) {
            handleAjaxError(request, status, error, $('#div_networkOpenzwaveAlert'));
            if($('#div_templateNetwork').html() != undefined && $('#div_templateNetwork').is(':visible')){
                setTimeout(function(){ network_load_info(); }, 2000);
            }
        },
        success: function (data) {
            $(".network .stats_ACKCnt").html(data.controllerStatistics.ACKCnt);
            $(".network .stats_ACKWaiting").html(data.controllerStatistics.ACKWaiting);
            $(".network .stats_CANCnt").html(data.controllerStatistics.CANCnt);
            $(".network .stats_NAKCnt").html(data.controllerStatistics.NAKCnt);
            $(".network .stats_OOFCnt").html(data.controllerStatistics.OOFCnt);
            $(".network .stats_SOFCnt").html(data.controllerStatistics.SOFCnt);
            $(".network .stats_badChecksum").html(data.controllerStatistics.badChecksum);
            $(".network .stats_badroutes").html(data.controllerStatistics.badroutes);
            $(".network .stats_broadcastReadCnt").html(data.controllerStatistics.broadcastReadCnt);
            $(".network .stats_broadcastWriteCnt").html(data.controllerStatistics.broadcastWriteCnt);
            $(".network .stats_callbacks").html(data.controllerStatistics.callbacks);
            $(".network .stats_dropped").html(data.controllerStatistics.dropped);
            $(".network .stats_netbusy").html(data.controllerStatistics.netbusy);
            $(".network .stats_noack").html(data.controllerStatistics.noack);
            $(".network .stats_nondelivery").html(data.controllerStatistics.nondelivery);
            $(".network .stats_readAborts").html(data.controllerStatistics.readAborts);
            $(".network .stats_readCnt").html(data.controllerStatistics.readCnt);
            $(".network .stats_retries").html(data.controllerStatistics.retries);
            $(".network .stats_routedbusy").html(data.controllerStatistics.routedbusy);
            $(".network .stats_writeCnt").html(data.controllerStatistics.writeCnt);

            $(".network .network-startTime").html(jeedom.openzwave.timestampConverter(data.startTime));
            var awakedDelay = data.awakedDelay;
            if (awakedDelay != null) {
                $(".network .network-awakedTime").html('opérationnel en ' + awakedDelay + ' secondes');
            }else {
                $(".network .network-awakedTime").html('');
            }
            $(".network .network-nodes-count").html(data.nodesCount);        
            $(".network .network-sleeping-nodes-count").html(data.sleepingNodesCount);
            $(".network .network-scenes-count").html(data.scenesCount);
            var pollInterval = jeedom.openzwave.durationConvert(parseInt(data.pollInterval, 0) / 1000);
            $(".network .network-poll-interval").html(pollInterval);
            $(".network .network-isready").html(data.isReady);
            $(".network .network-state-description").html(data.stateDescription);
            var stateled = "";
            switch (data.state) {
                case 0:
                stateled = "<i class='fa fa-exclamation-circle rediconcolor'></i>";
                break;
                case 1:
                stateled = "<i class='fa fa-exclamation-circle rediconcolor'></i>";
                break;
                case 3:
                stateled = "<i class='fa fa-exclamation-circle rediconcolor'></i>";
                break;
                case 5:
                stateled = "<i class='fa fa-circle yellowiconcolor'></i>";
                break;
                case 7:
                stateled = "<i class='fa fa-bullseye greeniconcolor'></i>";
                break;
                case 10:
                stateled = "<i class='fa fa-circle greeniconcolor'></i>";
                break;
            }
            $(".network .network-state-led").html(stateled);
            var node_capabilities = '';
            if (data.controllerNodeCapabilities.indexOf('primaryController') != -1) {
                node_capabilities += '<li>{{Contrôleur Primaire}}</li>'
            }
            if (data.controllerNodeCapabilities.indexOf('staticUpdateController') != -1) {
                node_capabilities += '<li>{{Contrôleur statique de mise à jour (SUC)}}</li>'
            }
            if (data.controllerNodeCapabilities.indexOf('bridgeController') != -1) {
                node_capabilities += '<li>{{Contrôleur secondaire}}</li>'
            }
            if (data.controllerNodeCapabilities.indexOf('listening') != -1) {
                node_capabilities += '<li>{{Le noeud est alimenté et écoute en permanence}}</li>'
            }
            if (data.controllerNodeCapabilities.indexOf('beaming') != -1) {
                node_capabilities += '<li>{{Le noeud est capable d\'envoyer une trame réseaux}}</li>';
            }
            $(".network .network-controller-node-capabilities").html(node_capabilities);
            var outgoingSendQueue = parseInt(data.outgoingSendQueue, 0);
            if (outgoingSendQueue == 0) {
                outgoingSendQueueDescription = "<i class='fa fa-circle fa-lg greeniconcolor'></i>";
            }else if (outgoingSendQueue <= 5) {
                outgoingSendQueueDescription = "<i class='fa fa-spinner fa-spin fa-lg greeniconcolor'></i>";
            }else if (outgoingSendQueue <= 15) {
                outgoingSendQueueDescription = "<i class='fa fa-spinner fa-spin fa-lg yellowiconcolor'></i>";
            }else {
                outgoingSendQueueDescription = "<i class='fa fa-spinner fa-spin fa-lg rediconcolor'></i>";
            }
            $(".network .network-outgoing-send-queue").html(outgoingSendQueue);
            $(".network .network-outgoing-send-queueWarning").html(outgoingSendQueueDescription);
            $(".network .network-controller-stats").html(data.controllerStatistics);
            $(".network .network-device-path").html(data.devicePath);
            $(".network .network-oz-library-version").html(data.OpenZwaveLibraryVersion);
            $(".network .network-poz-library-version").html(data.PythonOpenZwaveLibraryVersion);
            $(".network .network-node-neighbours").html(data.neighbors);
            var table_notifications = '';
            for (i = 0; i < data.notifications.length; i++) {
                table_notifications += '<tr>';
                table_notifications += '<td>' + jeedom.openzwave.timestampConverter(data.notifications[i].timestamp) + '</td>';
                table_notifications += '<td>' + data.notifications[i].details + '</td>';
                if (data.notifications[i].error_description != null && data.notifications[i].error_description != 'None.') {
                    table_notifications += '<td>' + data.notifications[i].error_description + '</td>';
                }else {
                    table_notifications += '<td></td>';
                }
                table_notifications += '</tr>';
            }
            $(".network .notification_variables").html(table_notifications);
            var disabledCommand = data.state < 5 || outgoingSendQueue > 0;
            $("#addDevice").prop("disabled", disabledCommand);
            $("#addDeviceSecure").prop("disabled", disabledCommand);
            $("#removeDevice").prop("disabled", disabledCommand);
            $("#cancelCommand").prop("disabled", data.mode == 0);
            $("#testNetwork").prop("disabled", disabledCommand);
            $("#healNetwork").prop("disabled", disabledCommand);
            $("#healNetwork2").prop("disabled", disabledCommand);
            $("#requestNodeNeighboursUpdate").prop("disabled", disabledCommand);
            $("#createNewPrimary").prop("disabled", disabledCommand);
            $("#replicationSend").prop("disabled", disabledCommand);
            $("#requestNetworkUpdate").prop("disabled", disabledCommand);
            $("#transferPrimaryRole").prop("disabled", disabledCommand);
            $("#receiveConfiguration").prop("disabled", disabledCommand);
            $("#writeConfigFile").prop("disabled", data.state < 5);
            $("#regenerateNodesCfgFile").prop("disabled", data.state < 5 || data.mode != 0);
            $("#softReset").prop("disabled", data.state < 5 || data.mode != 0);
            $("#hardReset").prop("disabled", data.state < 5 || data.mode != 0);

            if($('#div_templateNetwork').html() != undefined && $('#div_templateNetwork').is(':visible')){
                setTimeout(function(){ network_load_info(); }, 2000);
            }
        }
    });
}

function getRoutesCount(nodeId) {
    var routesCount = {};
    $.each(getFarNeighbours(nodeId), function (index, nnode) {
        if (nnode.nodeId in routesCount) {
            if (nnode.hops in routesCount[nnode.nodeId]){
                routesCount[nnode.nodeId][nnode.hops]++;
            } else{
                routesCount[nnode.nodeId][nnode.hops] = 1;
            }
        } else {
            routesCount[nnode.nodeId] = new Array();
            routesCount[nnode.nodeId][nnode.hops] = 1;
        }
    });
    return routesCount;
}

function getFarNeighbours(nodeId, exludeNodeIds, hops) {
    if (hops === undefined) {
        var hops = 0;
        var exludeNodeIds = [nodeId];
    }
    if (hops > 2) 
        return [];
    var nodesList = [];
    $.each(devicesRouting[nodeId].data.neighbours.value, function (index, nnodeId) {
        if (!(nnodeId in devicesRouting)){
            return; 
        }
        if (!in_array(nnodeId, exludeNodeIds)) {
            nodesList.push({nodeId: nnodeId, hops: hops});
            if (devicesRouting[nnodeId].data.isListening.value && devicesRouting[nnodeId].data.isRouting.value){
                $.merge(nodesList, getFarNeighbours(nnodeId, $.merge([nnodeId], exludeNodeIds), hops + 1));
            }
        }
    });
    return nodesList;
}



network_load_data();
network_load_info();
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
  if($(this).data('action') == 'hardReset' || $(this).data('action') == 'softReset'){
    $action = $(this).data('action');
    bootbox.confirm("Etes-vous sûr ? Cette opération est risquée", function (result) {
      if (result) {
        jeedom.openzwave.controller.action({
          action : $action,
          error: function (error) {
            $('#div_networkOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
          },
          success: function () {
            $('#div_networkOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
          }
        });
      }
    });
  }else{
    jeedom.openzwave.controller.action({
      action : $(this).data('action'),
      error: function (error) {
        $('#div_networkOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
      },
      success: function () {
        $('#div_networkOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
      }
    });
  }
});

$("#tab_graph").off("click").on("click", function () {
  network_load_data();
});

$("#tab_route").off("click").on("click", function () {
  jeedom.openzwave.network.info({
    info : 'getNeighbours',
    error: function (error) {
      $('#div_networkOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
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
          routingTable += '  <i class="fas fa-exclamation-triangle fa-lg" style="color:red; text-align:right"  title="{{Présumé mort}}"></i>';
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
          } else if ($.inArray(parseInt(nnodeId, 10), node.data.neighbours.value) != -1){
            rtClass = 'node-direct-link-color';
          }else if (routesCount[nnodeId] && routesCount[nnodeId][1] > 1){
            rtClass = 'node-remote-control-color';
          }else if (routesCount[nnodeId] && routesCount[nnodeId][1] == 1){
            rtClass = 'node-more-of-one-up-color';
          }else{
            rtClass = 'node-more-of-two-up-color';
          }
          routingTable += '<td class=' + rtClass + ' style="width: 35px"><i class="fa fa-square fa-2x" title="' + routeHops + '"></i></td>';
        });
        routingTable += '</td><td><button type="button" id="requestNodeNeighboursUpdate" data-nodeid="' + nodeId + '" class="btn btn-xs btn-primary requestNodeNeighboursUpdate" title="{{Mise à jour des noeuds voisins}}"><i class="fas fa-sync-alt"></i></button></td></tr>';
      });
      $('#div_routingTable').html('<table class="table table-bordered table-condensed"><thead><tr><th>{{Nom}}</th><th>ID</th>' + routingTableHeader + '<th><button type="button" id="healNetwork2" class="btn btn-xs btn-success healNetwork2" title="{{Soigner le réseau}}"><i class="fas fa-medkit"></i></button></th></tr></thead><tbody>' + routingTable + '</tbody></table>');
    }
  });
});

$(".bt_addDevice").off("click").on("click", function () {
  jeedom.openzwave.controller.addNodeToNetwork({
    secure : $(this).data('secure'),
    dataType: 'json',
    error: function (error) {
      $('#div_networkOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
    },
    success: function (data) {
      $('#div_networkOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
    }
  });
});

$("#removeDevice").off("click").on("click", function () {
  jeedom.openzwave.controller.removeNodeFromNetwork({
    error: function (error) {
      $('#div_networkOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
    },
    success: function (data) {
      $('#div_networkOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
    }
  });
});

$("#replicationSend").off("click").on("click", function () {
  return;
  jeedom.openzwave.controller.replicationSend({
    bridge_controller_id : bridge_controller_id,
    error: function (error) {
      $('#div_networkOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
    },
    success: function (data) {
      $('#div_networkOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
    }
  });
});

$("#regenerateNodesCfgFile").off("click").on("click", function () {
  bootbox.confirm("Etes-vous sûr ? Cela va redémarrer votre réseau", function (result) {
    if (result) {
      jeedom.openzwave.network.action({
        action:'removeUnknownsDevicesZWConfig',
        error: function (error) {
          $('#div_networkOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
        },
        success: function (data) {
          $('#div_networkOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
        }
      });
    }
  });
});
$("body").off("click", ".requestNodeNeighboursUpdate").on("click", ".requestNodeNeighboursUpdate", function (e) {
  jeedom.openzwave.node.action({
    action : 'requestNodeNeighbourUpdate',
    node_id : $(this).attr('data-nodeid'),
    error: function (error) {
      $('#div_networkOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
    },
    success: function (data) {
      $('#div_networkOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
      network_load_info();
      network_load_data();
    }
  });
});

function network_load_data(){
  $('#graph_network svg').remove();
  jeedom.openzwave.network.info({
    info:'getNeighbours',
    error: function (error) {
      $('#div_networkOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
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
      $('#graph_network svg').remove();
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
    error: function (error) {
      $('#div_networkOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
      if($('#div_templateNetwork').html() != undefined && $('#div_templateNetwork').is(':visible')){
        setTimeout(function(){
          network_load_data();
          network_load_info();
        }, 2000);
      }
    },
    success: function (data) {
      data.startTime = jeedom.openzwave.timestampConverter(data.startTime);
      data.pollInterval = jeedom.openzwave.durationConvert(parseInt(data.pollInterval, 0) / 1000);
      data.awakedDelay = (data.awakedDelay != null) ?  'opérationnel en ' + data.awakedDelay + ' secondes':'';
      switch (data.state) {
        case 0:
        data.state = "<i class='fa fa-exclamation-circle rediconcolor'></i>";
        break;
        case 1:
        data.state = "<i class='fa fa-exclamation-circle rediconcolor'></i>";
        break;
        case 3:
        data.state = "<i class='fa fa-exclamation-circle rediconcolor'></i>";
        break;
        case 5:
        data.state = "<i class='fa fa-circle yellowiconcolor'></i>";
        break;
        case 7:
        data.state = "<i class='fa fa-bullseye greeniconcolor'></i>";
        break;
        case 10:
        data.state = "<i class='fa fa-circle greeniconcolor'></i>";
        break;
      }
      data.node_capabilities = '';
      if (data.controllerNodeCapabilities.indexOf('primaryController') != -1) {
        data.node_capabilities += '<li>{{Contrôleur Primaire}}</li>'
      }
      if (data.controllerNodeCapabilities.indexOf('staticUpdateController') != -1) {
        data.node_capabilities += '<li>{{Contrôleur statique de mise à jour (SUC)}}</li>'
      }
      if (data.controllerNodeCapabilities.indexOf('bridgeController') != -1) {
        data.node_capabilities += '<li>{{Contrôleur secondaire}}</li>'
      }
      if (data.controllerNodeCapabilities.indexOf('listening') != -1) {
        data.node_capabilities += '<li>{{Le noeud est alimenté et écoute en permanence}}</li>'
      }
      if (data.controllerNodeCapabilities.indexOf('beaming') != -1) {
        data.node_capabilities += '<li>{{Le noeud est capable d\'envoyer une trame réseaux}}</li>';
      }
      data.outgoingSendQueue = parseInt(data.outgoingSendQueue, 0);
      if (data.outgoingSendQueue == 0) {
        data.outgoingSendQueueDescription = "<i class='fa fa-circle fa-lg greeniconcolor'></i>";
      }else if (data.outgoingSendQueue <= 5) {
        data.outgoingSendQueueDescription = "<i class='fa fa-spinner fa-spin fa-lg greeniconcolor'></i>";
      }else if (data.outgoingSendQueue <= 15) {
        data.outgoingSendQueueDescription = "<i class='fa fa-spinner fa-spin fa-lg yellowiconcolor'></i>";
      }else {
        data.outgoingSendQueueDescription = "<i class='fa fa-spinner fa-spin fa-lg rediconcolor'></i>";
      }
      $('#div_templateNetwork').setValues(data, '.zwaveNetworkAttr');
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

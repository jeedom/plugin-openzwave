
var app_network = {
    // note variable nodes is global!

    updater: false,
    
    timestampConverter :function(time){
    	if(time==1)
       return "N/A";
     var ret;
     var date = new Date(time*1000);
     var hours = date.getHours();
     if(hours<10){
       hours="0"+hours;
     }
     var minutes = date.getMinutes();
     if(minutes<10){
       minutes="0"+minutes;
     }
     var seconds = date.getSeconds();
     if(seconds<10){
       seconds="0"+seconds;
     }
     var num = date.getDate();
     if(num<10){
       num="0"+num;
     }
     var month = date.getMonth()+1;
     if(month<10){
       month="0"+month;
     }
     var year = date.getFullYear();
     var formattedTime = hours + ':' + minutes + ':' + seconds;
     var formattedDate = num + "/" + month + "/" + year;
     return formattedDate+' '+formattedTime;
   },
   init: function(){
     app_network.load_infos();
     app_network.updater = setInterval(function(){ 
      if($('#div_templateNetwork').is(':visible')){
        app_network.load_infos();
      }else{
        app_network.hide();   
      }
    }, 2000);

     $("#confirm_reset").off("click").on("click",function() {
      var text=$("#confirm_text").val();
      if(text=="YES"){
       app_network.hardReset();
       $('#confirmModal').modal('hide');
     }else{
       alert('You haven\'t confirmed with YES'); 
     }
   });
     $("#tab_graph").off("click").on("click",function() {
      app_network.load_data();
    });
     $("#tab_route").off("click").on("click",function() {
      app_network.displayRoutingTable()
    });
     $("#addDevice").off("click").on("click",function() {
      app_network.addDevice();
    });
     $("#removeDevice").off("click").on("click",function() {
      app_network.removeDevice();
    });
     $("#cancelCommand").off("click").on("click",function() {
      app_network.cancelCommand();
    });
     $("#testNetwork").off("click").on("click",function() {
      app_network.testNetwork();
    });
     $("#healNetwork").off("click").on("click",function() {
      app_network.healNetwork();
    });
     $("#createNewPrimary").off("click").on("click",function() {
      app_network.createNewPrimary();
    });
     $("#replicationSend").off("click").on("click",function() {
      app_network.replicationSend();
    });
     $("#requestNetworkUpdate").off("click").on("click",function() {
      app_network.requestNetworkUpdate();
    });
     $("#transferPrimaryRole").off("click").on("click",function() {
      app_network.transferPrimaryRole();
    });
     $("#writeconfigfile").off("click").on("click",function() {
      app_network.writeConfigFile();
    });
     $("#softReset").off("click").on("click",function() {
      app_network.softReset();
    });
     $("#hardReset").off("click").on("click",function() {
      $('#confirmModal').modal('show');
    });
    $("body").off("click",".requestNodeNeighboursUpdate").on("click",".requestNodeNeighboursUpdate",function (e) {
	var nodeid = $(this).attr('data-nodeid');
	app_network.request_node_neighbours_update(nodeid);
	});


   },
   addDevice: function(){
    $.ajax({ 
      url: path+"ZWaveAPI/Run/controller.AddNodeToNetwork(1)", 
      dataType: 'json',
      async: true, 
      error: function (request, status, error) {
        handleAjaxError(request, status, error,$('#div_networkOpenzwaveAlert'));
      },
      success: function(data) {
        if(data['result']== true){
          app_network.sendOk();
        }else{
          $('#div_networkOpenzwaveAlert').showAlert({message: '{{Echec !}}', level: 'danger'});
        }
      }
    });
  },
  removeDevice: function(){
    $.ajax({ 
      url: path+"ZWaveAPI/Run/controller.RemoveNodeFromNetwork(1)", 
      dataType: 'json',
      async: true, 
      error: function (request, status, error) {
        handleAjaxError(request, status, error,$('#div_networkOpenzwaveAlert'));
      },
      success: function(data) {
        if(data['result']== true){
          app_network.sendOk();
        }else{
         $('#div_networkOpenzwaveAlert').showAlert({message: '{{Echec !}}', level: 'danger'});
       }
     }
   });
  },
  cancelCommand: function(){
    $.ajax({ 
      url: path+"ZWaveAPI/Run/CancelCommand()", 
      dataType: 'json',
      async: true, 
      error: function (request, status, error) {
        handleAjaxError(request, status, error,$('#div_networkOpenzwaveAlert'));
      },
      success: function(data) {
        if(data['result']== true){
          app_network.sendOk();
        }else{
         $('#div_networkOpenzwaveAlert').showAlert({message: '{{Echec !}}', level: 'danger'});
       }
     }
   });
  },
  testNetwork: function(){
    $.ajax({ 
      url: path+"ZWaveAPI/Run/devices[0].TestNetwork()", 
      dataType: 'json',
      async: true, 
      error: function (request, status, error) {
        handleAjaxError(request, status, error,$('#div_networkOpenzwaveAlert'));
      },
      success: function(data) {
        if(data['result']== true){
          app_network.sendOk();
        }else{
         $('#div_networkOpenzwaveAlert').showAlert({message: '{{Echec !}}', level: 'danger'});
       }
     }
   });
  },
  healNetwork: function(){
    $.ajax({ 
      url: path+"ZWaveAPI/Run/controller.HealNetwork()", 
      dataType: 'json',
      async: true, 
      error: function (request, status, error) {
        handleAjaxError(request, status, error,$('#div_networkOpenzwaveAlert'));
      },
      success: function(data) {
        if(data['result']== true){
          app_network.sendOk();
        }else{
         $('#div_networkOpenzwaveAlert').showAlert({message: '{{Echec !}}', level: 'danger'});
       }
     }
   });
  },
  createNewPrimary: function(){
    $.ajax({ 
      url: path+"ZWaveAPI/Run/CreateNewPrimary()", 
      dataType: 'json',
      async: true, 
      error: function (request, status, error) {
        handleAjaxError(request, status, error,$('#div_networkOpenzwaveAlert'));
      },
      success: function(data) {
        app_network.sendOk();
      }
    });
  },
  replicationSend: function(){
    $.ajax({ 
      url: path+"ZWaveAPI/Run/ReplicationSend()", 
      dataType: 'json',
      async: true, 
      error: function (request, status, error) {
        handleAjaxError(request, status, error,$('#div_networkOpenzwaveAlert'));
      },
      success: function(data) {
       app_network.sendOk();
     }
   });
  },
  requestNetworkUpdate: function(){
    $.ajax({ 
      url: path+"ZWaveAPI/Run/controller.RequestNetworkUpdate()", 
      dataType: 'json',
      async: true, 
      error: function (request, status, error) {
        handleAjaxError(request, status, error,$('#div_networkOpenzwaveAlert'));
      },
      success: function(data) {
        if(data['result']== true){
          app_network.sendOk();
        }else{
         $('#div_networkOpenzwaveAlert').showAlert({message: '{{Echec !}}', level: 'danger'});
       }
     }
   });
  },
  transferPrimaryRole: function(){
    $.ajax({ 
      url: path+"ZWaveAPI/Run/TransferPrimaryRole()", 
      dataType: 'json',
      async: true, 
      error: function (request, status, error) {
        handleAjaxError(request, status, error,$('#div_networkOpenzwaveAlert'));
      },
      success: function(data) {
        app_network.sendOk();
      }
    });
  },
  writeConfigFile: function(){
    $.ajax({ 
      url: path+"ZWaveAPI/Run/WriteZWConfig()", 
      dataType: 'json',
      async: true, 
      error: function (request, status, error) {
        handleAjaxError(request, status, error,$('#div_networkOpenzwaveAlert'));
      },
      success: function(data) {
        app_network.sendOk();
      }
    });
  },
  softReset: function(){
    $.ajax({ 
      url: path+"/ZWaveAPI/Run/SerialAPISoftReset()", 
      dataType: 'json',
      async: true, 
      error: function (request, status, error) {
        handleAjaxError(request, status, error,$('#div_networkOpenzwaveAlert'));
      },
      success: function(data) {
       if(data['result']== true){
        app_network.sendOk();
      }else{
        $('#div_networkOpenzwaveAlert').showAlert({message: '{{Echec !}}', level: 'danger'});
      }
    }
  });
  },
  hardReset: function(){
    	//TODO: add a confirmation yes/no before execute
      $.ajax({ 
        url: path+"ZWaveAPI/Run/HardReset()", 
        dataType: 'json',
        async: true, 
        error: function (request, status, error) {
          handleAjaxError(request, status, error,$('#div_networkOpenzwaveAlert'));
        },
        success: function(data) {
         if(data['result']== true){
          app_network.sendOk();
        }else{
         $('#div_networkOpenzwaveAlert').showAlert({message: '{{Echec !}}', level: 'danger'});
       }
     }
   });
    },
    request_node_neighbours_update: function(node_id){
		$.ajax({ 
			url: path+"ZWaveAPI/Run/devices["+node_id+"].RequestNodeNeighbourUpdate()", 
			dataType: 'json',
			async: true, 
			error: function (request, status, error) {
				handleAjaxError(request, status, error,$('#div_networkOpenzwaveAlert'));
			},
			success: function(data) {
				if(data['result']== true){
					app_network.sendOk();
					app_network.load_data(); 
				}else{
					$('#div_networkOpenzwaveAlert').showAlert({message: 'Echec !', level: 'danger'});
				}
			}
		});
	},
    load_data: function(){
      $('#graph_network').html('<div id="graph-node-name"></div>');
      $.ajax({ 
        url: path+"ZWaveAPI/Data/0", 
        dataType: 'json',
        async: true, 
        error: function (request, status, error) {
          handleAjaxError(request, status, error,$('#div_networkOpenzwaveAlert'));
        },
        success: function(data) {
            //console.log('chargement ok');
            nodes = data['devices'];
                // auto select first node
                var graph = Viva.Graph.graph();

                for (z in nodes){
				//console.log('add node '+z);
       if(nodes[z].data.name.value != ''){
        graph.addNode(z,{'name':'<span class="label label-primary">'+nodes[z].data.location.value+'</span> '+nodes[z].data.name.value});
      }else{
        graph.addNode(z,{'name':nodes[z].data.product_name.value});
      }

      for (neighbour in nodes[z].data.neighbours.value){
		        	//console.log('add link '+neighbour);
              if(typeof nodes[neighbour] != 'undefined'){
               graph.addLink(z, neighbour);
             }
           }
         }

         var graphics = Viva.Graph.View.svgGraphics(),
         nodeSize = 24,
                // we use this method to highlight all realted links
                // when user hovers mouse over a node:
                highlightRelatedNodes = function(nodeId, isOn) {
                   // just enumerate all realted nodes and update link color:
                   graph.forEachLinkedNode(nodeId, function(node, link){
                     var linkUI = graphics.getLinkUI(link.id);
                     if (linkUI) {
                           // linkUI is a UI object created by graphics below
                           linkUI.attr('stroke', isOn ? 'red' : 'gray');
                         }
                       });
                 };
            // Since we are using SVG we can easily subscribe to any supported
            // events (http://www.w3.org/TR/SVG/interact.html#SVGEvents ),
            // including mouse events:
            graphics.node(function(node) {
              // This time it's a group of elements: http://www.w3.org/TR/SVG/struct.html#Groups
              if(typeof node.data == 'undefined'){
              	graph.removeNode(node.id);
              	//break;
              }

              var ui = Viva.Graph.svg('g'),
              
                  // Create SVG text element with user id as content
                  svgText = Viva.Graph.svg('text').attr('y', '0px').text(node.id),
                  img = Viva.Graph.svg('rect')
                  .attr("width", 10)
                  .attr("height", 10)
                  .attr("fill", "#00a2e8");
                  ui.append(svgText);
                  ui.append(img);
              $(ui).hover(function() { // mouse over
                $('#graph-node-name').html(node.data.name);
                highlightRelatedNodes(node.id, true);
                }, function() { // mouse out
                  highlightRelatedNodes(node.id, false);
                });
              return ui;
            }).placeNode(function(nodeUI, pos) {
                // 'g' element doesn't have convenient (x,y) attributes, instead
                // we have to deal with transforms: http://www.w3.org/TR/SVG/coords.html#SVGGlobalTransformAttribute
                nodeUI.attr('transform',
                  'translate(' +
                    (pos.x - nodeSize/2) + ',' + (pos.y - nodeSize/2) +
                    ')');
              });
            var middle = graph.getNode(1);
            if(typeof middle !== 'undefined'){
              middle.isPinned = true;
            }
            var layout = Viva.Graph.Layout.forceDirected(graph, {
             stableThreshold: 0.9,
             dragCoeff : 0.01,
             springCoeff : 0.0004,
             gravity : -1.5,
             springLength : 150
           });
            var renderer = Viva.Graph.View.renderer(graph, {
              layout: layout,
              graphics : graphics,
              container : document.getElementById('graph_network')
            });
            renderer.run();
            setTimeout(function(){ renderer.pause();renderer.reset(); }, 500);


          }
        });
},
load_stats: function(node_id){
  $.ajax({ 
    url: path+"ZWaveAPI/Data/0", 
    dataType: 'json',
    async: true, 
    error: function (request, status, error) {
      handleAjaxError(request, status, error,$('#div_networkOpenzwaveAlert'));
    },
    success: function(data) {            
     app_nodes.show_stats();               
   }
 });
},

show_stats: function (){
 var network = $(".network");
 network.find(".stats_ACKCnt").html(infos.controllerStatistics.ACKCnt);
 network.find(".stats_ACKWaiting").html(infos.controllerStatistics.ACKWaiting);
 network.find(".stats_CANCnt").html(infos.controllerStatistics.CANCnt);
 network.find(".stats_NAKCnt").html(infos.controllerStatistics.NAKCnt);
 network.find(".stats_OOFCnt").html(infos.controllerStatistics.OOFCnt);
 network.find(".stats_SOFCnt").html(infos.controllerStatistics.SOFCnt);
 network.find(".stats_badChecksum").html(infos.controllerStatistics.badChecksum);
 network.find(".stats_badroutes").html(infos.controllerStatistics.badroutes);
 network.find(".stats_broadcastReadCnt").html(infos.controllerStatistics.broadcastReadCnt);
 network.find(".stats_broadcastWriteCnt").html(infos.controllerStatistics.broadcastWriteCnt);
 network.find(".stats_callbacks").html(infos.controllerStatistics.callbacks);
 network.find(".stats_dropped").html(infos.controllerStatistics.dropped);
 network.find(".stats_netbusy").html(infos.controllerStatistics.netbusy);		
 network.find(".stats_noack").html(infos.controllerStatistics.noack);
 network.find(".stats_nondelivery").html(infos.controllerStatistics.nondelivery);
 network.find(".stats_readAborts").html(infos.controllerStatistics.readAborts);
 network.find(".stats_readCnt").html(infos.controllerStatistics.readCnt);
 network.find(".stats_retries").html(infos.controllerStatistics.retries);
 network.find(".stats_routedbusy").html(infos.controllerStatistics.routedbusy);
 network.find(".stats_writeCnt").html(infos.controllerStatistics.writeCnt);
},

hide: function(){
  clearInterval(app_network.updater);
},
load_infos: function(){
  $.ajax({ 
    url: path+"ZWaveAPI/Run/network_status()", 
    dataType: 'json',
    async: true, 
    global : false,
    error: function (request, status, error) {
      handleAjaxError(request, status, error,$('#div_networkOpenzwaveAlert'));
    },
    success: function(data) {
      infos = data;
      app_network.show_infos();
      app_network.show_stats();
    }
  });
},
show_infos: function (){
  var network = $(".network");		
  network.find(".network-startTime").html(app_network.timestampConverter(infos.startTime));    
        network.find(".network-nodes-count").html(infos.nodesCount);              // set the nodeid
        network.find(".network-sleeping-nodes-count").html(infos.sleepingNodesCount);
        network.find(".network-scenes-count").html(infos.scenesCount);
        
        var pollInterval = parseInt(infos.pollInterval,0)/1000;
        
        network.find(".network-poll-interval").html(pollInterval);
        network.find(".network-isready").html(infos.isReady);
        network.find(".network-state-description").html(infos.stateDescription);
        var stateled = "";        
        switch(infos.state)
        {
          case 0:{
        	//STATE_STOPPED
        	stateled = "<i class='fa fa-exclamation-circle rediconcolor'></i>" ;
        	break;
        }
        case 1:{
        	//STATE_FAILED        	
        	stateled = "<i class='fa fa-exclamation-circle rediconcolor'></i>" ;        
        	break;
        }
        case 3:{
        	//STATE_RESETTED        	
        	stateled = "<i class='fa fa-exclamation-circle rediconcolor'></i>" ;
        	break;
        }
        case 5:{
        	//STATE_STARTED
        	stateled = "<i class='fa fa-circle yellowiconcolor'></i>" ;
        	break;
        }
        case 7:{
        	//STATE_AWAKED
        	stateled = "<i class='fa fa-bullseye greeniconcolor'></i>" ;
        	break;
        }
        case 10:{
        	//STATE_READY       
        	stateled = "<i class='fa fa-circle greeniconcolor'></i>" ;
        	break;
        }
      }
      network.find(".network-state-led").html(stateled);
      network.find(".network-controller-capabilities").html(infos.controllerCapabilities);
      network.find(".network-controller-node-capabilities").html(infos.controllerNodeCapabilities);
      var outgoingSendQueue = parseInt(infos.outgoingSendQueue,0);
      var outgoingSendQueueWarning = "";
      if(outgoingSendQueue<=5){
       outgoingSendQueueDescription = "<i class='fa fa-circle greeniconcolor'></i>" ;
     }
     else if(outgoingSendQueue<=15){        	
       outgoingSendQueueDescription = "<i class='fa fa-circle yellowiconcolor'></i>" ;
     }
     else{
       outgoingSendQueueDescription = "<i class='fa fa-exclamation-circle rediconcolor'></i>" ;
     }
     network.find(".network-outgoing-send-queue").html(outgoingSendQueue);
     network.find(".network-outgoing-send-queueWarning").html(outgoingSendQueueDescription);        

     network.find(".network-controller-stats").html(infos.controllerStatistics);
     network.find(".network-device-path").html(infos.devicePath);
     network.find(".network-oz-library-version").html(infos.OpenZwaveLibraryVersion);
     network.find(".network-poz-library-version").html(infos.PythonOpenZwaveLibraryVersion);
     network.find(".network-node-neighbours").html(infos.neighbors);

     network.find(".network-notification").html(infos.notification.state);
     network.find(".network-notificationMessage").html(infos.notification.details);
     network.find(".network-notificationTime").html(app_network.timestampConverter(infos.notification.timestamp));

     var disabledCommand = infos.state<5;

     $("#addDevice").prop("disabled",disabledCommand);
     $("#removeDevice").prop("disabled",disabledCommand);
     $("#cancelCommand").prop("disabled",disabledCommand);
     $("#testNetwork").prop("disabled",disabledCommand);
     $("#healNetwork").prop("disabled",disabledCommand);
     $("#createNewPrimary").prop("disabled",disabledCommand);
     $("#replicationSend").prop("disabled",disabledCommand);
     $("#requestNetworkUpdate").prop("disabled",disabledCommand);
     $("#transferPrimaryRole").prop("disabled",disabledCommand);
     $("#writeConfigFile").prop("disabled",disabledCommand);
     $("#softReset").prop("disabled",disabledCommand);
     $("#hardReset").prop("disabled",disabledCommand);


   },
   update: function (){
    app_nodes.draw_nodes();
  },
  sendOk : function(){
    $('#li_state').show();
    setTimeout(function(){ $('#li_state').hide(); }, 3000);
  },
  show: function (){
    app_network.load_infos();
  },
  getRoutesCount: function (nodeId){
   var routesCount = {};
   $.each(app_network.getFarNeighbours(nodeId), function (index, nnode) {
    if (nnode.nodeId in routesCount) {
      if (nnode.hops in routesCount[nnode.nodeId])
        routesCount[nnode.nodeId][nnode.hops]++;
      else
        routesCount[nnode.nodeId][nnode.hops] = 1;
    } else {
      routesCount[nnode.nodeId] = new Array();
      routesCount[nnode.nodeId][nnode.hops] = 1;
    }
  });
   return routesCount;
 },
 getFarNeighbours: function (nodeId, exludeNodeIds, hops){
  if (hops === undefined) {
    console.log('je passe');
    var hops = 0;
    var exludeNodeIds = [nodeId];
  }
        if (hops > 2) // Z-Wave allows only 4 routers, but we are interested in only 2, since network becomes unstable if more that 2 routers are used in communications
          return [];
        var nodesList = [];
        $.each(devicesRouting[nodeId].data.neighbours.value, function (index, nnodeId) {
          if (!(nnodeId in devicesRouting))
                return; // skip deviced reported in routing table but absent in reality. This may happen after restore of routing table.
              if (!in_array(nnodeId, exludeNodeIds)) {
                nodesList.push({nodeId: nnodeId, hops: hops});
                if (devicesRouting[nnodeId].data.isListening.value && devicesRouting[nnodeId].data.isRouting.value)
                  $.merge(nodesList, app_network.getFarNeighbours(nnodeId, $.merge([nnodeId], exludeNodeIds) /* this will not alter exludeNodeIds */, hops + 1));
              }
            });
        return nodesList;
      },
      displayRoutingTable: function (){
    $.ajax({// fonction permettant de faire de l'ajax
     url: path+"ZWaveAPI/Data/0", 
     dataType: 'json',
     async: true, 
     error: function (request, status, error) {
      handleAjaxError(request, status, error, $('#div_networkOpenzwaveAlert'));
    },
        success: function (data) { // si l'appel a bien fonctionné
        devicesRouting = data.devices;
            var skipPortableAndVirtual = true; // to minimize routing table by removing not interesting lines
            var routingTable = '';
            var routingTableHeader = '';
            $.each(devicesRouting, function (nodeId, node) {
              if (nodeId == 255){
                return;
              }
              if (skipPortableAndVirtual && (node.data.isVirtual.value || node.data.basicType.value == 1)){
                return;
              }
              var routesCount = app_network.getRoutesCount(nodeId);
              routingTableHeader += '<th>' + nodeId + '</th>';
              var name = node.data.product_name.value
              if(node.data.name.value != ''){
                var name = node.data.location.value+' - '+node.data.name.value
              }
              routingTable += '<tr><td>' + name + '</td><td>' + nodeId + '</td>';
              $.each(devicesRouting, function (nnodeId, nnode) {
                if (nnodeId == 255)
                  return;
                if (skipPortableAndVirtual && (nnode.data.isVirtual.value || nnode.data.basicType.value == 1))
                  return;
                var rtClass;
                if (!routesCount[nnodeId])
                        routesCount[nnodeId] = new Array(); // create empty array to let next line work
                      var routeHops = (routesCount[nnodeId][0] || '0')+"/";
                      routeHops += (routesCount[nnodeId][1] || '0')+"/";
                      routeHops += (routesCount[nnodeId][2] || '0');
                      if (nodeId == nnodeId || node.data.isVirtual.value || nnode.data.isVirtual.value || node.data.basicType.value == 1 || nnode.data.basicType.value == 1) {
                        rtClass = 'rtUnavailable';
                        routeHops = '';
                      } else if ($.inArray(parseInt(nnodeId, 10), node.data.neighbours.value) != -1)
                      rtClass = 'success';
                      else if (routesCount[nnodeId] && routesCount[nnodeId][1] > 1)
                        rtClass = 'active';
                      else if (routesCount[nnodeId] && routesCount[nnodeId][1] == 1)
                        rtClass = 'warning';
                      else
                        rtClass = 'danger';
                      routingTable += '<td class="' + rtClass + ' tooltips" title="' + routeHops + '"></td>';
                    });
routingTable += '</td><td><button type="button" id="requestNodeNeighboursUpdate" data-nodeid="'+nodeId+'" class="btn btn-xs btn-primary requestNodeNeighboursUpdate tooltips" title="{{Mise à jour des noeuds voisins}}"><i class="fa fa-sitemap"></i></button></td></tr>';
});
$('#div_routingTable').html('<table class="table table-bordered table-condensed"><thead><tr><th>{{Nom}}</th><th>ID</th>' + routingTableHeader + '<th>{{}}</th></tr></thead><tbody>' + routingTable + '</tbody></table>');
initTooltips();
}
});

}
}

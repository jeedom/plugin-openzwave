
var app_network = {
    // note variable nodes is global!

    updater: false,
    console_updater: false,
    durationConvert: function(d) {
      d = Number(d);
      var h = Math.floor(d / 3600);
      var m = Math.floor(d % 3600 / 60);
      var s = Math.floor(d % 3600 % 60);
      return ((h > 0 ? h + " heure(s) " + (m < 10 ? "0" : "") : "") + m + " minute(s) " + (s < 10 ? "0" : "") + s) + ' seconde(s)'; 
    },
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
     $("#saveconf").click(function(){
      $.ajax({ 
        type:'POST', 
        url: path+"ZWaveAPI/Run/network.SaveZWConfig()", 
        contentType: "text/plain", 
        data: $("#zwcfgfile").val(),
        error: function (request, status, error) {
          handleAjaxError(request, status, error,$('#div_networkOpenzwaveAlert'));
        },
        success: function(data) {
          $('#div_networkOpenzwaveAlert').showAlert({message: '{{Sauvegarde réussie}}', level: 'success'});
        }
      });
    });
     $("#tab_config").off("click").on("click",function() {
      $.ajax({ 
        url: path+"ZWaveAPI/Run/network.GetZWConfig()", 
        dataType: 'json', 
        error: function (request, status, error) {
          handleAjaxError(request, status, error,$('#div_configOpenzwaveAlert'));
        },
        success: function(data){
          $("#zwcfgfile").val(data['result']);
        }
      });
    });
     $("#stopLiveLog").off("click").on("click",function() {
      clearInterval(app_network.console_updater);
      $("#stopLiveLog").hide();
      $("#startLiveLog").show();
    });
     $("#startLiveLog").off("click").on("click",function() {
      app_network.console_updater = setInterval(app_network.console_refresh,2000);
      $("#startLiveLog").hide();
      $("#stopLiveLog").show();
    });
     $(".console-out").html("");
     $("#tab_console").off("click").on("click",function() {
      $("#startLiveLog").hide();
      app_network.console_updater = setInterval(app_network.console_refresh,2000);
    });
     $("#tab_graph").off("click").on("click",function() {
      app_network.load_data();
    });
     $("#tab_route").off("click").on("click",function() {
      app_network.displayRoutingTable()
    });
     $("#addDevice").off("click").on("click",function() {
      app_network.addDevice(false);
    });
     $("#addDeviceSecure").off("click").on("click",function() {
      app_network.addDevice(true);
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
     $("#receiveConfiguration").off("click").on("click",function() {
       app_network.receiveConfiguration();
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
     $("#regenerateNodesCfgFile").off("click").on("click",function() {
      bootbox.confirm("Etes-vous sûr ? Cela va redémarrer votre réseau", function(result) {
        if(result){
         app_network.regenerate_nodes_cfg_file();
       }
     }); 
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
   console_refresh: function(){
    if(!$('#log').is(':visible')){
      clearInterval(app_network.console_updater);
    }
    $.ajax({ 
      url: path+"ZWaveAPI/Run/network.GetOZLogs()", 
      dataType: 'json',
      async: true, 
      global : false,
      error: function (request, status, error) {
        handleAjaxError(request, status, error,$('#div_networkOpenzwaveAlert'));
      },
      success: function(data) {
        if (!$(".console-out").is(':visible')) {
          clearInterval(app_console.updater);
          return;
        }
        if(data['result']){
         $(".console-out").html(data['result']);
         var h = parseInt($('#log')[0].scrollHeight);
         $('#log').scrollTop(h);
       }else{
        $(".console-out").append("error...");
      }
    }
  });
  },
  addDevice: function(_secure){
    var secure = 0;
    if(_secure){
     var secure = 1;
   }
   $.ajax({ 
    url: path+"ZWaveAPI/Run/controller.AddNodeToNetwork(1,"+secure+")", 
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
    url: path+"ZWaveAPI/Run/controller.CancelCommand()", 
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
    url: path+"ZWaveAPI/Run/controller.TestNetwork()", 
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
    url: path+"ZWaveAPI/Run/controller.CreateNewPrimary()", 
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
receiveConfiguration: function(){
 $.ajax({ 
   url: path+"ZWaveAPI/Run/controller.ReceiveConfiguration()", 
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
  //TODO: add bridController selection and pass as argument 
  $.ajax({ 
    url: path+"ZWaveAPI/Run/controller.ReplicationSend(bridge_controller_id)", 
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
  //TODO: add bridController selection and pass as argument 
  $.ajax({ 
    url: path+"ZWaveAPI/Run/controller.RequestNetworkUpdate(bridge_controller_id)", 
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
    url: path+"ZWaveAPI/Run/controller.TransferPrimaryRole()", 
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
    url: path+"ZWaveAPI/Run/network.WriteZWConfig()", 
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
regenerate_nodes_cfg_file: function(){
  $.ajax({ 
    url: path+"ZWaveAPI/Run/network.RemoveUnknownsDevicesZWConfig()", 
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
    url: path+"/ZWaveAPI/Run/controller.SerialAPISoftReset()", 
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
  $.ajax({ 
    url: path+"ZWaveAPI/Run/controller.HardReset()", 
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
     app_network.displayRoutingTable();
   }else{
     $('#div_networkOpenzwaveAlert').showAlert({message: 'Echec !', level: 'danger'});
   }
 }
});
},
load_data: function(){      
  $('#graph_network').html('<div id="graph-node-name"></div>');
  $.ajax({ 
    url: path+"ZWaveAPI/Run/network.GetNeighbours()", 
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
                  graph.addNode(z,{'name':'<span class="label label-primary">'+nodes[z].data.location.value+'</span> '+nodes[z].data.name.value, 'neighbours' : nodes[z].data.neighbours.value, 'generic' : nodes[z].data.neighbours.enabled, 'interview' : parseInt(nodes[z].data.state.value)});
                }else{
                  graph.addNode(z,{'name':nodes[z].data.product_name.value, 'neighbours' : nodes[z].data.neighbours.value, 'generic' : nodes[z].data.neighbours.enabled,'interview' : parseInt(nodes[z].data.state.value)});
                }
                if (nodes[z].data.neighbours.value.length<1 && nodes[z].data.neighbours.enabled !=1){
                  if(typeof nodes[1] != 'undefined'){
                   graph.addLink(z, 1, { isdash: 1, lengthfactor : 0.6 });
                 }
               } else {
                for (neighbour in nodes[z].data.neighbours.value){
                  neighbourid=nodes[z].data.neighbours.value[neighbour];
                  if(typeof nodes[neighbourid] != 'undefined'){
                    graph.addLink(z, neighbourid, { isdash: 0, lengthfactor : 0 });
                  }
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
                           linkUI.attr('stroke', isOn ? '#FF0000' : '#B7B7B7');
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
              nodecolor='#00a2e8';
              if (node.data.generic!=1) {
                nodecolor='#7BCC7B';
              }else if (node.data.neighbours.length < 1 && node.id != 1 && node.data.interview >= 13) {
                nodecolor='#d20606';
              } else if (node.data.neighbours.indexOf(1) == -1 && node.id != 1 && node.data.interview >= 13) {
               nodecolor='#E5E500';
             } else if (node.data.interview < 13) {
               nodecolor='#979797';
             }
             var ui = Viva.Graph.svg('g'),

                  // Create SVG text element with user id as content
                  svgText = Viva.Graph.svg('text').attr('y', '0px').text(node.id),
                  img = Viva.Graph.svg('rect')
                  .attr("width", 10)
                  .attr("height", 10)
                  .attr("fill", nodecolor);
                  ui.append(svgText);
                  ui.append(img);
              $(ui).hover(function() { // mouse over
                var link ='index.php?v=d&p=openzwave&m=openzwave&server_id='+$("#sel_zwaveNetworkServerId").value()+'&logical_id='+node.id;
                numneighbours=node.data.neighbours.length;
                interview=node.data.interview;
                if (numneighbours<1 && interview>= 13){
                  if (node.data.generic != 1) {
                    sentenceneighbours='{{Télécommande}}'
                  } else {
                    sentenceneighbours='{{Pas de voisins}}';
                  }
                } else if (interview>= 13) {
                 sentenceneighbours=numneighbours+ ' {{voisins}} ['+node.data.neighbours+']';
               } else {
                 sentenceneighbours='{{Interview incomplet}}';
               }
               if (node.id != 1){
                linkname='<a href="'+link+'">'+node.data.name+'</a>'
              }else {
               linkname=node.data.name
             }
             $('#graph-node-name').html(linkname + ' : ' + sentenceneighbours);
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
                    (pos.x - nodeSize/3) + ',' + (pos.y - nodeSize/2.5) +
                    ')');
              });
var middle = graph.getNode(1);
if(typeof middle !== 'undefined'){
  middle.isPinned = true;
}
var idealLength = 200;
var layout = Viva.Graph.Layout.forceDirected(graph, {
 springLength: idealLength,
 stableThreshold: 0.9,
 dragCoeff : 0.01,
 springCoeff : 0.0004,
 gravity : -20,
 springTransform: function (link, spring) {
  spring.length = idealLength * (1 - link.data.lengthfactor);
}
});
graphics.link(function(link){
  dashvalue='5, 0';
  if (link.data.isdash== 1){
    dashvalue='5, 2';
  }
  return Viva.Graph.svg('line')
  .attr('stroke', '#B7B7B7')
  .attr('stroke-dasharray', dashvalue)
  .attr('stroke-width', '0.4px');
});
var renderer = Viva.Graph.View.renderer(graph, {
  layout: layout,
  graphics : graphics,
  prerender: 10,
  renderLinks : true,
  container : document.getElementById('graph_network')
});
renderer.run();
setTimeout(function(){ renderer.pause();renderer.reset(); }, 200);
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
  clearInterval(app_network.console_updater);
},
load_infos: function(){
  $.ajax({ 
    url: path+"ZWaveAPI/Run/network.GetStatus()", 
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
        
        var pollInterval = app_network.durationConvert(parseInt(infos.pollInterval,0)/1000);
        
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
    //console.log('je passe');
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
     url: path+"ZWaveAPI/Run/network.GetNeighbours()", 
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
              
              if(node.data.basicType.value != 2){
                var link ='index.php?v=d&p=openzwave&m=openzwave&server_id='+$("#sel_zwaveNetworkServerId").value()+'&logical_id='+nodeId;
              }else{
                var link ='#';
              }
              if(node.data.name.value != ''){
                routingTableHeader += '<th class="tooltips" title="'+node.data.location.value+' '+ node.data.name.value+'" >' + nodeId + '</th>';
                var name = '<span class="nodeConfiguration cursor" data-node-id="'+nodeId+'" data-server-id="'+$("#sel_zwaveNetworkServerId").value()+'"><span class="label label-primary">'+node.data.location.value+'</span> '+node.data.name.value+'</span>';
              }else{
               routingTableHeader += '<th class="tooltips" title="'+node.data.product_name.valuee+'" >' + nodeId + '</th>';
               var name = '<span class="nodeConfiguration cursor" data-node-id="'+nodeId+'" data-server-id="'+$("#sel_zwaveNetworkServerId").value()+'">'+ node.data.product_name.value+'</span>';
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
routingTable += '</td><td><button type="button" id="requestNodeNeighboursUpdate" data-nodeid="'+nodeId+'" class="btn btn-xs btn-primary requestNodeNeighboursUpdate tooltips" title="{{Mise à jour des noeuds voisins}}"><i class="fa fa-refresh"></i></button></td></tr>';
});
$('#div_routingTable').html('<table class="table table-bordered table-condensed"><thead><tr><th>{{Nom}}</th><th>ID</th>' + routingTableHeader + '<th>{{}}</th></tr></thead><tbody>' + routingTable + '</tbody></table>');
initTooltips();
}
});

}
}

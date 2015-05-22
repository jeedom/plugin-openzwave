
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
    init: function()
    {
       app_network.load_infos();
        
		$("#confirm_reset").off("click").on("click",function() {
            var text=$("#confirm_text").val();
            if(text=="YES"){
            	app_network.hardReset();
            	$('#confirmModal').modal('hide');
            }else{
            	alert('You haven\'t confirmed with YES'); 
            }
            //app_network.addDevice();
        });
        $("#tab_graph").off("click").on("click",function() {
    		app_network.load_data();
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
        $("#addController").off("click").on("click",function() {
            app_network.addController();
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

  
    },
    addDevice: function()
    {
    $.ajax({ 
            url: path+"ZWaveAPI/Run/controller.AddNodeToNetwork(1)", 
            dataType: 'json',
            async: true, 
            success: function(data) {
				if(data['result']== true){
					$('#alert_console_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent !</span></div>');
				}else{
					$('#alert_console_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
				}
            },
            error: function(data) {
            	$('#alert_console_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
            }
        });
    },
    removeDevice: function()
    {
    $.ajax({ 
            url: path+"ZWaveAPI/Run/controller.RemoveNodeFromNetwork(1)", 
            dataType: 'json',
            async: true, 
            success: function(data) {
				if(data['result']== true){
					$('#alert_console_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent !</span></div>');
				}else{
					$('#alert_console_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
				}
            },
            error: function(data) {
            	$('#alert_console_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
            }
        });
    },
    cancelCommand: function()
    {
    $.ajax({ 
            url: path+"ZWaveAPI/Run/CancelCommand()", 
            dataType: 'json',
            async: true, 
            success: function(data) {
				if(data['result']== true){
					$('#alert_console_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent !</span></div>');
				}else{
					$('#alert_console_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
				}
            },
            error: function(data) {
            	$('#alert_console_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
            }
        });
    },
    testNetwork: function()
    {
    $.ajax({ 
            url: path+"ZWaveAPI/Run/devices[0].TestNetwork()", 
            dataType: 'json',
            async: true, 
            success: function(data) {
				if(data['result']== true){
					$('#alert_console_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent !</span></div>');
				}else{
					$('#alert_console_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
				}
            },
            error: function(data) {
            	$('#alert_console_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
            }
        });
    },
    healNetwork: function()
    {
    $.ajax({ 
            url: path+"ZWaveAPI/Run/controller.HealNetwork()", 
            dataType: 'json',
            async: true, 
            success: function(data) {
				if(data['result']== true){
					$('#alert_console_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent !</span></div>');
				}else{
					$('#alert_console_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
				}
            },
            error: function(data) {
            	$('#alert_console_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
            }
        });
    },
    addController: function()
    {
    $.ajax({ 
            url: path+"ZWaveAPI/Run/addController()", 
            dataType: 'json',
            async: true, 
            success: function(data) {
            	$('#alert_console_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong> Messages Sent !</span></div>');
            },
            error: function(data) {
            	$('#alert_console_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong>'+data['error']+'</span></div>');
            }
        });
    },
    createNewPrimary: function()
    {
    $.ajax({ 
            url: path+"ZWaveAPI/Run/CreateNewPrimary()", 
            dataType: 'json',
            async: true, 
            success: function(data) {
            	$('#alert_console_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong> Messages Sent !</span></div>');
            },
            error: function(data) {
            	$('#alert_console_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong>'+data['error']+'</span></div>');
            }
        });
    },
    replicationSend: function()
    {
    $.ajax({ 
            url: path+"ZWaveAPI/Run/ReplicationSend()", 
            dataType: 'json',
            async: true, 
            success: function(data) {
				$('#alert_console_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > '+data['refresh count']+' Values Refreshed !</span></div>');
            },
            error: function(data) {
            	$('#alert_console_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong>'+data['error']+'</span></div>');
            }
        });
    },
    requestNetworkUpdate: function()
    {
    $.ajax({ 
            url: path+"ZWaveAPI/Run/controller.RequestNetworkUpdate()", 
            dataType: 'json',
            async: true, 
            success: function(data) {
				if(data['result']== true){
					$('#alert_console_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent !</span></div>');
				}else{
					$('#alert_console_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
				}
            },
            error: function(data) {
            	$('#alert_console_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
            }
        });
    },
    transferPrimaryRole: function()
    {
    $.ajax({ 
            url: path+"ZWaveAPI/Run/TransferPrimaryRole()", 
            dataType: 'json',
            async: true, 
            success: function(data) {
            	$('#alert_console_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent ! '+data['result']+'</span></div>');
            },
            error: function(data) {
            	$('#alert_console_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
            }
        });
    },
    writeConfigFile: function()
    {
    $.ajax({ 
            url: path+"ZWaveAPI/Run/WriteZWConfig()", 
            dataType: 'json',
            async: true, 
            success: function(data) {
            	$('#alert_console_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent ! '+data['result']+'</span></div>');
            },
            error: function(data) {
            	$('#alert_console_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
            }
        });
    },
    softReset: function()
    {
    $.ajax({ 
            url: path+"/ZWaveAPI/Run/SerialAPISoftReset()", 
            dataType: 'json',
            async: true, 
            success: function(data) {
            	if(data['result']== true){
					$('#alert_console_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent !</span></div>');
				}else{
					$('#alert_console_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
				}
            },
            error: function(data) {
            	$('#alert_console_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
            }
        });
    },
    hardReset: function()
    {
    	//TODO: add a confirmation yes/no before execute
    $.ajax({ 
            url: path+"ZWaveAPI/Run/HardReset()", 
            dataType: 'json',
            async: true, 
            success: function(data) {
            	if(data['result']== true){
					$('#alert_console_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent !</span></div>');
				}else{
					$('#alert_console_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
				}
            },
            error: function(data) {
            	$('#alert_console_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
            }
        });
    },
    load_data: function()
    {
    $('#graph_network').html('<div id="graph-node-name"></div>');
    $.ajax({ 
            url: path+"ZWaveAPI/Data/0", 
            dataType: 'json',
            async: true, 
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
              	middle.isPinned = true;
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
			  	
                
            },
            error: function(data) {
            $('#alert_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong> ('+JSON.stringify(data, null, 4)+')</span></div>');
            }
        });
    },
    load_stats: function(node_id)
    {
    $.ajax({ 
            url: path+"ZWaveAPI/Data/0", 
            dataType: 'json',
            async: true, 
            success: function(data) {            
            	app_nodes.show_stats();
                // auto select first node                
            },
            error: function(data) {
            $('#alert_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong> ('+JSON.stringify(data, null, 4)+')</span></div>');
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
	
    hide: function()
    {
        clearInterval(app_nodes.updater);
    },
	load_infos: function()
    {
    $.ajax({ 
            url: path+"ZWaveAPI/Run/network_status()", 
            dataType: 'json',
            async: true, 
            success: function(data) {
            
                infos = data;
                app_network.show_infos();
                app_network.show_stats();
                // auto select first node
                
            },
            error: function(data) {
            $('#alert_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong> ('+JSON.stringify(data, null, 4)+')</span></div>');
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
    	$("#addController").prop("disabled",disabledCommand);
    	$("#createNewPrimary").prop("disabled",disabledCommand);
    	$("#replicationSend").prop("disabled",disabledCommand);
    	$("#requestNetworkUpdate").prop("disabled",disabledCommand);
    	$("#transferPrimaryRole").prop("disabled",disabledCommand);
    	$("#writeConfigFile").prop("disabled",disabledCommand);
    	$("#softReset").prop("disabled",disabledCommand);
    	$("#hardReset").prop("disabled",disabledCommand);
        
        
	},
    update: function ()
    {
      app_nodes.draw_nodes();
    },
    show: function ()
    {
      
      app_network.load_infos();
    }


}

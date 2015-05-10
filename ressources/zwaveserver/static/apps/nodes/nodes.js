
var app_nodes = {
    // note variable nodes is global!

    selected_node: 0,
    groups: [],
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
    	console.log(path);
    	app_nodes.load_data();
    	$('#node-queryStageDescrition').popover({title: '', placement: 'right', trigger: 'hover'});
    	$("#node-nav").on("click","li",function() {
    		var nid = $(this).attr("nid");
    		app_nodes.selected_node = nid;
    		app_nodes.draw_nodes();
    		app_nodes.load_data();
    		app_nodes.load_stats(app_nodes.selected_node);
    		app_nodes.show_groups();
            //app_nodes.load_groups(app_nodes.selected_node);
        });
    	$("#tab-summary").on("click",function() {
    		app_nodes.draw_nodes();
    		app_nodes.load_data();
    	});
    	$("#tab-values").on("click",function() {
    		app_nodes.draw_nodes();
    		app_nodes.load_data();
    	});
    	$("#tab-parameters").on("click",function() {
    		app_nodes.draw_nodes();
    		app_nodes.load_data();
    	});
    	$("#tab-groups").on("click",function() {
    		app_nodes.draw_nodes();
    		app_nodes.load_data();
    		app_nodes.show_groups();
            //app_nodes.load_groups(app_nodes.selected_node);
        });
    	$("#tab-systems").on("click",function() {
    		app_nodes.draw_nodes();
    		app_nodes.load_data();
    	});
    	$("#tab-actions").on("click",function() {
    		app_nodes.draw_nodes();
    		app_nodes.load_data();
    	});
    	$("#tab-stats").on("click",function() {
    		app_nodes.draw_nodes();
    		app_nodes.load_data();
    		app_nodes.load_stats(app_nodes.selected_node);
    	});
    	$("body").on("click",".requestNodeNeighboursUpdate",function (e) {
    		app_nodes.request_node_neighbours_update(app_nodes.selected_node);
    	});
    	$("body").on("click",".healNode",function (e) {
    		app_nodes.healNode(app_nodes.selected_node);
    	});
    	$("#testNode").on("click",function() {
    		app_nodes.test_node(app_nodes.selected_node);
    	});
    	$("#refreshNodeValues").on("click",function() {
    		app_nodes.refresh_node_values(app_nodes.selected_node);
    	});
    	$("body").on("click",".refreshNodeInfo",function (e) {
    		app_nodes.refresh_node_info(app_nodes.selected_node);
    	});
    	$("body").on("click",".hasNodeFailed",function (e) {
    		app_nodes.has_node_failed(app_nodes.selected_node);
    	});
    	$("#removeFailedNode").on("click",function() {
    		app_nodes.remove_failed_node(app_nodes.selected_node);
    	});
    	$("#replaceFailedNode").on("click",function() {
    		app_nodes.replace_failed_node(app_nodes.selected_node);
    	});
    	$("#sendNodeInformation").on("click",function() {
    		app_nodes.send_node_information(app_nodes.selected_node);
    	});
    	$("body").on("click",".addGroup",function (e) {
    		var group = $(this).data('groupindex');
    		$('#groupsModal').data('groupindex', group);
    		$('#groupsModal').modal('show');
    	});
    	$("body").on("click",".deleteGroup",function (e) {
    		var group = $(this).data('groupindex');
    		var node = $(this).data('nodeindex');
    		app_nodes.delete_group(app_nodes.selected_node,group,node);
    	});
    	$('#groupsModal').on('show.bs.modal', function (e) {
    		var modal = $(this);
    		var group = $(this).data('groupindex');
    		var arr_exists_nodes=nodes[app_nodes.selected_node].groups[group].associations.split(';');
    		modal.find('.modal-body').html(' ');
    		modal.find('.modal-title').text('Group '+group+' : Add an association for node ' + app_nodes.selected_node);
    		var options_node = '<div><b>Node : </b>  <select class="form-control" id="newvaluenode">';
    		$.each(nodes, function(key, val) {
    			if(arr_exists_nodes.indexOf(key)==-1 && key!=app_nodes.selected_node){
    				options_node +='<option value="'+key+'">'+key+' : '+val.data.name.value+'</option>';
    			}
    		});
    		options_node += '</select></div>';
    		modal.find('.modal-body').append(options_node);

    	});
    	$("#saveGroups").on("click",function (e) {
    		var groupGroup = $('#groupsModal').data('groupindex');
    		var groupNode = $('#newvaluenode').val();
    		$.ajax({ 
    			url: path+"ZWaveAPI/Run/devices["+app_nodes.selected_node+"].instances[0].commandClasses[0x85].Add("+groupGroup+","+groupNode+")", 
    			dataType: 'json',
    			async: true, 
    			success: function(data) {
	            	//app_nodes.load_groups(app_nodes.selected_node);
	            	app_nodes.draw_nodes();
	            	app_nodes.load_data();
	            	app_nodes.show_groups();
	            	$('#alert_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent !</span></div>');
	            	$('#groupsModal').modal('hide');
	            }
	        });
    	});
    	$("body").on("click",".editValue",function (e) {
    		var idx = $(this).data('valueidx');
    		var instance = $(this).data('valueinstance');
    		var cc = $(this).data('valuecc');
    		var name = $(this).data('valuename');
    		var value = $(this).data('valuevalue');
    		var type = $(this).data('valuetype');
    		var dataitems = $(this).data('valuedataitems');
    		$('#valuesModal').data('valuename', name);
    		$('#valuesModal').data('valuetype', type);
    		$('#valuesModal').data('valueinstance', instance);
    		$('#valuesModal').data('valuecc', cc);
    		$('#valuesModal').data('valuevalue', value);
    		$('#valuesModal').data('valuedataitems', dataitems);
    		$('#valuesModal').data('valueidx', idx).modal('show');
    	});
    	$('#valuesModal').on('show.bs.modal', function (e) {
    		var valueIdx = $(this).data('valueidx');
    		var valueType = $(this).data('valuetype');
    		var valueInstance = $(this).data('valueinstance');
    		var valueCc = $(this).data('valuecc');
    		var valueName = $(this).data('valuename');
    		var valueValue = $(this).data('valuevalue');
    		var valueDataitems = $(this).data('valuedataitems').split(";");
    		var modal = $(this);
    		modal.find('.modal-title').text('Change value for value ' + valueName);
    		modal.find('.modal-body').html(valueName);
    		modal.find('.modal-body').append('<b> : </b>');
    		if(valueType == "List"){
    			var options = '<select class="form-control" id="newvaluevalue">';
    			$.each(valueDataitems, function(key, val) {
    				if(val==valueValue){
    					options +='<option value="'+val+'" selected="selected">'+val+'</option>';
    				}else{
    					options +='<option value="'+val+'">'+val+'</option>';
    				}
    			});
    			options += '</select>';
    			modal.find('.modal-body').append(options);

    		}else if(valueType == "Bool"){
    			if(valueValue==true){
    				modal.find('.modal-body').append('<input type="radio" name="newvaluevalue" id="on" value="255" checked> ON ');
    				modal.find('.modal-body').append('<input type="radio" name="newvaluevalue" id="off" value="0"> OFF ');
    			}else{
    				modal.find('.modal-body').append('<input type="radio" name="newvaluevalue" id="on" value="255"> ON ');
    				modal.find('.modal-body').append('<input type="radio" name="newvaluevalue" id="off" value="0" checked> OFF ');
    			}
    		}else if(valueType == "Button"){
    			modal.find('.modal-body').append('<input type="radio" name="newvaluevalue" id="push" value="Press" checked> Push Button ');
    			modal.find('.modal-body').append('<input type="radio" name="newvaluevalue" id="push" value="Release"> Release Button ');
    		}else{
    			modal.find('.modal-body').append('<input type="text" class="form-control" id="newvaluevalue" value="'+valueValue+'">');
    		}
    	});
$("body").on("click",".editPolling",function (e) {
	var idx = $(this).data('valueidx');
	var instance = $(this).data('valueinstance');
	var cc = $(this).data('valuecc');
	var polling = $(this).data('valuepolling');
	$('#pollingModal').data('valueinstance', instance);
	$('#pollingModal').data('valuecc', cc);
	$('#pollingModal').data('valuepolling', polling);
	$('#pollingModal').data('valueidx', idx).modal('show');
});
$('#pollingModal').on('show.bs.modal', function (e) {
	var valueIdx = $(this).data('valueidx');
	var valueInstance = $(this).data('valueinstance');
	var valueCc = $(this).data('valuecc');
	var valuePolling = $(this).data('valuepolling');
	var modal = $(this);
	modal.find('.modal-title').text('Change polling ');
	modal.find('.modal-body').html("<b>Change polling : </b>");
	modal.find('.modal-body').append('<input type="text" class="form-control" id="newvaluevalue" value="'+valuePolling+'">');

});
$("body").on("click",".editParam",function (e) {
	var id = $(this).data('paramid');
	var name = $(this).data('paramname');
	var value = $(this).data('paramvalue');
	var type = $(this).data('paramtype');
	$('#paramsModal').data('paramname', name);
	$('#paramsModal').data('paramtype', type);
	$('#paramsModal').data('paramvalue', value);
	$('#paramsModal').data('paramid', id).modal('show');
});
$('#paramsModal').on('show.bs.modal', function (e) {
	var paramId = $(this).data('paramid');
	var paramType = $(this).data('paramtype');
	var paramName = $(this).data('paramname');
	var paramValue = $(this).data('paramvalue');
	var modal = $(this);
	modal.find('.modal-title').text('Change value for parameter ' + paramId);
	modal.find('.modal-body').html(paramName);
	modal.find('.modal-body').append('<b> : </b>');
	if(paramType == "List"){
		$.ajax({ 
			url: path+"ZWaveAPI/Run/devices["+app_nodes.selected_node+"].commandClasses[0x70].data", 
			dataType: 'json',
			async: true, 
			success: function(data) {
				var options = '<select class="form-control" id="newvalue">';
				$.each(data[paramId].val.value4, function(key, val) {
					if(val==paramValue){
						options +='<option value="'+val+'" selected="selected">'+val+'</option>';
					}else{
						options +='<option value="'+val+'">'+val+'</option>';
					}
				});
				options += '</select>';
				modal.find('.modal-body').append(options);

			}
		});
	}else{
		modal.find('.modal-body').append('<input type="text" class="form-control" id="newvalue" value="'+paramValue+'">');
	}
});
$("#sendNodeInformation").on("click",function() {
	app_nodes.send_node_information(app_nodes.selected_node);
});
$("#saveParam").on("click",function (e) {
	var paramId = $('#paramsModal').data('paramid');
	var paramValue = $('#newvalue').val();
	var paramLength = paramValue.length;
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+app_nodes.selected_node+"].commandClasses[0x70].Set("+paramId+","+paramValue+","+paramLength+")", 
		dataType: 'json',
		async: true, 
		success: function(data) {
			app_nodes.draw_nodes();
			app_nodes.load_data();
			$('#alert_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent !</span></div>');
			$('#paramsModal').modal('hide');
		}
	});
});
$("#applyValue").on("click",function (e) {
	var valueType = $('#valuesModal').data('valuetype');
	var valueIdx = $('#valuesModal').data('valueidx');
	var valueInstance = $('#valuesModal').data('valueinstance');
	var valueCc = $('#valuesModal').data('valuecc');
	if(valueType == "Bool"){
		var valueValue = $('input[name=newvaluevalue]:checked', '#valuesModal').val();
	}else if(valueType == "Button"){
		var valueValue = $('input[name=newvaluevalue]:checked', '#valuesModal').val();
	}else{
		var valueValue = $('#newvaluevalue').val();
	}
	if(valueType == "Button"){
		$.ajax({ 
			url: path+"ZWaveAPI/Run/devices["+app_nodes.selected_node+"].instances["+valueInstance+"].commandClasses[0x"+Number(valueCc).toString(16)+"].data["+valueIdx+"]."+valueValue+"Button()", 
			dataType: 'json',
			async: true, 
			success: function(data) {
				app_nodes.draw_nodes();
				app_nodes.load_data();
				$('#alert_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent !</span></div>');
				$('#valuesModal').modal('hide');
				app_nodes.draw_nodes();
			}
		});
	}else if(valueType == "Raw"){
		$.ajax({ 
			url: path+"ZWaveAPI/Run/devices["+app_nodes.selected_node+"].UserCode.SetRaw("+valueIdx+",["+valueValue+"],1)", 
			dataType: 'json',
			async: true, 
			success: function(data) {
				app_nodes.draw_nodes();
				app_nodes.load_data();
				$('#alert_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent !</span></div>');
				$('#valuesModal').modal('hide');
				app_nodes.draw_nodes();
			}
		});
	}
	else{
		$.ajax({ 
			url: path+"ZWaveAPI/Run/devices["+app_nodes.selected_node+"].instances["+valueInstance+"].commandClasses[0x"+Number(valueCc).toString(16)+"].data["+valueIdx+"].Set("+valueValue+")", 
			dataType: 'json',
			async: true, 
			success: function(data) {
				app_nodes.draw_nodes();
				app_nodes.load_data();
				$('#alert_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent !</span></div>');
				$('#valuesModal').modal('hide');
				app_nodes.draw_nodes();
			}
		});
	}
});
$("#savePolling").on("click",function (e) {
	var valueIdx = $('#pollingModal').data('valueidx');
	var valueInstance = $('#pollingModal').data('valueinstance');
	var valueCc = $('#pollingModal').data('valuecc');
	var valueValue = $('#newvaluevalue').val();
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+app_nodes.selected_node+"].instances["+valueInstance+"].commandClasses[0x"+Number(valueCc).toString(16)+"].data["+valueIdx+"].SetPolling("+valueValue+")", 
		dataType: 'json',
		async: true, 
		success: function(data) {
			app_nodes.draw_nodes();
			app_nodes.load_data();
			$('#alert_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent !</span></div>');
			$('#pollingModal').modal('hide');
			app_nodes.draw_nodes();
		}
	});
});

},
delete_group: function(node_id,group,node)
{
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].instances[0].commandClasses[0x85].Remove("+group+","+node+")", 
		dataType: 'json',
		async: true, 
		success: function(data) {
            	//app_nodes.load_groups(app_nodes.selected_node);
            	app_nodes.draw_nodes();
            	app_nodes.load_data();
            	app_nodes.show_groups();
            	$('#alert_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent !</span></div>');
            },
            error: function(data) {
            	$('#alert_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
            }
        });
},
request_node_neighbours_update: function(node_id)
{
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].RequestNodeNeighbourUpdate()", 
		dataType: 'json',
		async: true, 
		success: function(data) {
			if(data['result']== true){
				$('#alert_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent !</span></div>');
			}else{
				$('#alert_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
			}
		},
		error: function(data) {
			$('#alert_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
		}
	});
},
healNode: function(node_id)
{
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].HealNode()", 
		dataType: 'json',
		async: true, 
		success: function(data) {
			if(data['result']== true){
				$('#alert_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent !</span></div>');
			}else{
				$('#alert_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
			}
		},
		error: function(data) {
			$('#alert_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
		}
	});
},
test_node: function(node_id)
{
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].TestNetwork()", 
		dataType: 'json',
		async: true, 
		success: function(data) {
			$('#alert_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong> Messages Sent !</span></div>');
		},
		error: function(data) {
			$('#alert_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong>'+data['error']+'</span></div>');
		}
	});
},
refresh_node_values: function(node_id)
{
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].RefreshAllValues()", 
		dataType: 'json',
		async: true, 
		success: function(data) {
			$('#alert_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > '+data['refresh count']+' Values Refreshed !</span></div>');
		},
		error: function(data) {
			$('#alert_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong>'+data['error']+'</span></div>');
		}
	});
},
refresh_node_info: function(node_id)
{
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].RefreshNodeInfo()", 
		dataType: 'json',
		async: true, 
		success: function(data) {
			if(data['result']== true){
				$('#alert_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent !</span></div>');
			}else{
				$('#alert_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
			}
		},
		error: function(data) {
			$('#alert_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
		}
	});
},
has_node_failed: function(node_id)
{
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].HasNodeFailed()", 
		dataType: 'json',
		async: true, 
		success: function(data) {
			$('#alert_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent ! '+data['result']+'</span></div>');
		},
		error: function(data) {
			$('#alert_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
		}
	});
},
remove_failed_node: function(node_id)
{
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].RemoveFailedNode()", 
		dataType: 'json',
		async: true, 
		success: function(data) {
			if(data['result']== true){
				$('#alert_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent !</span></div>');
			}else{
				$('#alert_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
			}
		},
		error: function(data) {
			$('#alert_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
		}
	});
},
replace_failed_node: function(node_id)
{
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].ReplaceFailedNode()", 
		dataType: 'json',
		async: true, 
		success: function(data) {
			if(data['result']== true){
				$('#alert_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent !</span></div>');
			}else{
				$('#alert_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
			}
		},
		error: function(data) {
			$('#alert_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
		}
	});
},
send_node_information: function(node_id)
{
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].SendNodeInformation()", 
		dataType: 'json',
		async: true, 
		success: function(data) {
			$('#alert_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent ! '+data['result']+'</span></div>');
		},
		error: function(data) {
			$('#alert_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
		}
	});
},
load_data: function()
{
	$.ajax({ 
		url: path+"ZWaveAPI/Data/0", 
		dataType: 'json',
		async: true, 
		success: function(data) {
			console.log('chargement ok');
			nodes = data['devices'];
			controller = data['controller'];
			app_nodes.draw_nodes();
                // auto select first node
                
            },
            error: function(data) {
            	alert('error'+JSON.stringify(data, null, 4));
            }
        });
},
load_stats: function(node_id)
{
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].GetNodeStatistics()", 
		dataType: 'json',
		async: true, 
		success: function(data) {
			console.log('ok');
			stats = data['statistics'];
			app_nodes.show_stats();
                // auto select first node
                
            },
            error: function(data) {
            	alert('error'+JSON.stringify(data, null, 4));
            }
        });
},
load_groups: function(node_id)
{
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].instances[0].commandClasses[133].data", 
		dataType: 'json',
		async: true, 
		success: function(data) {
			console.log('ok');
			groups = data;
			app_nodes.show_groups();

		},
		error: function(data) {
			alert('error'+JSON.stringify(data, null, 4));
		}
	});
},
show: function()
{

	if(typeof node_id !== 'undefined' && !isNaN(node_id)){
		app_nodes.selected_node = node_id;
	}else{
		app_nodes.selected_node = 1;
	}
	
	setTimeout(function() {
		app_nodes.draw_nodes();
	}, 1000);
        //app_nodes.update();
        //app_nodes.updater = setInterval(app_nodes.update,2000);
    },
    
    hide: function()
    {
    	clearInterval(app_nodes.updater);
    },

    draw_nodes: function ()
    {
    	$("#node-nav").html("");
        //$("#node-content").html("");
        var template_node = $("#template-node").html();
        var template_variable = $("#template-variable").html();
        var template_parameter = $("#template-parameter").html();
        var template_system = $("#template-system").html();
        
        var networkstate = controller.data.networkstate.value;
        var disabledCommand = networkstate<5;
        
        $("#requestNodeNeighboursUpdate").prop("disabled",disabledCommand);
        $("#healNode").prop("disabled",disabledCommand);
        $("#testNode").prop("disabled",disabledCommand);
        $("#refreshNodeValues").prop("disabled",disabledCommand);
        $("#refreshNodeInfo").prop("disabled",disabledCommand);
        $("#hasNodeFailed").prop("disabled",disabledCommand);
        $("#removeFailedNode").prop("disabled",disabledCommand);
        $("#replaceFailedNode").prop("disabled",disabledCommand);
        $("#sendNodeInformation").prop("disabled",disabledCommand);

        if(typeof node_id !== 'undefined' && !isNaN(node_id)){
        	$('.nodes-rightpane').removeClass('col-md-9 col-md-offset-3').addClass('col-md-12');
        }else{
        	$("#node-nav").parent().show();
        }     	

        for (z in nodes)
        {
        	
            // node entry in left hand side navigation list
            var iconcolor="";
            if(nodes[z].data.isFailed){
            	var nodeIsFailed = nodes[z].data.isFailed.value
            }else{
            	var nodeIsFailed = "false";
            }
        	//var nodeIsFailed = nodes[z].data.isFailed.value=="true";
        	var queryStage = nodes[z].data.state.value;
        	
        	if(nodeIsFailed== "true"){
        		iconcolor="fa-chain-broken rediconcolor";            	
        	}
        	else if(queryStage == "Complete"){
        		iconcolor="fa-heartbeat greeniconcolor";
        	}else{
        		iconcolor="fa-heartbeat yellowiconcolor";
        	}
        	if(typeof node_id === 'undefined' || isNaN(node_id)){
        		$("#node-nav").append("<li nid="+z+" class='node-item'c><a><i class='fa "+iconcolor+"'></i> "+z+": "+nodes[z].data.name.value+"</a></li>");
        	}

            // make a copy of node info & variables block template, set its nodeid
            var display = "";
            //if (app_nodes.selected_node!=z) display = "display:none";
            //$("#node-content").append("<div class='node' nid="+z+" style='"+display+"'>"+template_node+"</div>");
            if (app_nodes.selected_node==z){
            	$("#node").attr("nid", z);
	            // select the copied block
	            var node = $(".node");
	            var isWarning = false;
	            
	            var warningMessage = "";
	            
	            node.find(".node-id").html(z);              // set the nodeid
	            
	            var productName = nodes[z].data.name.value;
	            var manufacturerName = nodes[z].data.vendorString.value;
	            node.find(".node-name").html(productName);
	            node.find(".node-vendor").html(manufacturerName);


	            node.find(".node-zwave-id").html("Manufacturer id: " +nodes[z].data.manufacturerId.value +" product type: " +nodes[z].data.manufacturerProductType.value + " product id: " + nodes[z].data.manufacturerProductId.value);            		

	            node.find(".node-lastSeen").html(app_nodes.timestampConverter(nodes[z].data.lastReceived.updateTime));


	            var basicDeviceClass = parseInt(nodes[z].data.basicType.value,0);
	            var basicDeviceClassDescription = "";	            
	            switch(basicDeviceClass){
	            	case 1:
	            	basicDeviceClassDescription = "Controller";
	            	break;
	            	case 2:
	            	basicDeviceClassDescription = "Static Controller";
	            	break;
	            	case 3:
	            	basicDeviceClassDescription = "Slave";
	            	break;
	            	case 4:
	            	basicDeviceClassDescription = "Routing Slave";
	            	break;
	            	default:
	            	basicDeviceClassDescription = basicDeviceClass;
	            	break;
	            }
	            
	            var genericDeviceClass = parseInt(nodes[z].data.genericType.value,0);
	            var genericDeviceClassDescription = "";
	            
	            //The ‘Generic’ device class defines the basic functionality that the devices will support as a controller or slave.	         
	            switch(genericDeviceClass){
	            case 1: //REMOTE_CONTROLLER   = 0x01
	            genericDeviceClassDescription = "Remote controller";
	            break;
	            case 2: //STATIC_CONTROLLER   = 0x02,
	            genericDeviceClassDescription = "Static controller";
	            break;
	            case 3: //AV_CONTROL_POINT    = 0x03,
	            genericDeviceClassDescription = "A/V Control Point";
	            break;
	            case 4: //DISPLAY             = 0x04,
	            genericDeviceClassDescription = "Display";
	            break;
	            case 7: //GARAGE_DOOR             = 0x07,
	            genericDeviceClassDescription = "Garage Door";
	            break;
	            case 8: //THERMOSTAT          = 0x08,
	            genericDeviceClassDescription = "Thermostat";
	            break;
	            case 9: //WINDOW_COVERING     = 0x09,
	            genericDeviceClassDescription = "Window Covering";
	            break;
	            case 15: //REPEATER_SLAVE      = 0x0f,
	            genericDeviceClassDescription = "Repeater Slave";
	            break;
	            case 16: //BINARY_SWITCH       = 0x10,
	            genericDeviceClassDescription = "Binary Switch";
	            break;
	            case 17: //MULTILEVEL_SWITCH   = 0x11,
	            genericDeviceClassDescription = "Multi level Switch";
	            break;
	            case 18: //REMOTE_SWITCH       = 0x12,
	            genericDeviceClassDescription = "Remote Switch";
	            break;
	            case 19: // TOGGLE_SWITCH       = 0x13,
	            genericDeviceClassDescription = "Toggle Switch";
	            break;
	            case 20: // Z_IP_GATEWAY       = 0x14,
	            genericDeviceClassDescription = "Z/IP Gateway";
	            break;
	            case 21: // Z_IP_NODE       = 0x15,
	            genericDeviceClassDescription = "Z/IP Node";
	            break;
	            case 22: //VENTILATION         = 0x16,
	            genericDeviceClassDescription = "Ventilation";
	            break;
	            case 30: //REMOTE_SWITCH2       = 0x18,
	            genericDeviceClassDescription = "Remote Switch 2";
	            break;
	            case 32: //BINARY_SENSOR       = 0x20,
	            genericDeviceClassDescription = "Binary Sensorr";
	            break;
	            case 33: //MULTILEVEL_SENSOR   = 0x21
	            genericDeviceClassDescription = "Multilevel-Sensor";
	            break;
	            case 34: //WATER_CONTROL   = 0x22
	            genericDeviceClassDescription = "Water Control";
	            break;
	            case 48: //PULSE_METER         = 0x30
	            genericDeviceClassDescription = "Pulse Meter";
	            case 49: //METER         = 0x31
	            genericDeviceClassDescription = "Meter";
	            break;
	            case 64: //ENTRY_CONTROL       = 0x40
	            genericDeviceClassDescription = "Entry Control";
	            break;
	            case 85: //NON_INTEROPERABLE        = 0x55
	            genericDeviceClassDescription = "Semi-Interoperable";
	            break;
	            case 161: //ALARM_SENSOR        = 0xa1
	            genericDeviceClassDescription = "Alarm Sensor";
	            break;
	            case 255: //NON_INTEROPERABLE        = 0xff
	            genericDeviceClassDescription = "Non-Interoperable";
	            break;	

	            default:
	            genericDeviceClassDescription = "Unknown";
	            break;
	        }

	        var specificDeviceClass = parseInt(nodes[z].data.specificType.value,0);
	        var specificDeviceClassDescription = nodes[z].data.type.value;	            

	        node.find(".node-basic").html(basicDeviceClassDescription);
	        node.find(".node-generic").html(genericDeviceClassDescription);
	        node.find(".node-specific").html(specificDeviceClassDescription);

	        var nodeCanSleep = nodes[z].data.can_wake_up.value=="true";
	        if(nodeCanSleep){
	        	if(nodes[z].data.isAwake.value=="true"){
	        		node.find(".node-sleep").html("Is awake");
	        	}
	        	else{
	        		node.find(".node-sleep").html("Is sleeping");
	        	}
	        }
	        else{
	        	node.find(".node-sleep").html("");
	        }

	        if(nodeIsFailed=="true" & networkstate>=7){
	            	//this warning must stay in place
	            	isWarning = true;
	            	warningMessage +="<li>The controller think this device as failed, use <button type='button' id='hasNodeFailed_summary' class='btn btn-xs btn-primary hasNodeFailed'>Has Node Failed ?</button> action to try to revived the device.</li>"
	            }
	            
	            var queryStageDescrition = "";
	            var queryStageIndex = 0;	            
	            switch(queryStage){
	            	case "None":
	            	queryStageDescrition = "Query process hasn't started for this node";
	            	queryStageIndex = 0;
	            	break;
	            	case "ProtocolInfo":
	            	queryStageDescrition = "Retrieve protocol information";
	            	queryStageIndex = 1;
	            	break;
	            	case "Probe":
	            	queryStageDescrition = "Ping device to see if alive";
	            	queryStageIndex = 2;
	            	break;
	            	case "WakeUp":
	            	queryStageDescrition = "Start wake up process if a sleeping node";
	            	queryStageIndex = 3;
	            	break;
	            	case "ManufacturerSpecific1":
	            	queryStageDescrition = "Retrieve manufacturer name and product ids if ProtocolInfo lets us";
	            	queryStageIndex = 4;
	            	break;
	            	case "NodeInfo":
	            	queryStageDescrition = "Retrieve info about supported, controlled command classes";
	            	queryStageIndex = 5;
	            	break;
	            	case "SecurityReport":
	            	queryStageDescrition = "Retrive a list of Command Classes that require Security";
	            	queryStageIndex = 6;
	            	break;
	            	case "ManufacturerSpecific2":
	            	queryStageDescrition = "Retrieve manufacturer name and product ids";
	            	queryStageIndex = 7;
	            	break;
	            	case "Versions":
	            	queryStageDescrition = "Retrieve version information";
	            	queryStageIndex = 8;
	            	break;
	            	case "Instances":
	            	queryStageDescrition = "Retrieve information about multiple command class instances";
	            	queryStageIndex = 9;
	            	break;
	            	case "Static":
	            	queryStageDescrition = "Retrieve static information";
	            	queryStageIndex = 10;
	            	break;
	            	case "Probe1":
	            	queryStageDescrition = "Ping a device upon starting with configuration";
	            	queryStageIndex = 11;
	            	break;
	            	case "Associations":
	            	queryStageDescrition = "Retrieve information about associations";
	            	queryStageIndex = 12;
	            	break;
	            	case "Neighbors":
	            	queryStageDescrition = "Retrieve node neighbor list";
	            	queryStageIndex = 13;
	            	break;
	            	case "Session":
	            	queryStageDescrition = "Retrieve session information";
	            	queryStageIndex = 14;
	            	break;
	            	case "Dynamic":
	            	queryStageDescrition = "Retrieve dynamic information";
	            	queryStageIndex = 15;
	            	break;
	            	case "Configuration":
	            	queryStageDescrition = "Retrieve configurable parameter information";
	            	queryStageIndex = 16;
	            	break;
	            	case "Complete":
	            	queryStageDescrition = "Query process is completed for this node";
	            	queryStageIndex = 17;
	            	break;	            	
	            }
	            
	            node.find(".node-queryStage").html(queryStage);
	            var myPopover = $('#node-queryStageDescrition').data('bs.popover');
	            if (queryStageIndex < 17){
	            	myPopover.options.content = queryStageDescrition + " (" +queryStageIndex + "/17)";
	            }
	            else{
	            	myPopover.options.content = queryStageDescrition;
	            }		         
	            node.find(".node-maxBaudRate").html(nodes[z].data.maxBaudRate.value);
	            if(nodes[z].data.isRouting.value=="true"){
	            	node.find(".node-routing").html("<li>Device is a routing node (capable of passing commands along to other nodes in the network)</li>");
	            }
	            else{
	            	node.find(".node-routing").html("");
	            }
	            if(nodes[z].data.isSecurity.value=="true"){
	            	node.find(".node-isSecurity").html("<li>Device supports security features</li>");
	            	/* TODO: display Security Flag
	            	Security = 0x01
	            	Controller = 0x02
	            	SpecificDevice = 0x04
	            	RoutingSlave = 0x08
	            	BeamCapability = 0x10
	            	Sensor250ms	= 0x20
	            	Sensor1000ms = 0x40
	            	OptionalFunctionality = 0x80 
	            	*/
	            	node.find(".node-security").html("Security class: " + nodes[z].data.security.value);
	            }
	            else{
	            	node.find(".node-isSecurity").html("");
	            	node.find(".node-security").html("");
	            }
	            if(nodes[z].data.isListening.value=="true"){
	            	node.find(".node-listening").html("<li>Device is powered and listening constantly</li>");
	            }	
	            else{
	            	node.find(".node-listening").html("");
	            }
	            if(nodes[z].data.isFrequentListening.value=="true"){
	            	node.find(".node-isFrequentListening").html("<li>Device can be woken up with a beam</li>");
	            }
	            else{
	            	node.find(".node-isFrequentListening").html("");	
	            }
	            if(nodes[z].data.isBeaming.value=="true"){
	            	node.find(".node-isBeaming").html("<li>Device is beam capable</li>");
	            }  
	            else{
	            	node.find(".node-isBeaming").html("");
	            }        
	            
	            var neighbours = nodes[z].data.neighbours.value.join();
	            if(queryStageIndex > 13){
	            	if (neighbours != "" ){
	            		node.find(".node-neighbours").html(neighbours);
	            	}
	            	else{
	            		node.find(".node-neighbours").html("...");		  
	            		if(networkstate>=7){
	            			warningMessage +="<li>The neighbours is not available for this device.<br/>Use <button type='button' class='btn btn-xs btn-primary healNode'>Heal Node</button> or <button type='button' class='btn btn-xs btn-primary requestNodeNeighboursUpdate'>Request Node Neighbours Update</button> action to force a neighbours refresh.</li>";		            	
	            			isWarning = true;
	            		}
	            	}
	            }
	            else{  
	            	node.find(".node-neighbours").html("<i>the neighbours is not yet available.</i>");
	            }
	            if (queryStageIndex > 7 & productName == ""){
	            	if(networkstate>=7){
	            		warningMessage +="<li>The Product Name and the Manufacturer informations are not detected.<br/>Use <button type='button' class='btn btn-xs btn-primary refreshNodeInfo'>Refresh Node Info</button> action to trigger the fetching of fixed data about this node.</li>";
	            		isWarning = true;	 
	            	}
	            }	
	            
	            if (isWarning){ 
	            	if (nodeCanSleep){
	            		warningMessage += "<br><p>This is a sleeping device, he need a 'wake-up' before any command can be executed.<br/>You can manualy trigger a 'wake-up' directly on device or wait the normal 'wake-up'.<br/>See: 'Wake-up Interval in System TAB</p>";	            		
	            	}	            	
	            	node.find(".panel-danger").show();
	            	node.find(".node-warning").html(warningMessage);
	            }	            
	            else{
	            	node.find(".panel-danger").hide();
	            	node.find(".node-warning").html("");
	            }
	            var variables = "";
	            var parameters = "";
	            var system_variables = "";
	            for (instance in nodes[z].instances){
	            	for (commandclass in nodes[z].instances[instance].commandClasses){

	            		for (index in nodes[z].instances[instance].commandClasses[commandclass].data){
	            			if(!isNaN(index)){								
	            				var id=instance+":"+commandclass+":"+index;								
	            				var genre = nodes[z].instances[instance].commandClasses[commandclass].data[index].genre;
	            				if(genre =="Config"){									
	            					parameters += "<tr pid='"+id+"'>"+template_parameter+"</tr>";
	            				}else if(genre == "System"){									
	            					system_variables += "<tr sid='"+id+"'>"+template_system+"</tr>";
	            				}else{
	            					variables += "<tr vid='"+id+"'>"+template_variable+"</tr>";
	            				}								
	            			}
	            		}	
	            	}
	            }
	            node.find(".variables").html(variables);
	            node.find(".parameters").html(parameters);
	            node.find(".system_variables").html(system_variables);
	            for (instance in nodes[z].instances){
	            	for (commandclass in nodes[z].instances[instance].commandClasses){
	            		for (index in nodes[z].instances[instance].commandClasses[commandclass].data){
	            			var id=instance+":"+commandclass+":"+index;

	            			var row = node.find("tr[vid='"+id+"']");
	            			var row_parameter = node.find("tr[pid='"+id+"']");
	            			var row_system = node.find("tr[sid='"+id+"']");

							//var date = new Date(nodes[z].instances[instance].commandClasses[commandclass].data[index].updateTime * 1000).format('h:i:s');
							row.find("td[key=variable-instance]").html(instance);
							row.find("td[key=variable-cc]").html(commandclass+' (0x'+Number(commandclass).toString(16)+')');
							row.find("td[key=variable-index]").html(index);
							row.find("td[key=variable-name]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].name);
							row.find("td[key=variable-type]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].typeZW+' ('+nodes[z].instances[instance].commandClasses[commandclass].data[index].type+')');
							row.find("td[key=variable-value]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].value +" "+ nodes[z].instances[instance].commandClasses[commandclass].data[index].units);
							if(nodes[z].instances[instance].commandClasses[commandclass].data[index].read_only==false){
								row.find("td[key=variable-edit]").html('<button type="button" class="btn btn-primary editValue" data-valueidx="'+index+'" data-valueinstance="'+instance+'" data-valuecc="'+commandclass+'" data-valuedataitems="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].data_items+'" data-valuetype="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].typeZW+'" data-valuename="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].name+'" data-valuevalue="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].value+'"><i class="fa fa-wrench"></i></button>');
							}
							row.find("td[key=variable-polling]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].poll_intensity);
							if(nodes[z].instances[instance].commandClasses[commandclass].data[index].write_only==false){
								row.find("td[key=variable-editpolling]").html('<button type="button" class="btn btn-primary editPolling" data-valueidx="'+index+'" data-valuepolling="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].poll_intensity+'" data-valueinstance="'+instance+'" data-valuecc="'+commandclass+'" data-valuedataitems="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].data_items+'" data-valuetype="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].typeZW+'" data-valuename="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].name+'" data-valuevalue="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].value+'"><i class="fa fa-wrench"></i></button>');
							}
							row.find("td[key=variable-updatetime]").html(app_nodes.timestampConverter(nodes[z].instances[instance].commandClasses[commandclass].data[index].updateTime));

							row_system.find("td[key=system-instance]").html(instance);
							row_system.find("td[key=system-cc]").html(commandclass+' (0x'+Number(commandclass).toString(16)+')');
							row_system.find("td[key=system-index]").html(index);
							row_system.find("td[key=system-name]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].name);
							row_system.find("td[key=system-type]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].typeZW+' ('+nodes[z].instances[instance].commandClasses[commandclass].data[index].type+')');
							row_system.find("td[key=system-value]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].value +" "+ nodes[z].instances[instance].commandClasses[commandclass].data[index].units);
							if(nodes[z].instances[instance].commandClasses[commandclass].data[index].read_only==false){
								row_system.find("td[key=system-edit]").html('<button type="button" class="btn btn-primary editValue" data-valueidx="'+index+'" data-valueinstance="'+instance+'" data-valuecc="'+commandclass+'" data-valuedataitems="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].data_items+'" data-valuetype="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].typeZW+'" data-valuename="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].name+'" data-valuevalue="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].value+'"><i class="fa fa-wrench"></i></button>');
							}
							row_system.find("td[key=system-updatetime]").html(app_nodes.timestampConverter(nodes[z].instances[instance].commandClasses[commandclass].data[index].updateTime));


							row_parameter.find("td[key=parameter-index]").html(index);
							row_parameter.find("td[key=parameter-name]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].name);
							row_parameter.find("td[key=parameter-type]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].typeZW);
							row_parameter.find("td[key=parameter-value]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].value);
							row_parameter.find("td[key=parameter-edit]").html('<button type="button" class="btn btn-primary editParam" data-paramid="'+index+'" data-paramtype="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].typeZW+'" data-paramname="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].name+'" data-paramvalue="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].value+'"><i class="fa fa-wrench"></i></button>');
							row_parameter.find("td[key=parameter-help]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].help);
						}
					}
				}
			}
		}
	},
	show_stats: function (){
		var node = $(".node");
		node.find(".stats_av_req_rtt").html(stats.averageRequestRTT);
		node.find(".stats_av_res_rtt").html(stats.averageResponseRTT);
		node.find(".stats_la_req_rtt").html(stats.lastRequestRTT);
		node.find(".stats_la_res_rtt").html(stats.lastResponseRTT);
		node.find(".stats_quality").html(stats.quality);
		node.find(".stats_rec_cnt").html(stats.receivedCnt);
		node.find(".stats_rec_dups").html(stats.receivedDups);
		node.find(".stats_rec_ts").html(stats.receivedTS);
		node.find(".stats_rec_uns").html(stats.receivedUnsolicited);
		node.find(".stats_retries").html(stats.retries);
		node.find(".stats_sen_cnt").html(stats.sentCnt);
		node.find(".stats_sen_failed").html(stats.sentFailed);
		node.find(".stats_sen_ts").html(stats.sentTS);
	},
	show_groups: function (){
		var node = $(".node");
		var template_group = $("#template-group").html();
		var $template = $(".template");
		var tr_groups="";
		var node_groups=nodes[app_nodes.selected_node].groups;
		app_nodes.groups=[];
		$("#groups").empty();
		$("#groups").append('<br>');
		for (z in node_groups){
			if (!isNaN(z)){
				var values=node_groups[z].associations.split(';');
				tr_groups="";
				for(val in values){
					if(values.length > 0 && values[val]!=""){

						var id=z+'-'+values[val];
						var node_id=values[val];
						if(nodes[node_id]){
							var node_name=nodes[node_id].data.name.value;
						}else{
							var node_name="UNDEFINED";
						}
						tr_groups += "<tr gid='"+id+"'><td>"+node_id+" : "+node_name+"</td><td align='right'><button type='button' class='btn btn-danger btn-sm deleteGroup' data-groupindex='"+z+"' data-nodeindex='"+node_id+"'><i class='fa fa-trash-o'></i> Delete</button></td></tr>";
					}
				}
				if(values.length < node_groups[z].maximumAssociations){
					var $newPanel = '<div class="panel panel-primary template"><div class="panel-heading"><div class="btn-group pull-right"><a id="addGroup" class="btn btn-info btn-sm addGroup" data-groupindex="'+z+'"><i class="fa fa-plus"></i> Add a node</a></div><h3 class="panel-title" style="padding-top:10px;">'+z+' : '+node_groups[z].label+' (max association: '+node_groups[z].maximumAssociations+')</h3></div><div class="panel-body"><table class="table">'+tr_groups+'</table></div></div>';
				}else{
					var $newPanel = '<div class="panel panel-primary template"><div class="panel-heading"><div class="btn-group pull-right"><a id="addGroup" class="btn btn-info btn-sm addGroup" disabled data-groupindex="'+z+'"><i class="fa fa-plus"></i> Add a node</a></div><h3 class="panel-title" style="padding-top:10px;">'+z+' : '+node_groups[z].label+' (max association: '+node_groups[z].maximumAssociations+')</h3></div><div class="panel-body"><table class="table">'+tr_groups+'</table></div></div>';
				}
				$("#groups").append($newPanel);
			}
		}


	},
	update: function ()
	{
        /*
        $.ajax({ 
            url: path+"api", 
            dataType: 'json', 
            async: true, 
            success: function(data) {
                nodes = data;
                app_nodes.draw_nodes();
            }
        });
*/
app_nodes.draw_nodes();
}


}

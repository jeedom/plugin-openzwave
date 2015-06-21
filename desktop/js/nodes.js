
var app_nodes = {
	selected_node: 0,
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
		controller_id = -1
		app_nodes.load_data(true);
		app_nodes.updater = setInterval(function(){ 
			if($('#template-node').is(':visible')){
				app_nodes.load_data(false); 
			}else{
				app_nodes.hide();	
			}
		}, 2000);
		$('#node-queryStageDescrition').popover({title: '', placement: 'right', trigger: 'hover'});
		$("#tab-parameters").off("click").on("click",function() {
			if(!nodes[app_nodes.selected_node].instances[0].commandClasses[112]){
				$("#parameters").html('<br><div><b>{{Aucun paramètre prédefini trouvé pour ce noeud}}</b></div><br>');
				$("#parameters").append('<div class="row"><label class="col-lg-1">{{Paramètre :}} </label><div class="col-lg-1"><input type="text" class="form-control" id="paramidperso"></div><label class="col-lg-1">{{Valeur :}} </label><div class="col-lg-1"><input type="text" class="form-control" id="newvalueperso"></div><label class="col-lg-1">{{Taile :}}</label><div class="col-lg-1"><input type="text" class="form-control" id="sizeperso"></div> <div class="col-lg-2"><button id="sendparamperso" class="btn btn-primary">{{Envoyer le paramètre}}</a></div></div>');
				$("#sendparamperso").off("click").on("click",function() {
					var paramId = $("#paramidperso").val();
					var paramValue = $('#newvalueperso').val();
					var paramLength = $('#sizeperso').val();
					$.ajax({ 
						url: path+"ZWaveAPI/Run/devices["+app_nodes.selected_node+"].commandClasses[0x70].Set("+paramId+","+paramValue+","+paramLength+")", 
						dataType: 'json',
						async: true, error: function (request, status, error) {
							handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
						},
						success: function(data) {
							app_nodes.sendOk();
						}
					});
				});
			}
		});

$("#tab-groups").off("click").on("click",function() {
	app_nodes.show_groups();
});

$("#tab-stats").off("click").on("click",function() {
	app_nodes.load_stats(app_nodes.selected_node);
});
$("body").off("click",".requestNodeNeighboursUpdate").on("click",".requestNodeNeighboursUpdate",function (e) {
	app_nodes.request_node_neighbours_update(app_nodes.selected_node);
});
$("body").off("click",".healNode").on("click",".healNode",function (e) {
	app_nodes.healNode(app_nodes.selected_node);
});
$("#testNode").off("click").on("click",function() {
	app_nodes.test_node(app_nodes.selected_node);
});
$("#refreshNodeValues").off("click").on("click",function() {
	app_nodes.refresh_node_values(app_nodes.selected_node);
});
$("#requestNodeDynamic").off("click").on("click",function() {
	app_nodes.request_node_dynamic(app_nodes.selected_node);
});
$("body").off("click",".refreshNodeInfo").on("click",".refreshNodeInfo",function (e) {
	app_nodes.refresh_node_info(app_nodes.selected_node);
});
$("body").off("click",".hasNodeFailed").on("click",".hasNodeFailed",function (e) {
	app_nodes.has_node_failed(app_nodes.selected_node);
});
$("#removeFailedNode").off("click").on("click",function() {
	app_nodes.remove_failed_node(app_nodes.selected_node);
});
$("#replaceFailedNode").off("click").on("click",function() {
	app_nodes.replace_failed_node(app_nodes.selected_node);
});
$("#sendNodeInformation").off("click").on("click",function() {
	app_nodes.send_node_information(app_nodes.selected_node);
});
$("#regenerateNodeCfgFile").off("click").on("click",function() {
	bootbox.confirm("{{Etes-vous sûr ? Cela va redémarrer votre réseau}}", function(result) {
		if(result){
			app_nodes.send_regenerate_node_cfg_file(app_nodes.selected_node);
		}
	}); 
});
$("body").off("click",".copyParams").on("click",".copyParams",function (e) {
	$('#copyParamsModal').modal('show');
});
$("body").off("click",".addGroup").on("click",".addGroup",function (e) {
	var group = $(this).data('groupindex');
	$('#groupsModal').data('groupindex', group);
	$('#groupsModal').modal('show');
});
$("body").off("click",".deleteGroup").on("click",".deleteGroup",function (e) {
	var group = $(this).data('groupindex');
	var node = $(this).data('nodeindex');
	app_nodes.delete_group(app_nodes.selected_node,group,node);
});
$('#copyParamsModal').off('show.bs.modal').on('show.bs.modal', function (e) {
	var modal = $(this);
	modal.find('.modal-body').html(' ');
	modal.find('.modal-title').text('{{Copier les paramètres pour le module}} ' + app_nodes.selected_node);
	var options_node = '<div><b>Node : </b>  <select class="form-control" id="newvaluenode" style="display:inline-block;width:400px;">';
	var foundIdentical=0;
	$.each(nodes, function(key, val) {
		if(key!=app_nodes.selected_node && val.description.product_name==nodes[app_nodes.selected_node].data.product_name.value){
			foundIdentical=1;
			if(val.description.name != ''){
				options_node +='<option value="'+key+'">'+key+' : '+val.description.location+' - '+val.description.name+'</option>';
			}else{
				options_node +='<option value="'+key+'">'+key+' : '+val.description.product_name+'</option>';
			}
		}
	});
	options_node += '</select></div>';
	if(foundIdentical==0){
		modal.find('#saveCopyParams').hide();
		options_node = '{{Aucun module identique trouvé}}';
	}
	modal.find('.modal-body').append(options_node);
});
$('#groupsModal').off('show.bs.modal').on('show.bs.modal', function (e) {
	var modal = $(this);
	var group = $(this).data('groupindex');
	var arr_exists_nodes=nodes[app_nodes.selected_node].groups[group].associations.split(';');
	modal.find('.modal-body').html(' ');
	modal.find('.modal-title').text('{{Groupe }}'+group+' : {{Ajouter une association pour le noeud}} ' + app_nodes.selected_node);
	var options_node = '<div><b>Node : </b>  <select class="form-control" id="newvaluenode" style="display:inline-block;width:400px;">';
	$.each(nodes, function(key, val) {
		if(arr_exists_nodes.indexOf(key)==-1 && key!=app_nodes.selected_node){
			if(val.description.name != ''){
				options_node +='<option value="'+key+'">'+key+' : '+val.description.location+' - '+val.description.name+'</option>';
			}else{
				options_node +='<option value="'+key+'">'+key+' : '+val.description.product_name+'</option>';
			}
		}
	});
	options_node += '</select></div>';
	modal.find('.modal-body').append(options_node);
});
$("#saveCopyParams").off("click").on("click",function (e) {
	var toNode = app_nodes.selected_node;
	var fromNode = $('#newvaluenode').val();
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+fromNode+"].CopyConfigurations("+toNode+")", 
		dataType: 'json',
		async: true, 
		error: function (request, status, error) {
			handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
		},
		success: function(data) {
			app_nodes.draw_nodes();
			app_nodes.load_data(true);
			app_nodes.show_groups();
			app_nodes.sendOk();
			$('#copyParamsModal').modal('hide');
		}
	});
});
$("#saveGroups").off("click").on("click",function (e) {
	var groupGroup = $('#groupsModal').data('groupindex');
	var groupNode = $('#newvaluenode').val();
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+app_nodes.selected_node+"].instances[0].commandClasses[0x85].Add("+groupGroup+","+groupNode+")", 
		dataType: 'json',
		async: true, 
		error: function (request, status, error) {
			handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
		},
		success: function(data) {
			app_nodes.draw_nodes();
			app_nodes.load_data(false);
			app_nodes.show_groups();
			app_nodes.sendOk();
			$('#groupsModal').modal('hide');
		}
	});
});
$("body").off("click",".editValue").on("click",".editValue",function (e) {
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
$('#valuesModal').off('show.bs.modal').on('show.bs.modal', function (e) {
	var valueIdx = $(this).data('valueidx');
	var valueType = $(this).data('valuetype');
	var valueInstance = $(this).data('valueinstance');
	var valueCc = $(this).data('valuecc');
	var valueName = $(this).data('valuename');
	var valueValue = $(this).data('valuevalue');
	var valueDataitems = $(this).data('valuedataitems').split(";");
	var modal = $(this);
	modal.find('.modal-title').text('{{Changer la valeur de}} ' + valueName);
	modal.find('.modal-body').html(valueName);
	modal.find('.modal-body').append('<b> : </b>');
	if(valueType == "List"){
		var options = '<select class="form-control" id="newvaluevalue" style="display:inline-block;width:400px;">';
		$.each(valueDataitems, function(key, val) {
			if(val==valueValue){
				options +='<option value="'+val+'" selected="selected">'+val+'</option>';
			}else{
				options +='<option value="'+val+'">'+val+'</option>';
			}
		});
		options += '</select>';
		modal.find('.modal-body').empty().append(options);

	}else if(valueType == "Bool"){
		if(valueValue==true){
			modal.find('.modal-body').append('<input type="radio" name="newvaluevalue" id="on" value="255" checked> {{ON}} ');
			modal.find('.modal-body').append('<input type="radio" name="newvaluevalue" id="off" value="0"> {{OFF}} ');
		}else{
			modal.find('.modal-body').append('<input type="radio" name="newvaluevalue" id="on" value="255"> {{ON}} ');
			modal.find('.modal-body').append('<input type="radio" name="newvaluevalue" id="off" value="0" checked> {{OFF}} ');
		}
	}else if(valueType == "Button"){
		modal.find('.modal-body').append('<input type="radio" name="newvaluevalue" id="push" value="Press" checked> {{Presser le bouton}} ');
		modal.find('.modal-body').append('<input type="radio" name="newvaluevalue" id="push" value="Release"> {{Relacher le bouton}} ');
	}else{
		modal.find('.modal-body').append('<input type="text" class="form-control" id="newvaluevalue" style="display:inline-block;width:400px;" value="'+valueValue+'">');
	}
});
$("body").off("click",".forceRefresh").on("click",".forceRefresh",function (e) {
	var index = $(this).attr('data-valueidx');
	var cc = $(this).attr('data-valuecc');
	$.ajax({ 
		url: path+"/ZWaveAPI/Run/devices["+app_nodes.selected_node+"].instances["+index+"].commandClasses["+cc+"].Get()", 
		dataType: 'json',
		async: true, 
		error: function (request, status, error) {
			handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
		},
		success: function(data) {
			app_nodes.sendOk();
		}
	});
});
$("body").off("click",".editPolling").on("click",".editPolling",function (e) {
	var idx = $(this).data('valueidx');
	var instance = $(this).data('valueinstance');
	var cc = $(this).data('valuecc');
	var polling = $(this).data('valuepolling');
	$('#pollingModal').data('valueinstance', instance);
	$('#pollingModal').data('valuecc', cc);
	$('#pollingModal').data('valuepolling', polling);
	$('#pollingModal').data('valueidx', idx).modal('show');
});
$('#pollingModal').off('show.bs.modal').on('show.bs.modal', function (e) {
	var valueIdx = $(this).data('valueidx');
	var valueInstance = $(this).data('valueinstance');
	var valueCc = $(this).data('valuecc');
	var valuePolling = $(this).data('valuepolling');
	var modal = $(this);
	modal.find('.modal-title').text('{{Changer le rafraichissement}}');
	modal.find('.modal-body').html("<b>{{Fréquence : }}</b>");
	var select = '<select class="form-control" style="display:inline-block;width : 200px;" id="newvaluevalue">';
	select += '<option value="0">{{Auto}}</option>';
	select += '<option value="1">{{30 min}}</option>';
	select += '<option value="2">{{15 min}}</option>';
	select += '<option value="3">{{10 min}}</option>';
	select += '<option value="6">{{5 min}}</option>';
	select += '<option value="30">{{1 min}}</option>';
	select += '</option>';
	modal.find('.modal-body').append(select);
	modal.find('.modal-body').find('#newvaluevalue').val(valuePolling);
});
$("body").off("click",".editParam").on("click",".editParam",function (e) {
	var id = $(this).data('paramid');
	var name = $(this).data('paramname');
	var value = $(this).data('paramvalue');
	var type = $(this).data('paramtype');
	$('#paramsModal').data('paramname', name);
	$('#paramsModal').data('paramtype', type);
	$('#paramsModal').data('paramvalue', value);
	$('#paramsModal').data('paramid', id).modal('show');
});
$('#paramsModal').off('show.bs.modal').on('show.bs.modal', function (e) {
	var paramId = $(this).data('paramid');
	var paramType = $(this).data('paramtype');
	var paramName = $(this).data('paramname');
	var paramValue = $(this).data('paramvalue');
	var modal = $(this);
	modal.find('.modal-title').text('{{Changer la valeur pour le paramètre}} ' + paramId);
	modal.find('.modal-body').html(paramName);
	modal.find('.modal-body').append('<b> : </b>');
	if(paramType == "List"){
		$.ajax({ 
			url: path+"ZWaveAPI/Run/devices["+app_nodes.selected_node+"].commandClasses[0x70].data", 
			dataType: 'json',
			async: true, 
			error: function (request, status, error) {
				handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
			},
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
				modal.find('.modal-body').empty().append(options);

			}
		});
	}else if(paramType == "Bool"){
		if(paramValue==true){
			modal.find('.modal-body').append('<input type="radio" name="newvalue" id="on" value="1" checked> {{ON}} ');
			modal.find('.modal-body').append('<input type="radio" name="newvalue" id="off" value="0"> {{OFF}} ');
		}else{
			modal.find('.modal-body').append('<input type="radio" name="newvalue" id="on" value="1"> {{ON}} ');
			modal.find('.modal-body').append('<input type="radio" name="newvalue" id="off" value="0" checked> {{OFF}} ');
		}
	}else if(paramType == "Button"){
		modal.find('.modal-body').append('<input type="radio" name="newvalue" id="push" value="Press" checked> {{Presser le bouton}} ');
		modal.find('.modal-body').append('<input type="radio" name="newvalue" id="push" value="Release"> {{Relacher le bouton}} ');
	}else{
		modal.find('.modal-body').append('<input type="text" class="form-control" id="newvalue" style="display:inline-block;width:400px;" value="'+paramValue+'">');
	}
});
$("#sendNodeInformation").off("click").on("click",function() {
	app_nodes.send_node_information(app_nodes.selected_node);
});
$("#saveParam").off("click").on("click",function (e) {
	var paramId = $('#paramsModal').data('paramid');
	var paramType = $('#paramsModal').data('paramtype');
	if(paramType == "Bool"){
		var paramValue = $('input[name=newvalue]:checked', '#paramsModal').val();
	}else if(paramType == "Button"){
		var paramValue = $('input[name=newvalue]:checked', '#paramsModal').val();
	}else{
		var paramValue = $('#newvalue').val();
	}
	var paramValue2 = paramValue.replace(/\//g,'@');
	var paramLength = paramValue.length;
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+app_nodes.selected_node+"].commandClasses[0x70].Set("+paramId+","+paramValue2+","+paramLength+")", 
		dataType: 'json',
		async: true, 
		error: function (request, status, error) {
			handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
		},
		success: function(data) {
			app_nodes.sendOk();
			app_nodes.load_data(false); 
			$('#paramsModal').modal('hide');
		}
	});
});
$("#applyValue").off("click").on("click",function (e) {
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
			error: function (request, status, error) {
				handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
			},
			success: function(data) {
				app_nodes.sendOk();
				$('#valuesModal').modal('hide');
				app_nodes.load_data(false); 
			}
		});
	}else if(valueType == "Raw"){
		$.ajax({ 
			url: path+"ZWaveAPI/Run/devices["+app_nodes.selected_node+"].UserCode.SetRaw("+valueIdx+",["+valueValue+"],1)", 
			dataType: 'json',
			async: true, 
			error: function (request, status, error) {
				handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
			},
			success: function(data) {
				app_nodes.sendOk();
				$('#valuesModal').modal('hide');
				app_nodes.load_data(false); 
			}
		});
	}
	else{
		$.ajax({ 
			url: path+"ZWaveAPI/Run/devices["+app_nodes.selected_node+"].instances["+valueInstance+"].commandClasses[0x"+Number(valueCc).toString(16)+"].data["+valueIdx+"].Set("+encodeURIComponent(valueValue)+")", 
			dataType: 'json',
			async: true, 
			error: function (request, status, error) {
				handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
			},
			success: function(data) {
				app_nodes.sendOk();
				$('#valuesModal').modal('hide');
				app_nodes.load_data(false); 
			}
		});
	}
});
$("#savePolling").off("click").on("click",function (e) {
	var valueIdx = $('#pollingModal').data('valueidx');
	var valueInstance = $('#pollingModal').data('valueinstance');
	var valueCc = $('#pollingModal').data('valuecc');
	var valueValue = $('#newvaluevalue').val();
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+app_nodes.selected_node+"].instances["+valueInstance+"].commandClasses[0x"+Number(valueCc).toString(16)+"].data["+valueIdx+"].SetPolling("+encodeURIComponent(valueValue)+")", 
		dataType: 'json',
		async: true, 
		error: function (request, status, error) {
			handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
		},
		success: function(data) {
			app_nodes.draw_nodes();
			app_nodes.load_data(false);
			app_nodes.sendOk();
			$('#pollingModal').modal('hide');
			app_nodes.draw_nodes();
		}
	});
});

},
sendOk : function(){
	$('#li_state').show();
	setTimeout(function(){ $('#li_state').hide(); }, 3000);
},
delete_group: function(node_id,group,node){
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].instances[0].commandClasses[0x85].Remove("+group+","+node+")", 
		dataType: 'json',
		async: true, 
		success: function(data) {
			app_nodes.draw_nodes();
			app_nodes.load_data(false);
			app_nodes.show_groups();
			app_nodes.sendOk();
		},
		error: function (request, status, error) {
			handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
		}
	});
},
request_node_neighbours_update: function(node_id){
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].RequestNodeNeighbourUpdate()", 
		dataType: 'json',
		async: true, 
		error: function (request, status, error) {
			handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
		},
		success: function(data) {
			if(data['result']== true){
				app_nodes.sendOk();
				app_nodes.load_data(false); 
			}else{
				$('#div_nodeConfigureOpenzwaveAlert').showAlert({message: 'Echec !', level: 'danger'});
			}
		}
	});
},
healNode: function(node_id){
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].HealNode()", 
		dataType: 'json',
		async: true, 
		error: function (request, status, error) {
			handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
		},
		success: function(data) {
			if(data['result']== true){
				app_nodes.sendOk();
				app_nodes.load_data(false); 
			}else{
				$('#div_nodeConfigureOpenzwaveAlert').showAlert({message: 'Echec !', level: 'danger'});
			}
		}
	});
},
test_node: function(node_id){
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].TestNetwork()", 
		dataType: 'json',
		async: true, 
		error: function (request, status, error) {
			handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
		},
		success: function(data) {
			app_nodes.sendOk();
			app_nodes.load_data(false); 
		}
	});
},
refresh_node_values: function(node_id){
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].RefreshAllValues()", 
		dataType: 'json',
		async: true, 
		error: function (request, status, error) {
			handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
		},
		success: function(data) {
			app_nodes.sendOk();
			app_nodes.load_data(false); 
		}
	});
},
request_node_dynamic: function(node_id){
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].RequestNodeDynamic()", 
		dataType: 'json',
		async: true, 
		error: function (request, status, error) {
			handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
		},
		success: function(data) {
			app_nodes.sendOk();
			app_nodes.load_data(false); 
		}
	});
},
refresh_node_info: function(node_id){
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].RefreshNodeInfo()", 
		dataType: 'json',
		async: true, 
		error: function (request, status, error) {
			handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
		},
		success: function(data) {
			if(data['result']== true){
				app_nodes.sendOk();
				app_nodes.load_data(false); 
			}else{
				$('#div_nodeConfigureOpenzwaveAlert').showAlert({message: 'Echec !', level: 'danger'});
			}
		}
	});
},
has_node_failed: function(node_id){
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].HasNodeFailed()", 
		dataType: 'json',
		async: true, 
		error: function (request, status, error) {
			handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
		},
		success: function(data) {
			app_nodes.sendOk();
			app_nodes.load_data(false); 
		}
	});
},
remove_failed_node: function(node_id){
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].RemoveFailedNode()", 
		dataType: 'json',
		async: true, 
		error: function (request, status, error) {
			handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
		},
		success: function(data) {
			if(data['result']== true){
				app_nodes.sendOk();
				app_nodes.load_data(false); 
			}else{
				$('#div_nodeConfigureOpenzwaveAlert').showAlert({message: 'Echec !', level: 'danger'});
			}
		}
	});
},
replace_failed_node: function(node_id){
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].ReplaceFailedNode()", 
		dataType: 'json',
		async: true, 
		error: function (request, status, error) {
			handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
		},
		success: function(data) {
			if(data['result']== true){
				app_nodes.sendOk();
				app_nodes.load_data(false); 
			}else{
				$('#div_nodeConfigureOpenzwaveAlert').showAlert({message: 'Echec !', level: 'danger'});
			}
		}
	});
},
send_node_information: function(node_id){
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].SendNodeInformation()", 
		dataType: 'json',
		async: true, 
		error: function (request, status, error) {
			handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
		},
		success: function(data) {
			app_nodes.sendOk();
			app_nodes.load_data(false); 
		}
	});
},
send_regenerate_node_cfg_file: function(node_id){
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].RemoveDeviceZWConfig()", 
		dataType: 'json',
		async: true, 
		error: function (request, status, error) {
			handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
		},
		success: function(data) {
			app_nodes.sendOk();
			app_nodes.load_data(false); 
		}
	});
},
load_all: function(){
	$.ajax({ 
		url: path+"ZWaveAPI/GetNodesList()", 
		dataType: 'json',
		global: false,
		async: true,     
		error: function (request, status, error) {
			handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
		},  
		success: function(data) {
			var node = nodes[node_id];
			nodes = data['devices'];
			nodes[node_id] = node;
			controller_id = -1;
			for(var i in data['devices']){
				if(data['devices'][i]['description']['is_static_controller']){
					controller_id = i;
				}
			}
			app_nodes.draw_nodes();
			app_nodes.show_groups();
		}
	});
},
load_data: function(_global){
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"]", 
		dataType: 'json',
		async: true, 
		global : _global,
		error: function (request, status, error) {
			handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
		},
		success: function(data) {
			if(Object.keys(nodes).length == 0){
				app_nodes.load_all();
			}
			nodes[node_id] = data;
			app_nodes.draw_nodes();
			app_nodes.show_groups();
		}
	});
},
load_stats: function(node_id){
	$.ajax({ 
		url: path+"ZWaveAPI/Run/devices["+node_id+"].GetNodeStatistics()", 
		dataType: 'json',
		async: true, 
		global : (typeof node_id !== 'undefined' && !isNaN(node_id)) ? false : true,
		error: function (request, status, error) {
			handleAjaxError(request, status, error,$('#div_nodeConfigureOpenzwaveAlert'));
		},
		success: function(data) {
			stats = data['statistics'];
			app_nodes.show_stats();
		}
	});
},
show: function(){
	if(typeof node_id !== 'undefined' && !isNaN(node_id)){
		app_nodes.selected_node = node_id;
	}else{
		app_nodes.selected_node = 1;
	}
},
hide: function()
{
	clearInterval(app_nodes.updater);
	openzwave_node_translation = null;
},

draw_nodes: function ()
{
	$("#node-nav").html("");
	var template_node = $("#template-node").html();
	var template_variable = $("#template-variable").html();
	var template_parameter = $("#template-parameter").html();
	var template_system = $("#template-system").html();
	var z = app_nodes.selected_node;
	if(nodes[z].data.isFailed){
		var nodeIsFailed = nodes[z].data.isFailed.value
	}else{
		var nodeIsFailed = false;
	}
	var queryStage = nodes[z].data.state.value;

	$("#node").attr("nid", z);
	            // select the copied block
	            var node = $(".node");
	            var isWarning = false;
	            
	            var warningMessage = "";
	            
	            node.find(".node-id").html(z);              // set the nodeid
	            if(nodes[z].data.name.value == ''){
	            	var name ='';
	            }else{
	            	var name = nodes[z].data.name.value;
	            }
	            var location = nodes[z].data.location.value;
	            var productName = nodes[z].data.product_name.value;
	            var manufacturerName = nodes[z].data.vendorString.value;
	            node.find(".node-productname").html(productName);
	            node.find(".node-location").html(location);
	            node.find(".node-name").html(name);
	            node.find(".node-vendor").html(manufacturerName);


	            node.find(".node-zwave-id").html("{{Identifiant du fabricant :}} <span class='label label-default'>" +nodes[z].data.manufacturerId.hex +"</span> {{type de produit :}} <span class='label label-default'>" +nodes[z].data.manufacturerProductType.hex + "</span> {{identifiant du produit :}} <span class='label label-default'>" + nodes[z].data.manufacturerProductId.hex+"</span>");            		

	            node.find(".node-lastSeen").html(app_nodes.timestampConverter(nodes[z].data.lastReceived.updateTime));


	            var basicDeviceClass = parseInt(nodes[z].data.basicType.value,0);
	            var basicDeviceClassDescription = "";	            
	            switch(basicDeviceClass){
	            	case 1:
	            	basicDeviceClassDescription = "{{Controlleur}}";
	            	break;
	            	case 2:
	            	basicDeviceClassDescription = "{{Controlleur static}}";
	            	break;
	            	case 3:
	            	basicDeviceClassDescription = "{{Esclave}}";
	            	break;
	            	case 4:
	            	basicDeviceClassDescription = "{{Esclave pouvant être routé}}";
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
	            genericDeviceClassDescription = "{{Télécommande}}";
	            break;
	            case 2: //STATIC_CONTROLLER   = 0x02,
	            genericDeviceClassDescription = "{{Controlleur statique}}";
	            break;
	            case 3: //AV_CONTROL_POINT    = 0x03,
	            genericDeviceClassDescription = "{{A/V controleur}}";
	            break;
	            case 4: //DISPLAY             = 0x04,
	            genericDeviceClassDescription = "{{Afficheur}}";
	            break;
	            case 7: //GARAGE_DOOR             = 0x07,
	            genericDeviceClassDescription = "{{Porte de garage}}";
	            break;
	            case 8: //THERMOSTAT          = 0x08,
	            genericDeviceClassDescription = "{{Thermostat}}";
	            break;
	            case 9: //WINDOW_COVERING     = 0x09,
	            genericDeviceClassDescription = "{{Fenêtre}}";
	            break;
	            case 15: //REPEATER_SLAVE      = 0x0f,
	            genericDeviceClassDescription = "{{Repéteur esclave}}";
	            break;
	            case 16: //BINARY_SWITCH       = 0x10,
	            genericDeviceClassDescription = "{{Interrupteur}}";
	            break;
	            case 17: //MULTILEVEL_SWITCH   = 0x11,
	            genericDeviceClassDescription = "{{Interrupteur multi niveau}}";
	            break;
	            case 18: //REMOTE_SWITCH       = 0x12,
	            genericDeviceClassDescription = "{{Interrupteur}}";
	            break;
	            case 19: // TOGGLE_SWITCH       = 0x13,
	            genericDeviceClassDescription = "{{Interrupteur}}";
	            break;
	            case 20: // Z_IP_GATEWAY       = 0x14,
	            genericDeviceClassDescription = "{{Z/IP Gateway}}";
	            break;
	            case 21: // Z_IP_NODE       = 0x15,
	            genericDeviceClassDescription = "{{Z/IP Node}}";
	            break;
	            case 22: //VENTILATION         = 0x16,
	            genericDeviceClassDescription = "{{Ventilation}}";
	            break;
	            case 30: //REMOTE_SWITCH2       = 0x18,
	            genericDeviceClassDescription = "{{Interrupteur}}";
	            break;
	            case 32: //BINARY_SENSOR       = 0x20,
	            genericDeviceClassDescription = "{{Capteur binaire}}";
	            break;
	            case 33: //MULTILEVEL_SENSOR   = 0x21
	            genericDeviceClassDescription = "{{Capteur multi niveau}}";
	            break;
	            case 34: //WATER_CONTROL   = 0x22
	            genericDeviceClassDescription = "{{Niveau d'eau}}";
	            break;
	            case 48: //PULSE_METER         = 0x30
	            genericDeviceClassDescription = "{{Mesure d'impulsion}}";
	            case 49: //METER         = 0x31
	            genericDeviceClassDescription = "{{Mesure}}";
	            break;
	            case 64: //ENTRY_CONTROL       = 0x40
	            genericDeviceClassDescription = "{{Controle d'entrée}}";
	            break;
	            case 85: //NON_INTEROPERABLE        = 0x55
	            genericDeviceClassDescription = "{{Semi-Interoperable}}";
	            break;
	            case 161: //ALARM_SENSOR        = 0xa1
	            genericDeviceClassDescription = "{{Alarme}}";
	            break;
	            case 255: //NON_INTEROPERABLE        = 0xff
	            genericDeviceClassDescription = "{{Non-Interoperable}}";
	            break;	
	            default:
	            genericDeviceClassDescription = "{{Inconnue}}";
	            break;
	        }

	        var specificDeviceClass = parseInt(nodes[z].data.specificType.value,0);
	        var specificDeviceClassDescription = nodes[z].data.type.value;	            

	        node.find(".node-basic").html(basicDeviceClassDescription);
	        node.find(".node-generic").html(genericDeviceClassDescription);
	        node.find(".node-specific").html(specificDeviceClassDescription);
	        var battery_level = nodes[z].data.battery_level.value
	        var nodeCanSleep = nodes[z].data.can_wake_up.value;
	        if (battery_level != null){
	        	if(nodeCanSleep){
	        		if(nodes[z].data.isAwake.value){
	        			node.find(".node-sleep").html("{{Réveillé}}");
	        		}
	        		else{
	        			node.find(".node-sleep").html("{{Endormi}}");
	        		}
	        	}else{
	        		node.find(".node-sleep").html("{{Endormi}}");
	        	}
	        }
	        else{
	        	node.find(".node-sleep").html("{{Secteur}}");
	        }
	        

	        if(controller_id != -1){
	        	var node_groups=nodes[z].groups;
	        	var found=0;
	        	var hasGroup = false;
	        	for (zz in node_groups){
	        		if (!isNaN(zz)){
	        			hasGroup = true;
	        			var values=node_groups[zz].associations.split(';');
	        			tr_groups="";
	        			for(val in values){
	        				if(values.length > 0 && values[val]!=""){
	        					var node_id=values[val];
	        					if (node_id==controller_id){
	        						found=1;
	        					}
	        				}
	        			}
	        		}
	        	}
	        	if(hasGroup && found==0){
	        		isWarning = true;
	        		warningMessage +="<li>{{Le controleur n'est inclus dans aucun groupe du module.}}</li>";
	        	}
	        }
	        if(nodeIsFailed){
	            	//this warning must stay in place
	            	isWarning = true;
	            	warningMessage +="<li>{{Le controleur pense que ce noeud est en echec, essayez }} <button type='button' id='hasNodeFailed_summary' class='btn btn-xs btn-primary hasNodeFailed'><i class='fa fa-question'></i> {{Noeud en échec}}</button> {{ou}} <button type='button' id='testNode' class='btn btn-info'><i class='fa fa-check-square-o'></i> {{Tester Noeud}}</button> {{pour essayer de corriger.}}</li>";
	            }
	            
	            var queryStageDescrition = "";
	            var queryStageIndex = 0;	            
	            switch(queryStage){
	            	case "None":
	            	queryStageDescrition = "{{Le processus de demande n'a pas encore commencé pour ce noeud}}";
	            	queryStageIndex = 0;
	            	break;
	            	case "ProtocolInfo":
	            	queryStageDescrition = "{{Récupération des informations du protocole}}";
	            	queryStageIndex = 1;
	            	break;
	            	case "Probe":
	            	queryStageDescrition = "{{Interrogation du module pour voir sil est en vie}}";
	            	queryStageIndex = 2;
	            	break;
	            	case "WakeUp":
	            	queryStageDescrition = "{{Début du processus de reveil du noeud si celui-ci dort}}";
	            	queryStageIndex = 3;
	            	break;
	            	case "ManufacturerSpecific1":
	            	queryStageDescrition = "{{Récupération des paramètres constructeur du noeud}}";
	            	queryStageIndex = 4;
	            	break;
	            	case "NodeInfo":
	            	queryStageDescrition = "{{Récupération des informations sur les classes du noeud}}";
	            	queryStageIndex = 5;
	            	break;
	            	case "SecurityReport":
	            	queryStageDescrition = "{{Récupération des classes de sécurité du noeud}}";
	            	queryStageIndex = 6;
	            	break;
	            	case "ManufacturerSpecific2":
	            	queryStageDescrition = "{{Récupération des paramètres constructeur du noeud}}";
	            	queryStageIndex = 7;
	            	break;
	            	case "Versions":
	            	queryStageDescrition = "{{Récupération des informations de version}}";
	            	queryStageIndex = 8;
	            	break;
	            	case "Instances":
	            	queryStageDescrition = "{{Récupération des informations d'instance du noeud}}";
	            	queryStageIndex = 9;
	            	break;
	            	case "Static":
	            	queryStageDescrition = "{{Récupération des informations statistiques}}";
	            	queryStageIndex = 10;
	            	break;
	            	case "Probe1":
	            	queryStageDescrition = "{{Intérrogation du module pour récupérer sa configuration}}";
	            	queryStageIndex = 11;
	            	break;
	            	case "Associations":
	            	queryStageDescrition = "{{Récupération des informations d'associations}}";
	            	queryStageIndex = 12;
	            	break;
	            	case "Neighbors":
	            	queryStageDescrition = "{{Récupération de la liste des voisins}}";
	            	queryStageIndex = 13;
	            	break;
	            	case "Session":
	            	queryStageDescrition = "{{Récupération des informations de sessions}}";
	            	queryStageIndex = 14;
	            	break;
	            	case "Dynamic":
	            	queryStageDescrition = "{{Récupération des informations dynamique}}";
	            	queryStageIndex = 15;
	            	break;
	            	case "Configuration":
	            	queryStageDescrition = "{{Récupération des informations de configuration}}";
	            	queryStageIndex = 16;
	            	break;
	            	case "Complete":
	            	queryStageDescrition = "{{Processus de demande d'information sur le noeud complet}}";
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
	            if(nodes[z].data.isRouting.value){
	            	node.find(".node-routing").html("<li>{{Le noeud a des capacités de routage (capable de faire passer des commandes à d'autres noeuds)}}</li>");
	            }
	            else{
	            	node.find(".node-routing").html("");
	            }
	            if(nodes[z].data.isSecurity.value){
	            	node.find(".node-isSecurity").html("<li>{{Le noeud supporte les caracteristiques de sécurité avancées}}</li>");
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
	            	node.find(".node-security").html("{{Classe de sécurité:}} " + nodes[z].data.security.value);
	            }
	            else{
	            	node.find(".node-isSecurity").html("");
	            	node.find(".node-security").html("");
	            }
	            if(nodes[z].data.isListening.value){
	            	node.find(".node-listening").html("<li>{{Le noeud est alimenté et écoute en permanence}}</li>");
	            }	
	            else{
	            	node.find(".node-listening").html("");
	            }
	            if(nodes[z].data.isFrequentListening.value){
	            	node.find(".node-isFrequentListening").html("<li>{{Le noeud peut être reveillé}}</li>");
	            }
	            else{
	            	node.find(".node-isFrequentListening").html("");	
	            }
	            if(nodes[z].data.isBeaming.value){
	            	node.find(".node-isBeaming").html("<li>{{Le noeud est capable d'envoyer une trame réseaux}}</li>");
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
	            		if(genericDeviceClass != 1){
	            			warningMessage +="<li{{Liste des voisins non disponible}} <br/>{{Utilisez}} <button type='button' id='healNode' class='btn btn-success healNode'><i class='fa fa-medkit'></i> {{Soigner le noeud}}</button> {{ou}} <button type='button' id='requestNodeNeighboursUpdate' class='btn btn-primary requestNodeNeighboursUpdate'><i class='fa fa-sitemap'></i> {{Mise à jour des noeuds voisins}}</button> {{pour corriger.}}</li>";		            	
	            			isWarning = true;
	            		}
	            	}
	            }
	            else{  
	            	node.find(".node-neighbours").html("<i>{{La liste des noeuds voisin n'est pas encore disponible.}}</i>");
	            }
	            if (queryStageIndex > 7 & productName == ""){
	            	
	            	warningMessage +="<li>{{Les identifiants constructeur ne sont pas detectés.}}<br/>{{Utilisez}} <button type='button' id='refreshNodeInfo' class='btn btn-success refreshNodeInfo'><i class='fa fa-retweet'></i> {{Rafraîchir infos du noeud}}</button> {{pour corriger}}</li>";
	            	isWarning = true;	
	            }	
	            
	            if (isWarning){ 
	            	if (nodeCanSleep){
	            		warningMessage += "<br><p>{{Le noeud est dormant et nécessite un reveil avant qu'une commande puisse être exécutée.<br/>Vous pouvez le reveiller manuellement ou attendre son délai de réveil.}}<br/>{{Voir l'interval de réveil dans l'onglet Système}}</p>";	            		
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
	            					var pending_state = nodes[z].instances[instance].commandClasses[commandclass].data[index].pendingState;
	            					switch(pending_state){
	            						case 1:
	            						parameters += "<tr class='greenrow' pid='"+id+"'>"+template_parameter+"</tr>"; 
	            						break;
	            						case 2:
	            						parameters += "<tr class='redrow' pid='"+id+"'>"+template_parameter+"</tr>"; 
	            						break;
	            						case 3:
	            						parameters += "<tr class='yellowrow' pid='"+id+"'>"+template_parameter+"</tr>"; 
	            						break;
	            						default:
	            						parameters += "<tr pid='"+id+"'>"+template_parameter+"</tr>";
	            					}
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
	            if(typeof openzwave_node_translation === 'undefined' ||  openzwave_node_translation == null){
	            	openzwave_node_translation = app_nodes.get_translation();
	            }
	            if(typeof openzwave_node_translation.configuration === 'undefined'){
	            	openzwave_node_translation = {configuration : {}};
	            }
	            for (instance in nodes[z].instances){
	            	for (commandclass in nodes[z].instances[instance].commandClasses){
	            		for (index in nodes[z].instances[instance].commandClasses[commandclass].data){
	            			var id=instance+":"+commandclass+":"+index;
	            			var row = node.find("tr[vid='"+id+"']");
	            			var row_parameter = node.find("tr[pid='"+id+"']");
	            			var row_system = node.find("tr[sid='"+id+"']");
	            			row.find("td[key=variable-instance]").html(instance);
	            			row.find("td[key=variable-cc]").html(commandclass+' (0x'+Number(commandclass).toString(16)+')');
	            			row.find("td[key=variable-index]").html(index);
	            			row.find("td[key=variable-name]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].name);
	            			row.find("td[key=variable-type]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].typeZW+' ('+nodes[z].instances[instance].commandClasses[commandclass].data[index].type+')');
	            			var value = '';

	            			if(nodes[z].instances[instance].commandClasses[commandclass].data[index].read_only==false){
	            				value += '<button type="button" class="btn btn-xs btn-primary editValue" data-valueidx="'+index+'" data-valueinstance="'+instance+'" data-valuecc="'+commandclass+'" data-valuedataitems="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].data_items+'" data-valuetype="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].typeZW+'" data-valuename="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].name+'" data-valuevalue="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].val+'"><i class="fa fa-wrench"></i></button> ';
	            			}




	            			value += nodes[z].instances[instance].commandClasses[commandclass].data[index].val +" "+ nodes[z].instances[instance].commandClasses[commandclass].data[index].units;
	            			row.find("td[key=variable-value]").html(value);
	            			var polling = '<span style="width : 22px;"></span>';
	            			
	            			if(nodes[z].instances[instance].commandClasses[commandclass].data[index].write_only==false){
	            				if(nodes[z].data.isListening.value){
	            					var polling = '<a style="position:relative;top:-1px;" class="btn btn-primary btn-xs editPolling cursor" data-valueidx="'+index+'" data-valuepolling="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].poll_intensity+'" data-valueinstance="'+instance+'" data-valuecc="'+commandclass+'" data-valuedataitems="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].data_items+'" data-valuetype="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].typeZW+'" data-valuename="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].name+'" data-valuevalue="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].val+'"><i class="fa fa-wrench"></i></a> ';
	            				}
	            				row.find("td[key=variable-refresh]").html('<button type="button" class="btn btn-xs btn-primary forceRefresh" data-valueidx="'+index+'" data-valueinstance="'+instance+'" data-valuecc="'+commandclass+'" data-valuedataitems="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].data_items+'" data-valuetype="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].typeZW+'" data-valuename="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].name+'" data-valuevalue="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].val+'"><i class="fa fa-refresh"></i></button>');
	            			}
	            			if(nodes[z].instances[instance].commandClasses[commandclass].data[index].poll_intensity == 0){
	            				polling += '<span class="label label-success" style="font-size:1em;">{{Auto}}</span>';
	            			}else if(nodes[z].instances[instance].commandClasses[commandclass].data[index].poll_intensity == 1){
	            				polling += '<span class="label label-success" style="font-size:1em;">{{30 min}}</span>';
	            			}else if(nodes[z].instances[instance].commandClasses[commandclass].data[index].poll_intensity == 2){
	            				polling += '<span class="label label-success" style="font-size:1em;">{{15 min}}</span>';
	            			}else if(nodes[z].instances[instance].commandClasses[commandclass].data[index].poll_intensity == 3){
	            				polling += '<span class="label label-warning" style="font-size:1em;">{{10 min}}</span>';
	            			}else if(nodes[z].instances[instance].commandClasses[commandclass].data[index].poll_intensity == 6){
	            				polling += '<span class="label label-warning" style="font-size:1em;">{{5 min}}</span>';
	            			}else if(nodes[z].instances[instance].commandClasses[commandclass].data[index].poll_intensity == 30){
	            				polling += '<span class="label label-danger" style="font-size:1em;">{{1 min}}</span>';
	            			}else{
	            				polling += '<span class="label label-default" style="font-size:1em;">'+nodes[z].instances[instance].commandClasses[commandclass].data[index].poll_intensity+'</span>';
	            			}
	            			row.find("td[key=variable-polling]").html(polling);
	            			row.find("td[key=variable-updatetime]").html(app_nodes.timestampConverter(nodes[z].instances[instance].commandClasses[commandclass].data[index].updateTime));

	            			row_system.find("td[key=system-instance]").html(instance);
	            			row_system.find("td[key=system-cc]").html(commandclass+' (0x'+Number(commandclass).toString(16)+')');
	            			row_system.find("td[key=system-index]").html(index);
	            			row_system.find("td[key=system-name]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].name);
	            			row_system.find("td[key=system-type]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].typeZW+' ('+nodes[z].instances[instance].commandClasses[commandclass].data[index].type+')');
	            			row_system.find("td[key=system-value]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].val +" "+ nodes[z].instances[instance].commandClasses[commandclass].data[index].units);
	            			if(nodes[z].instances[instance].commandClasses[commandclass].data[index].read_only==false){
	            				row_system.find("td[key=system-edit]").html('<button type="button" class="btn btn-xs btn-primary editValue" data-valueidx="'+index+'" data-valueinstance="'+instance+'" data-valuecc="'+commandclass+'" data-valuedataitems="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].data_items+'" data-valuetype="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].typeZW+'" data-valuename="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].name+'" data-valuevalue="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].val+'"><i class="fa fa-wrench"></i></button>');
	            			}
	            			row_system.find("td[key=system-updatetime]").html(app_nodes.timestampConverter(nodes[z].instances[instance].commandClasses[commandclass].data[index].updateTime));
	            			if(typeof openzwave_node_translation.configuration[index] === 'undefined' ){
	            				row_parameter.find("td[key=parameter-name]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].name);
	            			}else{
	            				row_parameter.find("td[key=parameter-name]").html(openzwave_node_translation['configuration'][index].name);
	            			}
	            			row_parameter.find("td[key=parameter-index]").html(index);

	            			row_parameter.find("td[key=parameter-type]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].typeZW);
	            			row_parameter.find("td[key=parameter-value]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].val);
	            			row_parameter.find("td[key=parameter-edit]").html('<button type="button" class="btn btn-xs btn-primary editParam" data-paramid="'+index+'" data-paramtype="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].typeZW+'" data-paramname="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].name+'" data-paramvalue="'+nodes[z].instances[instance].commandClasses[commandclass].data[index].val+'"><i class="fa fa-wrench"></i></button>');
	            			if(typeof openzwave_node_translation.configuration[index] === 'undefined' ){
	            				row_parameter.find("td[key=parameter-help]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].help);
	            			}else{
	            				row_parameter.find("td[key=parameter-help]").html(openzwave_node_translation['configuration'][index].help);
	            			}
	            		}
	            	}
	            }


	        },
	        get_translation : function(){
	        	if(typeof node_id === 'undefined' || isNaN(node_id)){
	        		return {configuration : {}};
	        	}
	        	var result = {configuration : {}};
	        	$.ajax({ 
	        		url: "plugins/openzwave/core/ajax/openzwave.ajax.php", 
	        		dataType: 'json',
	        		async: false, 
	        		global : false,
	        		data: {
	        			action: "getConfiguration",
	        			translation : 1,
	        			manufacturer_id:nodes[node_id].data.manufacturerId.value,
	        			product_type: nodes[node_id].data.manufacturerProductType.value,
	        			product_id: nodes[node_id].data.manufacturerProductId.value,
	        		},
	        		success: function(data) {
	        			result = data.result;
	        		}
	        	});
	        	return result;
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
	        						if(nodes[node_id].description.name != ''){
	        							var node_name = nodes[node_id].description.location+' '+nodes[node_id].description.location;
	        						}else{
	        							var node_name=nodes[node_id].description.product_name;
	        						}
	        					}else{
	        						var node_name="UNDEFINED";
	        					}
	        					tr_groups += "<tr gid='"+id+"'><td>"+node_id+" : "+node_name+"</td><td align='right'><button type='button' class='btn btn-danger btn-sm deleteGroup' data-groupindex='"+z+"' data-nodeindex='"+node_id+"'><i class='fa fa-trash-o'></i> {{Supprimer}}</button></td></tr>";
	        				}
	        			}
	        			if(values.length < node_groups[z].maximumAssociations || values[val]==""){
	        				var newPanel = '<div class="panel panel-primary template"><div class="panel-heading"><div class="btn-group pull-right"><a id="addGroup" class="btn btn-info btn-sm addGroup" data-groupindex="'+z+'"><i class="fa fa-plus"></i> {{Ajouter un noeud}}</a></div><h3 class="panel-title" style="padding-top:10px;">'+z+' : '+node_groups[z].label+' {{(nombre maximum d\'association :}} '+node_groups[z].maximumAssociations+')</h3></div><div class="panel-body"><table class="table">'+tr_groups+'</table></div></div>';
	        			}else{
	        				var newPanel = '<div class="panel panel-primary template"><div class="panel-heading"><div class="btn-group pull-right"><a id="addGroup" class="btn btn-info btn-sm addGroup" disabled data-groupindex="'+z+'"><i class="fa fa-plus"></i> {{Ajouter un noeud}}</a></div><h3 class="panel-title" style="padding-top:10px;">'+z+' : '+node_groups[z].label+' {{(nombre maximum d\'association :}} '+node_groups[z].maximumAssociations+')</h3></div><div class="panel-body"><table class="table">'+tr_groups+'</table></div></div>';
	        			}
	        			$("#groups").append(newPanel);
	        		}
	        	}
	        },
	    }

var app_nodes = {
    selected_node: 0,
    updater: false,
    timestampConverter: function (time) {
        if (time == 1)
            return "N/A";
        var ret;
        var date = new Date(time * 1000);
        var hours = date.getHours();
        if (hours < 10) {
            hours = "0" + hours;
        }
        var minutes = date.getMinutes();
        if (minutes < 10) {
            minutes = "0" + minutes;
        }
        var seconds = date.getSeconds();
        if (seconds < 10) {
            seconds = "0" + seconds;
        }
        var num = date.getDate();
        if (num < 10) {
            num = "0" + num;
        }
        var month = date.getMonth() + 1;
        if (month < 10) {
            month = "0" + month;
        }
        var year = date.getFullYear();
        var formattedTime = hours + ':' + minutes + ':' + seconds;
        var formattedDate = num + "/" + month + "/" + year;
        return formattedDate + ' ' + formattedTime;
    },
    init: function () {
        controller_id = -1
        app_nodes.load_data(true);
        app_nodes.updater = setInterval(function () {
            if ($('#template-node').is(':visible')) {
                app_nodes.load_data(false);
            } else {
                app_nodes.hide();
            }
        }, 2000);
        $('#node-queryStageDescrition').popover({title: '', placement: 'right', trigger: 'hover'});
        $("#tab-parameters").off("click").on("click", function () {
            if (!nodes[app_nodes.selected_node].instances[0].commandClasses[112]) {
                $("#parameters").html('<br><div><b>{{Aucun paramètre prédefini trouvé pour ce noeud}}</b></div><br>');
                $("#parameters").append('<div class="row"><label class="col-lg-2">{{Paramètre :}} </label><div class="col-lg-1"><input type="text" class="form-control" id="paramidperso"></div><label class="col-lg-1">{{Valeur :}} </label><div class="col-lg-1"><input type="text" class="form-control" id="newvalueperso"></div><label class="col-lg-1">{{Taile :}}</label><div class="col-lg-1"><input type="text" class="form-control" id="sizeperso"></div> <div class="col-lg-2"><button id="sendparamperso" class="btn btn-primary">{{Envoyer le paramètre}}</a></div></div>');
                $("#sendparamperso").off("click").on("click", function () {
                    var paramId = $("#paramidperso").val();
                    var paramValue = $('#newvalueperso').val();
                    var paramLength = $('#sizeperso').val();
                    $.ajax({
                        url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + app_nodes.selected_node + "].commandClasses[0x70].Set(" + paramId + "," + paramValue + "," + paramLength + ")",
                        dataType: 'json',
                        async: true, error: function (request, status, error) {
                            handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
                        },
                        success: function (data) {
                            app_nodes.sendOk();
                        }
                    });
                });
            }
        });
        $("#tab-groups").off("click").on("click", function () {
            app_nodes.show_groups();
        });
        $("#tab-stats").off("click").on("click", function () {
            app_nodes.load_stats(app_nodes.selected_node);
        });
        $("body").off("click", ".requestNodeNeighboursUpdate").on("click", ".requestNodeNeighboursUpdate", function (e) {
            app_nodes.request_node_neighbours_update(app_nodes.selected_node);
        });
        $("body").off("click", ".healNode").on("click", ".healNode", function (e) {
            app_nodes.healNode(app_nodes.selected_node);
        });
        $("body").off("click", ".assignReturnRoute").on("click", ".assignReturnRoute", function (e) {
            app_nodes.assign_return_route_node(app_nodes.selected_node);
        });
        $("#refreshNodeValues").off("click").on("click", function () {
            app_nodes.refresh_node_values(app_nodes.selected_node);
        });
        $("#requestNodeDynamic").off("click").on("click", function () {
            app_nodes.request_node_dynamic(app_nodes.selected_node);
        });
        $("body").off("click", ".refreshNodeInfo").on("click", ".refreshNodeInfo", function (e) {
            app_nodes.refresh_node_info(app_nodes.selected_node);
        });
        $("body").off("click", ".hasNodeFailed").on("click", ".hasNodeFailed", function (e) {
            app_nodes.has_node_failed(app_nodes.selected_node);
        });
        $("body").off("click", ".testNode").on("click", ".testNode", function (e) {
            app_nodes.test_node(app_nodes.selected_node);
        });
        $("#removeFailedNode").off("click").on("click", function () {
            app_nodes.remove_failed_node(app_nodes.selected_node);
        });
        $("#removeGhostNode").off("click").on("click", function () {
            bootbox.dialog({
                    title: "{{Suppression automatique du nœud fantôme}}",
                    message: '<form class="form-horizontal"> ' +
                    '<label class="control-label" > {{Les étapes suivantes seront éxécutées:}} </label> ' +
                    '<br>' +
                    '<ul>' +
                    '<li class="active">{{Arrêt du réseau Z-Wave.}}</li>' +
                    '<li class="active">{{Retirer classe de commande de Wake Up du fichier ZWCFG.}}</li>' +
                    '<li class="active">{{Redémarrage du réseau Z-Wave.}}</li>' +
                    '<li class="active">{{Attendre que le réseau soit à nouveau opérationnel (2-5 minutes).}}</li>' +
                    '<li class="active">{{Nœud passe en échec}}</li>' +
                    '<li class="active">{{Supprimer le nœud en échec}}</li>' +
                    '<li class="active">{{Validation de la suppression}}</li>' +
                    '</ul>' +
                    '<label class="lbl lbl-warning" for="name">{{Attention, cette action entraîne un redémarrage de votre réseau.}}</label> ' +
                    '</form>',
                    buttons: {
                        main: {
                            label: "{{Annuler}}",
                            className: "btn-danger"
                        },
                        success: {
                            label: "{{Lancer}}",
                            className: "btn-success",
                            callback: function () {
                                app_nodes.remove_ghost_node(app_nodes.selected_node);
                            }
                        }
                    }
                }
            );
        });
        $("#replaceFailedNode").off("click").on("click", function () {
            bootbox.dialog({
                    title: "{{Remplacer nœud en échec}}",
                    message: '<form class="form-horizontal"> ' +
                    '<label class="control-label" > {{Cette action permet de remplacer un nœud en échec.}} </label> ' +
                    '<br>' +
                    '<label class="lbl lbl-warning" for="name">{{Attention, le controleur sera automatiquement en mode inclusion. Veuillez lancer la procédure sur votre module après la confirmation de cette action.}}</label> ' +
                    '</form>',
                    buttons: {
                        main: {
                            label: "{{Annuler}}",
                            className: "btn-danger"
                        },
                        success: {
                            label: "{{Remplacer}}",
                            className: "btn-success",
                            callback: function () {
                                app_nodes.replace_failed_node(app_nodes.selected_node);
                            }
                        }
                    }
                }
            );
        });
        $("#sendNodeInformation").off("click").on("click", function () {
            app_nodes.send_node_information(app_nodes.selected_node);
        });
        $("#regenerateNodeCfgFile").off("click").on("click", function () {
            var productName = nodes[app_nodes.selected_node].data.product_name.value;
            var manufacturerName = nodes[app_nodes.selected_node].data.vendorString.value;
            bootbox.dialog({
                    title: "{{Régénérer la détection du nœud}}",
                    message: '<form class="form-horizontal"> ' +
                    '<label class="control-label" > {{Lancer la regénérer sur ?}} </label> ' +
                    '<div> <div class="radio"> <label > ' +
                    '<input type="radio" name="awesomeness" id="awesomeness-1" value="0" checked="checked"> {{Ce module seulement}} </label> ' +
                    '</div><div class="radio"> <label > ' +
                    '<input type="radio" name="awesomeness" id="awesomeness-0" value="1"> ' +
                    ' {{Tous les modules}} <b>' + manufacturerName + ' ' + productName + '</b></label> ' +
                    '</div> ' +
                    '</div><br>' +
                    '<label class="lbl lbl-warning" for="name">{{Attention, cette action entraîne un redémarrage de votre réseau.}}</label> ' +
                    '</form>',
                    buttons: {
                        main: {
                            label: "{{Annuler}}",
                            className: "btn-danger",
                            callback: function () {
                            }
                        },
                        success: {
                            label: "{{Lancer}}",
                            className: "btn-success",
                            callback: function () {
                                var all = $("input[name='awesomeness']:checked").val()
                                app_nodes.send_regenerate_node_cfg_file(app_nodes.selected_node, all);
                            }
                        }
                    }
                }
            );
        });
        $("body").off("click", ".copyParams").on("click", ".copyParams", function (e) {
            $('#copyParamsModal').modal('show');
        });
        $("body").off("click", ".copyToParams").on("click", ".copyToParams", function (e) {
            $('#copyToParamsModal').modal('show');
        });
        $("body").off("click", ".refreshParams").on("click", ".refreshParams", function (e) {
            app_nodes.refresh_parameters(app_nodes.selected_node);
        });
        $("body").off("click", ".addGroup").on("click", ".addGroup", function (e) {
            var group = $(this).data('groupindex');
            if(group == -1){
                return;
            }
            $('#groupsModal').data('groupindex', group);
            $('#groupsModal').modal('show');
        });
        $("body").off("click", ".deleteGroup").on("click", ".deleteGroup", function (e) {
            var group = $(this).data('groupindex');
            var node = $(this).data('nodeid');
            var instance = $(this).data('nodeinstance');
            console.log('deleteGroup group:' + group + ' node:' + node + ' instance:' + instance);
            app_nodes.delete_group(app_nodes.selected_node, group, node, instance);
        });
        $("body").off("click", ".findUsage").on("click", ".findUsage", function (e) {
            var associations = nodes[app_nodes.selected_node].associations;
            var description = nodes[app_nodes.selected_node].data.name.value;
            var message = '<form class="form-horizontal"><div class="panel-body"> ' +
                '<p  style="font-size : 1em;"> {{Liste des groupes d\'associations où le module }} <b><span class="node-name label label-default" style="font-size : 1em;">' + description + '</span></b> {{est utilisé:}} </p> ' +
                '<br>' +
                '<ul>';
            $.each(associations, function (key, val) {
                message += '<li class="active"><p>';
                if (nodes[key].description.name != '') {
                    message += nodes[key].description.location + ' - <b>' + nodes[key].description.name + '</b>';
                } else {
                    message += '<b>' + nodes[key].description.product_name + '</b>';
                }
                message += '<br><ul class="fa-ul">'
                $.each(val, function (key2, val2) {
                    message += '<li><i class="fa fa-arrow-right btn-success" aria-hidden="true"></i>  ' + val2.label + ' (' + val2.index + ')</li>';
                });
                message += '</ul></p></li>';
            })
            message += '</ul>' +
                '</div></form>';
            bootbox.dialog({
                    title: "{{Associé via quels modules}}",
                    message: message,
                    buttons: {
                        main: {
                            label: "{{OK}}",
                            className: "btn-success"
                        }
                    }
                }
            );
        });
        $('#copyParamsModal').off('show.bs.modal').on('show.bs.modal', function (e) {
            var modal = $(this);
            modal.find('.modal-body').html(' ');
            modal.find('.modal-title').text('{{Sélection du module source}}');
            var options_node = '<div class="row"><div class="col-md-2"><b>{{Source}}</b></div>';
            options_node += '<div class="col-md-10"><select class="form-control" id="newvaluenode" style="display:inline-block;width:400px;">';
            var foundIdentical = 0;
            $.each(nodes, function (key, val) {
                var manufacturerId = nodes[app_nodes.selected_node].data.manufacturerId.value;
                var manufacturerProductId = nodes[app_nodes.selected_node].data.manufacturerProductId.value;
                var manufacturerProductType = nodes[app_nodes.selected_node].data.manufacturerProductType.value;
                if (key != app_nodes.selected_node && val.product.is_valid &&
                    val.product.manufacturer_id == manufacturerId &&
                    val.product.product_id == manufacturerProductId &&
                    val.product.product_type == manufacturerProductType) {
                    foundIdentical = 1;
                    options_node += '<option value="' + key + '">' + key + ' ';
                    if (val.description.name != '') {
                        options_node +=  val.description.location + ' - ' + val.description.name;
                    } else {
                        options_node += val.description.product_name;
                    }
                    options_node += '</option>';
                }
            });
            options_node += '</select></div></div>';
            options_node += '<br>';
            options_node += '<div class="row"><div class="col-md-2"><b>{{Destination}}</b></div>';
            options_node += '<div class="col-md-10">';
            options_node += app_nodes.selected_node + ' ';
            if (nodes[app_nodes.selected_node].data.name.value != '') {
                options_node += nodes[app_nodes.selected_node].data.location.value + ' - ' + nodes[app_nodes.selected_node].data.name.value;
            }
            else {
                options_node += nodes[app_nodes.selected_node].data.product_name.value;
            }
            options_node += '</div>';
            options_node += '</div>';
            if (foundIdentical == 0) {
                modal.find('#saveCopyParams').hide();
                options_node = '{{Aucun module identique trouvé}}';
            }
            modal.find('.modal-body').append(options_node);
        });
        $("#saveCopyParams").off("click").on("click", function (e) {
            var toNode = app_nodes.selected_node;
            var fromNode = $('#newvaluenode').val();
            $.ajax({
                url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + fromNode + "].CopyConfigurations(" + toNode + ")",
                dataType: 'json',
                async: true,
                error: function (request, status, error) {
                    handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
                },
                success: function (data) {
                    app_nodes.draw_nodes();
                    app_nodes.load_data(true);
                    app_nodes.show_groups();
                    app_nodes.sendOk();
                    $('#copyParamsModal').modal('hide');
                }
            });
        });
        $('#copyToParamsModal').off('show.bs.modal').on('show.bs.modal', function (e) {
            var modal = $(this);
            modal.find('.modal-body').html(' ');
            modal.find('.modal-title').text('{{Sélection des modules a appliquer ces paramètres}}');
            var options_node = '<div class="container-fluid">';
            options_node += '<div class="row"><div class="col-md-2"><b>{{Source}}</b></div>';
            options_node += '<div class="col-md-10">  ' + app_nodes.selected_node + ' ';
            if (nodes[app_nodes.selected_node].data.name.value != '') {
                options_node += nodes[app_nodes.selected_node].data.location.value + ' ' + nodes[app_nodes.selected_node].data.name.value;
            }
            else {
                options_node += nodes[app_nodes.selected_node].data.product_name.value;
            }
            options_node += '</div></div><br>';
            options_node +=  '<div class="row"><div class="col-md-2"><b>{{Destination}}</b></div><div class="col-md-10">(' + nodes[app_nodes.selected_node].data.product_name.value +')</div></div>';
            options_node += '<form name="targetForm" action="" class="form-horizontal">';
            var foundIdentical = 0;
            $.each(nodes, function (key, val) {
                var manufacturerId = nodes[app_nodes.selected_node].data.manufacturerId.value;
                var manufacturerProductId = nodes[app_nodes.selected_node].data.manufacturerProductId.value;
                var manufacturerProductType = nodes[app_nodes.selected_node].data.manufacturerProductType.value;
                if (key != app_nodes.selected_node && val.product.is_valid &&
                    val.product.manufacturer_id == manufacturerId &&
                    val.product.product_id == manufacturerProductId &&
                    val.product.product_type == manufacturerProductType) {
                    options_node += '<div class="row">';
                    options_node += '<div class="col-md-2"></div>';
                    options_node += '<div class="col-md-10">';
                    options_node += '<div class="checkbox-inline"><label>';
                    options_node += '<input type="checkbox" name="type" value="' + key + '"/>';
                    foundIdentical = 1;
                    if (val.description.name != '') {
                        options_node += key + ' ' + val.description.location + ' ' + val.description.name ;
                    } else {
                        options_node += key + ' ' + val.description.product_name ;
                    }
                    options_node +=  '</label></div>';
                    options_node +=  '</div></div>';
                }
            });
            options_node += '</form>';
            if (foundIdentical == 0) {
                modal.find('#saveCopyToParams').hide();
                options_node = '{{Aucun module identique trouvé}}';
            }
            modal.find('.modal-body').append(options_node);
        });
        $("#saveCopyToParams").off("click").on("click", function (e) {
            var fromNode = app_nodes.selected_node;
            $("input:checkbox[name=type]:checked").each(function(){
                var toNode = $(this).val();
                $.ajax({
                    url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + fromNode + "].CopyConfigurations(" + toNode + ")",
                    dataType: 'json',
                    async: true,
                    error: function (request, status, error) {
                        handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
                    },
                    success: function (data) {
                    }
                });
            });
            $('#copyToParamsModal').modal('hide');
        });
        $('#groupsModal').off('show.bs.modal').on('show.bs.modal', function (e) {
            var modal = $(this);
            var group = $(this).data('groupindex');
            var associations = [];
            for (var i in nodes[app_nodes.selected_node].groups[group].associations) {
                associations.push(nodes[app_nodes.selected_node].groups[group].associations[i][0] + ";" + nodes[app_nodes.selected_node].groups[group].associations[i][1]);
            }
            var support_multi_instance = nodes[app_nodes.selected_node].multi_instance.support == 1;
            var node_keys = [];
            $.each(nodes, function (key, val) {
                if (key != app_nodes.selected_node) {
                    if (val.capabilities.isListening || val.capabilities.isFlirs) {
                        if (support_multi_instance) {
                            if (val.description.is_static_controller) {
                                node_keys.push(key + ';0');
                                node_keys.push(key + ';1');
                            }
                            else if(val.multi_instance.instances == 1){
                                node_keys.push(key + ';0');
                            }
                            else {
                                for (i = 1; i <= val.multi_instance.instances; i++) {
                                    node_keys.push(key + ';' + i);
                                }
                            }
                        }
                        else{
                            node_keys.push(key + ';0');
                        }
                    }
                }
            });
            modal.find('.modal-body').html(' ');
            modal.find('.modal-title').text('{{Groupe }}' + group + ' : {{Ajouter une association pour le noeud}} ' + app_nodes.selected_node);
            var options_node = '<div><b>Node : </b>  <select class="form-control" id="newvaluenode" style="display:inline-block;width:400px;">';
            for (var i in node_keys) {
                if (associations.indexOf(node_keys[i]) >= 0) {
                    continue;
                }
                var values = node_keys[i].split(";");
                var nodeId = parseInt(values[0]);
                var node = nodes[nodeId];
                var nodeInstance = values[1];
                if (node.description.name != '') {
                    options_node += '<option value="' + node_keys[i] + '">' + nodeId + ' : ' + node.description.location + ' - ' + node.description.name;
                } else {
                    options_node += '<option value="' + node_keys[i] + '">' + nodeId + ' : ' + node.description.product_name;
                }
                if (support_multi_instance && nodeInstance >= 1) {
                    var instanceDisplay = nodeInstance - 1;
                    options_node += ' (' + instanceDisplay + ')';
                }
                options_node += '</option>'
            }
            options_node += '</select></div>';
            modal.find('.modal-body').append(options_node);
        });
        $("#saveGroups").off("click").on("click", function (e) {
            var groupIndex = $('#groupsModal').data('groupindex');
            var values = $('#newvaluenode').val().split(";");
            var nodeId = values[0];
            var nodeInstance = values[1];
            var url = '';
            if (nodeInstance > 0) {
                url = "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + app_nodes.selected_node + "].Associations[" + groupIndex + "].Add(" + nodeId + "," + nodeInstance + ")";
            }
            else {
                url = "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + app_nodes.selected_node + "].instances[0].commandClasses[0x85].Add(" + groupIndex + "," + nodeId + ")";
            }

            $.ajax({
                url: url,
                dataType: 'json',
                async: true,
                error: function (request, status, error) {
                    handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
                },
                success: function (data) {
                    app_nodes.draw_nodes();
                    app_nodes.load_data(false);
                    app_nodes.show_groups();
                    app_nodes.sendOk();
                    $('#groupsModal').modal('hide');
                }
            });
        });
        $("body").off("click", ".editValue").on("click", ".editValue", function (e) {
            var idx = $(this).data('valueidx');
            var instance = $(this).data('valueinstance');
            var cc = $(this).data('valuecc');
            var name = $(this).data('valuename');
            var value = $(this).data('valuevalue');
            var type = $(this).data('valuetype');
            var dataitems = $(this).data('valuedataitems');
            var genre = $(this).data('valuegenre');
            $('#valuesModal').data('valuename', name);
            $('#valuesModal').data('valuetype', type);
            $('#valuesModal').data('valueinstance', instance);
            $('#valuesModal').data('valuecc', cc);
            $('#valuesModal').data('valuevalue', value);
            $('#valuesModal').data('valuedataitems', dataitems);
            $('#valuesModal').data('valuegenre', genre);
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
            var valueGenre = $(this).data('valuegenre');
            var modal = $(this);
            modal.find('.modal-title').text('{{Changer la valeur de}} ' + valueName);
            modal.find('.modal-body').html(valueName);
            modal.find('.modal-body').append('<b> : </b>');
            if (valueType == "List") {
                var options = '<select class="form-control" id="newvaluevalue" style="display:inline-block;width:400px;">';
                $.each(valueDataitems, function (key, val) {
                    if (val == valueValue) {
                        options += '<option value="' + val + '" selected="selected">' + val + '</option>';
                    } else {
                        options += '<option value="' + val + '">' + val + '</option>';
                    }
                });
                options += '</select>';
                modal.find('.modal-body').empty().append(options);

            } else if (valueType == "Bool") {
                var trueString = '&nbsp;{{ON}}&nbsp;';
                var falseString = '&nbsp;{{OFF}}';
                if (valueGenre =="System"){
                    trueString = '&nbsp;{{Oui}}&nbsp;';
                    falseString = '&nbsp;{{Non}}';
                }
                if (valueValue == true) {
                    modal.find('.modal-body').append('<input type="radio" name="newvaluevalue" id="on" value="255" checked>' + trueString);
                    modal.find('.modal-body').append('<input type="radio" name="newvaluevalue" id="off" value="0">' + falseString);
                } else {
                    modal.find('.modal-body').append('<input type="radio" name="newvaluevalue" id="on" value="255">' + trueString);
                    modal.find('.modal-body').append('<input type="radio" name="newvaluevalue" id="off" value="0" checked>' + falseString);
                }
            } else if (valueType == "Button") {
                modal.find('.modal-body').append('<input type="radio" name="newvaluevalue" id="push" value="Press" checked> {{Presser le bouton}} ');
                modal.find('.modal-body').append('<input type="radio" name="newvaluevalue" id="push" value="Release"> {{Relacher le bouton}} ');
            } else {
                modal.find('.modal-body').append('<input type="text" class="form-control" id="newvaluevalue" style="display:inline-block;width:400px;" value="' + valueValue + '">');
            }
        });
        $("body").off("click", ".forceRefresh").on("click", ".forceRefresh", function (e) {
            var index = $(this).attr('data-valueidx');
            var cc = $(this).attr('data-valuecc');
            var instance = $(this).attr('data-valueinstance');
            $.ajax({
                url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=/ZWaveAPI/Run/devices[" + app_nodes.selected_node + "].instances[" + instance + "].commandClasses[" + cc + "].data[" + index + "].Refresh()",
                dataType: 'json',
                async: true,
                error: function (request, status, error) {
                    handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
                },
                success: function (data) {
                    app_nodes.sendOk();
                }
            });
        });
        $("body").off("click", ".editPolling").on("click", ".editPolling", function (e) {
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
            select += '<option value="1">{{5 min}}</option>';
            //select += '<option value="2">{{15 min}}</option>';
            //select += '<option value="3">{{10 min}}</option>';
            //select += '<option value="6">{{5 min}}</option>';
            //select += '<option value="30">{{1 min}}</option>';
            select += '</option>';
            modal.find('.modal-body').append(select);
            modal.find('.modal-body').find('#newvaluevalue').val(valuePolling);
        });
        $("body").off("click", ".editParam").on("click", ".editParam", function (e) {
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
            if (paramType == "List") {
                $.ajax({
                    url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + app_nodes.selected_node + "].commandClasses[0x70].data",
                    dataType: 'json',
                    async: true,
                    error: function (request, status, error) {
                        handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
                    },
                    success: function (data) {
                        var options = '<select class="form-control" id="newvalue">';
                        $.each(data[paramId].val.value4, function (key, val) {
                            if (val == paramValue) {
                                if (typeof openzwave_node_translation.configuration[paramId] !== 'undefined' && openzwave_node_translation['configuration'][paramId].hasOwnProperty('list') && typeof openzwave_node_translation['configuration'][paramId].list[val] !== 'undefined') {
                                    options += '<option value="' + val + '" selected="selected">' + openzwave_node_translation['configuration'][paramId].list[val] + '</option>';
                                } else {
                                    options += '<option value="' + val + '" selected="selected">' + val + '</option>';
                                }
                            } else {
                                if (typeof openzwave_node_translation.configuration[paramId] !== 'undefined' && openzwave_node_translation['configuration'][paramId].hasOwnProperty('list') && typeof openzwave_node_translation['configuration'][paramId].list[val] !== 'undefined') {
                                    options += '<option value="' + val + '">' + openzwave_node_translation['configuration'][paramId].list[val] + '</option>';
                                } else {
                                    options += '<option value="' + val + '">' + val + '</option>';
                                }
                            }
                        });
                        options += '</select>';
                        modal.find('.modal-body').empty().append(options);

                    }
                });
            } else if (paramType == "Bool") {
                if (paramValue == true) {
                    modal.find('.modal-body').append('<input type="radio" name="newvalue" id="on" value="1" checked> {{Oui}} ');
                    modal.find('.modal-body').append('<input type="radio" name="newvalue" id="off" value="0"> {{Non}} ');
                } else {
                    modal.find('.modal-body').append('<input type="radio" name="newvalue" id="on" value="1"> {{Oui}} ');
                    modal.find('.modal-body').append('<input type="radio" name="newvalue" id="off" value="0" checked> {{Non}} ');
                }
            } else if (paramType == "Button") {
                modal.find('.modal-body').append('<input type="radio" name="newvalue" id="push" value="Press" checked> {{Presser le bouton}} ');
                modal.find('.modal-body').append('<input type="radio" name="newvalue" id="push" value="Release"> {{Relacher le bouton}} ');
            } else {
                modal.find('.modal-body').append('<input type="text" class="form-control" id="newvalue" style="display:inline-block;width:400px;" value="' + paramValue + '">');
            }
        });
        $("#sendNodeInformation").off("click").on("click", function () {
            app_nodes.send_node_information(app_nodes.selected_node);
        });
        $("#saveParam").off("click").on("click", function (e) {
            var paramId = $('#paramsModal').data('paramid');
            var paramType = $('#paramsModal').data('paramtype');
            if (paramType == "Bool") {
                var paramValue = $('input[name=newvalue]:checked', '#paramsModal').val();
            } else if (paramType == "Button") {
                var paramValue = $('input[name=newvalue]:checked', '#paramsModal').val();
            } else {
                var paramValue = $('#newvalue').val();
            }
            var paramValue2 = paramValue.replace(/\//g, '@');
            var paramLength = paramValue.length;
            $.ajax({
                url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + app_nodes.selected_node + "].commandClasses[0x70].Set(" + paramId + "," + encodeURIComponent(paramValue2) + "," + paramLength + ")",
                dataType: 'json',
                async: true,
                error: function (request, status, error) {
                    handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
                },
                success: function (data) {
                    app_nodes.sendOk();
                    app_nodes.load_data(false);
                    $('#paramsModal').modal('hide');
                }
            });
        });
        $("#applyValue").off("click").on("click", function (e) {
            var valueType = $('#valuesModal').data('valuetype');
            var valueIdx = $('#valuesModal').data('valueidx');
            var valueInstance = $('#valuesModal').data('valueinstance');
            var valueCc = $('#valuesModal').data('valuecc');
            if (valueType == "Bool") {
                var valueValue = $('input[name=newvaluevalue]:checked', '#valuesModal').val();
            } else if (valueType == "Button") {
                var valueValue = $('input[name=newvaluevalue]:checked', '#valuesModal').val();
            } else {
                var valueValue = $('#newvaluevalue').val();
            }
            if (valueType == "Button") {
                $.ajax({
                    url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + app_nodes.selected_node + "].instances[" + valueInstance + "].commandClasses[0x" + Number(valueCc).toString(16) + "].data[" + valueIdx + "]." + valueValue + "Button()",
                    dataType: 'json',
                    async: true,
                    error: function (request, status, error) {
                        handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
                    },
                    success: function (data) {
                        app_nodes.sendOk();
                        $('#valuesModal').modal('hide');
                        app_nodes.load_data(false);
                    }
                });
            } else if (valueType == "Raw") {
                $.ajax({
                    url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + app_nodes.selected_node + "].UserCode.SetRaw(" + valueIdx + ",[" + valueValue + "],1)",
                    dataType: 'json',
                    async: true,
                    error: function (request, status, error) {
                        handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
                    },
                    success: function (data) {
                        app_nodes.sendOk();
                        $('#valuesModal').modal('hide');
                        app_nodes.load_data(false);
                    }
                });
            }
            else {
                $.ajax({
                    url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + app_nodes.selected_node + "].instances[" + valueInstance + "].commandClasses[0x" + Number(valueCc).toString(16) + "].data[" + valueIdx + "].Set(" + encodeURIComponent(valueValue) + ")",
                    dataType: 'json',
                    async: true,
                    error: function (request, status, error) {
                        handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
                    },
                    success: function (data) {
                        app_nodes.sendOk();
                        $('#valuesModal').modal('hide');
                        app_nodes.load_data(false);
                    }
                });
            }
        });
        $("#savePolling").off("click").on("click", function (e) {
            var valueIdx = $('#pollingModal').data('valueidx');
            var valueInstance = $('#pollingModal').data('valueinstance');
            var valueCc = $('#pollingModal').data('valuecc');
            var valueValue = $('#newvaluevalue').val();
            $.ajax({
                url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + app_nodes.selected_node + "].instances[" + valueInstance + "].commandClasses[0x" + Number(valueCc).toString(16) + "].data[" + valueIdx + "].SetPolling(" + encodeURIComponent(valueValue) + ")",
                dataType: 'json',
                async: true,
                error: function (request, status, error) {
                    handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
                },
                success: function (data) {
                    app_nodes.draw_nodes();
                    app_nodes.load_data(false);
                    app_nodes.sendOk();
                    $('#pollingModal').modal('hide');
                    app_nodes.draw_nodes();
                }
            });
        });

    },
    sendOk: function () {
        $('#li_state').show();
        setTimeout(function () {
            $('#li_state').hide();
        }, 3000);
    },
    delete_group: function (node_id, group, node, instance) {
        var url = "";
        if (instance > 0) {
            url = "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].Associations[" + group + "].Remove(" + node + "," + instance + ")";
        } else {
            url = "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].instances[0].commandClasses[0x85].Remove(" + group + "," + node + ")"
        }
        $.ajax({
            url: url,
            dataType: 'json',
            async: true,
            success: function (data) {
                app_nodes.draw_nodes();
                app_nodes.load_data(false);
                app_nodes.show_groups();
                app_nodes.sendOk();
            },
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
            }
        });
    },
    request_node_neighbours_update: function (node_id) {
        $.ajax({
            url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].RequestNodeNeighbourUpdate()",
            dataType: 'json',
            async: true,
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
            },
            success: function (data) {
                if (data['result'] == true) {
                    app_nodes.sendOk();
                    app_nodes.load_data(false);
                } else {
                    $('#div_nodeConfigureOpenzwaveAlert').showAlert({
                        message: '{{Echec}} :' + data.data,
                        level: 'danger'
                    });
                }
            }
        });
    },
    healNode: function (node_id) {
        $.ajax({
            url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].HealNode()",
            dataType: 'json',
            async: true,
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
            },
            success: function (data) {
                if (data.result == true) {
                    app_nodes.sendOk();
                    app_nodes.load_data(false);
                } else {
                    $('#div_nodeConfigureOpenzwaveAlert').showAlert({
                        message: '{{Echec}} :' + data.data,
                        level: 'danger'
                    });
                }
            }
        });
    },
    assign_return_route_node: function (node_id) {
        $.ajax({
            url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].AssignReturnRoute()",
            dataType: 'json',
            async: true,
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
            },
            success: function (data) {
                app_nodes.sendOk();
                app_nodes.load_data(false);
            }
        });
    },
    test_node: function (node_id) {
        $.ajax({
            url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].TestNode()",
            dataType: 'json',
            async: true,
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
            },
            success: function (data) {
                app_nodes.sendOk();
                app_nodes.load_data(false);
            }
        });
    },
    refresh_node_values: function (node_id) {
        $.ajax({
            url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].RefreshAllValues()",
            dataType: 'json',
            async: true,
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
            },
            success: function (data) {
                app_nodes.sendOk();
                app_nodes.load_data(false);
            }
        });
    },
    request_node_dynamic: function (node_id) {
        $.ajax({
            url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].RequestNodeDynamic()",
            dataType: 'json',
            async: true,
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
            },
            success: function (data) {
                app_nodes.sendOk();
                app_nodes.load_data(false);
            }
        });
    },
    refresh_node_info: function (node_id) {
        $.ajax({
            url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].RefreshNodeInfo()",
            dataType: 'json',
            async: true,
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
            },
            success: function (data) {
                if (data['result'] == true) {
                    app_nodes.sendOk();
                    app_nodes.load_data(false);
                } else {
                    $('#div_nodeConfigureOpenzwaveAlert').showAlert({
                        message: '{{Echec}} :' + data.data,
                        level: 'danger'
                    });
                }
            }
        });
    },
    has_node_failed: function (node_id) {
        $.ajax({
            url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].HasNodeFailed()",
            dataType: 'json',
            async: true,
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
            },
            success: function (data) {
                app_nodes.sendOk();
                app_nodes.load_data(false);
            }
        });
    },
    remove_failed_node: function (node_id) {
        $.ajax({
            url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].RemoveFailedNode()",
            dataType: 'json',
            async: true,
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
            },
            success: function (data) {
                if (data['result'] == true) {
                    app_nodes.sendOk();
                    app_nodes.load_data(false);
                } else {
                    $('#div_nodeConfigureOpenzwaveAlert').showAlert({
                        message: '{{Echec}} :' + data.data,
                        level: 'danger'
                    });
                }
            }
        });
    },
    remove_ghost_node: function (node_id) {
        $.ajax({
            url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].GhostKiller()",
            dataType: 'json',
            async: true,
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
            },
            success: function (data) {
                if (data['result'] == true) {
                    app_nodes.sendOk();
                    app_nodes.load_data(false);
                } else {
                    $('#div_nodeConfigureOpenzwaveAlert').showAlert({
                        message: '{{Echec}} :' + data.data,
                        level: 'danger'
                    });
                }
            }
        });
    },
    replace_failed_node: function (node_id) {
        $.ajax({
            url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].ReplaceFailedNode()",
            dataType: 'json',
            async: true,
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
            },
            success: function (data) {
                if (data['result'] == true) {
                    app_nodes.sendOk();
                    app_nodes.load_data(false);
                } else {
                    $('#div_nodeConfigureOpenzwaveAlert').showAlert({
                        message: '{{Echec}} :' + data.data,
                        level: 'danger'
                    });
                }
            }
        });
    },
    send_node_information: function (node_id) {
        $.ajax({
            url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].SendNodeInformation()",
            dataType: 'json',
            async: true,
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
            },
            success: function (data) {
                app_nodes.sendOk();
                app_nodes.load_data(false);
            }
        });
    },
    send_regenerate_node_cfg_file: function (node_id, all) {
        $.ajax({
            url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].RemoveDeviceZWConfig(" + all + ")",
            dataType: 'json',
            async: true,
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
            },
            success: function (data) {
                app_nodes.sendOk();
                app_nodes.load_data(false);
            }
        });
    },
    refresh_parameters: function (node_id) {
        $.ajax({
            url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].commandClasses[0x70].Refresh()",
            dataType: 'json',
            async: true,
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
            },
            success: function (data) {
                app_nodes.sendOk();
                app_nodes.load_data(false);
            }
        });
    },
    load_all: function () {
        $.ajax({
            url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/network.GetNodesList()",
            dataType: 'json',
            global: false,
            async: true,
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
            },
            success: function (data) {
                var node = nodes[node_id];
                nodes = data['devices'];
                nodes[node_id] = node;
                controller_id = -1;
                for (var i in data['devices']) {
                    if (isset(data['devices'][i]['description']) && isset(data['devices'][i]['description']['is_static_controller']) && data['devices'][i]['description']['is_static_controller']) {
                        controller_id = i;
                    }
                }
                app_nodes.draw_nodes();
                app_nodes.show_groups();
            }
        });
    },
    load_data: function (_global) {
        $.ajax({
            url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "]",
            dataType: 'json',
            async: true,
            global: _global,
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
            },
            success: function (data) {
                if (Object.keys(nodes).length == 0) {
                    app_nodes.load_all();
                }
                nodes[node_id] = data;
                app_nodes.draw_nodes();
                app_nodes.show_groups();
            }
        });
    },
    load_stats: function (node_id) {
        $.ajax({
            url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].GetNodeStatistics()",
            dataType: 'json',
            async: true,
            global: (typeof node_id !== 'undefined' && !isNaN(node_id)) ? false : true,
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
            },
            success: function (data) {
                stats = data['statistics'];
                app_nodes.show_stats();
            }
        });
    },
    show: function () {
        if (typeof node_id !== 'undefined' && !isNaN(node_id)) {
            app_nodes.selected_node = node_id;
        } else {
            app_nodes.selected_node = 1;
        }
    },
    hide: function () {
        clearInterval(app_nodes.updater);
        openzwave_node_translation = null;
    },

    draw_nodes: function () {
        $("#node-nav").html("");
        var template_node = $("#template-node").html();
        var template_variable = $("#template-variable").html();
        var template_parameter = $("#template-parameter").html();
        var template_system = $("#template-system").html();
        var z = app_nodes.selected_node;
        if (!isset(nodes[z])) {
            return;
        }
        if (nodes[z].data.isFailed) {
            var nodeIsFailed = nodes[z].data.isFailed.value
        } else {
            var nodeIsFailed = false;
        }
        var queryStage = nodes[z].data.state.value;
        $("#node").attr("nid", z);
        // select the copied block
        var node = $(".node");
        var isWarning = false;
        var warningMessage = "";
        node.find(".node-id").html(z);              // set the nodeid
        if (nodes[z].data.name.value == '') {
            var name = '';
        } else {
            var name = nodes[z].data.name.value;
        }
        var location = nodes[z].data.location.value;
        var productName = nodes[z].data.product_name.value;
        var manufacturerName = nodes[z].data.vendorString.value;
        node.find(".node-productname").html(productName);
        node.find(".node-location").html(location);
        node.find(".node-name").html(name);
        node.find(".node-vendor").html(manufacturerName);
        node.find(".node-zwave-id").html("{{Identifiant du fabricant :}} <span class='label label-default' style='font-size : 1em;'>" + nodes[z].data.manufacturerId.value + " [" + nodes[z].data.manufacturerId.hex + "]</span> {{Type de produit :}} <span class='label label-default' style='font-size : 1em;'>" + nodes[z].data.manufacturerProductType.value + ' [' + nodes[z].data.manufacturerProductType.hex + "]</span> {{Identifiant du produit :}} <span class='label label-default' style='font-size : 1em;'>" + nodes[z].data.manufacturerProductId.value + ' [' + nodes[z].data.manufacturerProductId.hex + "]</span>");
        node.find(".node-lastSeen").html(app_nodes.timestampConverter(nodes[z].data.lastReceived.updateTime));
        if (nodes[z].last_notification.next_wakeup != null) {
            node.find(".node-next-wakeup").html(app_nodes.timestampConverter(nodes[z].last_notification.next_wakeup));
            node.find(".node-next-wakeup-span").show();
        } else {
            node.find(".node-next-wakeup-span").hide();
        }
        var basicDeviceClass = parseInt(nodes[z].data.basicType.value, 0);
        var basicDeviceClassDescription = "";
        switch (basicDeviceClass) {
            case 1:
                // Controller
                basicDeviceClassDescription = "{{Contrôleur}}";
                break;
            case 2:
                // Static Controller
                basicDeviceClassDescription = "{{Contrôleur statique}}";
                break;
            case 3:
                // Slave
                basicDeviceClassDescription = "{{Esclave}}";
                break;
            case 4:
                // Routing Slave
                basicDeviceClassDescription = "{{Esclave pouvant être routé}}";
                break;
            default:
                basicDeviceClassDescription = basicDeviceClass;
                break;
        }

        var genericDeviceClass = parseInt(nodes[z].data.genericType.value, 0);
        var genericDeviceClassDescription = "";

        //The ‘Generic’ device class defines the basic functionality that the devices will support as a controller or slave.
        switch (genericDeviceClass) {
            case 1: // Generic Controller   = 0x01
                genericDeviceClassDescription = "{{Télécommande}}";
                break;
            case 2: // Static Controller   = 0x02,
                genericDeviceClassDescription = "{{Contrôleur statique}}";
                break;
            case 3: // Av Control Point    = 0x03,
                genericDeviceClassDescription = "{{Contrôleur A/V}}";
                break;
            case 4: // Display             = 0x04,
                genericDeviceClassDescription = "{{Afficheur}}";
                break;
            case 5: // Network Extender             = 0x05,
                genericDeviceClassDescription = "{{Répéteur de signal}}";
                break;
            case 6: // Appliance             = 0x06,
                genericDeviceClassDescription = "{{Appareil}}";
                break;
            case 7: // Sensor Notification             = 0x07,
                genericDeviceClassDescription = "{{Capteur de notification}}";
                break;
            case 8: // Thermostat          = 0x08,
                genericDeviceClassDescription = "{{Thermostat}}";
                break;
            case 9: // Window Covering     = 0x09,
                genericDeviceClassDescription = "{{Couvre-fenêtres}}";
                break;
            case 15: // Repeater Slave      = 0x0f,
                genericDeviceClassDescription = "{{Répéteur esclave}}";
                break;
            case 16: // Switch Binary       = 0x10,
                genericDeviceClassDescription = "{{Interrupteur binaire}}";
                break;
            case 17: // Switch Multilevel   = 0x11,
                genericDeviceClassDescription = "{{Interrupteur multi-niveau}}";
                break;
            case 18: // Switch Remote       = 0x12,
                genericDeviceClassDescription = "{{Interrupteur distant}}";
                break;
            case 19: // Switch Toggle       = 0x13,
                genericDeviceClassDescription = "{{Interrupteur à levier}}";
                break;
            case 20: // Z_IP_GATEWAY       = 0x14,
                genericDeviceClassDescription = "{{Passerelle Z-Wave/IP}}";
                break;
            case 21: // Zip Node       = 0x15,
                genericDeviceClassDescription = "{{Noeud Z-Wave/IP}}";
                break;
            case 22: // Ventilation         = 0x16,
                genericDeviceClassDescription = "{{Ventilation}}";
                break;
            case 23: // Security Panel         = 0x17,
                genericDeviceClassDescription = "{{Panneau de sécurité}}";
                break;
            case 24: // Wall Controller       = 0x18,
                genericDeviceClassDescription = "{{Contrôleur mural}}";
                break;
            case 32: // Sensor Binary       = 0x20,
                genericDeviceClassDescription = "{{Capteur binaire}}";
                break;
            case 33: // Sensor Multilevel   = 0x21
                genericDeviceClassDescription = "{{Capteur multi-niveau}}";
                break;
            case 34: //WATER_CONTROL   = 0x22
                genericDeviceClassDescription = "{{Niveau d'eau}}";
                break;
            case 48: // Meter Pulse       = 0x30
                genericDeviceClassDescription = "{{Mesure d'impulsion}}";
            case 49: // Meter         = 0x31
                genericDeviceClassDescription = "{{Mesure}}";
                break;
            case 64: // Entry Control       = 0x40
                genericDeviceClassDescription = "{{Contrôle d'entrée}}";
                break;
            case 80: // Semi Interoperable        = 0x50
                genericDeviceClassDescription = "{{Semi-interopérable}}";
                break;
            case 161: // Sensor Alarm        = 0xa1
                genericDeviceClassDescription = "{{Capteur d'alarme}}";
                break;
            case 255: // Non Interoperable        = 0xff
                genericDeviceClassDescription = "{{Non interopérable}}";
                break;
            default:
                genericDeviceClassDescription = "{{Inconnue}}";
                break;
        }

        var specificDeviceClass = parseInt(nodes[z].data.specificType.value, 0);
        var specificDeviceClassDescription = nodes[z].data.type.value;

        node.find(".node-basic").html(basicDeviceClassDescription);
        node.find(".node-generic").html(genericDeviceClassDescription);
        node.find(".node-specific").html(specificDeviceClassDescription);

        var queryStageIndex = 0;
        var queryStageDescrition = "";
        switch (queryStage) {
            case "None":
                queryStageDescrition = "{{Initialisation du processus de recherche de noeud}}";
                queryStageIndex = 0;
                break;
            case "ProtocolInfo":
                queryStageDescrition = "{{Récupérer des informations de protocole}}";
                queryStageIndex = 1;
                break;
            case "Probe":
                queryStageDescrition = "{{Ping le module pour voir s’il est réveillé}}";
                queryStageIndex = 2;
                break;
            case "WakeUp":
                queryStageDescrition = "{{Démarrer le processus de réveil}}";
                queryStageIndex = 3;
                break;
            case "ManufacturerSpecific1":
                queryStageDescrition = "{{Récupérer le nom du fabricant et les identifiants de produits}}";
                queryStageIndex = 4;
                break;
            case "NodeInfo":
                queryStageDescrition = "{{Récupérer les infos sur la prise en charge des classes de commandes supportées}}";
                queryStageIndex = 5;
                break;
            case "NodePlusInfo":
                queryStageDescrition = "{{Récupérer les infos ZWave+ sur la prise en charge des classes de commandes supportées}}";
                queryStageIndex = 5;
                break;
            case "SecurityReport":
                queryStageDescrition = "{{Récupérer la liste des classes de commande qui nécessitent de la sécurité}}";
                queryStageIndex = 6;
                break;
            case "ManufacturerSpecific2":
                queryStageDescrition = "{{Récupérer le nom du fabricant et les identifiants de produits}}";
                queryStageIndex = 7;
                break;
            case "Versions":
                queryStageDescrition = "{{Récupérer des informations de version}}";
                queryStageIndex = 8;
                break;
            case "Instances":
                queryStageDescrition = "{{Récupérer des informations multi-instances de classe de commande}}";
                queryStageIndex = 9;
                break;
            case "Static":
                queryStageDescrition = "{{Récupérer des informations statiques}}";
                queryStageIndex = 10;
                break;
            case "CacheLoad":
                queryStageDescrition = "{{Ping le module lors du redémarrage avec config cache de l’appareil}}";
                queryStageIndex = 11;
                break;
            case "Associations":
                queryStageDescrition = "{{Récupérer des informations sur les associations}}";
                queryStageIndex = 12;
                break;
            case "Neighbors":
                queryStageDescrition = "{{Récupérer la liste des noeuds voisins}}";
                queryStageIndex = 13;
                break;
            case "Session":
                queryStageDescrition = "{{Récupérer des informations de session}}";
                queryStageIndex = 14;
                break;
            case "Dynamic":
                queryStageDescrition = "{{Récupérer des informations dynamiques}}";
                queryStageIndex = 15;
                break;
            case "Configuration":
                queryStageDescrition = "{{Récupérer des informations de paramètre configurable}}";
                queryStageIndex = 16;
                break;
            case "Complete":
                queryStageDescrition = "{{Le processus de l’interview est terminé}}";
                queryStageIndex = 17;
                node.find(".node-queryStage").removeClass("label-default").addClass("label-success");
                break;
        }
        var nodeCanSleep = nodes[z].data.can_wake_up.value;
        if (queryStageIndex > 2) {
            if (nodes[z].data.isListening.value) {
                node.find(".node-sleep").removeClass("label-default");
                node.find(".node-sleep").html('<i class="fa fa-plug text-success fa-lg"></i>');
                node.find(".node-battery-span").hide();
            }
            else {
                var battery_level = nodes[z].data.battery_level.value
                node.find(".node-sleep").removeClass("label-success").addClass("label-default")
                if (battery_level != null) {
                    if (nodes[z].data.isFrequentListening.value) {
                        node.find(".node-sleep").html("{{Endormi <i>(FLiRS)</i>}}");
                    }
                    else if (nodeCanSleep) {
                        if (nodes[z].data.isAwake.value) {
                            node.find(".node-sleep").removeClass("label-default").addClass("label-success")
                            node.find(".node-sleep").html("{{Réveillé}}");
                        }
                        else {
                            node.find(".node-sleep").html("{{Endormi}}");
                        }
                    }
                    else {
                        node.find(".node-sleep").html("{{Endormi}}");
                    }
                    node.find(".node-battery").html(battery_level + ' %');
                    node.find(".node-battery-span").show();
                }
                else if (nodeCanSleep) {
                    node.find(".node-sleep").html("---");
                    node.find(".node-battery-span").hide();
                }
            }
        }
        else {
            node.find(".node-sleep").html("---");
            node.find(".node-battery-span").hide();
        }
        if (controller_id != -1) {
            var node_groups = nodes[z].groups;
            var found = false;
            var hasGroup = false;
            for (zz in node_groups) {
                if (!isNaN(zz)) {
                    hasGroup = true;
                    for (var i in node_groups[zz].associations) {
                        var node_id = node_groups[zz].associations[i][0];
                        if (node_id == controller_id) {
                            found = true;
                            break;
                        }
                    }
                }
            }
            if (hasGroup && !found && queryStageIndex > 12) {
                isWarning = true;
                warningMessage += "<li>{{Le contrôleur n'est inclus dans aucun groupe du module.}}</li>";
            }
        }
        if (nodeIsFailed) {
            isWarning = true;
            warningMessage += "<li>{{Le contrôleur pense que ce noeud est en échec, essayez }} " +
                "<button type='button' id='hasNodeFailed_summary' class='btn btn-xs btn-primary hasNodeFailed'><i class='fa fa-heartbeat' aria-hidden='true'></i> {{Nœud en échec ?}}</button> " +
                "{{ou}} " +
                "<button type='button' id='testNode' class='btn btn-info testNode'><i class='fa fa-check-square-o'></i> {{Tester le nœud}}</button> " +
                "{{pour essayer de corriger.}}</li>";
        }
        // activate available actions
        $("#requestNodeNeighboursUpdate").prop("disabled", nodeIsFailed);
        $("#healNode").prop("disabled", nodeIsFailed);
        $("#assignReturnRoute").prop("disabled", nodeIsFailed);
        $("#refreshNodeValues").prop("disabled", nodeIsFailed);
        $("#requestNodeDynamic").prop("disabled", nodeIsFailed);
        $("#refreshNodeInfo").prop("disabled", nodeIsFailed);
        $("#removeFailedNode").prop("disabled", !nodeIsFailed);
        $("#replaceFailedNode").prop("disabled", !nodeIsFailed);
        $("#sendNodeInformation").prop("disabled", nodeIsFailed);
        // always allow the special action
        $("#regenerateNodeCfgFile").prop("disabled", false);
        // remote control don't wakeup, we will trick the flag
        if (genericDeviceClass == 1) {
            nodeCanSleep = true;
        }
        $("#removeGhostNode").prop("disabled", nodeIsFailed || !nodeCanSleep);

        if (nodeIsFailed) {
            node.find(".node-queryStage").html("Dead");
            node.find(".node-queryStage").removeClass("label-default").addClass("label-danger");
        } else {
            node.find(".node-queryStage").html(queryStage);
            node.find(".node-queryStage").removeClass("label-danger").addClass("label-default");
        }

        var myPopover = $('#node-queryStageDescrition').data('bs.popover');
        if (queryStageIndex < 17) {
            myPopover.options.content = queryStageDescrition + " (" + queryStageIndex + "/17)";
        }
        else {
            myPopover.options.content = queryStageDescrition;
        }
        node.find(".node-maxBaudRate").html(nodes[z].data.maxBaudRate.value);
        if (nodes[z].data.isRouting.value) {
            node.find(".node-routing").html("<li>{{Le noeud a des capacités de routage (capable de faire passer des commandes à d'autres noeuds)}}</li>");
        }
        else {
            node.find(".node-routing").html("");
        }
        if (nodes[z].data.isSecurity.value) {
            node.find(".node-isSecurity").html("<li>{{Le noeud supporte les caractéristiques de sécurité avancées}}</li>");
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
        else {
            node.find(".node-isSecurity").html("");
            node.find(".node-security").html("");
        }
        if (nodes[z].data.isListening.value) {
            node.find(".node-listening").html("<li>{{Le noeud est alimenté et écoute en permanence}}</li>");
        }
        else {
            node.find(".node-listening").html("");
        }
        if (nodes[z].data.isFrequentListening.value) {
            node.find(".node-isFrequentListening").html("<li>{{<i>FLiRS</i>, routeurs esclaves à écoute fréquente}}</li>");
        }
        else {
            node.find(".node-isFrequentListening").html("");
        }
        if (nodes[z].data.isBeaming.value) {
            node.find(".node-isBeaming").html("<li>{{Le noeud est capable d'envoyer une trame réseau}}</li>");
        }
        else {
            node.find(".node-isBeaming").html("");
        }

        if (nodes[z].data.isZwavePlus.value) {
            node.find(".node-zwaveplus").html(" {{ZWAVE PLUS}}");
        }
        else {
            node.find(".node-zwaveplus").html("");
        }
        if (nodes[z].data.isSecured.enabled) {
            if (nodes[z].data.isSecured.value) {
                node.find(".node-isSecured").html("<i class='fa fa-lock' aria-hidden='true'></i>");
            }
            else {
                node.find(".node-isSecured").html("<i class='fa fa-unlock' aria-hidden='true'></i>");
            }
        }
        else{
            node.find(".node-isSecured").html("");
        }
        var neighbours = nodes[z].data.neighbours.value.join();
        if (queryStageIndex > 13) {
            if (neighbours != "") {
                node.find(".node-neighbours").html(neighbours);
            }
            else {
                node.find(".node-neighbours").html("...");
                if (genericDeviceClass != 1 && (genericDeviceClass != 8 || nodes[z].data.isListening.value)) {
                    warningMessage += "<li{{Liste des voisins non disponible}} <br/>{{Utilisez}} <button type='button' id='healNode' class='btn btn-success healNode'><i class='fa fa-medkit'></i> {{Soigner le noeud}}</button> {{ou}} <button type='button' id='requestNodeNeighboursUpdate' class='btn btn-primary requestNodeNeighboursUpdate'><i class='fa fa-sitemap'></i> {{Mise à jour des noeuds voisins}}</button> {{pour corriger.}}</li>";
                    isWarning = true;
                }
            }
        }
        else {
            node.find(".node-neighbours").html("<i>{{La liste des noeuds voisin n'est pas encore disponible.}}</i>");
        }
        if (queryStageIndex > 7 && productName == "") {

            warningMessage += "<li>{{Les identifiants constructeur ne sont pas detectés.}}<br/>{{Utilisez}} <button type='button' id='refreshNodeInfo' class='btn btn-success refreshNodeInfo'><i class='fa fa-retweet'></i> {{Rafraîchir infos du noeud}}</button> {{pour corriger}}</li>";
            isWarning = true;
        }

        if (isWarning) {
            if (nodeCanSleep) {
                warningMessage += "<br><p>{{Le noeud est dormant et nécessite un réveil avant qu'une commande puisse être exécutée.<br/>Vous pouvez le réveiller manuellement ou attendre son délai de réveil.}}<br/>{{Voir l'interval de réveil dans l'onglet Système}}</p>";
            }
            node.find(".panel-danger").show();
            node.find(".node-warning").html(warningMessage);
        }
        else {
            node.find(".panel-danger").hide();
            node.find(".node-warning").html("");
        }
        var variables = "";
        var parameters = "";
        var system_variables = "";
        for (instance in nodes[z].instances) {
            for (commandclass in nodes[z].instances[instance].commandClasses) {
                for (index in nodes[z].instances[instance].commandClasses[commandclass].data) {
                    if (!isNaN(index)) {
                        var id = instance + ":" + commandclass + ":" + index;
                        var genre = nodes[z].instances[instance].commandClasses[commandclass].data[index].genre;
                        var pending_state = nodes[z].instances[instance].commandClasses[commandclass].data[index].pendingState;
                        if (genre == "Config") {
                            switch (pending_state) {
                                case 1:
                                    parameters += "<tr class='greenrow' pid='" + id + "'>" + template_parameter + "</tr>";
                                    break;
                                case 2:
                                    parameters += "<tr class='redrow' pid='" + id + "'>" + template_parameter + "</tr>";
                                    break;
                                case 3:
                                    parameters += "<tr class='yellowrow' pid='" + id + "'>" + template_parameter + "</tr>";
                                    break;
                                default:
                                    parameters += "<tr pid='" + id + "'>" + template_parameter + "</tr>";
                            }
                        } else if (genre == "System") {
                            switch (pending_state) {
                                case 1:
                                    system_variables += "<tr class='greenrow' sid='" + id + "'>" + template_system + "</tr>";
                                    break;
                                case 2:
                                    system_variables += "<tr class='redrow' sid='" + id + "'>" + template_system + "</tr>";
                                    break;
                                case 3:
                                    system_variables += "<tr class='yellowrow' sid='" + id + "'>" + template_system + "</tr>";
                                    break;
                                default:
                                    system_variables += "<tr sid='" + id + "'>" + template_system + "</tr>";
                            }
                        } else {
                            variables += "<tr vid='" + id + "'>" + template_variable + "</tr>";
                        }
                    }
                }
            }
        }
        node.find(".variables").html(variables);
        node.find(".parameters").html(parameters);
        node.find(".system_variables").html(system_variables);
        if (typeof openzwave_node_translation === 'undefined' || openzwave_node_translation == null) {
            openzwave_node_translation = app_nodes.get_translation();
        }
        if (typeof openzwave_node_translation.configuration === 'undefined') {
            openzwave_node_translation = {configuration: {}};
        }
        for (instance in nodes[z].instances) {
            for (commandclass in nodes[z].instances[instance].commandClasses) {
                var first_index_polling = true;
                for (index in nodes[z].instances[instance].commandClasses[commandclass].data) {
                    var id = instance + ":" + commandclass + ":" + index;
                    var row = node.find("tr[vid='" + id + "']");
                    var row_parameter = node.find("tr[pid='" + id + "']");
                    var row_system = node.find("tr[sid='" + id + "']");
                    // values
                    row.find("td[key=variable-instance]").html(instance);
                    row.find("td[key=variable-cc]").html(commandclass + ' (0x' + Number(commandclass).toString(16) + ')');
                    row.find("td[key=variable-index]").html(index);
                    row.find("td[key=variable-name]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].name);
                    row.find("td[key=variable-type]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].typeZW + ' (' + nodes[z].instances[instance].commandClasses[commandclass].data[index].type + ')');
                    var value = '';
                    var genre = nodes[z].instances[instance].commandClasses[commandclass].data[index].genre;
                    if (nodes[z].instances[instance].commandClasses[commandclass].data[index].read_only == false) {
                        value += '<button type="button" class="btn btn-xs btn-primary editValue" data-valueidx="' + index + '" data-valueinstance="' + instance + '" data-valuecc="' + commandclass + '" data-valuedataitems="' + nodes[z].instances[instance].commandClasses[commandclass].data[index].data_items + '" data-valuetype="' + nodes[z].instances[instance].commandClasses[commandclass].data[index].typeZW + '" data-valuename="' + nodes[z].instances[instance].commandClasses[commandclass].data[index].name + '" data-valuevalue="' + nodes[z].instances[instance].commandClasses[commandclass].data[index].val + '" data-valuegenre="' +genre +'"><i class="fa fa-wrench"></i></button> ';
                    }

                    if (nodes[z].instances[instance].commandClasses[commandclass].data[index].write_only == true) {

                    }else if (nodes[z].instances[instance].commandClasses[commandclass].data[index].type == 'bool') {
                        var boolValue = nodes[z].instances[instance].commandClasses[commandclass].data[index].val;
                        if (nodes[z].instances[instance].commandClasses[commandclass].data[index].name != 'Exporting'){
                            if (boolValue) {
                                value +='<span class="label label-success" style="font-size:1em;">{{ON}}</span>';
                            } else {
                                value += '<span class="label label-danger" style="font-size:1em;">{{OFF}}</span>';
                            }
                        }
                        else{
                            if (boolValue) {
                                value +='{{ON}}';
                            } else {
                                value += '{{OFF}}';
                            }
                        }

                    }else if (nodes[z].instances[instance].commandClasses[commandclass].data[index].write_only == false) {
                        value += nodes[z].instances[instance].commandClasses[commandclass].data[index].val + " " + nodes[z].instances[instance].commandClasses[commandclass].data[index].units;
                    }

                        row.find("td[key=variable-value]").html(value);
                    var polling = '<span style="width : 22px;"></span>';
                    if (nodes[z].instances[instance].commandClasses[commandclass].data[index].write_only == false && first_index_polling) {
                        first_index_polling = false;

                        var polling = '<a style="position:relative;top:-1px;" class="btn btn-primary btn-xs editPolling cursor" data-valueidx="' + index + '" data-valuepolling="' + nodes[z].instances[instance].commandClasses[commandclass].data[index].poll_intensity + '" data-valueinstance="' + instance + '" data-valuecc="' + commandclass + '" data-valuedataitems="' + nodes[z].instances[instance].commandClasses[commandclass].data[index].data_items + '" data-valuetype="' + nodes[z].instances[instance].commandClasses[commandclass].data[index].typeZW + '" data-valuename="' + nodes[z].instances[instance].commandClasses[commandclass].data[index].name + '" data-valuevalue="' + nodes[z].instances[instance].commandClasses[commandclass].data[index].val + '"><i class="fa fa-wrench"></i></a> ';
                        row.find("td[key=variable-refresh]").html('<button type="button" class="btn btn-xs btn-primary forceRefresh" data-valueidx="' + index + '" data-valueinstance="' + instance + '" data-valuecc="' + commandclass + '" data-valuedataitems="' + nodes[z].instances[instance].commandClasses[commandclass].data[index].data_items + '" data-valuetype="' + nodes[z].instances[instance].commandClasses[commandclass].data[index].typeZW + '" data-valuename="' + nodes[z].instances[instance].commandClasses[commandclass].data[index].name + '" data-valuevalue="' + nodes[z].instances[instance].commandClasses[commandclass].data[index].val + '"><i class="fa fa-refresh"></i></button>');


                        if (nodes[z].instances[instance].commandClasses[commandclass].data[index].poll_intensity == 0) {
                            polling += '<span class="label label-success" style="font-size:1em;">{{Auto}}</span>';
                        } else if (nodes[z].instances[instance].commandClasses[commandclass].data[index].poll_intensity == 1) {
                            polling += '<span class="label label-warning" style="font-size:1em;">{{5 min}}</span>';
                        } else if (nodes[z].instances[instance].commandClasses[commandclass].data[index].poll_intensity == 2) {
                            //polling += '<span class="label label-success" style="font-size:1em;">{{15 min}}</span>';
                            polling += '<span class="label label-default" style="font-size:1em;">' + nodes[z].instances[instance].commandClasses[commandclass].data[index].poll_intensity + '</span>';
                        } else if (nodes[z].instances[instance].commandClasses[commandclass].data[index].poll_intensity == 3) {
                            //polling += '<span class="label label-warning" style="font-size:1em;">{{10 min}}</span>';
                            polling += '<span class="label label-default" style="font-size:1em;">' + nodes[z].instances[instance].commandClasses[commandclass].data[index].poll_intensity + '</span>';
                        } else if (nodes[z].instances[instance].commandClasses[commandclass].data[index].poll_intensity == 6) {
                            //polling += '<span class="label label-warning" style="font-size:1em;">{{5 min}}</span>';
                            polling += '<span class="label label-default" style="font-size:1em;">' + nodes[z].instances[instance].commandClasses[commandclass].data[index].poll_intensity + '</span>';
                        } else if (nodes[z].instances[instance].commandClasses[commandclass].data[index].poll_intensity == 30) {
                            //polling += '<span class="label label-danger" style="font-size:1em;">{{1 min}}</span>';
                            polling += '<span class="label label-default" style="font-size:1em;">' + nodes[z].instances[instance].commandClasses[commandclass].data[index].poll_intensity + '</span>';
                        } else {
                            polling += '<span class="label label-default" style="font-size:1em;">' + nodes[z].instances[instance].commandClasses[commandclass].data[index].poll_intensity + '</span>';
                        }
                    }
                    row.find("td[key=variable-polling]").html(polling);
                    if (nodes[z].instances[instance].commandClasses[commandclass].data[index].write_only == false) {
                        row.find("td[key=variable-updatetime]").html(app_nodes.timestampConverter(nodes[z].instances[instance].commandClasses[commandclass].data[index].updateTime));
                    }

                    var expected_data = null;
                    var pending_state = nodes[z].instances[instance].commandClasses[commandclass].data[index].pendingState;
                    if (pending_state >= 2) {
                        expected_data = nodes[z].instances[instance].commandClasses[commandclass].data[index].expected_data;
                    }
                    var data_item = nodes[z].instances[instance].commandClasses[commandclass].data[index].val;
                    if (nodes[z].instances[instance].commandClasses[commandclass].data[index].type == 'bool') {
                        if (data_item == true) {
                            data_item = '{{Oui}}';
                        } else {
                            data_item = '{{Non}}';
                        }
                    }
                    if (nodes[z].instances[instance].commandClasses[commandclass].data[index].write_only) {
                        data_item = '';
                    }
                    //systems
                    var data_units = nodes[z].instances[instance].commandClasses[commandclass].data[index].units;
                    row_system.find("td[key=system-instance]").html(instance);
                    row_system.find("td[key=system-cc]").html(commandclass + ' (0x' + Number(commandclass).toString(16) + ')');
                    row_system.find("td[key=system-index]").html(index);
                    row_system.find("td[key=system-name]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].name);
                    row_system.find("td[key=system-type]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].typeZW + ' (' + nodes[z].instances[instance].commandClasses[commandclass].data[index].type + ')');
                    var system_data = data_item + " " + data_units;
                    if (expected_data != null) {
                        system_data += '<br>(<i>' + expected_data + " " + data_units + '</i>)';
                    }
                    row_system.find("td[key=system-value]").html(system_data);
                    if (nodes[z].instances[instance].commandClasses[commandclass].data[index].read_only == false) {
                        row_system.find("td[key=system-edit]").html('<button type="button" class="btn btn-xs btn-primary editValue" data-valueidx="' + index + '" data-valueinstance="' + instance + '" data-valuecc="' + commandclass + '" data-valuedataitems="' + nodes[z].instances[instance].commandClasses[commandclass].data[index].data_items + '" data-valuetype="' + nodes[z].instances[instance].commandClasses[commandclass].data[index].typeZW + '" data-valuename="' + nodes[z].instances[instance].commandClasses[commandclass].data[index].name + '" data-valuevalue="' + nodes[z].instances[instance].commandClasses[commandclass].data[index].val + '" data-valuegenre="' +genre +'"><i class="fa fa-wrench"></i></button>');
                    }
                    if (nodes[z].instances[instance].commandClasses[commandclass].data[index].write_only == false) {
                        row_system.find("td[key=system-updatetime]").html(app_nodes.timestampConverter(nodes[z].instances[instance].commandClasses[commandclass].data[index].updateTime));
                    }
                    //parameters
                    if (typeof openzwave_node_translation.configuration[index] !== 'undefined' && openzwave_node_translation['configuration'][index].hasOwnProperty('name')) {
                        row_parameter.find("td[key=parameter-name]").html(
                            openzwave_node_translation['configuration'][index].name);
                    } else {
                        row_parameter.find("td[key=parameter-name]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].name);
                    }
                    row_parameter.find("td[key=parameter-index]").html(index);
                    row_parameter.find("td[key=parameter-type]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].typeZW);

                    if (typeof openzwave_node_translation.configuration[index] !== 'undefined' && openzwave_node_translation['configuration'][index].hasOwnProperty('list') && typeof openzwave_node_translation['configuration'][index].list[nodes[z].instances[instance].commandClasses[commandclass].data[index].val] !== 'undefined') {
                        var translation_item = openzwave_node_translation['configuration'][index].list[data_item];
                        if (expected_data != null) {
                            translation_item += '<br>(<i>' + openzwave_node_translation['configuration'][index].list[expected_data] + '</i>)';
                        }
                        row_parameter.find("td[key=parameter-value]").html(translation_item);
                    } else {
                        if (expected_data != null) {
                            data_item += '<br>(<i>' + expected_data + '</i>)';
                        }
                        row_parameter.find("td[key=parameter-value]").html(data_item);
                    }
                    if (nodes[z].instances[instance].commandClasses[commandclass].data[index].read_only == false) {
                        data_item = nodes[z].instances[instance].commandClasses[commandclass].data[index].val;
                        if (nodes[z].instances[instance].commandClasses[commandclass].data[index].write_only) {
                            data_item = '';
                        }
                        row_parameter.find("td[key=parameter-edit]").html('<button type="button" class="btn btn-xs btn-primary editParam" data-paramid="' + index + '" data-paramtype="' + nodes[z].instances[instance].commandClasses[commandclass].data[index].typeZW + '" data-paramname="' + nodes[z].instances[instance].commandClasses[commandclass].data[index].name + '" data-paramvalue="' + data_item + '"><i class="fa fa-wrench"></i></button>');
                    }
                    if (typeof openzwave_node_translation.configuration[index] !== 'undefined' && openzwave_node_translation['configuration'][index].hasOwnProperty('help')) {
                        row_parameter.find("td[key=parameter-help]").html(openzwave_node_translation['configuration'][index].help);
                    } else {
                        row_parameter.find("td[key=parameter-help]").html(nodes[z].instances[instance].commandClasses[commandclass].data[index].help);
                    }
                }
            }
        }
    },
    get_translation: function () {
        if (typeof node_id === 'undefined' || isNaN(node_id)) {
            return {configuration: {}};
        }
        var result = {configuration: {}};
        $.ajax({
            url: "plugins/openzwave/core/ajax/openzwave.ajax.php",
            dataType: 'json',
            async: false,
            global: false,
            data: {
                action: "getConfiguration",
                translation: 1,
                manufacturer_id: nodes[node_id].data.manufacturerId.value,
                product_type: nodes[node_id].data.manufacturerProductType.value,
                product_id: nodes[node_id].data.manufacturerProductId.value,
            },
            success: function (data) {
                result = data.result;
            }
        });
        return result;
    },
    show_stats: function () {
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
    show_groups: function () {
        var node = $(".node");
        var template_group = $("#template-group").html();
        var $template = $(".template");
        var tr_groups = "";
        var node_groups = nodes[app_nodes.selected_node].groups;
        $("#groups").empty();
        $("#groups").append('<br/>');
        $("#groups").append('<a class="btn btn-info btn-sm findUsage pull-right"><i class="fa fa-sitemap"></i> {{Associé à quels modules}}</a>');
        $("#groups").append('<br/><br/>');
        for (z in node_groups) {
            if (!isNaN(z)) {
                tr_groups = "";
                for (var i in node_groups[z].associations) {
                    var node_id = node_groups[z].associations[i][0];
                    var node_instance = node_groups[z].associations[i][1];
                    var id = z + '-' + node_id + '-' + node_instance;
                    if (nodes[node_id]) {
                        if (nodes[node_id].description.name != '') {
                            var node_name = nodes[node_id].description.location + ' ' + nodes[node_id].description.name;
                        } else {
                            var node_name = nodes[node_id].description.product_name;
                        }
                        if (node_instance > 0) {
                            var instanceDisplay = node_instance -1;
                            node_name += " (Instance: " + instanceDisplay + ")";
                        }
                    } else {
                        var node_name = "UNDEFINED";
                    }
                    tr_groups += "<tr gid='" + id + "'><td>" + node_id + " : " + node_name + "</td><td align='right'>";
                    tr_groups += "<button type='button' class='btn btn-danger btn-sm deleteGroup' data-groupindex='" + z + "' data-nodeid='" + node_id + "' data-nodeinstance='" + node_instance + "'><i class='fa fa-trash-o'></i> {{Supprimer}}</button>"
                    tr_groups += "</td></tr>";
                }
                var newPanel = '<div class="panel panel-primary template"><div class="panel-heading"><div class="btn-group pull-right">';
                if (count(node_groups[z].associations) < node_groups[z].maximumAssociations) {
                    newPanel += '<a id="addGroup" class="btn btn-info btn-sm addGroup" data-groupindex="' + z + '">';
                } else {
                    newPanel += '<a id="addGroup" class="btn btn-info btn-sm addGroup" disabled data-groupindex="-1">';
                }
                newPanel += '<i class="fa fa-plus"></i> {{Ajouter un noeud}}</a></div>';
                var pending_state = node_groups[z].pending;
                switch (pending_state) {
                    case 1:
                        newPanel += '<h3 class="panel-title" style="padding-top:10px;">';
                        break;
                    case 2:
                        newPanel += '<h3 class="panel-title rejectcolor" style="padding-top:10px;">';
                        break;
                    case 3:
                        newPanel += '<h3 class="panel-title pendingcolor" style="padding-top:10px;">';
                        break;
                    default:
                        newPanel += '<h3 class="panel-title" style="padding-top:10px;">';
                }
                newPanel += z + ' : ' + node_groups[z].label + ' {{(nombre maximum d\'associations :}} ' + node_groups[z].maximumAssociations + ')';

                switch (pending_state) {
                    case 1:
                        break;
                    case 2:
                        break;
                    case 3:
                        newPanel += '  <i class="fa fa-spinner fa-spin" aria-hidden="true"></i>';
                        break;
                    default:
                        break;
                }
                newPanel += '</h3></div><div class="panel-body"><table class="table">' + tr_groups + '</table></div></div>';
                $("#groups").append(newPanel);
            }
        }


    },
}

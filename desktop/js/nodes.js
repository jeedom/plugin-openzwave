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
 BASIC_CLASS_DESC={1:'{{Contrôleur}}',2:'{{Contrôleur statique}}',3:'{{Esclave}}',4:'{{Esclave pouvant être routé}}'}
 GENERIC_CLASS_DESC={1:'{{Télécommande}}',2:'{{Contrôleur statique}}',3:'{{Contrôleur A/V}}',4:'{{Afficheur}}',5: '{{Répéteur de signal}}',6: '{{Appareil}}',7: '{{Capteur de notification}}',8: '{{Thermostat}}',9: '{{Couvre-fenêtres}}',15: '{{Répéteue}}',16:'{{Interrupteur binaire}}',17: '{{Interrupteur multi-niveau}}',18: '{{Interrupteur distant}}',19: '{{Interrupteur à levier}}',20: '{{Passerelle Z-Wave/IP}}',21: '{{Noeud Z-Wave/IP}}',22: '{{Ventilation}}',23:'{{Panneau de sécurité}}',24: '{{Contrôleur mural}}',32: '{{Capteur binaire}}',33: '{{Capteur multi-niveau}}',34:'{{Niveau d\'eau}}',48:'{{Mesure d\'impulsion}}',49:'{{Mesure}}',64:'{{Contrôle d\'entrée}}',80: '{{Semi-interopérable}}',161:'{{Capteur d\'alarme}}',255:'{{Non interopérable}}'}
 QUERY_STAGE_DESC={'None':'{{Initialisation du processus de recherche de noeud}}','ProtocolInfo':'{{Récupérer des informations de protocole}}','Probe':'{{Ping le module pour voir s’il est réveillé}}','WakeUp':'{{Démarrer le processus de réveil}}','ManufacturerSpecific1':'{{Récupérer le nom du fabricant et les identifiants de produits}}','NodeInfo':'{{Récupérer les infos sur la prise en charge des classes de commandes supportées}}','NodePlusInfo':'{{Récupérer les infos ZWave+ sur la prise en charge des classes de commandes supportées}}','SecurityReport':'{{Récupérer la liste des classes de commande qui nécessitent de la sécurité}}','ManufacturerSpecific2':'{{Récupérer le nom du fabricant et les identifiants de produits}}','Versions':'{{Récupérer des informations de version}}','Instances':'{{Récupérer des informations multi-instances de classe de commande}}','Static':'{{Récupérer des informations statiques}}','CacheLoad':'{{Ping le module lors du redémarrage avec config cache de l’appareil}}','Associations':'{{Récupérer des informations sur les associations}}','Neighbors':'{{Récupérer la liste des noeuds voisins}}','Session':'{{Récupérer des informations de session}}','Dynamic':'{{Récupérer des informations dynamiques}}','Configuration':'{{Récupérer des informations de paramètre configurable}}','Complete':'{{Le processus de l’interview est terminé}}'}
 nodes = {};
 node_selected = {};
 controller_id = -1;
 var template_node = $("#template-node").html();
 var template_variable = $("#template-variable").html();
 var template_parameter = $("#template-parameter").html();
 var template_system = $("#template-system").html();
 var isWarning = false;
 var warningMessage = "";

 $('.node_action').on('click',function(){
    jeedom.openzwave.node.action({
        action : $(this).data('action'),
        node_id : node_id,
        error: function (error) {
            $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
        },
        success: function () {
         $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: 'Action réalisée avec succès', level: 'success'});
     }
 });
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
                    app_nodes.remove_ghost_node(node_id);
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
                    app_nodes.replace_failed_node(node_id);
                }
            }
        }
    }
    );
});

 $("#regenerateNodeCfgFile").off("click").on("click", function () {
    var productName = nodes[node_id].data.product_name.value;
    var manufacturerName = nodes[node_id].data.vendorString.value;
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
                    jeedom.openzwave.node.removeDeviceZWConfig({
                        node_id : node_id,
                        all : $("input[name='awesomeness']:checked").val(),
                        error: function (error) {
                            $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
                        },
                        success: function () {
                         $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: 'Action réalisée avec succès', level: 'success'});
                     }
                 });
                }
            }
        }
    }
    );
});

 $("body").off("click", ".findUsage").on("click", ".findUsage", function (e) {
    var associations = nodes[node_id].associations;
    var description = nodes[node_id].data.name.value;
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
        var manufacturerId = nodes[node_id].data.manufacturerId.value;
        var manufacturerProductId = nodes[node_id].data.manufacturerProductId.value;
        var manufacturerProductType = nodes[node_id].data.manufacturerProductType.value;
        if (key != node_id && val.product.is_valid &&
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
    options_node += node_id + ' ';
    if (nodes[node_id].data.name.value != '') {
        options_node += nodes[node_id].data.location.value + ' - ' + nodes[node_id].data.name.value;
    }
    else {
        options_node += nodes[node_id].data.product_name.value;
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
    var toNode = node_id;
    var fromNode = $('#newvaluenode').val();
    $.ajax({
        url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + fromNode + "].CopyConfigurations(" + toNode + ")",
        dataType: 'json',
        async: true,
        error: function (request, status, error) {
            handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
        },
        success: function (data) {
            $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: 'Action réalisée avec succès', level: 'success'});
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
    options_node += '<div class="col-md-10">  ' + node_id + ' ';
    if (nodes[node_id].data.name.value != '') {
        options_node += nodes[node_id].data.location.value + ' ' + nodes[node_id].data.name.value;
    }
    else {
        options_node += nodes[node_id].data.product_name.value;
    }
    options_node += '</div></div><br>';
    options_node +=  '<div class="row"><div class="col-md-2"><b>{{Destination}}</b></div><div class="col-md-10">(' + nodes[node_id].data.product_name.value +')</div></div>';
    options_node += '<form name="targetForm" action="" class="form-horizontal">';
    var foundIdentical = 0;
    $.each(nodes, function (key, val) {
        var manufacturerId = nodes[node_id].data.manufacturerId.value;
        var manufacturerProductId = nodes[node_id].data.manufacturerProductId.value;
        var manufacturerProductType = nodes[node_id].data.manufacturerProductType.value;
        if (key != node_id && val.product.is_valid &&
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
    var fromNode = node_id;
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
    for (var i in nodes[node_id].groups[group].associations) {
        associations.push(nodes[node_id].groups[group].associations[i][0] + ";" + nodes[node_id].groups[group].associations[i][1]);
    }
    var support_multi_instance = nodes[node_id].multi_instance.support == 1;
    var node_keys = [];
    $.each(nodes, function (key, val) {
        if (key != node_id) {
            if (val.description.is_static_controller || val.capabilities.isListening || val.capabilities.isFlirs) {
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
    modal.find('.modal-title').text('{{Groupe }}' + group + ' : {{Ajouter une association pour le noeud}} ' + node_id);
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
    var values = $('#newvaluenode').val().split(";");
    if ( values[1] > 0) {
        url = "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].Associations[" + $('#groupsModal').data('groupindex') + "].Add(" + values[0] + "," +  values[1] + ")";
    }else {
        url = "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].instances[0].commandClasses[0x85].Add(" + $('#groupsModal').data('groupindex') + "," + values[0] + ")";
    }
    $.ajax({
        url: url,
        dataType: 'json',
        async: true,
        error: function (request, status, error) {
            handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
        },
        success: function (data) {
         $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: 'Action réalisée avec succès', level: 'success'});
         $('#groupsModal').modal('hide');
     }
 });
});
 $("body").off("click", ".editValue").on("click", ".editValue", function (e) {
    $('#valuesModal').data('valuename', $(this).data('valuename'));
    $('#valuesModal').data('valuetype', $(this).data('valuetype'));
    $('#valuesModal').data('valueinstance', $(this).data('valueinstance'));
    $('#valuesModal').data('valuecc', $(this).data('valuecc'));
    $('#valuesModal').data('valuevalue', $(this).data('valuevalue'));
    $('#valuesModal').data('valuedataitems', $(this).data('valuedataitems'));
    $('#valuesModal').data('valuegenre', $(this).data('valuegenre'));
    $('#valuesModal').data('valueidx',  $(this).data('valueidx')).modal('show');
});
 $('#valuesModal').off('show.bs.modal').on('show.bs.modal', function (e) {
    var valueType = $(this).data('valuetype');
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
    $.ajax({
        url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=/ZWaveAPI/Run/devices[" + node_id + "].instances[" + $(this).attr('data-valueinstance') + "].commandClasses[" + $(this).attr('data-valuecc') + "].data[" + $(this).attr('data-valueidx') + "].Refresh()",
        dataType: 'json',
        async: true,
        error: function (request, status, error) {
            handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
        },
        success: function (data) {
            $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: 'Action réalisée avec succès', level: 'success'});
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
            url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].commandClasses[0x70].data",
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
            url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].instances[" + valueInstance + "].commandClasses[0x" + Number(valueCc).toString(16) + "].data[" + valueIdx + "]." + valueValue + "Button()",
            dataType: 'json',
            async: true,
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
            },
            success: function (data) {
             $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: 'Action réalisée avec succès', level: 'success'});
             $('#valuesModal').modal('hide');
         }
     });
    } else if (valueType == "Raw") {
        $.ajax({
            url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].UserCode.SetRaw(" + valueIdx + ",[" + valueValue + "],1)",
            dataType: 'json',
            async: true,
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
            },
            success: function (data) {
                $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: 'Action réalisée avec succès', level: 'success'});
                $('#valuesModal').modal('hide');
            }
        });
    }else {
        $.ajax({
            url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].instances[" + valueInstance + "].commandClasses[0x" + Number(valueCc).toString(16) + "].data[" + valueIdx + "].Set(" + encodeURIComponent(valueValue) + ")",
            dataType: 'json',
            async: true,
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
            },
            success: function (data) {
                $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: 'Action réalisée avec succès', level: 'success'});
                $('#valuesModal').modal('hide');
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
        url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].instances[" + valueInstance + "].commandClasses[0x" + Number(valueCc).toString(16) + "].data[" + valueIdx + "].SetPolling(" + encodeURIComponent(valueValue) + ")",
        dataType: 'json',
        async: true,
        error: function (request, status, error) {
            handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
        },
        success: function (data) {
          $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: 'Action réalisée avec succès', level: 'success'});
          $('#pollingModal').modal('hide');
      }
  });
});

 $("#tab-parameters").off("click").on("click", function () {
    if (!nodes[node_id].instances[0].commandClasses[112]) {
        $("#parameters").html('<br><div><b>{{Aucun paramètre prédefini trouvé pour ce noeud}}</b></div><br>');
        $("#parameters").append('<div class="row"><label class="col-lg-2">{{Paramètre :}} </label><div class="col-lg-1"><input type="text" class="form-control" id="paramidperso"></div><label class="col-lg-1">{{Valeur :}} </label><div class="col-lg-1"><input type="text" class="form-control" id="newvalueperso"></div><label class="col-lg-1">{{Taile :}}</label><div class="col-lg-1"><input type="text" class="form-control" id="sizeperso"></div> <div class="col-lg-2"><button id="sendparamperso" class="btn btn-primary">{{Envoyer le paramètre}}</a></div></div>');
        $("#sendparamperso").off("click").on("click", function () {
            var paramId = $("#paramidperso").val();
            var paramValue = $('#newvalueperso').val();
            var paramLength = $('#sizeperso').val();
            $.ajax({
                url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].commandClasses[0x70].Set(" + paramId + "," + paramValue + "," + paramLength + ")",
                dataType: 'json',
                async: true, error: function (request, status, error) {
                    handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
                },
                success: function (data) {
                    $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: 'Action réalisée avec succès', level: 'success'});
                }
            });
        });
    }
});

 $("body").off("click", ".deleteGroup").on("click", ".deleteGroup", function (e) {
    if ($(this).data('nodeinstance') > 0) {
        url = "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].Associations[" + $(this).data('groupindex') + "].Remove(" + $(this).data('nodeid') + "," + $(this).data('nodeinstance') + ")";
    } else {
        url = "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].instances[0].commandClasses[0x85].Remove(" + $(this).data('groupindex') + "," + $(this).data('nodeid') + ")"
    }
    $.ajax({
        url: url,
        dataType: 'json',
        success: function (data) {
         $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: 'Action réalisée avec succès', level: 'success'});
     },
     error: function (request, status, error) {
        handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
    }
});
});

 $("body").off("click", ".addGroup").on("click", ".addGroup", function (e) {
    var group = $(this).data('groupindex');
    if(group == -1){
        return;
    }
    $('#groupsModal').data('groupindex', group);
    $('#groupsModal').modal('show');
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
        url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/devices[" + node_id + "].commandClasses[0x70].Set(" + paramId + "," + encodeURIComponent(paramValue2) + "," + paramLength + ")",
        dataType: 'json',
        async: true,
        error: function (request, status, error) {
            handleAjaxError(request, status, error, $('#div_nodeConfigureOpenzwaveAlert'));
        },
        success: function (data) {
         $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: 'Action réalisée avec succès', level: 'success'});
         $('#paramsModal').modal('hide');
     }
 });
});

 $("body").off("click", ".copyParams").on("click", ".copyParams", function (e) {
    $('#copyParamsModal').modal('show');
});
 $("body").off("click", ".copyToParams").on("click", ".copyToParams", function (e) {
    $('#copyToParamsModal').modal('show');
});

 function load_all_node(){
    jeedom.openzwave.network.info({
        info : 'getNodesList',
        error: function (error) {
            $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
        },
        success: function (data) {
            nodes = data['devices'];
            for (var i in data['devices']) {
                if (isset(data['devices'][i]['description']) && isset(data['devices'][i]['description']['is_static_controller']) && data['devices'][i]['description']['is_static_controller']) {
                    controller_id = i;
                }
            }
            display_node_info();
        }
    });
}

function display_node_stats(){
   jeedom.openzwave.node.info({
    node_id : node_id,
    info:'getNodeStatistics',
    error: function (error) {
        $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
    },
    success: function (data) {
        $('#div_nodeConfigure').setValues(data, '.zwaveStatsAttr');
    }
});
}

function display_node_info(){
   jeedom.openzwave.node.info({
    node_id : node_id,
    info:'all',
    global:false,
    error: function (error) {
        $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
    },
    success: function (data) {
        node_selected = data;
        var nodeIsFailed = (data.data.isFailed) ? data.data.isFailed.value : false;
        data.data.lastReceived.updateTime = jeedom.openzwave.timestampConverter(data.data.lastReceived.updateTime)
        data.data.basicDeviceClassDescription = (isset(BASIC_CLASS_DESC[data.data.basicType.value])) ? BASIC_CLASS_DESC[parseInt(data.data.basicType.value, 0)] : basicDeviceClass;
        data.data.genericDeviceClassDescription = (isset(GENERIC_CLASS_DESC[data.data.genericType.value])) ? GENERIC_CLASS_DESC[data.data.genericType.value] : '';
        var queryStageDescrition = (isset(QUERY_STAGE_DESC[data.data.state.value])) ? QUERY_STAGE_DESC[data.data.state.value] : '{{Inconnue}}';
        var queryStageIndex = 0;
        for(i in QUERY_STAGE_DESC){
            if(i == data.data.state.value){
                break;
            }
            queryStageIndex++;
        }
        if (data.last_notification.next_wakeup != null) {
            $("#div_nodeConfigure .node-next-wakeup-span").show();
        } else {
            $("#div_nodeConfigure .node-next-wakeup-span").hide();
        }
        data.data.zwave_id = "{{Identifiant du fabricant :}} <span class='label label-default' style='font-size : 1em;'>" + data.data.manufacturerId.value + " [" + data.data.manufacturerId.hex + "]</span> {{Type de produit :}} <span class='label label-default' style='font-size : 1em;'>" + data.data.manufacturerProductType.value + ' [' + data.data.manufacturerProductType.hex + "]</span> {{Identifiant du produit :}} <span class='label label-default' style='font-size : 1em;'>" + data.data.manufacturerProductId.value + ' [' + data.data.manufacturerProductId.hex + "]</span>";
        data.data.queryStage = (nodeIsFailed) ? 'Dead' : data.data.state.value;
        if (queryStageIndex > 2) {
            if (data.data.isListening.value) {
                $("#div_nodeConfigure .node-sleep").removeClass("label-default");
                $("#div_nodeConfigure .node-sleep").html('<i class="fa fa-plug text-success fa-lg"></i>');
                $("#div_nodeConfigure .node-battery-span").hide();
            }else {
                $("#div_nodeConfigure .node-sleep").removeClass("label-success").addClass("label-default")
                if (data.data.battery_level.value != null) {
                    if (data.data.isFrequentListening.value) {
                        $("#div_nodeConfigure .node-sleep").html("{{Endormi <i>(FLiRS)</i>}}");
                    } else if (data.data.can_wake_up.value) {
                        if (data.data.isAwake.value) {
                            $("#div_nodeConfigure .node-sleep").removeClass("label-default").addClass("label-success")
                            $("#div_nodeConfigure .node-sleep").html("{{Réveillé}}");
                        }else {
                            $("#div_nodeConfigure .node-sleep").html("{{Endormi}}");
                        }
                    }
                    else {
                        $("#div_nodeConfigure .node-sleep").html("{{Endormi}}");
                    }
                    $("#div_nodeConfigure .node-battery-span").show();
                }else if (data.data.can_wake_up.value) {
                    $("#div_nodeConfigure .node-sleep").html("---");
                    $("#div_nodeConfigure .node-battery-span").hide();
                }
            }
        }else {
            $("#div_nodeConfigure .node-sleep").html("---");
            $("#div_nodeConfigure .node-battery-span").hide();
        }
        $('#div_nodeConfigure').setValues(data.data, '.zwaveNodeAttr');
        if (controller_id != -1) {
            var found = false;
            var hasGroup = false;
            for (zz in data.groups) {
                if (!isNaN(zz)) {
                    hasGroup = true;
                    for (var i in data.groups[zz].associations) {
                        var node_id = data.groups[zz].associations[i][0];
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
        if (data.data.genericType.value == 1) {
            data.data.can_wake_up.value = true;
        }
        $("#removeGhostNode").prop("disabled", nodeIsFailed || !data.data.can_wake_up.value);

        if (data.data.isRouting.value) {
            $("#div_nodeConfigure .node-routing").html("<li>{{Le noeud a des capacités de routage (capable de faire passer des commandes à d'autres noeuds)}}</li>");
        }else {
            $("#div_nodeConfigure .node-routing").html("");
        }
        if (data.data.isSecurity.value) {
            $("#div_nodeConfigure .node-isSecurity").html("<li>{{Le noeud supporte les caractéristiques de sécurité avancées}}</li>");
            $("#div_nodeConfigure .node-security").html("{{Classe de sécurité:}} " + data.data.security.value);
        }else {
            $("#div_nodeConfigure .node-isSecurity").html("");
            $("#div_nodeConfigure .node-security").html("");
        }
        if (data.data.isListening.value) {
            $("#div_nodeConfigure .node-listening").html("<li>{{Le noeud est alimenté et écoute en permanence}}</li>");
        }else {
            $("#div_nodeConfigure .node-listening").html("");
        } if (data.data.isFrequentListening.value) {
            $("#div_nodeConfigure .node-isFrequentListening").html("<li>{{<i>FLiRS</i>, routeurs esclaves à écoute fréquente}}</li>");
        }else {
            $("#div_nodeConfigure .node-isFrequentListening").html("");
        }
        if (data.data.isBeaming.value) {
            $("#div_nodeConfigure .node-isBeaming").html("<li>{{Le noeud est capable d'envoyer une trame réseau}}</li>");
        }else {
            $("#div_nodeConfigure .node-isBeaming").html("");
        }
        if (data.data.isZwavePlus.value) {
            $("#div_nodeConfigure .node-zwaveplus").html(" {{ZWAVE PLUS}}");
        }else {
            $("#div_nodeConfigure .node-zwaveplus").html("");
        }
        if (data.data.isSecured.enabled) {
            if (data.data.isSecured.value) {
                $("#div_nodeConfigure .node-isSecured").html("<i class='fa fa-lock' aria-hidden='true'></i>");
            }else {
                $("#div_nodeConfigure .node-isSecured").html("<i class='fa fa-unlock' aria-hidden='true'></i>");
            }
        }else{
            $("#div_nodeConfigure .node-isSecured").html("");
        }
        var neighbours = data.data.neighbours.value.join();
        if (queryStageIndex > 13) {
            if (neighbours != "") {
                $("#div_nodeConfigure .node-neighbours").html(neighbours);
            }else {
                $("#div_nodeConfigure .node-neighbours").html("...");
                if (genericDeviceClass != 1 && (genericDeviceClass != 8 || data.data.isListening.value)) {
                    warningMessage += "<li{{Liste des voisins non disponible}} <br/>{{Utilisez}} <button type='button' id='healNode' class='btn btn-success healNode'><i class='fa fa-medkit'></i> {{Soigner le noeud}}</button> {{ou}} <button type='button' id='requestNodeNeighboursUpdate' class='btn btn-primary requestNodeNeighboursUpdate'><i class='fa fa-sitemap'></i> {{Mise à jour des noeuds voisins}}</button> {{pour corriger.}}</li>";
                    isWarning = true;
                }
            }
        }else {
            $("#div_nodeConfigure .node-neighbours").html("<i>{{La liste des noeuds voisin n'est pas encore disponible.}}</i>");
        }
        if (queryStageIndex > 7 && data.data.product_name.value == "") {
            warningMessage += "<li>{{Les identifiants constructeur ne sont pas detectés.}}<br/>{{Utilisez}} <button type='button' id='refreshNodeInfo' class='btn btn-success refreshNodeInfo'><i class='fa fa-retweet'></i> {{Rafraîchir infos du noeud}}</button> {{pour corriger}}</li>";
            isWarning = true;
        }
        if (isWarning) {
            if (data.data.can_wake_up.value) {
                warningMessage += "<br><p>{{Le noeud est dormant et nécessite un réveil avant qu'une commande puisse être exécutée.<br/>Vous pouvez le réveiller manuellement ou attendre son délai de réveil.}}<br/>{{Voir l'interval de réveil dans l'onglet Système}}</p>";
            }
            $("#div_nodeConfigure .panel-danger").show();
            $("#div_nodeConfigure .node-warning").html(warningMessage);
        }else {
            $("#div_nodeConfigure .panel-danger").hide();
            $("#div_nodeConfigure .node-warning").html("");
        }
        var variables = "";
        var parameters = "";
        var system_variables = "";
        for (instance in data.instances) {
            for (commandclass in data.instances[instance].commandClasses) {
                for (index in data.instances[instance].commandClasses[commandclass].data) {
                    if (!isNaN(index)) {
                        var id = instance + ":" + commandclass + ":" + index;
                        var genre = data.instances[instance].commandClasses[commandclass].data[index].genre;
                        var pending_state = data.instances[instance].commandClasses[commandclass].data[index].pendingState;
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
        $("#div_nodeConfigure .variables").html(variables);
        $("#div_nodeConfigure .parameters").html(parameters);
        $("#div_nodeConfigure .system_variables").html(system_variables);
        openzwave_node_translation = {configuration: {}};
        for (instance in data.instances) {
            for (commandclass in data.instances[instance].commandClasses) {
                var first_index_polling = true;
                for (index in data.instances[instance].commandClasses[commandclass].data) {
                    var id = instance + ":" + commandclass + ":" + index;
                    var row = $("#div_nodeConfigure tr[vid='" + id + "']");
                    var row_parameter = $("#div_nodeConfigure tr[pid='" + id + "']");
                    var row_system = $("#div_nodeConfigure tr[sid='" + id + "']");
                    row.find("td[key=variable-instance]").html(instance);
                    row.find("td[key=variable-cc]").html(commandclass + ' (0x' + Number(commandclass).toString(16) + ')');
                    row.find("td[key=variable-index]").html(index);
                    row.find("td[key=variable-name]").html(data.instances[instance].commandClasses[commandclass].data[index].name);
                    row.find("td[key=variable-type]").html(data.instances[instance].commandClasses[commandclass].data[index].typeZW + ' (' + data.instances[instance].commandClasses[commandclass].data[index].type + ')');
                    var value = '';
                    var genre = data.instances[instance].commandClasses[commandclass].data[index].genre;
                    if (data.instances[instance].commandClasses[commandclass].data[index].read_only == false) {
                        value += '<button type="button" class="btn btn-xs btn-primary editValue" data-valueidx="' + index + '" data-valueinstance="' + instance + '" data-valuecc="' + commandclass + '" data-valuedataitems="' + data.instances[instance].commandClasses[commandclass].data[index].data_items + '" data-valuetype="' + data.instances[instance].commandClasses[commandclass].data[index].typeZW + '" data-valuename="' + data.instances[instance].commandClasses[commandclass].data[index].name + '" data-valuevalue="' + data.instances[instance].commandClasses[commandclass].data[index].val + '" data-valuegenre="' +genre +'"><i class="fa fa-wrench"></i></button> ';
                    }
                    if (data.instances[instance].commandClasses[commandclass].data[index].type == 'bool') {
                        var boolValue = data.instances[instance].commandClasses[commandclass].data[index].val;
                        if (data.instances[instance].commandClasses[commandclass].data[index].name != 'Exporting'){
                            if (boolValue) {
                                value +='<span class="label label-success" style="font-size:1em;">{{ON}}</span>';
                            } else {
                                value += '<span class="label label-danger" style="font-size:1em;">{{OFF}}</span>';
                            }
                        }else{
                            if (boolValue) {
                                value +='{{ON}}';
                            } else {
                                value += '{{OFF}}';
                            }
                        }
                    }else if (data.instances[instance].commandClasses[commandclass].data[index].write_only == false) {
                        value += data.instances[instance].commandClasses[commandclass].data[index].val + " " + data.instances[instance].commandClasses[commandclass].data[index].units;
                    }
                    row.find("td[key=variable-value]").html(value);
                    var polling = '<span style="width : 22px;"></span>';
                    if (data.instances[instance].commandClasses[commandclass].data[index].write_only == false && first_index_polling) {
                        first_index_polling = false;
                        var polling = '<a style="position:relative;top:-1px;" class="btn btn-primary btn-xs editPolling cursor" data-valueidx="' + index + '" data-valuepolling="' + data.instances[instance].commandClasses[commandclass].data[index].poll_intensity + '" data-valueinstance="' + instance + '" data-valuecc="' + commandclass + '" data-valuedataitems="' + data.instances[instance].commandClasses[commandclass].data[index].data_items + '" data-valuetype="' + data.instances[instance].commandClasses[commandclass].data[index].typeZW + '" data-valuename="' + data.instances[instance].commandClasses[commandclass].data[index].name + '" data-valuevalue="' + data.instances[instance].commandClasses[commandclass].data[index].val + '"><i class="fa fa-wrench"></i></a> ';
                        row.find("td[key=variable-refresh]").html('<button type="button" class="btn btn-xs btn-primary forceRefresh" data-valueidx="' + index + '" data-valueinstance="' + instance + '" data-valuecc="' + commandclass + '" data-valuedataitems="' + data.instances[instance].commandClasses[commandclass].data[index].data_items + '" data-valuetype="' + data.instances[instance].commandClasses[commandclass].data[index].typeZW + '" data-valuename="' + data.instances[instance].commandClasses[commandclass].data[index].name + '" data-valuevalue="' + data.instances[instance].commandClasses[commandclass].data[index].val + '"><i class="fa fa-refresh"></i></button>');
                        if (data.instances[instance].commandClasses[commandclass].data[index].poll_intensity == 0) {
                            polling += '<span class="label label-success" style="font-size:1em;">{{Auto}}</span>';
                        } else if (data.instances[instance].commandClasses[commandclass].data[index].poll_intensity == 1) {
                            polling += '<span class="label label-warning" style="font-size:1em;">{{5 min}}</span>';
                        } else if (data.instances[instance].commandClasses[commandclass].data[index].poll_intensity == 2) {
                            polling += '<span class="label label-default" style="font-size:1em;">' + data.instances[instance].commandClasses[commandclass].data[index].poll_intensity + '</span>';
                        } else if (data.instances[instance].commandClasses[commandclass].data[index].poll_intensity == 3) {
                            polling += '<span class="label label-default" style="font-size:1em;">' + data.instances[instance].commandClasses[commandclass].data[index].poll_intensity + '</span>';
                        } else if (data.instances[instance].commandClasses[commandclass].data[index].poll_intensity == 6) {
                            polling += '<span class="label label-default" style="font-size:1em;">' + data.instances[instance].commandClasses[commandclass].data[index].poll_intensity + '</span>';
                        } else if (data.instances[instance].commandClasses[commandclass].data[index].poll_intensity == 30) {
                            polling += '<span class="label label-default" style="font-size:1em;">' + data.instances[instance].commandClasses[commandclass].data[index].poll_intensity + '</span>';
                        } else {
                            polling += '<span class="label label-default" style="font-size:1em;">' + data.instances[instance].commandClasses[commandclass].data[index].poll_intensity + '</span>';
                        }
                    }
                    row.find("td[key=variable-polling]").html(polling);
                    if (data.instances[instance].commandClasses[commandclass].data[index].write_only == false) {
                        row.find("td[key=variable-updatetime]").html(jeedom.openzwave.timestampConverter(data.instances[instance].commandClasses[commandclass].data[index].updateTime));
                    }
                    var expected_data = null;
                    var pending_state = data.instances[instance].commandClasses[commandclass].data[index].pendingState;
                    if (pending_state >= 2) {
                        expected_data = data.instances[instance].commandClasses[commandclass].data[index].expected_data;
                    }
                    var data_item = data.instances[instance].commandClasses[commandclass].data[index].val;
                    if (data.instances[instance].commandClasses[commandclass].data[index].type == 'bool') {
                        if (data_item == true) {
                            data_item = '{{Oui}}';
                        } else {
                            data_item = '{{Non}}';
                        }
                    }
                    if (data.instances[instance].commandClasses[commandclass].data[index].write_only) {
                        data_item = '';
                    }
                    var data_units = data.instances[instance].commandClasses[commandclass].data[index].units;
                    row_system.find("td[key=system-instance]").html(instance);
                    row_system.find("td[key=system-cc]").html(commandclass + ' (0x' + Number(commandclass).toString(16) + ')');
                    row_system.find("td[key=system-index]").html(index);
                    row_system.find("td[key=system-name]").html(data.instances[instance].commandClasses[commandclass].data[index].name);
                    row_system.find("td[key=system-type]").html(data.instances[instance].commandClasses[commandclass].data[index].typeZW + ' (' + data.instances[instance].commandClasses[commandclass].data[index].type + ')');
                    var system_data = data_item + " " + data_units;
                    if (expected_data != null) {
                        system_data += '<br>(<i>' + expected_data + " " + data_units + '</i>)';
                    }
                    row_system.find("td[key=system-value]").html(system_data);
                    if (data.instances[instance].commandClasses[commandclass].data[index].read_only == false) {
                        row_system.find("td[key=system-edit]").html('<button type="button" class="btn btn-xs btn-primary editValue" data-valueidx="' + index + '" data-valueinstance="' + instance + '" data-valuecc="' + commandclass + '" data-valuedataitems="' + data.instances[instance].commandClasses[commandclass].data[index].data_items + '" data-valuetype="' + data.instances[instance].commandClasses[commandclass].data[index].typeZW + '" data-valuename="' + data.instances[instance].commandClasses[commandclass].data[index].name + '" data-valuevalue="' + data.instances[instance].commandClasses[commandclass].data[index].val + '" data-valuegenre="' +genre +'"><i class="fa fa-wrench"></i></button>');
                    }
                    if (data.instances[instance].commandClasses[commandclass].data[index].write_only == false) {
                        row_system.find("td[key=system-updatetime]").html(jeedom.openzwave.timestampConverter(data.instances[instance].commandClasses[commandclass].data[index].updateTime));
                    }
                    if (typeof openzwave_node_translation.configuration[index] !== 'undefined' && openzwave_node_translation['configuration'][index].hasOwnProperty('name')) {
                        row_parameter.find("td[key=parameter-name]").html(openzwave_node_translation['configuration'][index].name);
                    } else {
                        row_parameter.find("td[key=parameter-name]").html(data.instances[instance].commandClasses[commandclass].data[index].name);
                    }
                    row_parameter.find("td[key=parameter-index]").html(index);
                    row_parameter.find("td[key=parameter-type]").html(data.instances[instance].commandClasses[commandclass].data[index].typeZW);
                    if (typeof openzwave_node_translation.configuration[index] !== 'undefined' && openzwave_node_translation['configuration'][index].hasOwnProperty('list') && typeof openzwave_node_translation['configuration'][index].list[data.instances[instance].commandClasses[commandclass].data[index].val] !== 'undefined') {
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
                    if (data.instances[instance].commandClasses[commandclass].data[index].read_only == false) {
                        data_item = data.instances[instance].commandClasses[commandclass].data[index].val;
                        if (data.instances[instance].commandClasses[commandclass].data[index].write_only) {
                            data_item = '';
                        }
                        row_parameter.find("td[key=parameter-edit]").html('<button type="button" class="btn btn-xs btn-primary editParam" data-paramid="' + index + '" data-paramtype="' + data.instances[instance].commandClasses[commandclass].data[index].typeZW + '" data-paramname="' + data.instances[instance].commandClasses[commandclass].data[index].name + '" data-paramvalue="' + data_item + '"><i class="fa fa-wrench"></i></button>');
                    }
                    if (typeof openzwave_node_translation.configuration[index] !== 'undefined' && openzwave_node_translation['configuration'][index].hasOwnProperty('help')) {
                        row_parameter.find("td[key=parameter-help]").html(openzwave_node_translation['configuration'][index].help);
                    } else {
                        row_parameter.find("td[key=parameter-help]").html(data.instances[instance].commandClasses[commandclass].data[index].help);
                    }
                }
            }
        }
        show_groups();
        if($('#div_nodeConfigure').html() != undefined && $('#div_nodeConfigure').is(':visible')){
            setTimeout(function(){ display_node_info(); }, 2000);
        }
    }
});
}

function show_groups(){
    var node = $(".node");
    var template_group = $("#template-group").html();
    var $template = $(".template");
    var tr_groups = "";
    $("#groups").empty();
    $("#groups").append('<br/>');
    $("#groups").append('<a class="btn btn-info btn-sm findUsage pull-right"><i class="fa fa-sitemap"></i> {{Associé à quels modules}}</a>');
    $("#groups").append('<br/><br/>');
    for (z in node_selected.groups) {
        if (!isNaN(z)) {
            tr_groups = "";
            for (var i in node_selected.groups[z].associations) {
                var node_id = node_selected.groups[z].associations[i][0];
                var node_instance = node_selected.groups[z].associations[i][1];
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
            if (count(node_selected.groups[z].associations) < node_selected.groups[z].maximumAssociations) {
                newPanel += '<a id="addGroup" class="btn btn-info btn-sm addGroup" data-groupindex="' + z + '">';
            } else {
                newPanel += '<a id="addGroup" class="btn btn-info btn-sm addGroup" disabled data-groupindex="-1">';
            }
            newPanel += '<i class="fa fa-plus"></i> {{Ajouter un noeud}}</a></div>';
            var pending_state = node_selected.groups[z].pending;
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
            newPanel += z + ' : ' + node_selected.groups[z].label + ' {{(nombre maximum d\'associations :}} ' + node_selected.groups[z].maximumAssociations + ')';
            switch (pending_state) {
                case 3:
                newPanel += '  <i class="fa fa-spinner fa-spin" aria-hidden="true"></i>';
                break;
            }
            newPanel += '</h3></div><div class="panel-body"><table class="table">' + tr_groups + '</table></div></div>';
            $("#groups").append(newPanel);
        }
    }
}


$("body").off("click", ".refreshParams").on("click", ".refreshParams", function (e) {
    jeedom.openzwave.node.refreshClass({
        node_id : node_id,
        class : "0x70",
        error: function (error) {
            $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
        },
        success: function () {
         $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: 'Action réalisée avec succès', level: 'success'});
     }
 })
});

function getTranslation(){
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
            manufacturer_id: node_selected.data.manufacturerId.value,
            product_type: node_selected.data.manufacturerProductType.value,
            product_id: node_selected.data.manufacturerProductId.value,
        },
        success: function (data) {
            result = data.result;
        }
    });
    return result;
}

display_node_stats();
load_all_node();
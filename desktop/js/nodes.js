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
         $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
     }
 });
});

 $("#removeGhostNode").off("click").on("click", function () {
    bootbox.confirm('{{Les étapes suivantes seront éxécutées:Arrêt du réseau Z-Wave,Retirer classe de commande de Wake Up du fichier ZWCFG,Redémarrage du réseau Z-WaveAttendre que le réseau soit à nouveau opérationnel (2-5 minutes),Nœud passe en échec,Supprimer le nœud en échec,Validation de la suppression.}}', function (result) {
     if (result) {
        jeedom.openzwave.node.action({
          node_id: node_id,
          action : 'removeGhostNode',
          error: function (error) {
            $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
        },
        success: function (data) {
           $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
       }
   });
    }
});
});

 $("#replaceFailedNode").off("click").on("click", function () {
   bootbox.confirm('{{Cette action permet de remplacer un nœud en échec.Attention, le controleur sera automatiquement en mode inclusion. Veuillez lancer la procédure sur votre module après la confirmation de cette action.}}', function (result) {
     if (result) {
        jeedom.openzwave.node.action({
          node_id: node_id,
          action : 'replaceFailedNode',
          error: function (error) {
            $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
        },
        success: function (data) {
           $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
       }
   });
    }
});
});

 $("#regenerateNodeCfgFile").off("click").on("click", function () {
    bootbox.prompt({
        title: "{{Lancer la regénérer sur ?}}",
        inputType: 'select',
        inputOptions: [
        {
            text: '{{Ce module seulement}}',
            value: '0',
        },
        {
            text: '{{Tous les modules}} : '+node_selected.data.product_name.value+'  '+node_selected.data.vendorString.value,
            value: '1',
        }
        ],
        callback: function (result) {
            if(result !== null){
             jeedom.openzwave.node.removeDeviceZWConfig({
                node_id : node_id,
                all : result,
                error: function (error) {
                    $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
                },
                success: function () {
                 $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
             }
         });
         }
     }
 });
});

 $("body").off("click", ".findUsage").on("click", ".findUsage", function (e) {
    var associations = node_selected.associations;
    var description = node_selected.data.name.value;
    var message = '{{Liste des groupes d\'associations où le module}} <b><span class="node-name label label-default" style="font-size : 1em;">' + description + '</span></b> {{est utilisé:}}</p><br><ul>';
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
    message += '</ul>'
    bootbox.alert(message);
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
   jeedom.openzwave.node.refreshData({
    node_id : node_id,
    instance : $(this).attr('data-valueinstance'),
    class :  $(this).attr('data-valuecc'),
    index : $(this).attr('data-valueidx'),
    error: function (error) {
        $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
    },
    success: function () {
       $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
   }
});
});

 $("body").off("click", ".editPolling").on("click", ".editPolling", function (e) {
    var idx = $(this).data('valueidx');
    var instance = $(this).data('valueinstance');
    var cc = $(this).data('valuecc');
    bootbox.prompt({
        title: "{{Changer le rafraichissement}}",
        inputType: 'select',
        inputOptions: [
        {text: '{{Auto}}',value: '0'},
        {text: '{{5 min}}',value: '1'}
        ],
        callback: function (result) {
         if(result != null){
            jeedom.openzwave.node.setPolling({
                node_id : node_id,
                instance : instance,
                class :  cc,
                index : idx,
                polling : result,
                error: function (error) {
                    $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
                },
                success: function () {
                   $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
               }
           });
        }
    }
});
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
        jeedom.openzwave.node.dataClass({
            node_id : node_id,
            class : 112,
            error: function (error) {
                $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
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
    if ($('#valuesModal').data('valuetype') == "Button") {
        jeedom.openzwave.node.button({
            node_id : node_id,
            instance : $('#valuesModal').data('valueinstance'),
            class :  $('#valuesModal').data('valuecc'),
            index : $('#valuesModal').data('valueidx'),
            action : $('input[name=newvaluevalue]:checked', '#valuesModal').val(),
            error: function (error) {
                $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
            },
            success: function () {
               $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
           }
       });
    } else if ($('#valuesModal').data('valuetype') == "Raw") {
     jeedom.openzwave.node.setRaw({
        node_id : node_id,
        slot_id : $('#valuesModal').data('valueidx'),
        value :  $('#newvaluevalue').val(),
        error: function (error) {
            $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
        },
        success: function () {
           $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
       }
   });
 }else {
    jeedom.openzwave.node.set({
        node_id : node_id,
        instance : $('#valuesModal').data('valueinstance'),
        class :  $('#valuesModal').data('valuecc'),
        index : $('#valuesModal').data('valueidx'),
        value : ($('#valuesModal').data('valuetype') == 'Bool') ? $('input[name=newvaluevalue]:checked', '#valuesModal').val() : $('#newvaluevalue').val(),
        error: function (error) {
            $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
        },
        success: function () {
           $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
       }
   });
}
$('#valuesModal').modal('hide');
});


 $("#tab-parameters").off("click").on("click", function () {
    if (!node_selected.instances[0].commandClasses[112]) {
        $("#parameters").html('<br><div><b>{{Aucun paramètre prédefini trouvé pour ce noeud}}</b></div><br>');
        $("#parameters").append('<div class="row"><label class="col-lg-2">{{Paramètre :}} </label><div class="col-lg-1"><input type="text" class="form-control" id="paramidperso"></div><label class="col-lg-1">{{Valeur :}} </label><div class="col-lg-1"><input type="text" class="form-control" id="newvalueperso"></div><label class="col-lg-1">{{Taile :}}</label><div class="col-lg-1"><input type="text" class="form-control" id="sizeperso"></div> <div class="col-lg-2"><a id="sendparamperso" class="btn btn-primary">{{Envoyer le paramètre}}</a></div></div>');
        $("#sendparamperso").off("click").on("click", function () {
            jeedom.openzwave.node.setParam({
                node_id : node_id,
                id :  $("#paramidperso").val(),
                length :  $('#sizeperso').val(),
                value : $('#newvalueperso').val(),
                error: function (error) {
                    $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
                },
                success: function () {
                   $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
               }
           });  
        });
    }
});

 $("body").off("click", ".deleteGroup").on("click", ".deleteGroup", function (e) {
   jeedom.openzwave.node.group({
    node_id : node_id,
    instance : $(this).data('nodeinstance'),
    group :  $(this).data('groupindex'),
    target_id : $(this).data('nodeid'),
    action: 'remove',
    error: function (error) {
        $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
    },
    success: function () {
       $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
   }
});
});

 $("body").off("click", ".addGroup").on("click", ".addGroup", function (e) {
    var group = $(this).data('groupindex');
    if(group == -1){
        return;
    }
    var associations = [];
    for (var i in node_selected.groups[group].associations) {
        associations.push(node_selected.groups[group].associations[i][0] + ";" + node_selected.groups[group].associations[i][1]);
    }
    var options = [];
    $.each(nodes, function (key, val) {
        if (key != node_id) {
            var text = (nodes[key].description.name != '') ? key + ' : '+nodes[key].description.location + ' - ' + nodes[key].description.name : key + ' : ' + nodes[key].description.product_name;
            if (val.description.is_static_controller || val.capabilities.isListening || val.capabilities.isFlirs) {
                if (node_selected.multi_instance.support) {
                    if (val.description.is_static_controller) {
                     if (associations.indexOf(key + ';0') < 0) {
                      options.push({value : key + ';0', text :  text + ' (0)'});
                  }
                  if (associations.indexOf(key + ';1') < 0) {
                     options.push({value : key + ';1', text :  text + ' (1)'});
                 }
             }else if(val.multi_instance.instances == 1){
               if (associations.indexOf(key + ';0') < 0) {
                  options.push({value : key + ';0', text :  text + ' (0)'});
              }
          }else {
            for (i = 1; i <= val.multi_instance.instances; i++) {
                if (associations.indexOf(key + ';'+i) >= 0) {
                    continue;
                }
                options.push({value : key + ';'+i, text :  text + ' ('+i+')'});
            }
        }
    }else{
       if (associations.indexOf(key + ';0') < 0) {
         options.push({value : key + ';0', text :  text + ' (0)'});
     }
 }
}
}
});
    bootbox.prompt({
        title: "{{Selectionner le noeud : }}",
        inputType: 'select',
        inputOptions: options,
        callback: function (result) {
            if(result===null){
                return;
            }
            var values = result.split(";");
            jeedom.openzwave.node.group({
                node_id : node_id,
                instance : values[1],
                group : group,
                target_id : values[0],
                action : 'add',
                error: function (error) {
                    $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
                },
                success: function () {
                   $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
               }
           });
        }
    });
});

 $("#saveParam").off("click").on("click", function (e) {
    if ( $('#paramsModal').data('paramtype') == "Bool") {
        var paramValue = $('input[name=newvalue]:checked', '#paramsModal').val();
    } else if ( $('#paramsModal').data('paramtype') == "Button") {
        var paramValue = $('input[name=newvalue]:checked', '#paramsModal').val();
    } else {
        var paramValue = $('#newvalue').val();
    }
    jeedom.openzwave.node.setParam({
        node_id : node_id,
        id :  $('#paramsModal').data('paramid'),
        length :  paramValue.length,
        value : paramValue.replace(/\//g, '@'),
        error: function (error) {
            $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
        },
        success: function () {
           $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
       }
   }); 
    $('#paramsModal').modal('hide'); 
});

 $("body").off("click", ".copyParams").on("click", ".copyParams", function (e) {
     var options_node = '<div class="row"><div class="col-md-2"><b>{{Source}}</b></div>';
     options_node += '<div class="col-md-10"><select class="form-control" id="newvaluenode" style="display:inline-block;width:400px;">';
     var foundIdentical = 0;
     $.each(nodes, function (key, val) {
        var manufacturerId = node_selected.data.manufacturerId.value;
        var manufacturerProductId = node_selected.data.manufacturerProductId.value;
        var manufacturerProductType = node_selected.data.manufacturerProductType.value;
        if (key != node_id && val.product.is_valid && val.product.manufacturer_id == manufacturerId && val.product.product_id == manufacturerProductId && val.product.product_type == manufacturerProductType) {
            foundIdentical = 1;
            options_node += '<option value="' + key + '">' + key + ' ';
            options_node +=  (val.description.name != '') ? val.description.location + ' - ' + val.description.name : val.description.product_name;
            options_node += '</option>';
        }
    });
     options_node += '</select></div></div>';
     options_node += '<br>';
     options_node += '<div class="row"><div class="col-md-2"><b>{{Destination}}</b></div>';
     options_node += '<div class="col-md-10">';
     options_node += node_id + ' ';
     options_node += (node_selected.data.name.value != '') ? node_selected.data.location.value + ' - ' + node_selected.data.name.value : node_selected.data.product_name.value;
     options_node += '</div>';
     options_node += '</div>';
     if (foundIdentical == 0) {
        modal.find('#saveCopyParams').hide();
        options_node = '{{Aucun module identique trouvé}}';
    }
    bootbox.dialog({
        title: "{{Sélection du module source}}",
        message: options_node,
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
                    jeedom.openzwave.node.copyConfigurations({
                        node_id : $('#newvaluenode').val(),
                        target_id : node_id,
                        error: function (error) {
                            $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
                        },
                        success: function () {
                         $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
                     }
                 });
                }
            }
        }
    });
});
 $("body").off("click", ".copyToParams").on("click", ".copyToParams", function (e) {
    var options_node = '<div class="container-fluid">';
    options_node += '<div class="row"><div class="col-md-2"><b>{{Source}}</b></div>';
    options_node += '<div class="col-md-10">  ' + node_id + ' ';
    node_selected +=  (node_selected.data.name.value != '') ? node_selected.data.location.value + ' ' + node_selected.data.name.value : node_selected.data.product_name.value;
    options_node += '</div></div><br>';
    options_node +=  '<div class="row"><div class="col-md-2"><b>{{Destination}}</b></div><div class="col-md-10">(' + node_selected.data.product_name.value +')</div></div>';
    options_node += '<form name="targetForm" action="" class="form-horizontal">';
    var foundIdentical = 0;
    $.each(nodes, function (key, val) {
        var manufacturerId = node_selected.data.manufacturerId.value;
        var manufacturerProductId = node_selected.data.manufacturerProductId.value;
        var manufacturerProductType = node_selected.data.manufacturerProductType.value;
        if (key != node_id && val.product.is_valid && val.product.manufacturer_id == manufacturerId && val.product.product_id == manufacturerProductId && val.product.product_type == manufacturerProductType) {
            options_node += '<div class="row">';
            options_node += '<div class="col-md-2"></div>';
            options_node += '<div class="col-md-10">';
            options_node += '<div class="checkbox-inline"><label>';
            options_node += '<input type="checkbox" class="cb_targetCopyParameters" name="type" value="' + key + '"/>';
            foundIdentical = 1;
            options_node += (val.description.name != '') ? key + ' ' + val.description.location + ' ' + val.description.name : key + ' ' + val.description.product_name ;
            options_node +=  '</label></div>';
            options_node +=  '</div></div>';
        }
        options_node += '</form>';
        if (foundIdentical == 0) {
            options_node = '{{Aucun module identique trouvé}}';
        }
    });
    bootbox.dialog({
        title: "{{Sélection des modules cible}}",
        message: options_node,
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
                  $("input:checkbox[name=type]:checked").each(function(){
                     jeedom.openzwave.node.copyConfigurations({
                        node_id : node_id,
                        target_id : $(this).val(),
                        error: function (error) {
                            $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
                        },
                        success: function () {
                           $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
                       }
                   });
                 });
              }
          }
      }
  });
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
        $("#div_nodeConfigure .node-sleep").html("---");
        $("#div_nodeConfigure .node-battery-span").hide();
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
                    }else {
                        $("#div_nodeConfigure .node-sleep").html("{{Endormi}}");
                    }
                    $("#div_nodeConfigure .node-battery-span").show();
                }
            }
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
            "<a id='hasNodeFailed_summary' class='btn btn-xs btn-primary hasNodeFailed'><i class='fa fa-heartbeat' aria-hidden='true'></i> {{Nœud en échec ?}}</a> " +
            "{{ou}} " +
            "<a id='testNode' class='btn btn-info testNode'><i class='fa fa-check-square-o'></i> {{Tester le nœud}}</a> " +
            "{{pour essayer de corriger.}}</li>";
        }
        if (data.data.genericType.value == 1) {
            data.data.can_wake_up.value = true;
        }
        $("#removeGhostNode").prop("disabled", nodeIsFailed || !data.data.can_wake_up.value);
        $('#div_nodeConfigure').find('.node-isSecured,.node-zwaveplus,.node-isBeaming,.node-isFrequentListening,.node-listening,.node-security,.node-isSecurity,.node-routing').html('');
        if (data.data.isRouting.value) {
            $("#div_nodeConfigure .node-routing").html("<li>{{Le noeud a des capacités de routage (capable de faire passer des commandes à d'autres noeuds)}}</li>");
        }
        if (data.data.isSecurity.value) {
            $("#div_nodeConfigure .node-isSecurity").html("<li>{{Le noeud supporte les caractéristiques de sécurité avancées}}</li>");
            $("#div_nodeConfigure .node-security").html("{{Classe de sécurité:}} " + data.data.security.value);
        }
        if (data.data.isListening.value) {
            $("#div_nodeConfigure .node-listening").html("<li>{{Le noeud est alimenté et écoute en permanence}}</li>");
        }
        if (data.data.isFrequentListening.value) {
            $("#div_nodeConfigure .node-isFrequentListening").html("<li>{{<i>FLiRS</i>, routeurs esclaves à écoute fréquente}}</li>");
        }
        if (data.data.isBeaming.value) {
            $("#div_nodeConfigure .node-isBeaming").html("<li>{{Le noeud est capable d'envoyer une trame réseau}}</li>");
        }
        if (data.data.isZwavePlus.value) {
            $("#div_nodeConfigure .node-zwaveplus").html(" {{ZWAVE PLUS}}");
        }
        if (data.data.isSecured.enabled && data.data.isSecured.value) {
            $("#div_nodeConfigure .node-isSecured").html("<i class='fa fa-lock' aria-hidden='true'></i>");
        }else {
            $("#div_nodeConfigure .node-isSecured").html("<i class='fa fa-unlock' aria-hidden='true'></i>");
        }
        if (queryStageIndex > 13) {
            if (data.data.neighbours.value.length > 0) {
                $("#div_nodeConfigure .node-neighbours").html( data.data.neighbours.value.join());
            }else {
                $("#div_nodeConfigure .node-neighbours").html("...");
                if (genericDeviceClass != 1 && (genericDeviceClass != 8 || data.data.isListening.value)) {
                    warningMessage += "<li{{Liste des voisins non disponible}} <br/>{{Utilisez}} <a id='healNode' class='btn btn-success healNode'><i class='fa fa-medkit'></i> {{Soigner le noeud}}</a> {{ou}} <a id='requestNodeNeighboursUpdate' class='btn btn-primary requestNodeNeighboursUpdate'><i class='fa fa-sitemap'></i> {{Mise à jour des noeuds voisins}}</a> {{pour corriger.}}</li>";
                    isWarning = true;
                }
            }
        }else {
            $("#div_nodeConfigure .node-neighbours").html("<i>{{La liste des noeuds voisin n'est pas encore disponible.}}</i>");
        }
        if (queryStageIndex > 7 && data.data.product_name.value == "") {
            warningMessage += "<li>{{Les identifiants constructeur ne sont pas detectés.}}<br/>{{Utilisez}} <a id='refreshNodeInfo' class='btn btn-success refreshNodeInfo'><i class='fa fa-retweet'></i> {{Rafraîchir infos du noeud}}</a> {{pour corriger}}</li>";
            isWarning = true;
        }
        $("#div_nodeConfigure .panel-danger").hide();
        $("#div_nodeConfigure .node-warning").html("");
        if (isWarning) {
            if (data.data.can_wake_up.value) {
                warningMessage += "<br><p>{{Le noeud est dormant et nécessite un réveil avant qu'une commande puisse être exécutée.<br/>Vous pouvez le réveiller manuellement ou attendre son délai de réveil.}}<br/>{{Voir l'interval de réveil dans l'onglet Système}}</p>";
            }
            $("#div_nodeConfigure .panel-danger").show();
            $("#div_nodeConfigure .node-warning").html(warningMessage);
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
        if (typeof openzwave_node_translation === 'undefined' || openzwave_node_translation == null) {
            openzwave_node_translation = getTranslation();
        }
        if (typeof openzwave_node_translation.configuration === 'undefined') {
            openzwave_node_translation = {configuration: {}};
        }
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
                        value += '<a class="btn btn-xs btn-primary editValue" data-valueidx="' + index + '" data-valueinstance="' + instance + '" data-valuecc="' + commandclass + '" data-valuedataitems="' + data.instances[instance].commandClasses[commandclass].data[index].data_items + '" data-valuetype="' + data.instances[instance].commandClasses[commandclass].data[index].typeZW + '" data-valuename="' + data.instances[instance].commandClasses[commandclass].data[index].name + '" data-valuevalue="' + data.instances[instance].commandClasses[commandclass].data[index].val + '" data-valuegenre="' +genre +'"><i class="fa fa-wrench"></i></a> ';
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
                        row.find("td[key=variable-refresh]").html('<a class="btn btn-xs btn-primary forceRefresh" data-valueidx="' + index + '" data-valueinstance="' + instance + '" data-valuecc="' + commandclass + '" data-valuedataitems="' + data.instances[instance].commandClasses[commandclass].data[index].data_items + '" data-valuetype="' + data.instances[instance].commandClasses[commandclass].data[index].typeZW + '" data-valuename="' + data.instances[instance].commandClasses[commandclass].data[index].name + '" data-valuevalue="' + data.instances[instance].commandClasses[commandclass].data[index].val + '"><i class="fa fa-refresh"></i></a>');
                        if (data.instances[instance].commandClasses[commandclass].data[index].poll_intensity == 0) {
                            polling += '<span class="label label-success" style="font-size:1em;">{{Auto}}</span>';
                        } else if (data.instances[instance].commandClasses[commandclass].data[index].poll_intensity == 1) {
                            polling += '<span class="label label-warning" style="font-size:1em;">{{5 min}}</span>';
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
                        row_system.find("td[key=system-edit]").html('<a class="btn btn-xs btn-primary editValue" data-valueidx="' + index + '" data-valueinstance="' + instance + '" data-valuecc="' + commandclass + '" data-valuedataitems="' + data.instances[instance].commandClasses[commandclass].data[index].data_items + '" data-valuetype="' + data.instances[instance].commandClasses[commandclass].data[index].typeZW + '" data-valuename="' + data.instances[instance].commandClasses[commandclass].data[index].name + '" data-valuevalue="' + data.instances[instance].commandClasses[commandclass].data[index].val + '" data-valuegenre="' +genre +'"><i class="fa fa-wrench"></i></a>');
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
                        row_parameter.find("td[key=parameter-edit]").html('<a class="btn btn-xs btn-primary editParam" data-paramid="' + index + '" data-paramtype="' + data.instances[instance].commandClasses[commandclass].data[index].typeZW + '" data-paramname="' + data.instances[instance].commandClasses[commandclass].data[index].name + '" data-paramvalue="' + data_item + '"><i class="fa fa-wrench"></i></a>');
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
                var target_id = node_selected.groups[z].associations[i][0];
                var node_instance = node_selected.groups[z].associations[i][1];
                var id = z + '-' + node_id + '-' + node_instance;
                if (nodes[target_id]) {
                    if (nodes[target_id].description.name != '') {
                        var node_name = nodes[target_id].description.location + ' ' + nodes[target_id].description.name;
                    } else {
                        var node_name = nodes[target_id].description.product_name;
                    }
                    if (node_instance > 0) {
                        var instanceDisplay = node_instance -1;
                        node_name += " (Instance: " + instanceDisplay + ")";
                    }
                } else {
                    var node_name = "UNDEFINED";
                }
                tr_groups += "<tr gid='" + id + "'><td>" + target_id + " : " + node_name + "</td><td align='right'>";
                tr_groups += "<a class='btn btn-danger btn-sm deleteGroup' data-groupindex='" + z + "' data-nodeid='" + target_id + "' data-nodeinstance='" + node_instance + "'><i class='fa fa-trash-o'></i> {{Supprimer}}</a>"
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
         $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
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
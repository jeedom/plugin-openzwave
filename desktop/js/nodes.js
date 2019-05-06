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
var isWarning = false;
var warningMessage = "";
var selected_node_id = -1;

$("body").off("click", ".node_action").on("click", ".node_action", function (e) {
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
        value: '0'
      },
      {
        text: '{{Tous les modules}} : '+node_selected.data.product_name.value+'  '+node_selected.data.vendorString.value,
        value: '1'
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
  var message = '{{Liste des groupes d\'associations où le module}} <b><span class="node-name label label-default" style="font-size : 1em;">' + node_selected.data.name.value + '</span></b> {{est utilisé:}}</p><br><ul>';
  $.each(node_selected.associations, function (key, val) {
    message += '<li class="active"><p>';
    if (nodes[key].description.name != '') {
      message += nodes[key].description.location + ' - <b>' + nodes[key].description.name + '</b>';
    } else {
      message += '<b>' + nodes[key].description.product_name + '</b>';
    }
    message += '<br><ul class="fa-ul">';
    $.each(val, function (key2, val2) {
      message += '<li><i class="fas fa-arrow-right btn-success" aria-hidden="true"></i>  ' + val2.label + ' (' + val2.index + ')</li>';
    });
    message += '</ul></p></li>';
  });
  message += '</ul>';
  bootbox.alert(message);
});

$("body").off("click", ".editValue").on("click", ".editValue", function (e) {
  var title = '{{Changer la valeur de}} '+ $(this).data('name');
  var valueApplyOption={
    node_id : node_id,
    instance :  $(this).data('instance'),
    class :  $(this).data('cc'),
    index : $(this).data('index'),
    error: function (error) {
      $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
    },
    success: function () {
      $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
    }
  };
  if ($(this).data('type') == "List") {
    var options = [];
    $.each($(this).data('valuedataitems').split(";"), function (key, val) {
      options.push({value : val,text:val})
    });
    bootbox.prompt({
      title: title,
      inputType: 'select',
      inputOptions : options,
      callback: function (result) {
        if(result === null){
          return;
        }
        valueApplyOption.value = result;
        jeedom.openzwave.node.set(valueApplyOption);
      }
    });
  } else if ($(this).data('type') == "Bool") {
    bootbox.prompt({
      title: title,
      inputType: 'select',
      inputOptions: [
        {text: '{{Oui/On}}',value: 255},
        {text: '{{Non/Off}}',value: 0}
      ],
      callback: function (result) {
        if(result === null){
          return;
        }
        valueApplyOption.value = result;
        jeedom.openzwave.node.set(valueApplyOption);
      }
    });
    
  } else if ($(this).data('type') == "Button") {
    bootbox.prompt({
      title: title,
      inputType: 'select',
      inputOptions: [
        {text: '{{Presser}}',value: 'press'},
        {text: '{{Relacher}}', value: 'release'}
      ],
      callback: function (result) {
        if(result === null){
          return;
        }
        valueApplyOption.action = result;
        jeedom.openzwave.node.button(valueApplyOption);
      }
    });
  } else if($(this).data('type') == "Raw") {
    var result = prompt(title);
    if(result === null){
      return;
    }
    jeedom.openzwave.node.setRaw({
      node_id : node_id,
      slot_id : $(this).data('index'),
      value : result,
      error: function (error) {
        $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
      },
      success: function () {
        $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
      }
    });
  }else {
    var result = prompt(title);
    if(result === null){
      return;
    }
    valueApplyOption.value = result;
    jeedom.openzwave.node.set(valueApplyOption);
  }
});

$("body").off("click", ".forceRefresh").on("click", ".forceRefresh", function (e) {
  jeedom.openzwave.node.refreshData({
    node_id : node_id,
    instance : $(this).attr('data-instance'),
    class :  $(this).attr('data-cc'),
    index : $(this).attr('data-index'),
    error: function (error) {
      $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
    },
    success: function () {
      $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
    }
  });
});

$("body").off("click", ".editPolling").on("click", ".editPolling", function (e) {
  var idx = $(this).data('index');
  var instance = $(this).data('instance');
  var cc = $(this).data('cc');
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
  var title = '{{Changer la valeur pour le paramètre}} : '+$(this).data('paramname')+' ('+ $(this).data('paramvalue')+')'
  var setParamOptions = {
    node_id : node_id,
    id :  $(this).data('paramid'),
    error: function (error) {
      $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
    },
    success: function () {
      $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
    }
  };
  if ($(this).data('paramtype') == "List") {
    jeedom.openzwave.node.dataClass({
      node_id : node_id,
      class : 112,
      error: function (error) {
        $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
      },
      success: function (data) {
        var options = [];
        $.each(data[setParamOptions.id].val.value4, function (key, val) {
          if (typeof openzwave_node_translation.configuration[setParamOptions.id] !== 'undefined' && openzwave_node_translation['configuration'][setParamOptions.id].hasOwnProperty('list') && typeof openzwave_node_translation['configuration'][setParamOptions.id].list[val] !== 'undefined') {
            options.push({value : val,text:openzwave_node_translation['configuration'][setParamOptions.id].list[val]})
          } else {
            options.push({value : val,text:val})
          }
        });
        bootbox.prompt({
          title: title,
          inputType: 'select',
          inputOptions: options,
          callback: function (result) {
            if(result === null){
              return;
            }
            setParamOptions.value = result.replace(/\//g, '@');
            setParamOptions.length = 0;
            jeedom.openzwave.node.setParam(setParamOptions);
          }
        });
      }
    });
    
  } else if ($(this).data('paramtype') == "Bool") {
    bootbox.prompt({
      title: title,
      inputType: 'select',
      inputOptions: [
        {text: '{{Oui}}',value: '1'},
        {text: '{{Non}}',value: '0'}
      ],
      callback: function (result) {
        if(result === null){
          return;
        }
        setParamOptions.value = result.replace(/\//g, '@');
        setParamOptions.length = 0;
        jeedom.openzwave.node.setParam(setParamOptions);
      }
    });
  } else if ($(this).data('paramtype') == "Button") {
    bootbox.prompt({
      title: title,
      inputType: 'select',
      inputOptions: [
        {text: '{{Presser}}', value: 'press'},
        {text: '{{Relacher}}',value: 'release'}
      ],
      callback: function (result) {
        if(result === null){
          return;
        }
        setParamOptions.value = result.replace(/\//g, '@');
        setParamOptions.length = 0;
        jeedom.openzwave.node.setParam(setParamOptions);
      }
    });
  }else {
    var result = prompt(title);
    if(result === null){
      return;
    }
    setParamOptions.value = result.replace(/\//g, '@');
    setParamOptions.length = 0;
    jeedom.openzwave.node.setParam(setParamOptions);
  }
});

$("#tab-parameters").off("click").on("click", function () {
  if (!node_selected.instances[1].commandClasses[112]) {
    $("#parameters").html('<br><div><b>{{Aucun paramètre prédefini trouvé pour ce noeud}}</b></div><br>');
    $("#parameters").append('<div class="row"><label class="col-lg-2">{{Paramètre (manuel) :}} </label><div class="col-lg-1"><input type="text" class="form-control" id="paramidperso"></div><label class="col-lg-1">{{Valeur :}} </label><div class="col-lg-1"><input type="text" class="form-control" id="newvalueperso"></div><label class="col-lg-1">{{Taile :}}</label><div class="col-lg-1"><input type="text" class="form-control" id="sizeperso"></div> <div class="col-lg-2"><a id="sendparamperso" class="btn btn-primary">{{Envoyer le paramètre}}</a></div></div>');
  }
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
              options.push({value : key + ';0', text :  text });
            }
            if (associations.indexOf(key + ';1') < 0) {
              options.push({value : key + ';1', text :  text + ' (1)'});
            }
          }else if(val.multi_instance.instances == 1){
            if (associations.indexOf(key + ';0') < 0) {
              options.push({value : key + ';0', text :  text});
            }
          }else {
            for (i = 1; i <= val.multi_instance.instances; i++) {
              if (i == 1 && associations.indexOf(key + ';0') < 0) {
                options.push({value : key + ';0', text :  text });
              }
              if (associations.indexOf(key + ';'+i) >= 0) {
                continue;
              }
              options.push({value : key + ';'+i, text :  text + ' ('+i+')'});
            }
          }
        }else{
          if (associations.indexOf(key + ';0') < 0) {
            options.push({value : key + ';0', text :  text });
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


$("body").off("click", ".copyParams").on("click", ".copyParams", function (e) {
  var options = [];
  $.each(nodes, function (key, val) {
    var manufacturerId = node_selected.data.manufacturerId.value;
    var manufacturerProductId = node_selected.data.manufacturerProductId.value;
    var manufacturerProductType = node_selected.data.manufacturerProductType.value;
    if (key != node_id && val.product.is_valid && val.product.manufacturer_id == manufacturerId && val.product.product_id == manufacturerProductId && val.product.product_type == manufacturerProductType) {
      var name = (val.description.name != '') ? val.description.location + ' - ' + val.description.name : val.description.product_name;
      options.push({value : key, text : key+' '+name})
    }
  });
  bootbox.prompt({
    title: "{{Sélection du module source}}",
    inputType: 'select',
    inputOptions : options,
    callback: function (result) {
      if(result == null){
        return;
      }
      jeedom.openzwave.node.copyConfigurations({
        node_id : result,
        target_id : node_id,
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
$("body").off("click", ".copyToParams").on("click", ".copyToParams", function (e) {
  var options = [];
  $.each(nodes, function (key, val) {
    var manufacturerId = node_selected.data.manufacturerId.value;
    var manufacturerProductId = node_selected.data.manufacturerProductId.value;
    var manufacturerProductType = node_selected.data.manufacturerProductType.value;
    if (key != node_id && val.product.is_valid && val.product.manufacturer_id == manufacturerId && val.product.product_id == manufacturerProductId && val.product.product_type == manufacturerProductType) {
      var name = (val.description.name != '') ? val.description.location + ' - ' + val.description.name : val.description.product_name;
      options.push({value : key, text : (val.description.name != '') ? key + ' ' + val.description.location + ' ' + val.description.name : key + ' ' + val.description.product_name})
    }
  });
  bootbox.prompt({
    title: "{{Sélection des modules cible}}",
    inputType: 'checkbox',
    inputOptions:options,
    callback: function (result) {
      if(result === null){
        return;
      }
      for(var i in result){
        jeedom.openzwave.node.copyConfigurations({
          node_id : node_id,
          target_id : result[i],
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
  var selected_node_id = node_id;
  jeedom.openzwave.node.info({
    node_id : node_id,
    info:'all',
    global:false,
    error: function (error) {
      $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
    },
    success: function (data) {
      warningMessage = '';
      node_selected = data;
      
      $("#div_nodeConfigure .node-id").html(selected_node_id);
      $("#div_nodeConfigure .node-name").html(data.data.name.value);
      
      var nodeIsFailed = (data.data.isFailed) ? data.data.isFailed.value : false;
      data.data.lastReceived.updateTime = jeedom.openzwave.timestampConverter(data.data.lastReceived.updateTime);
      data.data.basicDeviceClassDescription = (isset(BASIC_CLASS_DESC[data.data.basicType.value])) ? BASIC_CLASS_DESC[parseInt(data.data.basicType.value, 0)] : '';
      data.data.genericDeviceClassDescription = (isset(GENERIC_CLASS_DESC[data.data.genericType.value])) ? GENERIC_CLASS_DESC[data.data.genericType.value] : '';
      var queryStageDescrition = (isset(QUERY_STAGE_DESC[data.data.state.value])) ? QUERY_STAGE_DESC[data.data.state.value] : '{{Inconnue}}';
      var queryStageIndex = 0;
      for(i in QUERY_STAGE_DESC){
        if(i == data.data.state.value){
          break;
        }
        queryStageIndex++;
      }
      if (data.data.wakeup_interval.next_wakeup != null) {
        data.data.wakeup_interval.next_wakeup = jeedom.openzwave.timestampConverter(data.data.wakeup_interval.next_wakeup);
        $("#div_nodeConfigure .node-next-wakeup-span").show();
      } else {
        $("#div_nodeConfigure .node-next-wakeup-span").hide();
      }
      var manufacturer_span = "<span class='label label-default' style='font-size : 1em;'>";
      if (queryStageIndex > 7 && data.data.product_name.value == "") {
        manufacturer_span = "<span class='label label-danger' style='font-size : 1em;'>";
      }
      if (queryStageIndex > 2){
        data.data.zwave_id = "{{Identifiant du fabricant :}} "+ manufacturer_span + data.data.manufacturerId.value + " [" + data.data.manufacturerId.hex + "]</span> {{Type de produit :}} " +manufacturer_span + data.data.manufacturerProductType.value + ' [' + data.data.manufacturerProductType.hex + "]</span> {{Identifiant du produit :}} " + manufacturer_span + data.data.manufacturerProductId.value + ' [' + data.data.manufacturerProductId.hex + "]</span>";
      }
      else{
        data.data.zwave_id = "{{Identifiant du fabricant :}} "+ manufacturer_span +  "--</span> {{Type de produit :}} " + manufacturer_span + "--</span> {{Identifiant du produit :}} " + manufacturer_span + "--</span>";
      }
      $("#div_nodeConfigure .node-queryStage").html((nodeIsFailed) ? 'Dead' : data.data.state.value);
      if(nodeIsFailed) {
        $("#div_nodeConfigure .node-queryStage").removeClass("label-default").addClass("label-danger")
      }
      else{
        $("#div_nodeConfigure .node-queryStage").removeClass("label-danger").addClass("label-default")
      }
      $("#div_nodeConfigure .node-sleep").html("---");
      $("#div_nodeConfigure .node-battery-span").hide();
      if (queryStageIndex > 2) {
        if (data.data.isListening.value) {
          $("#div_nodeConfigure .node-sleep").removeClass("label-default");
          $("#div_nodeConfigure .node-sleep").html('<i class="fa fa-plug text-success fa-lg"></i>');
          $("#div_nodeConfigure .node-battery-span").hide();
        }else {
          $("#div_nodeConfigure .node-sleep").removeClass("label-success").addClass("label-default");
          if (data.data.battery_level.value != null) {
            if (data.data.isFrequentListening.value) {
              $("#div_nodeConfigure .node-sleep").html("{{Endormi <i>(FLiRS)</i>}}");
            } else if (data.data.can_wake_up.value) {
              if (data.data.isAwake.value) {
                $("#div_nodeConfigure .node-sleep").removeClass("label-default").addClass("label-success");
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
          warningMessage += "<li>{{Le contrôleur n'est inclus dans aucun groupe du module.}}</li>";
        }
      }
      if (nodeIsFailed) {
        warningMessage += "<li>{{Le contrôleur pense que ce noeud est en échec, essayez }} " +
        "<a data-action='hasNodeFailed' class='btn btn-xs btn-primary  node_action'><i class='fa fa-heartbeat' aria-hidden='true'></i> {{Nœud en échec ?}}</a> {{ou}}" +
        "<a data-action='testNode' class='btn btn-info  node_action'><i class='fas fa-check-square-o'></i> {{Tester le nœud}}</a> {{pour essayer de corriger.}}</li>"
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
      if (data.data.isSecured.enabled){
        if (data.data.isSecured.value) {
          $("#div_nodeConfigure .node-isSecured").html("<i class='fa fa-lock' aria-hidden='true'></i>");
        }else {
          $("#div_nodeConfigure .node-isSecured").html("<i class='fa fa-unlock' aria-hidden='true'></i>");
        }
      }
      $("#div_nodeConfigure .node-neighbours").removeClass("label-danger").addClass("label-default");
      if (queryStageIndex > 13) {
        if (data.data.neighbours.value.length > 0) {
          $("#div_nodeConfigure .node-neighbours").html( data.data.neighbours.value.join());
        }else {
          $("#div_nodeConfigure .node-neighbours").html("...");
          var genericDeviceClass = parseInt(data.data.genericType.value, 0);
          if (genericDeviceClass != 1 && (genericDeviceClass != 8 || data.data.isListening.value)) {
            warningMessage += "<li{{Liste des voisins non disponible}} <br/>{{Utilisez}} <a data-action='healNode' class='btn btn-success node_action'><i class='fa fa-medkit'></i> {{Soigner le noeud}}</a> {{ou}} <a data-action='requestNodeNeighboursUpdate' class='btn btn-primary node_action'><i class='fa fa-sitemap'></i> {{Mise à jour des noeuds voisins}}</a> {{pour corriger.}}</li>";
            $("#div_nodeConfigure .node-neighbours").removeClass("label-default").addClass("label-danger")
          }
        }
      }else {
        $("#div_nodeConfigure .node-neighbours").html("<i>{{La liste des noeuds voisin n'est pas encore disponible.}}</i>");
      }
      if (queryStageIndex > 7 && data.data.product_name.value == "") {
        warningMessage += "<li>{{Les identifiants constructeur ne sont pas detectés.}}<br/>{{Utilisez}} <a data-action='refreshNodeInfo' class='btn btn-success node_action'><i class='fa fa-retweet'></i> {{Rafraîchir infos du noeud}}</a> {{pour corriger}}</li>";
      }
      $("#div_nodeConfigure .panel-warning").hide();
      $("#div_nodeConfigure .zwaveNodeAttr[data-l1key=warning]").html("");
      if (warningMessage != '') {
        if (data.data.can_wake_up.value) {
          warningMessage += "<br><p>{{Le noeud est dormant et nécessite un réveil avant qu'une commande puisse être exécutée.<br/>Vous pouvez le réveiller manuellement ou attendre son délai de réveil.}}<br/>{{Voir l'interval de réveil dans l'onglet Système}}</p>";
        }
        $("#div_nodeConfigure .panel-warning").show();
        $("#div_nodeConfigure .zwaveNodeAttr[data-l1key=warning]").html(warningMessage);
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
                  parameters += "<tr class='greenrow' pid='" + id + "'>" + $("#template-parameter").html() + "</tr>";
                  break;
                  case 2:
                  parameters += "<tr class='redrow' pid='" + id + "'>" + $("#template-parameter").html() + "</tr>";
                  break;
                  case 3:
                  parameters += "<tr class='yellowrow' pid='" + id + "'>" + $("#template-parameter").html() + "</tr>";
                  break;
                  default:
                  parameters += "<tr pid='" + id + "'>" + $("#template-parameter").html() + "</tr>";
                }
              } else if (genre == "System") {
                switch (pending_state) {
                  case 1:
                  system_variables += "<tr class='greenrow' sid='" + id + "'>" + $("#template-system").html() + "</tr>";
                  break;
                  case 2:
                  system_variables += "<tr class='redrow' sid='" + id + "'>" + $("#template-system").html() + "</tr>";
                  break;
                  case 3:
                  system_variables += "<tr class='yellowrow' sid='" + id + "'>" + $("#template-system").html() + "</tr>";
                  break;
                  default:
                  system_variables += "<tr sid='" + id + "'>" + $("#template-system").html() + "</tr>";
                }
              } else {
                variables += "<tr vid='" + id + "'>" + $("#template-variable").html() + "</tr>";
              }
            }
          }
        }
      }
      fragment_variables = $('<tbody></tbody>').append(variables);
      fragment_parameters = $('<tbody></tbody>').append(parameters);
      fragment_system_variables = $('<tbody></tbody>').append(system_variables);
      openzwave_node_translation = getTranslation();
      if (typeof openzwave_node_translation.configuration === 'undefined') {
        openzwave_node_translation = {configuration: {}};
      }
      for (instance in data.instances) {
        for (commandclass in data.instances[instance].commandClasses) {
          var first_index_polling = true;
          for (index in data.instances[instance].commandClasses[commandclass].data) {
            var id = instance + ":" + commandclass + ":" + index;
            var row = fragment_variables.find("tr[vid='" + id + "']");
            var row_parameter = fragment_parameters.find("tr[pid='" + id + "']");
            var row_system = fragment_system_variables.find("tr[sid='" + id + "']");
            row.find("td[data-key=instance]").html(instance);
            row.find("td[data-key=cc]").html(commandclass + ' (0x' + Number(commandclass).toString(16) + ')');
            row.find("td[data-key=index]").html(index);
            row.find("td[data-key=name]").html(data.instances[instance].commandClasses[commandclass].data[index].name);
            row.find("td[data-key=type]").html(data.instances[instance].commandClasses[commandclass].data[index].typeZW + ' (' + data.instances[instance].commandClasses[commandclass].data[index].type + ')');
            var value = '';
            var genre = data.instances[instance].commandClasses[commandclass].data[index].genre;
            if (data.instances[instance].commandClasses[commandclass].data[index].read_only == false) {
              value += '<a class="btn btn-xs btn-primary editValue" data-index="' + index + '" data-instance="' + instance + '" data-cc="' + commandclass + '" data-valuedataitems="' + data.instances[instance].commandClasses[commandclass].data[index].data_items + '" data-type="' + data.instances[instance].commandClasses[commandclass].data[index].typeZW + '" data-name="' + data.instances[instance].commandClasses[commandclass].data[index].name + '" data-value="' + data.instances[instance].commandClasses[commandclass].data[index].val + '" data-valuegenre="' +genre +'"><i class="fas fa-wrench"></i></a> ';
            }
            if (data.instances[instance].commandClasses[commandclass].data[index].type == 'bool') {
              var boolValue = data.instances[instance].commandClasses[commandclass].data[index].val;
              if (data.instances[instance].commandClasses[commandclass].data[index].name != 'Exporting'){
                value += (boolValue) ? '<span class="label label-success" style="font-size:1em;">{{ON}}</span>' : '<span class="label label-danger" style="font-size:1em;">{{OFF}}</span>';
                
              }else{
                value += (boolValue) ? '{{ON}}' :'{{OFF}}' ;
              }
            }else if (data.instances[instance].commandClasses[commandclass].data[index].write_only == false) {
              value += data.instances[instance].commandClasses[commandclass].data[index].val + " " + data.instances[instance].commandClasses[commandclass].data[index].units;
            }
            row.find("td[data-key=value]").html(value);
            var polling = '<span style="width : 22px;"></span>';
            if (data.instances[instance].commandClasses[commandclass].data[index].write_only == false && first_index_polling) {
              first_index_polling = false;
              var polling = '<a style="position:relative;top:-1px;" class="btn btn-primary btn-xs editPolling cursor" data-index="' + index + '" data-polling="' + data.instances[instance].commandClasses[commandclass].data[index].poll_intensity + '" data-instance="' + instance + '" data-cc="' + commandclass + '" data-valuedataitems="' + data.instances[instance].commandClasses[commandclass].data[index].data_items + '" data-type="' + data.instances[instance].commandClasses[commandclass].data[index].typeZW + '" data-name="' + data.instances[instance].commandClasses[commandclass].data[index].name + '" data-value="' + data.instances[instance].commandClasses[commandclass].data[index].val + '"><i class="fas fa-wrench"></i></a> ';
              row.find("td[data-key=refresh]").html('<a class="btn btn-xs btn-primary forceRefresh" data-index="' + index + '" data-instance="' + instance + '" data-cc="' + commandclass + '" data-valuedataitems="' + data.instances[instance].commandClasses[commandclass].data[index].data_items + '" data-type="' + data.instances[instance].commandClasses[commandclass].data[index].typeZW + '" data-name="' + data.instances[instance].commandClasses[commandclass].data[index].name + '" data-value="' + data.instances[instance].commandClasses[commandclass].data[index].val + '"><i class="fas fa-sync-alt"></i></a>');
              if (data.instances[instance].commandClasses[commandclass].data[index].poll_intensity == 0) {
                polling += '<span class="label label-success" style="font-size:1em;">{{Auto}}</span>';
              } else if (data.instances[instance].commandClasses[commandclass].data[index].poll_intensity == 1) {
                polling += '<span class="label label-warning" style="font-size:1em;">{{5 min}}</span>';
              }
            }
            row.find("td[data-key=polling]").html(polling);
            if (data.instances[instance].commandClasses[commandclass].data[index].write_only == false) {
              row.find("td[data-key=updatetime]").html(jeedom.openzwave.timestampConverter(data.instances[instance].commandClasses[commandclass].data[index].updateTime));
            }
            var expected_data = null;
            var pending_state = data.instances[instance].commandClasses[commandclass].data[index].pendingState;
            if (pending_state >= 2) {
              expected_data = data.instances[instance].commandClasses[commandclass].data[index].expected_data;
            }
            var data_item = data.instances[instance].commandClasses[commandclass].data[index].val;
            if (data.instances[instance].commandClasses[commandclass].data[index].type == 'bool') {
              data_item = (data_item) ? '{{Oui}}' : '{{Non}}';
            }
            if (data.instances[instance].commandClasses[commandclass].data[index].write_only) {
              data_item = '';
            }
            var data_units = data.instances[instance].commandClasses[commandclass].data[index].units;
            row_system.find("td[data-key=instance]").html(instance);
            row_system.find("td[data-key=cc]").html(commandclass + ' (0x' + Number(commandclass).toString(16) + ')');
            row_system.find("td[data-key=index]").html(index);
            row_system.find("td[data-key=name]").html(data.instances[instance].commandClasses[commandclass].data[index].name);
            row_system.find("td[data-key=type]").html(data.instances[instance].commandClasses[commandclass].data[index].typeZW + ' (' + data.instances[instance].commandClasses[commandclass].data[index].type + ')');
            var system_data = data_item + " " + data_units;
            if (expected_data != null) {
              system_data += '<br>(<i>' + expected_data + " " + data_units + '</i>)';
            }
            row_system.find("td[data-key=value]").html(system_data);
            if (data.instances[instance].commandClasses[commandclass].data[index].read_only == false) {
              row_system.find("td[data-key=edit]").html('<a class="btn btn-xs btn-primary editValue" data-index="' + index + '" data-instance="' + instance + '" data-cc="' + commandclass + '" data-valuedataitems="' + data.instances[instance].commandClasses[commandclass].data[index].data_items + '" data-type="' + data.instances[instance].commandClasses[commandclass].data[index].typeZW + '" data-name="' + data.instances[instance].commandClasses[commandclass].data[index].name + '" data-value="' + data.instances[instance].commandClasses[commandclass].data[index].val + '" data-valuegenre="' +genre +'"><i class="fas fa-wrench"></i></a>');
            }
            if (data.instances[instance].commandClasses[commandclass].data[index].write_only == false) {
              row_system.find("td[data-key=updatetime]").html(jeedom.openzwave.timestampConverter(data.instances[instance].commandClasses[commandclass].data[index].updateTime));
            }
            if (typeof openzwave_node_translation.configuration[index] !== 'undefined' && openzwave_node_translation['configuration'][index].hasOwnProperty('name')) {
              row_parameter.find("td[data-key=name]").html(openzwave_node_translation['configuration'][index].name);
            } else {
              row_parameter.find("td[data-key=name]").html(data.instances[instance].commandClasses[commandclass].data[index].name);
            }
            row_parameter.find("td[data-key=index]").html(index);
            row_parameter.find("td[data-key=type]").html(data.instances[instance].commandClasses[commandclass].data[index].typeZW);
            if (typeof openzwave_node_translation.configuration[index] !== 'undefined' && openzwave_node_translation['configuration'][index].hasOwnProperty('list') && typeof openzwave_node_translation['configuration'][index].list[data.instances[instance].commandClasses[commandclass].data[index].val] !== 'undefined') {
              var translation_item = openzwave_node_translation['configuration'][index].list[data_item];
              if (expected_data != null) {
                translation_item += '<br>(<i>' + openzwave_node_translation['configuration'][index].list[expected_data] + '</i>)';
              }
              row_parameter.find("td[data-key=value]").html(translation_item);
            } else {
              if (expected_data != null) {
                data_item += '<br>(<i>' + expected_data + '</i>)';
              }
              row_parameter.find("td[data-key=value]").html(data_item);
            }
            if (data.instances[instance].commandClasses[commandclass].data[index].read_only == false) {
              data_item = data.instances[instance].commandClasses[commandclass].data[index].val;
              if (data.instances[instance].commandClasses[commandclass].data[index].write_only) {
                data_item = '';
              }
              row_parameter.find("td[data-key=edit]").html('<a class="btn btn-xs btn-primary editParam" data-paramid="' + index + '" data-paramtype="' + data.instances[instance].commandClasses[commandclass].data[index].typeZW + '" data-paramname="' + data.instances[instance].commandClasses[commandclass].data[index].name + '" data-paramvalue="' + data_item + '"><i class="fas fa-wrench"></i></a>');
            }
            if (typeof openzwave_node_translation.configuration[index] !== 'undefined' && openzwave_node_translation['configuration'][index].hasOwnProperty('help')) {
              row_parameter.find("td[data-key=help]").html(openzwave_node_translation['configuration'][index].help);
            } else {
              row_parameter.find("td[data-key=help]").html(data.instances[instance].commandClasses[commandclass].data[index].help);
            }
          }
        }
      }
      $("#div_nodeConfigure .variables").html(fragment_variables.html());
      $("#div_nodeConfigure .parameters").html(fragment_parameters.html());
      $("#div_nodeConfigure .system_variables").html(fragment_system_variables.html());
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
  $("#groups").append('<a class="btn btn-info btn-sm findUsage pull-right"><i class="fas fa-sitemap"></i> {{Associé à quels modules}}</a>');
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
            var instanceDisplay = node_instance;
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
      if (node_selected.groups[z].associations.length < node_selected.groups[z].maximumAssociations) {
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
      product_id: node_selected.data.manufacturerProductId.value
    },
    success: function (data) {
      result = data.result;
    }
  });
  return result;
}

display_node_stats();
load_all_node();

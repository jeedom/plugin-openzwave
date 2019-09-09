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

 function initOpenzwaveOpenzwave() {

    $('body').off('zwave::controller.data.controllerState').on('zwave::controller.data.controllerState', function (_event,_options) {
      if (_options.state == 1) {
        $('.changeIncludeState[data-mode=1]').removeClass('ui-btn-a').addClass('ui-btn-b');
        $('.changeIncludeState[data-mode=1]').attr('data-state', 0);
        $('#div_inclusionAlert').html('{{Vous êtes en mode inclusion. Cliquez à nouveau sur le bouton d\'inclusion pour sortir de ce mode}}');
        $('.changeIncludeState[data-mode=1]').html('<i class="fas fa-sign-in-alt fa-rotate-90" style="font-size: 6em;"></i><br/>{{Stop inclusion}}');
    }else if (_options.state == 5) {
        $('.changeIncludeState[data-mode=0]').removeClass('ui-btn-a').addClass('ui-btn-b');
        $('.changeIncludeState[data-mode=0]').attr('data-state', 0);
        $('#div_inclusionAlert').html('{{Vous êtes en mode exclusion. Cliquez à nouveau sur le bouton d\'exclusion pour sortir de ce mode}}');
        $('.changeIncludeState[data-mode=0]').html('<i class="fas fa-sign-out-alt fa-rotate-90" style="font-size: 6em;"></i><br/>{{Stop exclusion}}');
    }else{
        $('.changeIncludeState').removeClass('ui-btn-b').addClass('ui-btn-a');
        $('#div_inclusionAlert').html('{{Aucun mode actif}}');
        $('.changeIncludeState[data-mode=0]').html('<i class="fas fa-sign-out-alt fa-rotate-90" style="font-size: 6em;"></i><br/>{{Exclusion}}');
        $('.changeIncludeState[data-mode=1]').html('<i class="fas fa-sign-in-alt fa-rotate-90" style="font-size: 6em;"></i><br/>{{Inclusion}}');
        $('.changeIncludeState[data-mode=1]').attr('data-state', 1);
    }
});

    $('body').off('zwave::notification').on('zwave::notification', function (_event,_options) {
       $('#div_inclusionAlert').html(_options);
   });

    $('body').off('zwave::includeDevice').on('zwave::includeDevice', function (_event,_options) {
      $('.eqLogicAttr[data-l1key=id]').value('');
      if (_options != '') {
        $("#div_configIncludeDevice").show();
        $('.eqLogicAttr[data-l1key=id]').value(_options);
    }
});

    $('.changeIncludeState').on('click', function() {
     if($(this).attr('data-state') == 0){
        jeedom.openzwave.controller.action({
            action : 'cancelCommand',
            error: function (error) {
                $('#div_alert').showAlert({message: error.message, level: 'danger'});
            },
            success: function () {
               $('#div_alert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
           }
       });
        return;
    }
    if ($(this).attr('data-mode') == 0) {
     jeedom.openzwave.controller.removeNodeFromNetwork({
       error: function (error) {
        $('#div_alert').showAlert({message: error.message, level: 'danger'});
    },
    success: function (data) {
       $('#div_alert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
   }
});
     return;
 }
 jeedom.openzwave.controller.addNodeToNetwork({
    secure : 0,
    error: function (error) {
        $('#div_alert').showAlert({message: error.message, level: 'danger'});
    },
    success: function (data) {
        $('#div_alert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
    }
});
});

    $('#bt_validateConfigDevice').on('click', function() {
        jeedom.eqLogic.save({
            type: 'zwave',
            eqLogics: $("#div_configIncludeDevice").getValues('.eqLogicAttr'),
            error: function(error) {
                $('#div_alert').showAlert({message: error.message, level: 'danger'});
                $('.eqLogicAttr[data-l1key=id]').value('');
            },
            success: function() {
                $("#div_configIncludeDevice").hide();
            }
        });
    });

    jeedom.object.all({success: function(objects) {
        var options = '';
        for (var i in objects) {
            options += '<option value="' + objects[i].id + '">' + objects[i].name + '</option>'
        }
        $('.eqLogicAttr[data-l1key=object_id]').html(options);
        $('.eqLogicAttr[data-l1key=object_id]').selectmenu("refresh");
    }
});

}

jeedom.openzwave.network.info({
    info : 'getStatus',
    error: function (error) {
        $('#div_alert').showAlert({message: error.message, level: 'danger'});

    },
    success: function (data) {
        var networkState = data.mode;
        if (networkState == "0") {
            $('#div_inclusionAlert').html('{{Aucun mode actif}}');
        }
        if (networkState == "1") {
            $('#div_inclusionAlert').html('{{Vous êtes en mode inclusion. Cliquez à nouveau sur le bouton d\'inclusion pour sortir de ce mode}}');
            $('.changeIncludeState[data-mode=1]').removeClass('ui-btn-a').addClass('ui-btn-b');
            $('.changeIncludeState[data-mode=1]').attr('data-state', 0);
            $('.changeIncludeState[data-mode=1]').html('<i class="fas fa-sign-in-alt fa-rotate-90" style="font-size: 6em;"></i><br/>{{Stop inclusion}}');
        }
        if (networkState == "5") {
            $('#div_inclusionAlert').html('{{Vous êtes en mode exclusion. Cliquez à nouveau sur le bouton d\'exclusion pour sortir de ce mode}}');
            $('.changeIncludeState[data-mode=0]').removeClass('ui-btn-a').addClass('ui-btn-b');
            $('.changeIncludeState[data-mode=0]').attr('data-state', 0);
            $('.changeIncludeState[data-mode=0]').html('<i class="fas fa-sign-out-alt fa-rotate-90" style="font-size: 6em;"></i><br/>{{Stop exclusion}}');
        }
    }
});
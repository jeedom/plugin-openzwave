
/* This file is part of Jeedom.
 *
 * Jeedom is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Jeedom is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Jeedom. If not, see <http://www.gnu.org/licenses/>.
 */

 function initOpenzwaveOpenzwave() {

    if (socket != null) {
        socket.on('zwave::controller.data.controllerState', function(_options) {
           _options = json_decode(_options);
           if (_options.state == 1) {
            $('.changeIncludeState[data-mode=1][data-serverID='+_options.serverId+']').removeClass('ui-btn-a').addClass('ui-btn-b');
            $('.changeIncludeState[data-mode=1][data-serverID='+_options.serverId+']').attr('data-state', 0);
            $('#div_inclusionAlert'+_options.serverId).html('{{Vous êtes en mode inclusion. Cliquez à nouveau sur le bouton d\'inclusion pour sortir de ce mode}}');
            $('.changeIncludeState[data-mode=1][data-serverID='+_options.serverId+']').html('<i class="fa fa-sign-in fa-rotate-90" style="font-size: 6em;"></i><br/>{{Stop inclusion}}');
        }else if (_options.state == 5) {
            $('.changeIncludeState[data-mode=0][data-serverID='+_options.serverId+']').removeClass('ui-btn-a').addClass('ui-btn-b');
            $('.changeIncludeState[data-mode=0][data-serverID='+_options.serverId+']').attr('data-state', 0);
            $('#div_inclusionAlert'+_options.serverId).html('{{Vous êtes en mode exclusion. Cliquez à nouveau sur le bouton d\'exclusion pour sortir de ce mode}}');
            $('.changeIncludeState[data-mode=0][data-serverID='+_options.serverId+']').html('<i class="fa fa-sign-out fa-rotate-90" style="font-size: 6em;"></i><br/>{{Stop exclusion}}');
        }else{
            $('.changeIncludeState[data-serverID='+_options.serverId+']').removeClass('ui-btn-b').addClass('ui-btn-a');
            $('#div_inclusionAlert'+_options.serverId).html('{{Aucun mode actif}}');
            $('.changeIncludeState[data-mode=0][data-serverID='+_options.serverId+']').html('<i class="fa fa-sign-out fa-rotate-90" style="font-size: 6em;"></i><br/>{{Exclusion}}');
            $('.changeIncludeState[data-mode=1][data-serverID='+_options.serverId+']').html('<i class="fa fa-sign-in fa-rotate-90" style="font-size: 6em;"></i><br/>{{Inclusion}}');
            $('.changeIncludeState[data-mode=1][data-serverID='+_options.serverId+']').attr('data-state', 1);
            $('.changeIncludeState[data-mode=0][data-serverID='+_options.serverId+']').attr('data-state', 1);
        }
    });


socket.on('zwave::notification', function(_options) {
    $('#div_inclusionAlert').html(_options);
});


setTimeout(function() {
    socket.on('zwave::includeDevice', function(_options) {
        $('.eqLogicAttr[data-l1key=id]').value('');
        if (_options != '') {
            $("#popup_configIncludeDevice").popup("open");
            $('.eqLogicAttr[data-l1key=id]').value(_options);
        }
    });
}, 3000);
}

$('#div_listIncludeSever').delegate('.changeIncludeState','click', function() {
    changeIncludeState($(this).attr('data-mode'), $(this).attr('data-state'), $(this).attr('data-serverID'));
});


 $.ajax({// fonction permettant de faire de l'ajax
        type: "POST", // methode de transmission des données au fichier php
        url: "plugins/openzwave/core/ajax/openzwave.ajax.php", // url du fichier php
        data: {
            action: "listServerZwave",
        },
        dataType: 'json',
        async: false,
        error: function(request, status, error) {
            handleAjaxError(request, status, error, $('#div_inclusionAlert'));
        },
        success: function(data) { // si l'appel a bien fonctionné
        if (data.state != 'ok') {
            $('#div_inclusionAlert').html(data.result);
            return;
        }
        var listServerZwave = data.result;
        $('#div_listIncludeSever').empty();
        for(var i in listServerZwave){
            if(listServerZwave[i].name != null){
             var html = '';
             html += '<legend>'+listServerZwave[i].name+'</legend>';
             html += '<div id="div_inclusionAlert'+i+'" style="text-align: center;font-size: 2em;"></div>';
             html += '<div class="ui-grid-a">';
             html += '<div class="ui-block-a">';
             html += '<center>';
             html += '<a href="#" class="ui-btn ui-btn-a changeIncludeState" data-mode="1" data-state="1" data-serverID="'+i+'" style="margin: 5px;">';
             html += '<i class="fa fa-sign-in fa-rotate-90" style="font-size: 6em;"></i><br/>{{Inclusion}}';
             html += '</a>';
             html += '</center>';
             html += '</div>';
             html += '<div class="ui-block-b">';
             html += '<center>';
             html += '<a href="#" class="ui-btn ui-btn-a changeIncludeState" data-mode="0" data-state="1" data-serverID="'+i+'" style="margin: 5px;">';
             html += '<i class="fa fa-sign-out fa-rotate-90" style="font-size: 6em;"></i><br/>{{Exclusion}}';
             html += '</a>';
             html += '</center>';
             html += '</div>';
             html += '</div>';
             $('#div_listIncludeSever').append(html);
             var controllerState = getControllerState(i);
             var networkState = controllerState.result.data.mode.value;
             if (networkState == "0") {
                $('#div_inclusionAlert'+i).html('{{Aucun mode actif}}');
            }
            if (networkState == "1") {
                $('#div_inclusionAlert'+i).html('{{Vous êtes en mode inclusion. Cliquez à nouveau sur le bouton d\'inclusion pour sortir de ce mode}}');
                $('.changeIncludeState[data-mode=1][data-serverID='+i+']').removeClass('ui-btn-a').addClass('ui-btn-b');
                $('.changeIncludeState[data-mode=1][data-serverID='+i+']').attr('data-state', 0);
                $('.changeIncludeState[data-mode=1][data-serverID='+i+']').html('<i class="fa fa-sign-in fa-rotate-90" style="font-size: 6em;"></i><br/>{{Stop inclusion}}');
            }
            if (networkState == "5") {
                $('#div_inclusionAlert'+i).html('{{Vous êtes en mode exclusion. Cliquez à nouveau sur le bouton d\'exclusion pour sortir de ce mode}}');
                $('.changeIncludeState[data-mode=0][data-serverID='+i+']').removeClass('ui-btn-a').addClass('ui-btn-b');
                $('.changeIncludeState[data-mode=0][data-serverID='+i+']').attr('data-state', 0);
                $('.changeIncludeState[data-mode=0][data-serverID='+i+']').html('<i class="fa fa-sign-out fa-rotate-90" style="font-size: 6em;"></i><br/>{{Stop exclusion}}');
            }
        }
    }
}
});


$('#bt_validateConfigDevice').on('click', function() {
    jeedom.eqLogic.save({
        type: 'zwave',
        eqLogics: $("#popup_configIncludeDevice").getValues('.eqLogicAttr'),
        error: function(error) {
            $('#div_alert').showAlert({message: error.message, level: 'danger'});
            $('.eqLogicAttr[data-l1key=id]').value('');
            $("#popup_configIncludeDevice").popup("open");

        },
        success: function() {
            $("#popup_configIncludeDevice").popup("close");
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


function getControllerState(_serverID) {
    var result = '';
    $.ajax({// fonction permettant de faire de l'ajax
        type: "POST", // methode de transmission des données au fichier php
        url: "plugins/openzwave/core/ajax/openzwave.ajax.php", // url du fichier php
        data: {
            action: "getControllerState",
            serverID: _serverID,
        },
        dataType: 'json',
        async: false,
        error: function(request, status, error) {
            handleAjaxError(request, status, error, $('#div_inclusionAlert'));
        },
        success: function(data) { // si l'appel a bien fonctionné
        if (data.state != 'ok') {
            $('#div_inclusionAlert').html(data.result);
            return;
        }
        result = data.result;
    }
});
    return result;
}


function changeIncludeState(_mode, _state,_serverID) {
    $.ajax({// fonction permettant de faire de l'ajax
        type: "POST", // methode de transmission des données au fichier php
        url: "plugins/openzwave/core/ajax/openzwave.ajax.php", // url du fichier php
        data: {
            action: "changeIncludeState",
            mode: _mode,
            state: _state,
            serverID: _serverID,
        },
        dataType: 'json',
        error: function(request, status, error) {
            handleAjaxError(request, status, error);
        },
        success: function(data) { // si l'appel a bien fonctionné
        if (data.state != 'ok') {
            $('#div_alert').showAlert({message: data.result, level: 'danger'});
            return;
        }
    }
});
}

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

var app_config = {
    init: function () {
        $("#saveconf").click(function () {
            $.ajax({
                type: 'POST',
                url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/network.SaveZWConfig()",
                dataType: 'json',
                data: {
                    data: $("#zwcfgfile").val()
                },
                error: function (request, status, error) {
                    handleAjaxError(request, status, error, $('#div_configOpenzwaveAlert'));
                },
                success: function (data) {
                    if (data['result']) {
                        $('#div_configOpenzwaveAlert').showAlert({
                            message: '{{Sauvegarde de la configuration réussie. Le réseau va redémarrer}}',
                            level: 'success'
                        });
                    } else {
                        $('#div_configOpenzwaveAlert').showAlert({
                            message: '{{Echec de la sauvegarde de la configuration : }}' + data['data'],
                            level: 'danger'
                        });
                    }
                }
            });
        });
    },
    show: function () {
        $.ajax({
            url: "plugins/openzwave/core/php/jeeZwaveProxy.php?request=ZWaveAPI/Run/network.GetZWConfig()",
            dataType: 'json',
            error: function (request, status, error) {
                handleAjaxError(request, status, error, $('#div_configOpenzwaveAlert'));
            },
            success: function (data) {
                $("#zwcfgfile").val(data['result']);
            }
        });
    },
    hide: function () {

    }
}

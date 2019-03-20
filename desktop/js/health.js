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
 $('#bt_pingAllDevice').off().on('click', function () {
    jeedom.openzwave.controller.action({
        action : 'testNetwork',
        error: function (error) {
            $('#div_networkHealthAlert').showAlert({message: error.message, level: 'danger'});
        },
        success: function (data) {
            $('#div_networkHealthAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
            display_health_info();
        }
    });
});

 $('#table_healthNetwork').off().delegate('.bt_pingDevice', 'click', function () {
    jeedom.openzwave.node.action({
        action : 'testNode',
        node_id: $(this).attr('data-id'),
        error: function (error) {
           $('#div_networkHealthAlert').showAlert({message: error.message, level: 'danger'});
       },
       success: function (data) {
         $('#div_networkHealthAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
         display_health_info();
     }
 });
});

 $('#bt_refreshHealth').on('click',function(){
    display_health_info();
});

 function display_health_info(){
   jeedom.openzwave.network.info({
    info : 'getHealth',
    error: function (error) {
        $('#div_networkHealthAlert').showAlert({message: error.message, level: 'danger'});
    },
    success: function (data) {
        var nodes = data.devices;
        var tbody = '';
        var now = Math.floor(new Date().getTime() / 1000);
        for (var node_id in nodes) {
            if (nodes[node_id].data == undefined) {
                continue;
            }
            tbody += (nodes[node_id].data.isEnable.value) ?  '<tr>' : '<tr class="active">';
            tbody += '<td>';
            var name = '<span class="nodeConfiguration cursor" data-node-id="' + node_id + '">';
            if (nodes[node_id].data.description.name != '') {
                name += '<span  class="label label-primary" style="font-size : 1em;">' + nodes[node_id].data.description.location + '</span> ' + nodes[node_id].data.description.name;
            } else {
                name += nodes[node_id].data.description.product_name;
            }
            name += '</span>';
            tbody += (nodes[node_id].data.isEnable.value) ? name :  '<div style="opacity:0.5"><i>' + name + '</i></div>';
            tbody += '</td>';
            tbody += '<td>';
            tbody += (nodes[node_id].data.isEnable.value) ? node_id : '<div style="opacity:0.5"><i>' + node_id + '</i></div>';
            tbody += '</td>';
            tbody += '<td>';
            if (nodes[node_id].data.isSecured.enabled) {
                if (nodes[node_id].data.isSecured.value) {
                    tbody += '  <span title="{{Sécurisé}}"><i class="fa fa-lock text-success" aria-hidden="true"></i></span> ';
                } else {
                    tbody += '  <span title="{{Non sécurisé}}"><i class="fa fa-unlock  text-success" aria-hidden="true"></i></span> ';
                }
            }
            if (nodes[node_id].data.isZwavePlus.value) {
                tbody += ' <span title="{{ZWAVE PLUS}}"><i class="fa fa-plus-circle text-info" aria-hidden="true"></i></span> ';
            }
            if (nodes[node_id].data.isFrequentListening.value) {
                tbody += ' <span title="{{FLiRS}}"><i class="fa fa-assistive-listening-systems " aria-hidden="true"></i></span> ';
            }
            tbody += '</td>';
            tbody += '<td>';
            if (nodes[node_id].data.isEnable.value) {
                if (nodes[node_id].data.is_groups_ok != undefined && nodes[node_id].data.is_groups_ok.value) {
                    tbody += '<span class="label label-success" style="font-size : 1em;">{{OK}}</span>';
                } else {
                    if (nodes[node_id].data.is_groups_ok.enabled) {
                        tbody += '<span class="label label-danger" style="font-size : 1em;">{{NOK}}</span>';
                    }
                }
            }
            tbody += '</td>';
            tbody += '<td>';
            if (nodes[node_id].data.isEnable.value && nodes[node_id].data.is_manufacturer_specific_ok != undefined) {
                if (nodes[node_id].data.is_manufacturer_specific_ok.enabled){
                    if (nodes[node_id].data.is_manufacturer_specific_ok.value) {
                        tbody += '<span class="label label-success" style="font-size : 1em;">{{OK}}</span>';
                    } else {
                        tbody += '<span class="label label-danger" style="font-size : 1em;">{{NOK}}</span>';
                    }
                }
            }
            tbody += '</td>';
            tbody += '<td>';
            if (nodes[node_id].data.isEnable.value) {
                if (nodes[node_id].data.is_neighbours_ok != undefined && nodes[node_id].data.is_neighbours_ok.value) {
                    tbody += '<span class="label label-success" style="font-size : 1em;">{{OK}}</span>';
                } else {
                    if (nodes[node_id].data.is_neighbours_ok.enabled) {
                        tbody += '<span class="label label-danger" style="font-size : 1em;">{{NOK}}</span>';
                    }
                }
            }
            tbody += '</td>';
            tbody += '<td>';
            if (nodes[node_id].data.isEnable.value) {
                if (nodes[node_id].data.pending_changes != undefined && nodes[node_id].data.pending_changes.count > 0) {
                    tbody += '<span class="label label-warning" style="font-size : 1em;" title="' + nodes[node_id].data.pending_changes.count + ' {{configuration(s) en attente d\'être appliquée(s)}}" >' + nodes[node_id].data.pending_changes.count + '</span>';
                } else if (nodes[node_id].data.pending_changes != undefined && nodes[node_id].data.pending_changes.value == 0) {
                    tbody += '<span class="label label-success" style="font-size : 1em;">{{OK}}</span>';
                }
            }
            tbody += '</td>';
            tbody += '<td>';
            var status = '';
            var query_stage = '';
            if (nodes[node_id].data.state != undefined) {
                query_stage = nodes[node_id].data.state.value;
                if (nodes[node_id].data.isFailed != undefined && !nodes[node_id].data.isFailed.value) {
                    if (nodes[node_id].data.state.value == 'Complete') {
                        status += '<span class="label label-success" style="font-size : 1em;">' + nodes[node_id].data.state.value + '</span>';
                    } else {
                        status += '<span class="label label-warning" style="font-size : 1em;">' + nodes[node_id].data.state.value + '</span>';
                    }
                } else {
                    status += '<span class="label label-danger" style="font-size : 1em;">{{DEATH}}</span>';
                }
            } else {
                status += '<span class="label label-warning" style="font-size : 1em;">--</span>';
            }
            tbody += (nodes[node_id].data.isEnable.value) ? status : '<div style="opacity:0.5"><i>' + status + '</i></div>';
            tbody += '</td>';
            tbody += '<td>';
            if (nodes[node_id].data.isEnable.value) {
                if (query_stage != '' && query_stage != 'Probe'){
                    if (nodes[node_id].data.isListening.value) {
                        tbody += '<span class="label label-primary" style="font-size : 1em;" title="{{Secteur}}"><i class="fa fa-plug"></i></span>';
                    } else {
                        if (nodes[node_id].data.battery_level != undefined && nodes[node_id].data.battery_level.value != null) {
                            var updateTime = '';
                            if (nodes[node_id].data.battery_level.updateTime != undefined) {
                                updateTime = jeedom.openzwave.timestampConverter(nodes[node_id].data.battery_level.updateTime, false);
                            }
                            if (nodes[node_id].data.battery_level.value > 75) {
                                tbody += '<span class="label label-success" style="font-size : 1em;" title="' + updateTime + '">' + nodes[node_id].data.battery_level.value + '%</span>';
                            } else if (nodes[node_id].data.battery_level.value > 50) {
                                tbody += '<span class="label label-warning" style="font-size : 1em;" title="' + updateTime + '">' + nodes[node_id].data.battery_level.value + '%</span>';
                            } else {
                                tbody += '<span class="label label-danger" style="font-size : 1em;" title="' + updateTime + '">' + nodes[node_id].data.battery_level.value + '%</span>';
                            }
                        } else if (nodes[node_id].data.wakeup_interval != undefined && nodes[node_id].data.wakeup_interval.value != null) {
                            tbody += '<span class="label label-warning" style="font-size : 1em;">--</span>';
                        }
                    }
                }
                else{
                    tbody += '<span class="label label-warning" style="font-size : 1em;">--</span>';
                }
            }
            tbody += '</td>';
            tbody += '<td>';
            if (nodes[node_id].data.isEnable.value) {
                if (!nodes[node_id].data.isListening.value && nodes[node_id].data.wakeup_interval != undefined && nodes[node_id].data.wakeup_interval.value != null) {
                    if (nodes[node_id].data.wakeup_interval.value != 0 && nodes[node_id].data.wakeup_interval.value < 3600) {
                        tbody += '<span class="label label-warning" style="font-size : 1em;">'
                    }else {
                        tbody += '<span class="label label-info" style="font-size : 1em;">'
                    }
                    if (nodes[node_id].data.wakeup_interval.value != 0){
                        tbody += nodes[node_id].data.wakeup_interval.value + '</span>';
                    }
                    else{
                        tbody += '--</span>';
                    }

                }
            }
            tbody += '</td>';
            tbody += '<td>';
            if (nodes[node_id].data.isEnable.value) {
                tbody += '<span class="label label-primary" style="font-size : 1em;">' + nodes[node_id].data.statistics.total + '</span>';
            }
            tbody += '</td>';
            tbody += '<td>';
            if (nodes[node_id].data.isEnable.value) {
                if (nodes[node_id].data.statistics != undefined && nodes[node_id].data.statistics.total > 0 && nodes[node_id].data.statistics.delivered != null) {
                    if (nodes[node_id].data.statistics.delivered > 90) {
                        tbody += '<span class="label label-success" style="font-size : 1em;">' + nodes[node_id].data.statistics.delivered + '%</span>';
                    } else if (nodes[node_id].data.statistics.delivered > 75) {
                        tbody += '<span class="label label-warning" style="font-size : 1em;">' + nodes[node_id].data.statistics.delivered + '%</span>';
                    } else {
                        tbody += '<span class="label label-danger" style="font-size : 1em;">' + nodes[node_id].data.statistics.delivered + '%</span>';
                    }
                }
            }
            tbody += '</td>';
            tbody += '<td>';
            if (nodes[node_id].data.isEnable.value) {
                if (nodes[node_id].data.statistics != undefined && nodes[node_id].data.statistics.total > 0 && nodes[node_id].data.statistics.deliveryTime != null) {
                    if (nodes[node_id].data.statistics.deliveryTime > 500) {
                        tbody += '<span class="label label-danger" style="font-size : 1em;">' + nodes[node_id].data.statistics.deliveryTime + 'ms</span>';
                    } else if (nodes[node_id].data.statistics.deliveryTime > 250) {
                        tbody += '<span class="label label-warning" style="font-size : 1em;">' + nodes[node_id].data.statistics.deliveryTime + 'ms</span>';
                    } else {
                        tbody += '<span class="label label-success" style="font-size : 1em;">' + nodes[node_id].data.statistics.deliveryTime + 'ms</span>';
                    }
                }
            }
            tbody += '</td>';
            tbody += '<td>';
            if (nodes[node_id].data.isEnable.value) {
                if (nodes[node_id].data.isListening.value) {
                    tbody += jeedom.openzwave.timestampConverter(nodes[node_id].data.lastReceived.updateTime);
                }else if (nodes[node_id].last_notification.description != undefined && nodes[node_id].data.lastReceived != undefined && nodes[node_id].data.lastReceived.updateTime != null) {
                    tbody += jeedom.openzwave.timestampConverter(nodes[node_id].data.lastReceived.updateTime);
                    if (nodes[node_id].data.wakeup_interval != undefined && nodes[node_id].data.wakeup_interval.next_wakeup != null) {
                        if (now > nodes[node_id].data.wakeup_interval.next_wakeup) {
                            tbody += ' <i class="fas fa-arrow-right text-danger"></i><span class="label label-warning" style="font-size : 1em;" title="{{Le noeud ne s\'est pas réveillé comme prévue}}"> ' + jeedom.openzwave.timestampConverter(nodes[node_id].data.wakeup_interval.next_wakeup) + ' </span>';
                        }else {
                            tbody += ' <i class="fas fa-arrow-right"></i><br> ' + jeedom.openzwave.timestampConverter(nodes[node_id].data.wakeup_interval.next_wakeup) + ' <i class="fa fa-clock-o"></i>';
                        }
                    }
                } else if (nodes[node_id].data.isListening.value == false && nodes[node_id].data.last_notification == undefined && nodes[node_id].data.wakeup_interval != undefined && nodes[node_id].data.wakeup_interval.value != null && nodes[node_id].data.lastReceived != undefined && nodes[node_id].data.lastReceived.updateTime != null) {
                    if (now > nodes[node_id].data.lastReceived.updateTime + nodes[node_id].data.wakeup_interval.value && nodes[node_id].data.wakeup_interval.value >0) {
                        tbody += '<span class="label label" style="font-size : 1.5em;" title="{{Le noeud ne s\'est pas encore réveillé une fois depuis le lancement du démon}}"><i class="fa fa-exclamation-circle text-danger"></i></span>';
                    }
                }
            }
            tbody += '</td>';
            tbody += '<td>';
            if (nodes[node_id].data.isEnable.value) {
                tbody += '<a class="btn btn-info btn-xs bt_pingDevice" data-id="' + node_id + '"><i class="fa fa-eye"></i> {{Ping}}</a>';
            }
            tbody += '</td>';
            tbody += '</tr>';
        }
        $('#table_healthNetwork tbody').empty().append(tbody)
    }
});
}

display_health_info();
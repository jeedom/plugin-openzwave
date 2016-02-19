
var app_health = {
  // note variable nodes is global!

  updater: false,

  timestampConverter :function(time,_hourOnly){
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
    var num = date.getDate();
    if(num<10){
      num="0"+num;
    }
    var month = date.getMonth()+1;
    if(month<10){
      month="0"+month;
    }
    var year = date.getFullYear();
    var formattedTime = hours + ':' + minutes ;
    var formattedDate = num + "/" + month + "/" + year;
    if(_hourOnly){
      return formattedTime;
    }
    return formattedDate+' '+formattedTime;
  },
  init: function(){
    app_health.load_data(true);
    app_health.updater = setInterval(function(){
      if($('#table_healthNetwork').is(':visible')){
        app_health.load_data(false);
      }else{
        app_health.hide();
      }
    }, 2000);
    $('#bt_pingAllDevice').off().on('click',function(){
      $.ajax({
        url: path+"ZWaveAPI/Run/controller.TestNetwork()",
        dataType: 'json',
        async: true,
        error: function (request, status, error) {
          handleAjaxError(request, status, error,$('#div_networkHealthAlert'));
        },
        success: function(data) {
          app_health.sendOk();
          app_health.load_data(false);
        }
      });
    });

    $('#table_healthNetwork').off().delegate('.bt_pingDevice','click',function(){
      $.ajax({
        url: path+"ZWaveAPI/Run/devices["+$(this).attr('data-id')+"].TestNode()",
        dataType: 'json',
        async: true,
        error: function (request, status, error) {
          handleAjaxError(request, status, error,$('#div_networkHealthAlert'));
        },
        success: function(data) {
          app_health.sendOk();
          app_health.load_data(false);
        }
      });
    });
  },
  hide: function(){
    clearInterval(app_health.updater);
  },
  load_data: function(_global){
    $.ajax({
      url: path+"ZWaveAPI/Run/network.GetHealth()",
      dataType: 'json',
      async: true,
      global : _global,
      error: function (request, status, error) {
        handleAjaxError(request, status, error,$('#div_networkHealthAlert'));
      },
      success: function(data) {
        infos = data;
        app_health.show_infos(data.devices);
      }
    });
  },
  show_infos: function (nodes){
    var tbody = '';
    for(var i in nodes){
      if(nodes[i].data == undefined){
        continue;
      }
      if(isset(eqLogic_human_name[$('#sel_zwaveHealthServerId').value()+':'+i])){
        var name = '<span class="nodeConfiguration cursor" data-node-id="'+i+'" data-server-id="'+$("#sel_zwaveHealthServerId").value()+'">'+eqLogic_human_name[$('#sel_zwaveHealthServerId').value()+':'+i]+'</span>';
      }else if(nodes[i].data.description.name != ''){
        var name = '<span class="nodeConfiguration cursor" data-node-id="'+i+'" data-server-id="'+$("#sel_zwaveHealthServerId").value()+'"><span  class="label label-primary" style="font-size : 1em;">'+nodes[i].data.description.location+'</span> '+nodes[i].data.description.name+'</span>';
      }else{
        var name = '<span class="nodeConfiguration cursor" data-node-id="'+i+'" data-server-id="'+$("#sel_zwaveHealthServerId").value()+'">'+ nodes[i].data.description.product_name+'</span>';
      }
      tbody += '<tr>';
      tbody += '<td>';
      tbody += name;
      tbody += '</td>';
      tbody += '<td>';
      tbody += i;
      tbody += '</td>';
      tbody += '<td>';
      if(nodes[i].last_notification != undefined){
        if(nodes[i].last_notification.description == 'Timeout'){
          tbody += '<span class="label label-warning" style="font-size : 1em;" title="'+nodes[i].last_notification.help+'">'+nodes[i].last_notification.description+'</span>';
        }else if(nodes[i].last_notification.description == 'Dead'){
          tbody += '<span class="label label-danger" style="font-size : 1em;" title="'+nodes[i].last_notification.help+'">'+nodes[i].last_notification.description+'</span>';
        }else if(nodes[i].last_notification.description != undefined){
          tbody += '<span class="label label-primary" style="font-size : 1em;" title="'+nodes[i].last_notification.help+'">'+nodes[i].last_notification.description+'</span>';
        }else{
          tbody += '<span class="label label-primary" style="font-size : 1em;" title="{{Non disponible}}">...</span>';
        }
      }
      tbody += '</td>';
      tbody += '<td>';
      if(nodes[i].data.is_groups_ok != undefined && nodes[i].data.is_groups_ok.value){
        tbody += '<span class="label label-success" style="font-size : 1em;">{{OK}}</span>';
      }else{
        if(nodes[i].data.is_groups_ok.enabled){
          tbody += '<span class="label label-danger" style="font-size : 1em;">{{NOK}}</span>';
        }
      }
      tbody += '</td>';
      tbody += '<td>';
      if(nodes[i].data.is_manufacturer_specific_ok != undefined && nodes[i].data.is_manufacturer_specific_ok.value){
        tbody += '<span class="label label-success" style="font-size : 1em;">{{OK}}</span>';
      }else{
        tbody += '<span class="label label-danger" style="font-size : 1em;">{{NOK}}</span>';
      }
      tbody += '</td>';
      tbody += '<td>';
      if(nodes[i].data.is_neighbours_ok != undefined && nodes[i].data.is_neighbours_ok.value){
        tbody += '<span class="label label-success" style="font-size : 1em;">{{OK}}</span>';
      }else{
        if(nodes[i].data.is_neighbours_ok.enabled){
          tbody += '<span class="label label-danger" style="font-size : 1em;">{{NOK}}</span>';
        }
      }
      tbody += '</td>';
      tbody += '<td>';
      if(nodes[i].data.isFailed != undefined && !nodes[i].data.isFailed.value){
        if(nodes[i].data.state != undefined){
          if(nodes[i].data.state.value == 'Complete'){
            tbody += '<span class="label label-success" style="font-size : 1em;">'+nodes[i].data.state.value+'</span>';
          }else{
            tbody += '<span class="label label-warning" style="font-size : 1em;">'+nodes[i].data.state.value+'</span>';
          }
        }else{
          tbody += '<span class="label label-success" style="font-size : 1em;">{{OK}}</span>';
        }
      }else{
        tbody += '<span class="label label-danger" style="font-size : 1em;">{{DEATH}}</span>';
      }
      tbody += '</td>';
      tbody += '<td>';
      if(nodes[i].data.battery_level != undefined && nodes[i].data.battery_level.value != null) {
        var updateTime ='';
        if (nodes[i].data.battery_level.updateTime != undefined){
          updateTime = app_health.timestampConverter(nodes[i].data.battery_level.updateTime,false);
        }


        if (nodes[i].data.battery_level.value > 75) {
          tbody += '<span class="label label-success" style="font-size : 1em;" title="'+updateTime+'">' + nodes[i].data.battery_level.value + '%</span>';
        } else if (nodes[i].data.battery_level.value > 50) {
          tbody += '<span class="label label-warning" style="font-size : 1em;" title="'+updateTime+'">' + nodes[i].data.battery_level.value + '%</span>';
        } else {
          tbody += '<span class="label label-danger" style="font-size : 1em;" title="'+updateTime+'">' + nodes[i].data.battery_level.value + '%</span>';
        }
      }else if(nodes[i].data.wakeup_interval != undefined && nodes[i].data.wakeup_interval.value != null){
        tbody += '<span class="label label-warning" style="font-size : 1em;">--</span>';
      }else{
        tbody += '<span class="label label-primary" style="font-size : 1em;" title="{{Secteur}}"><i class="fa fa-plug"></i></span>';
      }
      tbody += '</td>';
      tbody += '<td>';
      if(nodes[i].data.wakeup_interval != undefined && nodes[i].data.wakeup_interval.value != null){
        tbody += '<span class="label label-info" style="font-size : 1em;">'+nodes[i].data.wakeup_interval.value+'</span>';
      }
      tbody += '</td>';
      tbody += '<td>';
      if(nodes[i].data.statistics != undefined && nodes[i].data.statistics.total >0){
        tbody += '<span class="label label-primary" style="font-size : 1em;">'+nodes[i].data.statistics.total+'</span>';
      }else if(nodes[i].data.statistics != undefined && nodes[i].data.statistics.total != null){
        tbody += '<span class="label label-warning" style="font-size : 1em;">'+nodes[i].data.statistics.total+'</span>';
      }
      tbody += '</td>';
      tbody += '<td>';
      if(nodes[i].data.statistics != undefined && nodes[i].data.statistics.total >0 && nodes[i].data.statistics.delivered != null){
        if(nodes[i].data.statistics.delivered > 90){
          tbody += '<span class="label label-success" style="font-size : 1em;">'+nodes[i].data.statistics.delivered+'%</span>';
        }else if(nodes[i].data.statistics.delivered > 75){
          tbody += '<span class="label label-warning" style="font-size : 1em;">'+nodes[i].data.statistics.delivered+'%</span>';
        }else{
          tbody += '<span class="label label-danger" style="font-size : 1em;">'+nodes[i].data.statistics.delivered+'%</span>';
        }
      }
      tbody += '</td>';
      tbody += '<td>';
      if(nodes[i].data.statistics != undefined && nodes[i].data.statistics.total >0 && nodes[i].data.statistics.deliveryTime != null){
        if(nodes[i].data.statistics.deliveryTime > 500){
          tbody += '<span class="label label-danger" style="font-size : 1em;">'+nodes[i].data.statistics.deliveryTime+'ms</span>';
        }else if(nodes[i].data.statistics.deliveryTime > 250){
          tbody += '<span class="label label-warning" style="font-size : 1em;">'+nodes[i].data.statistics.deliveryTime+'ms</span>';
        }else{
          tbody += '<span class="label label-success" style="font-size : 1em;">'+nodes[i].data.statistics.deliveryTime+'ms</span>';
        }
      }
      tbody += '</td>';
      tbody += '<td>';
      if(nodes[i].last_notification.description != undefined && nodes[i].data.lastReceived != undefined && nodes[i].data.lastReceived.updateTime != null){
        tbody += app_health.timestampConverter(nodes[i].data.lastReceived.updateTime,false);
        if(nodes[i].data.wakeup_interval != undefined && nodes[i].data.wakeup_interval.next_wakeup != null){
          tbody += ' <i class="fa fa-arrow-right"></i> ' + app_health.timestampConverter(nodes[i].data.wakeup_interval.next_wakeup,true)+' <i class="fa fa-clock-o"></i>';
        }
      }
      tbody += '</td>';
      tbody += '<td>';
      tbody += '<a class="btn btn-info btn-xs bt_pingDevice" data-id="'+i+'"><i class="fa fa-eye"></i> {{Ping}}</a>';
      tbody += '</td>';
      tbody += '</tr>';
    }
    $('#table_healthNetwork tbody').empty().append(tbody);
  },
  update: function (){

  },
  sendOk : function(){
    $('#span_state').show();
    setTimeout(function(){ $('#span_state').hide(); }, 3000);
  },
  show: function (){

  },

}

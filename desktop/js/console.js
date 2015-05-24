var app_console = {
	updater: false,
    init: function(){
        $("#stopLiveLog").off("click").on("click",function() {
            clearInterval(app_console.updater);
            $("#stopLiveLog").hide();
            $("#startLiveLog").show();
        });
        $("#startLiveLog").off("click").on("click",function() {
            app_console.updater = setInterval(app_console.refresh,2000);
            $("#startLiveLog").hide();
            $("#stopLiveLog").show();
        });
        $(".console-out").html("");
    },
    show: function(){
    	$("#startLiveLog").hide();
        app_console.updater = setInterval(app_console.refresh,2000);
    },
    refresh: function(){
    	$.ajax({ 
            url: path+"ZWaveAPI/Run/GetOZLogs()", 
            dataType: 'json',
            async: true, 
            global : false,
            error: function (request, status, error) {
            handleAjaxError(request, status, error,$('#div_consoleOpenzwaveAlert'));
        },
            success: function(data) {
                if (!$(".console-out").is(':visible')) {
                    clearInterval(app_console.updater);
                    return;
                }
                if(data['result']){
                   $(".console-out").html(data['result']);
                   var h = parseInt($('#log')[0].scrollHeight);
                   $('#log').scrollTop(h);
				}else{
					$(".console-out").append("error");
				}
            }
        });
    },
    hide: function(){
    	clearInterval(app_console.updater);
    }
}

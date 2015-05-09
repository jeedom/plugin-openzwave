var app_console = {
	updater: false,
    init: function()
    {
        $("#stopLiveLog").on("click",function() {
            clearInterval(app_console.updater);
            $("#stopLiveLog").hide();
            $("#startLiveLog").show();
        });
        $("#startLiveLog").on("click",function() {
            app_console.updater = setInterval(app_console.refresh,2000);
            $("#startLiveLog").hide();
            $("#stopLiveLog").show();
        });
        $(".console-out").html("");
    },
    
    show: function()
    {
    	$("#startLiveLog").hide();
        app_console.updater = setInterval(app_console.refresh,2000);
    },
    refresh: function(){
    	//$(".console-out").html("");
    	$.ajax({ 
            url: path+"ZWaveAPI/Run/GetOZLogs()", 
            dataType: 'json',
            async: true, 
            global : false,
            success: function(data) {
                if (!$(".console-out").is(':visible')) {
                    clearInterval(app_console.updater);
                    return;
                }
                if(data['result']){
                   $(".console-out").html(data['result']);
                   var h = parseInt($('#log')[0].scrollHeight);
                   $('#log').scrollTop(h);
					//$('#alert_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong > Command Sent !</span></div>');
				}else{
					$(".console-out").append("error");
				}
            },
            error: function(data) {
            	$('#alert_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span><strong>Error !</strong></span></div>');
            }
        });
    },
    hide: function()
    {
    	clearInterval(app_console.updater);
    }
}

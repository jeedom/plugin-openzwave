var app_config = {

    init: function()
    {
        $("#saveconf").click(function(){
        
            $.ajax({ 
                type:'POST', 
                url: path+"ZWaveAPI/Run/SaveZWConfig()", 
                contentType: "text/plain", 
                data: $("#zwcfgfile").val(),
                success: function(data) {
                	$('#alert_config_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span><strong>Success !</strong> File Saved !</span></div>');
                }
            });
        });
    },
    
    show: function()
    {
        $.ajax({ url: path+"ZWaveAPI/Run/GetZWConfig()", 
            dataType: 'json', success: function(data){
            $("#zwcfgfile").val(data['result']);
        }});
    },
    
    hide: function()
    {
    
    }
}

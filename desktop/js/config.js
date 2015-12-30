var app_config = {
    init: function(){
        $("#saveconf").click(function(){
            $.ajax({ 
                type:'POST', 
                url: path+"ZWaveAPI/Run/network.SaveZWConfig()", 
                contentType: "text/plain", 
                data: $("#zwcfgfile").val(),
                error: function (request, status, error) {
                    handleAjaxError(request, status, error,$('#div_configOpenzwaveAlert'));
                },
                success: function(data) {
                    $('#div_configOpenzwaveAlert').showAlert({message: '{{Sauvegarde de la configuration réussie. Le réseau va redémarrer}}', level: 'success'});
                }
            });
        });
    },
    show: function(){
        $.ajax({ 
            url: path+"ZWaveAPI/Run/network.GetZWConfig()", 
            dataType: 'json', 
            error: function (request, status, error) {
                handleAjaxError(request, status, error,$('#div_configOpenzwaveAlert'));
            },
            success: function(data){
                $("#zwcfgfile").val(data['result']);
            }
        });
    },
    hide: function(){

    }
}

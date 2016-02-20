var app_config = {
    init: function(){
        $("#saveconf").click(function(){
            $.ajax({
                type:'POST',
                url: path+"ZWaveAPI/Run/network.SaveZWConfig()",
                data: {
                    data : $("#zwcfgfile").val()
                },
                error: function (request, status, error) {
                    handleAjaxError(request, status, error,$('#div_configOpenzwaveAlert'));
                },
                success: function(data) {
                    if(data['result']){
                        $('#div_configOpenzwaveAlert').showAlert({message: '{{Sauvegarde de la configuration réussie. Le réseau va redémarrer}}', level: 'success'});
                    }else{
                        $('#div_configOpenzwaveAlert').showAlert({message: '{{Echec de la sauvegarde de la configuration : }}' + data['data'], level: 'danger'});
                    }
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

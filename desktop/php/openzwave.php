<?php
if (!isConnect('admin')) {
    throw new Exception('Error 401 Unauthorized');
}
sendVarToJS('eqType', 'openzwave');

$secure=0;
$options=array();
$port = config::byKey('port', 'openzwave');
$port_server = config::byKey('port_server', 'openzwave');
if($port_server==""){
	$port_server="8083";
}
if($port<>""){
	$options[] ='<option value="'.$_SERVER["SERVER_ADDR"].':'.$port_server.'">local</option>';
}
if (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] == 'on') {
	$secure=1;
}
foreach (jeeNetwork::byPlugin('openzwave') as $jeeNetwork) {
    $id_sat=$jeeNetwork->getId();
	$port_sat=config::byKey('port_server'.$id_sat, 'openzwave');
	if($port_sat==""){
		$port_sat="8083";
	}
	$ip_sat=$jeeNetwork->getRealIp().':'.$port_sat;
	$options[] ='<option value="'.$ip_sat.'">'.$jeeNetwork->getName().' ('.$ip_sat.')</option>';
}
echo '<div class="row row-overflow">

    <div class="col-lg-12 eqLogic" style="border-left: solid 1px #EEE; padding-left: 25px;">
        <div class="row">
            <div class="col-lg-12">
               <legend>Serveur OpenZwave <select id="server" style="width:100px;">'.implode("\n", $options).'</select></legend> 
            </div>
        </div>
        <div id="ui_expert" style="height:93%;"></div>
      	
    </div>
</div>';
?>
<script>

$("#server").on("change", function() {
	<?php if($secure==0){ ?>
		$("#ui_expert").html('<iframe src="http://'+$(this).val()+'" width="100%" height="100%"></iframe>');
	<?php }else{ ?>
		$("#ui_expert").html('{{Votre connexion à Jeedom est sécurisée. Pour accéder à l\'interface avancée, merci de cliquer sur le lien suivant : }}<a href="http://'+$(this).val()+'" target="_blank">http://'+$(this).val()+'</a>');
	<?php } ?>
});
$("#server").trigger("change", $("#server option:first").val());
</script>
<?php
include_file('desktop', 'openzwave', 'js', 'openzwave');
include_file('core', 'plugin.template', 'js');
?>
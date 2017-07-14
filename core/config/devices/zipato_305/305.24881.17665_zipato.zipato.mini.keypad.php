<?php
require_once dirname(__FILE__) . "/../../../../../../core/php/core.inc.php";
include_file('core', 'authentification', 'php');
if (!isConnect()) {
	echo '<div class="alert alert-danger div_alert">';
	echo translate::exec('401 - Accès non autorisé');
	echo '</div>';
	die();
}
?>
<legend>Mémoires du clavier <a class="btn btn-primary btn-xs pull-right" id="bt_refreshZipatoAssist"><i class="fa fa-refresh"></i></a></legend>
<div id="div_configureDeviceAlert"></div>
<div class="alert alert-info">
    Info : <br/>
    - Ce tableau vous permet de visualiser les mémoires occupées sur votre clavier<br/>
    - Pour enregistrer un nouveau code cliquez sur le bouton Vert sur la mémoire désirée et suivez les étapes<br/>
    - Pour vider une mémoire, cliquez sur le bouton rouge<br/>
    - Il est impossible d'enregistrer le même code/badge sur deux mémoires différentes<br/>
    - Il est est impossible (par mesure de sécurité) de lire la valeur d'un code enregistré<br/>
</div>
<table class="table table-condensed table-bordered">
    <thead>
        <tr>
            <th>1</th>
            <th>2</th>
            <th>3</th>
            <th>4</th>
            <th>5</th>
            <th>6</th>
            <th>7</th>
            <th>8</th>
            <th>9</th>
            <th>10</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <?php
$data = openzwave::callOpenzwave('/ZWaveAPI/Run/devices[' . init('logical_id') . ']', init('serverId'));
$data = $data['instances'][0]['commandClasses'][99]['data'];
for ($i = 1; $i < 11; $i++) {
	echo '<td>';
	echo '<a class="btn btn-success pull-right btn-xs bt_ziptatoKeypadSaveNewCode" data-position="' . $i . '"><i class="fa fa-floppy-o"></i></a>';
	if (isset($data[$i]) && $data[$i]['val'] != '00000000000000000000') {
		echo '<i class="fa fa-check"></i>';
		echo '<a class="btn btn-danger pull-right btn-xs bt_ziptatoKeypadRemoveCode"  data-position="' . $i . '"><i class="fa fa-times"></i></a>';
	} else {
		echo '<i class="fa fa-times"></i>';
	}
	echo '</td>';
}
?>
      </tr>
  </tbody>
</table>

<script>
    $('#bt_refreshZipatoAssist').on('click',function(){
        $('#md_modal').load('index.php?v=d&plugin=openzwave&modal=device.assistant&id=<?php echo init('id'); ?>&logical_id=<?php echo init('logical_id'); ?>');
    });

    $('.bt_ziptatoKeypadRemoveCode').on('click',function(){
        var position = $(this).attr('data-position');
        bootbox.confirm('Etes vous sur de vouloir supprimer ce code ?', function (result) {
            if (result) {
               jeedom.openzwave.node.setRaw({
                node_id : <?php echo init('logical_id'); ?>,
                slot_id : position,
                value : '00000000000000000000',
                error: function (error) {
                    $('#div_configureDeviceAlert').showAlert({message: error.message, level: 'danger'});
                },
                success: function () {
                  $('#div_configureDeviceAlert').showAlert({message: 'Code enregistré, merci de réveiller votre clavier pour qu\'il soit pris en compte (touche HOME puis 1 puis Enter) ', level: 'success'});
                  $('#md_modal').load('index.php?v=d&plugin=openzwave&modal=device.assistant&id=<?php echo init('id'); ?>&logical_id=<?php echo init('logical_id'); ?>');
                  $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
              }
          });
           }
       });
    });
    $('.bt_ziptatoKeypadSaveNewCode').on('click',function(){
        var position = $(this).attr('data-position');
        bootbox.confirm('Allez vers votre clavier et appuyez sur Home et passez votre badge en étant sur d\'entendre le bip (dans le cas d\'un code appuyez sur Home , tapez le code et appuyez sur Enter) . Une fois fait cliquer sur D\'ACCORD !', function (result) {
           jeedom.openzwave.node.info({
            node_id : <?php echo init('logical_id'); ?>,
            info:'all',
            error: function (error) {
                $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: error.message, level: 'danger'});
            },
            success: function (data) {
                jeedom.openzwave.node.setRaw({
                    node_id : <?php echo init('logical_id'); ?>,
                    slot_id : position,
                    value : data.instances[1].commandClasses[99].data[0].val,
                    error: function (error) {
                        $('#div_configureDeviceAlert').showAlert({message: error.message, level: 'danger'});
                    },
                    success: function () {
                      $('#div_configureDeviceAlert').showAlert({message: 'Code enregistré, merci de réveiller votre clavier pour qu\'il soit pris en compte (touche HOME puis 1 puis Enter) ', level: 'success'});
                      $('#md_modal').load('index.php?v=d&plugin=openzwave&modal=device.assistant&id=<?php echo init('id'); ?>&logical_id=<?php echo init('logical_id'); ?>');
                      $('#div_nodeConfigureOpenzwaveAlert').showAlert({message: '{{Action réalisée avec succès}}', level: 'success'});
                  }
              });
            }
        });
       });
    });
</script>
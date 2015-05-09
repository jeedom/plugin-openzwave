<?php

foreach (eqLogic::byType('zwave') as $eqLogic) {
	$eqLogic->setEqType_name('openzwave');
	$eqLogic->setConfiguration('serverID', 6); // TODO FIND NEW SERVER ID
	$eqLogic->save();
	foreach ($eqLogic->getCmd() as $cmd) {
		$cmd->setEqType('openzwave');
		$cmd->save();
	}
}

?>
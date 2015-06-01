<?php
if (php_sapi_name() != 'cli' || isset($_SERVER['REQUEST_METHOD']) || !isset($_SERVER['argc'])) {
	header("Status: 404 Not Found");
	header('HTTP/1.0 404 Not Found');
	$_SERVER['REDIRECT_STATUS'] = 404;
	echo "<h1>404 Not Found</h1>";
	echo "The page that you have requested could not be found.";
	exit();
}

require_once dirname(__FILE__) . '/../../../core/php/core.inc.php';

echo "Début de la migration vers openzwave\n";

$server_convertion = array(1 => 1, 2 => 2, 3 => 3);

for ($i = 1; $i <= 3; $i++) {
	if (config::byKey('zwaveAddr' . $i, 'zwave') != '' && config::byKey('zwaveAddr' . $i, 'zwave') != -1) {
		if (config::byKey('zwaveAddr' . $i, 'zwave') == '127.0.0.1' || config::byKey('zwaveAddr' . $i, 'zwave') == 'localhost') {
			$server_convertion[$i] = 0;
		} else {
			foreach (jeeNetwork::all() as $jeeNetwork) {
				if (config::byKey('zwaveAddr' . $i, 'zwave') == $jeeNetwork->getRealIp()) {
					$server_convertion[$i] = $jeeNetwork->getId();
				}
			}
		}
	}
}
$found = false;
foreach (eqLogic::byType('zwave') as $eqLogic) {
	$found = true;
	$eqLogic->setEqType_name('openzwave');
	$server_id = $eqLogic->getConfiguration('serverID', 1);
	if (isset($server_convertion[$server_id])) {
		$server_id = $server_convertion[$server_id];
	} else {
		$server_id = 0;
	}
	$eqLogic->setConfiguration('serverID', $server_id);
	foreach ($eqLogic->getCmd() as $cmd) {
		$cmd->setEqType('openzwave');
		$cmd->save();
	}
	$eqLogic->save();
}

if ($found) {
	$replace = array(
		'.level' => '.val',
		'data.' => 'data[0].',
		'data[0].sensorState.value' => 'data[0].val',
		'Set(#slider#)' => 'data[0].Set(#slider#)',
		'Reset()' => 'data[0].PressButton()',
	);
	foreach (eqLogic::byType('openzwave') as $eqLogic) {
		foreach ($eqLogic->getCmd() as $cmd) {
			$cmd->setConfiguration('value', str_replace(array_keys($replace), $replace, $cmd->getConfiguration('value')));
			if ($cmd->getConfiguration('class') == '0x80') {
				$cmd->setConfiguration('value', str_replace('data.last', 'data[0].val', $cmd->getConfiguration('value')));
				$cmd->setConfiguration('value', str_replace('data[0].last', 'data[0].val', $cmd->getConfiguration('value')));
			}
			if ($cmd->getConfiguration('class') == '0x30') {
				$cmd->setConfiguration('value', str_replace('data[1].val', 'data[0].val', $cmd->getConfiguration('value')));
			}
			$value = $cmd->getConfiguration('value');
			preg_match_all("/Set\(([0-9]*)\)/", $value, $matches);
			if (count($matches) == 2 && @is_numeric($matches[1][0]) && @$matches[1][0] != '') {
				$value = 'data[0].Set(' . $matches[1][0] . ')';
			}
			preg_match_all("/Set\(([0-9]*),([0-9]*)\)/", $value, $matches);
			if (count($matches) == 3 && @is_numeric($matches[1][0]) && @$matches[1][0] != '' && @is_numeric($matches[2][0]) && @$matches[2][0] != '') {
				$value = 'data[' . $matches[1][0] . '].Set(' . $matches[2][0] . ')';
			}
			preg_match_all("/Set\(([0-9]*),([0-9]*),([0-9]*)\)/", $value, $matches);
			if (count($matches) == 4 && @is_numeric($matches[1][0]) && @$matches[1][0] != '' && @is_numeric($matches[2][0]) && @$matches[2][0] != '' && @is_numeric($matches[3][0]) && @$matches[3][0] != '') {
				$value = 'data[0].' . $value;
			}
			$cmd->setConfiguration('value', $value);
			if ($eqLogic->getConfiguration('device') == 'fibaro.fgrm221') {
				if ($cmd->getConfiguration('class') == '0x25' && $this->getConfiguration('data[0].val') && $this->getType() == 'info') {
					$cmd->setConfiguration('class', '0x26');
				}
			}
			$cmd->save();
		}
	}
}

$cron = cron::byClassAndFunction('zwave', 'pull');
if (is_object($cron)) {
	$cron->halt();
	$cron->remove();
}

$plugin = plugin::byId('zwave');
if (is_object($plugin)) {
	$plugin->setIsEnable(0);
}

echo "\nFin de la migration vers openzwave!!!!!!";
echo "\n/!\IL EST VIVEMENT CONSEILLE DE REDEMARRER JEEDOM/!\ ";
?>
<?php

/* This file is part of Jeedom.
 *
 * Jeedom is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Jeedom is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Jeedom. If not, see <http://www.gnu.org/licenses/>.
 */
require_once dirname(__FILE__) . "/../../../../core/php/core.inc.php";

if (!jeedom::apiAccess(init('apikey'))) {
	connection::failed();
	echo 'Clef API non valide, vous n\'etes pas autorisé à effectuer cette action (jeeZwave)';
	die();
}

if (isset($_GET['test'])) {
	echo 'OK';
	die();
}

$results = json_decode(file_get_contents("php://input"), true);
if (!is_array($results)) {
	die();
}

if (isset($results['device'])) {
	if (!is_array($results['device'])) {
		$results['device'] = array($results['device']);
	}
	foreach ($results['device'] as $node_id => $datas) {
		$eqLogic = openzwave::getEqLogicByLogicalIdAndServerId($node_id, $results['serverId']);
		if (is_object($eqLogic)) {
			if (strpos($eqLogic->getConfiguration('fileconf'), 'fibaro.fgs221.fil.pilote') !== false) {
				foreach ($eqLogic->getCmd('info', '0&&1.0x0', null, true) as $cmd) {
					if ($cmd->getConfiguration('value') == 'pilotWire') {
						$cmd->event($cmd->getPilotWire());
					}
				}
				continue;
			}
			foreach ($datas as $result) {
				if ($eqLogic->getConfiguration('manufacturer_id') == '271' && $eqLogic->getConfiguration('product_type') == '2304' && ($eqLogic->getConfiguration('product_id') == '4096' || $eqLogic->getConfiguration('product_id') == '16384') && $result['CommandClass'] == '0x26') {
					foreach ($eqLogic->getCmd('info', '0.0x26', null, true) as $cmd) {
						if ($cmd->getConfiguration('value') == '#color#') {
							$cmd->event($cmd->getRGBColor());
							break;
						}
					}
				}
				foreach ($eqLogic->getCmd('info', $result['instance'] . '.' . $result['CommandClass'], null, true) as $cmd) {
					if ($cmd->getConfiguration('value') == 'data[' . $result['index'] . '].val') {
						$cmd->handleUpdateValue($result);
					}
				}
			}
		}
	}
}

if (isset($results['controller'])) {
	if (isset($results['controller']['state'])) {
		$jeeNetwork = jeeNetwork::byId($results['serverId']);
		if (is_object($jeeNetwork) || $results['serverId'] == 0) {
			nodejs::pushUpdate('zwave::controller.data.controllerState',
				array(
					'name' => ($results['serverId'] == 0) ? 'local' : $jeeNetwork->getName(),
					'state' => $results['controller']['state']['value'],
					'serverId' => $results['serverId'])
			);
		}
	}
	if (isset($results['controller']['excluded'])) {
		nodejs::pushUpdate('jeedom::alert', array(
			'level' => 'warning',
			'message' => __('Un périphérique Z-Wave est en cours d\'exclusion. Logical ID : ', __FILE__) . $results['controller']['excluded']['value'],
		));
		sleep(2);
		openzwave::syncEqLogicWithOpenZwave($results['serverId'], $results['controller']['excluded']['value']);
	}
	if (isset($results['controller']['included'])) {
		for ($i = 0; $i < 10; $i++) {
			nodejs::pushUpdate('jeedom::alert', array(
				'level' => 'warning',
				'message' => __('Nouveau module Z-Wave détecté. Début de l\'intégration.Pause de ', __FILE__) . (10 - $i) . __(' pour synchronisation avec le module', __FILE__),
			));
			sleep(1);
		}
		nodejs::pushUpdate('jeedom::alert', array(
			'level' => 'warning',
			'message' => __('Inclusion en cours...', __FILE__),
		));
		openzwave::syncEqLogicWithOpenZwave($results['serverId'], $results['controller']['included']['value']);
	}
}

if (isset($results['message'])) {
	log::add('openzwave', 'error', $results['message']);
}
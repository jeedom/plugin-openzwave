<?php

/* This file is part of Plugin openzwave for jeedom.
 *
 * Plugin openzwave for jeedom is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Plugin openzwave for jeedom is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Plugin openzwave for jeedom. If not, see <http://www.gnu.org/licenses/>.
 */
require_once dirname(__FILE__) . "/../../../../core/php/core.inc.php";

if (!jeedom::apiAccess(init('apikey'), 'openzwave') || getClientIp() != '127.0.0.1') {
	echo __('Clef API non valide ou client non autorisé, vous n\'êtes pas autorisé à effectuer cette action', __FILE__);
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
if (isset($results['devices'])) {
	foreach ($results['devices'] as $node_id => $datas) {
		$eqLogic = openzwave::byLogicalId($node_id, 'openzwave');
		if (is_object($eqLogic)) {
			foreach ($datas as $result) {
				foreach ($eqLogic->getCmd('info', $result['instance'] . '.' . $result['CommandClass'] . '.' . $result['index'], null, true) as $cmd) {
					$cmd->event($result['value']);
				}
				if ($result['CommandClass'] == '0x80') {
					$eqLogic->batteryStatus($result['value']);
				}
			}
		}
	}
}

if (isset($results['controller'])) {
	if (isset($results['controller']['state'])) {
		event::add('zwave::controller.data.controllerState',
			array('state' => $results['controller']['state']['value'])
		);
	}
	if (isset($results['controller']['excluded'])) {
		event::add('jeedom::alert', array(
			'level' => 'warning',
			'page' => 'openzwave',
			'message' => __('Un périphérique Z-Wave est en cours d\'exclusion. Logical ID : ', __FILE__) . $results['controller']['excluded']['value'],
		));
		sleep(2);
		openzwave::syncEqLogicWithOpenZwave($results['controller']['excluded']['value'], 1);
	}
	if (isset($results['controller']['included'])) {
		for ($i = 0; $i < 10; $i++) {
			event::add('jeedom::alert', array(
				'level' => 'warning',
				'page' => 'openzwave',
				'message' => __('Nouveau module Z-Wave détecté. Début de l\'intégration. Pause de ', __FILE__) . (10 - $i) . __(' pour synchronisation avec le module', __FILE__),
			));
			sleep(1);
		}
		event::add('jeedom::alert', array(
			'level' => 'warning',
			'page' => 'openzwave',
			'message' => __('Inclusion en cours...', __FILE__),
		));
		openzwave::syncEqLogicWithOpenZwave($results['controller']['included']['value']);
	}
}

if (isset($results['network'])) {
	if (isset($results['network']['state']) && isset($results['network']['state']['value'])) {
		switch ($results['network']['state']['value']) {
			case 0: # STATE_STOPPED = 0
				event::add('jeedom::alert', array(
					'level' => 'danger',
					'page' => 'openzwave',
					'message' => __('Le réseau Z-Wave est arrêté sur le serveur', __FILE__),
				));
				break;
			case 1: # STATE_FAILED = 1
				event::add('jeedom::alert', array(
					'level' => 'danger',
					'page' => 'openzwave',
					'message' => __('Le réseau Z-Wave est en erreur sur le serveur', __FILE__),
				));
				break;
			case 3: # STATE_RESET = 3
				event::add('jeedom::alert', array(
					'level' => 'danger',
					'page' => 'openzwave',
					'message' => __('Le réseau Z-Wave est remis à zéro sur le serveur', __FILE__),
				));
				break;
			case 5: # STATE_STARTED = 5
				event::add('jeedom::alert', array(
					'level' => 'warning',
					'page' => 'openzwave',
					'message' => __('Le réseau Z-Wave est en cours de démarrage sur le serveur', __FILE__),
				));
				break;
			case 7: # STATE_AWAKED = 7
				event::add('jeedom::alert', array(
					'level' => 'warning',
					'page' => 'openzwave',
					'message' => '',
				));
				break;
			case 10: # STATE_READY = 10
				event::add('jeedom::alert', array(
					'level' => 'warning',
					'page' => 'openzwave',
					'message' => '',
				));
				break;
		}
	}
}

if (isset($results['message'])) {
	log::add('openzwave', 'error', $results['message']);
}

if (isset($results['alert'])) {
	switch ($results['alert']['type']) {
		case 'node_dead':
			$message = '';
			$eqLogic = openzwave::byLogicalId($results['alert']['id'], 'openzwave');
			if (is_object($eqLogic)) {
				if ($eqLogic->getIsEnable()) {
					$message = __('Le noeud', __FILE__) . ' ' . $eqLogic->getHumanName() . ' (' . $results['alert']['id'] . ') ' . __('est présumé mort', __FILE__);
				}
			} else {
				$message = __('Le noeud', __FILE__) . ' ' . $results['alert']['id'] . ' ' . __('est présumé mort', __FILE__);
			}
			if ($message != '') {
				log::add('openzwave', 'error', $message, 'node_dead_' . $results['alert']['id']);
			}
			break;
		case 'node_alive':
			message::removeAll('openzwave', 'node_dead_' . $results['alert']['id']);
			break;
	}
}

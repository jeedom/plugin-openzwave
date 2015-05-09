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

try {
	require_once dirname(__FILE__) . '/../../../../core/php/core.inc.php';
	include_file('core', 'authentification', 'php');

	if (!isConnect('admin')) {
		throw new Exception('401 Unauthorized');
	}

	if (init('action') == 'updateOpenzwave') {
		openzwave::updateOpenzwave();
		ajax::success();
	}

	if (init('action') == 'stopDeamon') {
		if (init('type', 'local') == 'remote') {
			$jeeNetwork = jeeNetwork::byId(init('id'));
			if (!is_object($jeeNetwork)) {
				throw new Exception(__('Impossible de trouver l\'esclave : ', __FILE__) . init('id'));
			}
			$jsonrpc = $jeeNetwork->getJsonRpc();
			if (!$jsonrpc->sendRequest('stopDeamon', array('plugin' => 'openzwave'))) {
				throw new Exception($jsonrpc->getError(), $jsonrpc->getErrorCode());
			}
		} else {
			openzwave::stopDeamon();
			if (openzwave::deamonRunning()) {
				throw new Exception(__('Impossible d\'arrêter le démon', __FILE__));
			}
			config::save('port', 'none', 'openzwave');
		}
		ajax::success();
	}

	if (init('action') == 'startDeamon') {
		if (init('type', 'local') == 'remote') {
			$jeeNetwork = jeeNetwork::byId(init('id'));
			if (!is_object($jeeNetwork)) {
				throw new Exception(__('Impossible de trouver l\'esclave : ', __FILE__) . init('id'));
			}
			$jsonrpc = $jeeNetwork->getJsonRpc();
			if (!$jsonrpc->sendRequest('runDeamon', array('plugin' => 'openzwave', 'debug' => init('debug', 0)))) {
				throw new Exception($jsonrpc->getError(), $jsonrpc->getErrorCode());
			}
		} else {
			$port = config::byKey('port', 'openzwave', 'none');
			if ($port == 'none') {
				ajax::success();
			}
			openzwave::stopDeamon();
			if (openzwave::deamonRunning()) {
				throw new Exception(__('Impossible d\'arrêter le démon', __FILE__));
			}
			log::clear('openzwave');
			openzwave::runDeamon(init('debug', 0));
		}
		ajax::success();
	}

	if (init('action') == 'syncEqLogicWithRazberry') {
		foreach (zwave::listServerZwave() as $serverID => $server) {
			if (isset($server['name'])) {
				zwave::syncEqLogicWithRazberry($serverID);
			}
		}
		ajax::success();
	}

	if (init('action') == 'changeIncludeState') {
		zwave::changeIncludeState(init('mode'), init('state'), init('serverID'));
		ajax::success();
	}

	if (init('action') == 'restartDeamon') {
		$cron = cron::byClassAndFunction('zwave', 'pull');
		if (is_object($cron)) {
			$cron->stop();
		}
		ajax::success();
	}

	if (init('action') == 'getModuleInfo') {
		$eqLogic = zwave::byId(init('id'));
		if (!is_object($eqLogic)) {
			throw new Exception(__('Zwave eqLogic non trouvé : ', __FILE__) . init('id'));
		}
		ajax::success($eqLogic->getInfo());
	}

	if (init('action') == 'adminRazberry') {
		ajax::success(zwave::adminRazberry(init('command')));
	}

	if (init('action') == 'getZwaveInfo') {
		ajax::success(zwave::getZwaveInfo(init('path'), init('serverId', 1)));
	}

	if (init('action') == 'callRazberry') {
		ajax::success(zwave::callRazberry(init('call'), init('serverId', 1)));
	}

	if (init('action') == 'listServerZway') {
		ajax::success(zwave::listServerZwave());
	}

	if (init('action') == 'uploadConfZwave') {
		$uploaddir = dirname(__FILE__) . '/../config';
		if (!file_exists($uploaddir)) {
			mkdir($uploaddir);
		}
		$uploaddir .= '/devices/';
		if (!file_exists($uploaddir)) {
			mkdir($uploaddir);
		}
		if (!file_exists($uploaddir)) {
			throw new Exception(__('Répertoire d\'upload non trouvé : ', __FILE__) . $uploaddir);
		}
		if (!isset($_FILES['file'])) {
			throw new Exception(__('Aucun fichier trouvé. Vérifiez le paramètre PHP (post size limit)', __FILE__));
		}
		if (filesize($_FILES['file']['tmp_name']) > 2000000) {
			throw new Exception(__('Le fichier est trop gros (maximum 2Mo)', __FILE__));
		}
		if (!is_json(file_get_contents($_FILES['file']['tmp_name']))) {
			throw new Exception(__('Le fichier json est invalide', __FILE__));
		}
		if (!move_uploaded_file($_FILES['file']['tmp_name'], $uploaddir . '/' . $_FILES['file']['name'])) {
			throw new Exception(__('Impossible de déplacer le fichier temporaire', __FILE__));
		}
		ajax::success();
	}

	throw new Exception('Aucune methode correspondante');
	/*     * *********Catch exeption*************** */
} catch (Exception $e) {
	ajax::error(displayExeption($e), $e->getCode());
}
?>

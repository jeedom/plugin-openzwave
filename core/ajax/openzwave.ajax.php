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
		openzwave::updateOpenzwave(init('mode'));
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

	if (init('action') == 'rewriteNginxAndRestartCron') {
		openzwave::removeNginxRedirection();
		openzwave::listServerZwave();
		$cron = cron::byClassAndFunction('openzwave', 'pull');
		if (is_object($cron)) {
			$cron->stop();
		}
		ajax::success();
	}

	if (init('action') == 'syncEqLogicWithRazberry') {
		foreach (openzwave::listServerZwave() as $serverID => $server) {
			if (isset($server['name'])) {
				openzwave::syncEqLogicWithRazberry($serverID);
			}
		}
		ajax::success();
	}

	if (init('action') == 'sendNoOperation') {
		$eqLogic = openzwave::byId(init('id'));
		if (!is_object($eqLogic)) {
			throw new Exception(__('Zwave eqLogic non trouvé : ', __FILE__) . init('id'));
		}
		ajax::success($eqLogic->sendNoOperation());
	}

	if (init('action') == 'changeIncludeState') {
		openzwave::changeIncludeState(init('mode'), init('state'), init('serverID'));
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
		$eqLogic = openzwave::byId(init('id'));
		if (!is_object($eqLogic)) {
			throw new Exception(__('Zwave eqLogic non trouvé : ', __FILE__) . init('id'));
		}
		ajax::success($eqLogic->getInfo());
	}

	if (init('action') == 'getZwaveInfo') {
		ajax::success(openzwave::getZwaveInfo(init('path'), init('serverId', 1)));
	}

	if (init('action') == 'callRazberry') {
		ajax::success(openzwave::callOpenzwave(init('call'), init('serverId', 1)));
	}

	if (init('action') == 'listServerZwave') {
		ajax::success(openzwave::listServerZwave());
	}

	if (init('action') == 'autoDetectModule') {
		$eqLogic = openzwave::byId(init('id'));
		if (!is_object($eqLogic)) {
			throw new Exception(__('Zwave eqLogic non trouvé : ', __FILE__) . init('id'));
		}
		$eqLogic->createCommand();
		ajax::success();
	}

	if (init('action') == 'checkDoc') {
		try {
			$request_http = new com_http('http://doc.jeedom.fr/fr_FR/' . init('doc'));
			$request_http->setNoReportError(true);
			$result = $request_http->exec(1, 1);
			if (trim($result) != '' && strpos($result, '404 Not Found') === false) {
				ajax::success(1);
			}
		} catch (Exception $e) {

		}
		ajax::success(0);
	}

	if (init('action') == 'migrateZwave') {
		$cmd = 'sudo php ' . dirname(__FILE__) . '/../../script/migrate.php';
		$cmd .= ' >> ' . log::getPathToLog('openzwave_migrate') . ' 2>&1 &';
		exec($cmd);
		ajax::success();
	}

	if (init('action') == 'getAllPossibleConf') {
		$eqLogic = openzwave::byId(init('id'));
		if (!is_object($eqLogic)) {
			ajax::success();
		}
		ajax::success($eqLogic->getConfFilePath(true));
	}

	if (init('action') == 'getConfiguration') {
		if (config::byKey('language', 'core', 'fr_FR') != 'fr_FR') {
			ajax::success();
		}

		$id = init('manufacturer_id') . '.' . init('product_type') . '.' . init('product_id');
		$files = ls(dirname(__FILE__) . '/../config/devices', $id . '_*.json', false, array('files', 'quiet'));
		if (count($files) > 0) {
			$content = file_get_contents(dirname(__FILE__) . '/../config/devices/' . $files[0]);
			if (!is_json($content)) {
				ajax::success();
			}
			ajax::success(json_decode($content, true));
		}
		ajax::success();
	}

	throw new Exception('Aucune methode correspondante');
	/*     * *********Catch exeption*************** */
} catch (Exception $e) {
	ajax::error(displayExeption($e), $e->getCode());
}
?>

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
			if (!$jsonrpc->sendRequest('runDeamon', array('plugin' => 'openzwave'))) {
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
			openzwave::runDeamon();
		}
		ajax::success();
	}

	throw new Exception('Aucune methode correspondante');
	/*     * *********Catch exeption*************** */
} catch (Exception $e) {
	ajax::error(displayExeption($e), $e->getCode());
}
?>

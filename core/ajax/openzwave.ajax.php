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

try {
	require_once dirname(__FILE__) . '/../../../../core/php/core.inc.php';
	include_file('core', 'authentification', 'php');

	if (!isConnect('admin')) {
		throw new Exception('401 Unauthorized');
	}

	ajax::init();

	if (init('action') == 'syncEqLogicWithOpenZwave') {
		openzwave::syncEqLogicWithOpenZwave();
		ajax::success();
	}

	if (init('action') == 'restartDeamon') {
		$cron = cron::byClassAndFunction('zwave', 'pull');
		if (is_object($cron)) {
			$cron->stop();
		}
		ajax::success();
	}

	if (init('action') == 'callRazberry') {
		ajax::success(openzwave::callOpenzwave(init('call')));
	}

	if (init('action') == 'autoDetectModule') {
		$eqLogic = openzwave::byId(init('id'));
		if (!is_object($eqLogic)) {
			throw new Exception(__('Zwave eqLogic non trouvé : ', __FILE__) . init('id'));
		}
		foreach ($eqLogic->getCmd() as $cmd) {
			$cmd->remove();
		}
		$eqLogic->createCommand(true);
		ajax::success();
	}

	if (init('action') == 'migrateZwave') {
		$cmd = 'php ' . dirname(__FILE__) . '/../../script/migrate.php';
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

	if (init('action') == 'applyRecommended') {
		$eqLogic = openzwave::byId(init('id'));
		if (!is_object($eqLogic)) {
			ajax::success();
		}
		ajax::success($eqLogic->applyRecommended());
	}

	if (init('action') == 'getConfiguration') {
		if (init('translation') == 1 && config::byKey('language', 'core', 'fr_FR') != 'fr_FR') {
			ajax::success();
		}
		$id = init('manufacturer_id') . '.' . init('product_type') . '.' . init('product_id');
		$files = ls(dirname(__FILE__) . '/../config/devices', $id . '_*.json', false, array('files', 'quiet'));
		foreach (ls(dirname(__FILE__) . '/../config/devices', '*', false, array('folders', 'quiet')) as $folder) {
			foreach (ls(dirname(__FILE__) . '/../config/devices/' . $folder, $id . '_*.json', false, array('files', 'quiet')) as $file) {
				$files[] = $folder . $file;
			}
		}
		if (count($files) > 0) {
			if (init('json') != '') {
				$content = file_get_contents(dirname(__FILE__) . '/../config/devices/' . init('json'));
				if (!is_json($content)) {
					$content = file_get_contents(dirname(__FILE__) . '/../config/devices/' . $files[0]);
				}
			} else {
				$content = file_get_contents(dirname(__FILE__) . '/../config/devices/' . $files[0]);
			}
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

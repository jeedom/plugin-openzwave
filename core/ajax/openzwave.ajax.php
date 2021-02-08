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

	ajax::init(array('fileupload'));

	if (init('action') == 'syncEqLogicWithOpenZwave') {
		openzwave::syncEqLogicWithOpenZwave();
		ajax::success();
	}
	
	if (init('action') == 'doNetbackup') {
		openzwave::doNetbackup(init('name'),init('port'));
		ajax::success();
	}
	if (init('action') == 'doNetrestore') {
		openzwave::doNetrestore(init('name'),init('port'));
		ajax::success();
	}
	
	if (init('action') == 'listNetbackup') {
		$list = array();
		foreach (ls(dirname(__FILE__) . '/../../data', '*.bin', false, array('files', 'quiet')) as $file) {
			$list[] = array('folder'=>dirname(__FILE__) . '/../../data/'. $file,'name'=>$file);
		}
		ajax::success($list);
	}
	
	if (init('action') == 'deleteNetbackup') {
		$file = dirname(__FILE__) . '/../../data/'.init('backup');
		if (file_exists($file)){
			unlink($file);
		}
		ajax::success();
	}
	
	if (init('action') == 'syncconfOpenzwave') {
		openzwave::syncconfOpenzwave(false);
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
		if (init('createcommand') == 1){
			foreach ($eqLogic->getCmd() as $cmd) {
				$cmd->remove();
			}
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
			ajax::success(str_replace('#language#',config::byKey('language'),json_decode($content, true)));
		}
		ajax::success();
	}
	
	if (init('action') == 'fileupload') {
		$uploaddir = dirname(__FILE__). '/../../data';
		if (!file_exists($uploaddir)) {
			mkdir($uploaddir);
		}
		if (!file_exists($uploaddir)) {
			throw new Exception(__('Répertoire de téléversement non trouvé : ', __FILE__) . $uploaddir);
		}
		if (!isset($_FILES['file'])) {
			throw new Exception(__('Aucun fichier trouvé. Vérifiez le paramètre PHP (post size limit)', __FILE__));
		}
		$extension = strtolower(strrchr($_FILES['file']['name'], '.'));
		if (!in_array($extension, array('.bin'))) {
			throw new Exception('Extension du fichier non valide (autorisé .bin) : ' . $extension);
		}
		if (filesize($_FILES['file']['tmp_name']) > 500000) {
			throw new Exception(__('Le fichier est trop gros (maximum 500ko)', __FILE__));
		}
		if (!move_uploaded_file($_FILES['file']['tmp_name'], $uploaddir . '/' . $_FILES['file']['name'])) {
			throw new Exception(__('Impossible de déplacer le fichier temporaire', __FILE__));
		}
		if (!file_exists($uploaddir . '/' . $_FILES['file']['name'])) {
			throw new Exception(__('Impossible de téléverser le fichier (limite du serveur web ?)', __FILE__));
		}
		ajax::success();
	}

	throw new Exception('Aucune methode correspondante');
	/*     * *********Catch exeption*************** */
} catch (Exception $e) {
	ajax::error(displayException($e), $e->getCode());
}


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

/* * ***************************Includes********************************* */

class openzwave extends eqLogic {
	/*     * *************************Attributs****************************** */
	
	public static $_excludeOnSendPlugin = array('openzwave.log');
	
	/*     * ***********************Methode static*************************** */
	
	public static function callOpenzwave($_url) {
		if (strpos($_url, '?') !== false) {
			$url = 'http://127.0.0.1:' . config::byKey('port_server', 'openzwave', 8083) . '/' . trim($_url, '/') . '&apikey=' . jeedom::getApiKey('openzwave');
		} else {
			$url = 'http://127.0.0.1:' . config::byKey('port_server', 'openzwave', 8083) . '/' . trim($_url, '/') . '?apikey=' . jeedom::getApiKey('openzwave');
		}
		$ch = curl_init();
		curl_setopt_array($ch, array(
			CURLOPT_URL => $url,
			CURLOPT_HEADER => false,
			CURLOPT_RETURNTRANSFER => true,
		));
		$result = curl_exec($ch);
		if (curl_errno($ch)) {
			$curl_error = curl_error($ch);
			curl_close($ch);
			throw new Exception(__('Echec de la requête http : ', __FILE__) . $url . ' Curl error : ' . $curl_error, 404);
		}
		curl_close($ch);
		return is_json($result, $result);
	}
	
	public static function syncEqLogicWithOpenZwave($_logical_id = null, $_exclusion = 0) {
		try {
			$controlerState = self::callOpenzwave('/network?type=info&info=getStatus');
			$state = $controlerState['result']['state'];
		} catch (Exception $e) {
			$state = 10;
		}
		if ($state < 7) {
			event::add('jeedom::alert', array(
				'level' => 'warning',
				'page' => 'openzwave',
				'message' => __('Le contrôleur est occupé veuillez réessayer plus tard', __FILE__),
			));
			return;
		}
		if ($_logical_id !== null && $_logical_id != 0) {
			$eqLogic = self::byLogicalId($_logical_id, 'openzwave');
			if (is_object($eqLogic) && $_exclusion == 1) {
				event::add('jeedom::alert', array(
					'level' => 'warning',
					'page' => 'openzwave',
					'message' => __('Le module ', __FILE__) . $eqLogic->getHumanName() . __(' vient d\'être exclu', __FILE__),
				));
				if (config::byKey('autoRemoveExcludeDevice', 'openzwave') == 1) {
					$eqLogic->remove();
					event::add('zwave::includeDevice', '');
				}
				sleep(10);
				event::add('jeedom::alert', array(
					'level' => 'warning',
					'page' => 'openzwave',
					'message' => '',
				));
				return;
			} elseif ($_exclusion == 1) {
				sleep(3);
				event::add('jeedom::alert', array(
					'level' => 'warning',
					'page' => 'openzwave',
					'message' => __('Le module ', __FILE__) . __(' vient d\'être exclu', __FILE__),
				));
				sleep(3);
				event::add('jeedom::alert', array(
					'level' => 'warning',
					'page' => 'openzwave',
					'message' => '',
				));
				return;
			}
			$result = self::callOpenzwave('/node?node_id=' . $_logical_id . '&type=info&info=all');
			if (count($result) == 0) {
				event::add('jeedom::alert', array(
					'level' => 'warning',
					'message' => __('Aucun module trouvé correspondant à cette ID : ', __FILE__) . $_logical_id,
				));
				return;
			}
			event::add('jeedom::alert', array(
				'level' => 'warning',
				'page' => 'openzwave',
				'message' => __('Nouveau module en cours d\'inclusion', __FILE__),
			));
			$result = $result['result'];
			if (!is_object($eqLogic)) {
				$eqLogic = new openzwave();
			}
			$eqLogic->setEqType_name('openzwave');
			$eqLogic->setIsEnable(1);
			$eqLogic->setLogicalId($_logical_id);
			if (isset($result['data']['product_name']['value']) && trim($result['data']['product_name']['value']) != '') {
				$eqLogic->setName($eqLogic->getLogicalId() . ' ' . $result['data']['product_name']['value']);
			} else {
				$eqLogic->setName('Device ' . $_logical_id);
			}
			$eqLogic->setConfiguration('product_name', $result['data']['product_name']['value']);
			$eqLogic->setConfiguration('manufacturer_id', $result['data']['manufacturerId']['value']);
			$eqLogic->setConfiguration('product_type', $result['data']['manufacturerProductType']['value']);
			$eqLogic->setConfiguration('product_id', $result['data']['manufacturerProductId']['value']);
			$eqLogic->setIsVisible(1);
			$eqLogic->save();
			$eqLogic = openzwave::byId($eqLogic->getId());
			if (config::byKey('auto_applyRecommended', 'openzwave') == 1) {
				$eqLogic->applyRecommended();
			}
			$eqLogic->createCommand(false, $result);
			event::add('zwave::includeDevice', $eqLogic->getId());
			event::add('jeedom::alert', array(
				'level' => 'warning',
				'page' => 'openzwave',
				'message' => '',
			));
			return;
		}
		
		$results = self::callOpenzwave('/network?type=info&info=getNodesList');
		$findDevice = array();
		$include_device = '';
		if (count($results['result']['devices']) < 1) {
			event::add('jeedom::alert', array(
				'level' => 'warning',
				'page' => 'openzwave',
				'message' => __('Le nombre de module trouvé est inférieure à 1', __FILE__),
			));
			return;
		}
		foreach ($results['result']['devices'] as $nodeId => $result) {
			$findDevice[$nodeId] = $nodeId;
			if (!isset($result['product']['is_valid']) || !$result['product']['is_valid']) {
				continue;
			}
			$eqLogic = self::byLogicalId($nodeId, 'openzwave');
			if (!is_object($eqLogic)) {
				$eqLogic = new openzwave();
				$eqLogic->setEqType_name('openzwave');
				$eqLogic->setIsEnable(1);
				$eqLogic->setLogicalId($nodeId);
				if (isset($result['description']['product_name']) && trim($result['description']['product_name']) != '') {
					$eqLogic->setName($eqLogic->getLogicalId() . ' ' . $result['description']['product_name']);
				} else {
					$eqLogic->setName('Device ' . $nodeId);
				}
				$eqLogic->setConfiguration('product_name', $result['description']['product_name']);
				$eqLogic->setConfiguration('manufacturer_id', $result['product']['manufacturer_id']);
				$eqLogic->setConfiguration('product_type', $result['product']['product_type']);
				$eqLogic->setConfiguration('product_id', $result['product']['product_id']);
				$eqLogic->setIsVisible(1);
				$eqLogic->save();
				$eqLogic = openzwave::byId($eqLogic->getId());
				$include_device = $eqLogic->getId();
				$eqLogic->createCommand(false, $result);
			} else {
				if (isset($result['description']['product_name'])) {
					$eqLogic->setConfiguration('product_name', $result['description']['product_name']);
				}
				if (isset($result['product']['is_valid']) && $result['product']['is_valid']) {
					$eqLogic->setConfiguration('manufacturer_id', $result['product']['manufacturer_id']);
					$eqLogic->setConfiguration('product_type', $result['product']['product_type']);
					$eqLogic->setConfiguration('product_id', $result['product']['product_id']);
				}
				$eqLogic->save();
			}
		}
		if (config::byKey('autoRemoveExcludeDevice', 'openzwave') == 1) {
			foreach (self::byType('openzwave') as $eqLogic) {
				if (!isset($findDevice[$eqLogic->getLogicalId()])) {
					$eqLogic->remove();
				}
			}
		}
		event::add('zwave::includeDevice', $include_device);
		event::add('jeedom::alert', array(
			'level' => 'warning',
			'page' => 'openzwave',
			'message' => '',
		));
	}
	
	/*     * ********************************************************************** */
	/*     * ***********************OPENZWAVE MANAGEMENT*************************** */
	
	public static function dependancy_info() {
		$return = array();
		$return['log'] = 'openzwave_update';
		$return['progress_file'] = jeedom::getTmpFolder('openzwave') . '/dependance';
		$return['state'] = (self::compilationOk()) ? 'ok' : 'nok';
		if ($return['state'] == 'ok' && self::getVersion('openzwave') != -1 && version_compare(config::byKey('openzwave_version', 'openzwave'), self::getVersion('openzwave'), '>')) {
			$return['state'] = 'nok';
		}
		return $return;
	}
	
	public static function dependancy_install() {
		config::save('currentOzwVersion', config::byKey('openzwave_version', 'openzwave'), 'openzwave');
		log::remove(__CLASS__ . '_update');
		return array('script' => dirname(__FILE__) . '/../../resources/install_#stype#.sh ' . jeedom::getTmpFolder('openzwave') . '/dependance', 'log' => log::getPathToLog(__CLASS__ . '_update'));
	}
	
	public static function getVersion($_module = 'openzwave') {
		if ($_module == 'openzwave') {
			if (!file_exists('/opt/python-openzwave/openzwave/version')) {
				return config::byKey('currentOzwVersion', 'openzwave');
			}
			$version = file_get_contents('/opt/python-openzwave/openzwave/version');
			if (version_compare($version, config::byKey('currentOzwVersion', 'openzwave'), '>')) {
				config::save('currentOzwVersion', $version, 'openzwave');
			}
			return $version;
		}
	}
	
	public static function compilationOk() {
		if (shell_exec('ls /usr/local/lib/python2.*/dist-packages/openzwave*.egg/libopenzwave.so 2>/dev/null | wc -l') == 0) {
			return false;
		}
		return true;
	}
	
	public static function deamon_info() {
		$return = array();
		$return['state'] = 'nok';
		$pid_file = jeedom::getTmpFolder('openzwave') . '/deamon.pid';
		if (file_exists($pid_file)) {
			if (posix_getsid(trim(file_get_contents($pid_file)))) {
				$return['state'] = 'ok';
			} else {
				shell_exec(system::getCmdSudo() . 'rm -rf ' . $pid_file . ' 2>&1 > /dev/null');
			}
		}
		$return['launchable'] = 'ok';
		$port = config::byKey('port', 'openzwave');
		if ($port != 'auto') {
			$port = jeedom::getUsbMapping($port);
			if (@!file_exists($port)) {
				$return['launchable'] = 'nok';
				$return['launchable_message'] = __('Le port n\'est pas configuré', __FILE__);
			} else {
				exec(system::getCmdSudo() . 'chmod 777 ' . $port . ' > /dev/null 2>&1');
			}
		}
		return $return;
	}
	
	public static function deamon_start($_debug = false) {
		self::deamon_stop();
		$deamon_info = self::deamon_info();
		if ($deamon_info['launchable'] != 'ok') {
			throw new Exception(__('Veuillez vérifier la configuration', __FILE__));
		}
		$port = config::byKey('port', 'openzwave');
		if ($port != 'auto') {
			$port = jeedom::getUsbMapping($port);
		}
		$callback = network::getNetworkAccess('internal', 'proto:127.0.0.1:port:comp') . '/plugins/openzwave/core/php/jeeZwave.php';
		$port_server = config::byKey('port_server', 'openzwave', 8083);
		$openzwave_path = dirname(__FILE__) . '/../../resources';
		$config_path = dirname(__FILE__) . '/../../resources/openzwaved/config';
		$data_path = dirname(__FILE__) . '/../../data';
		if (!file_exists($data_path)) {
			exec('mkdir ' . $data_path . ' && chmod 775 -R ' . $data_path . ' && chown -R www-data:www-data ' . $data_path);
		}
		
		$suppressRefresh = 0;
		if (config::byKey('suppress_refresh', 'openzwave') == 1) {
			$suppressRefresh = 1;
		}
		$disabledNodes = '';
		foreach (self::byType('openzwave') as $eqLogic) {
			if (!$eqLogic->getIsEnable()) {
				$disabledNodes .= $eqLogic->getLogicalId() . ',';
			}
		}
		$disabledNodes = trim($disabledNodes, ',');
		
		$cmd = '/usr/bin/python ' . $openzwave_path . '/openzwaved/openzwaved.py ';
		$cmd .= ' --device ' . $port;
		$cmd .= ' --loglevel ' . log::convertLogLevel(log::getLogLevel('openzwave'));
		$cmd .= ' --port ' . $port_server;
		$cmd .= ' --config_folder ' . $config_path;
		$cmd .= ' --data_folder ' . $data_path;
		$cmd .= ' --callback ' . $callback;
		$cmd .= ' --apikey ' . jeedom::getApiKey('openzwave');
		$cmd .= ' --suppressRefresh ' . $suppressRefresh;
		$cmd .= ' --cycle ' . config::byKey('cycle', 'openzwave');
		$cmd .= ' --pid ' . jeedom::getTmpFolder('openzwave') . '/deamon.pid';
		if ($disabledNodes != '') {
			$cmd .= ' --disabledNodes ' . $disabledNodes;
		}
		
		log::add('openzwave', 'info', 'Lancement démon openzwave : ' . $cmd);
		exec($cmd . ' >> ' . log::getPathToLog('openzwave') . ' 2>&1 &');
		$i = 0;
		while ($i < 30) {
			$deamon_info = self::deamon_info();
			if ($deamon_info['state'] == 'ok') {
				break;
			}
			sleep(1);
			$i++;
		}
		if ($i >= 30) {
			log::add('openzwave', 'error', 'Impossible de lancer le démon openzwave, relancer le démon en debug et vérifiez la log', 'unableStartDeamon');
			return false;
		}
		message::removeAll('openzwave', 'unableStartDeamon');
		log::add('openzwave', 'info', 'Démon openzwave lancé');
	}
	
	public static function deamon_stop() {
		$deamon_info = self::deamon_info();
		if ($deamon_info['state'] == 'ok') {
			try {
				self::callOpenzwave('/network?action=stop&type=action');
			} catch (Exception $e) {
				
			}
		}
		$pid_file = jeedom::getTmpFolder('openzwave') . '/deamon.pid';
		if (file_exists($pid_file)) {
			$pid = intval(trim(file_get_contents($pid_file)));
			system::kill($pid);
		}
		system::kill('openzwaved.py');
		$port = config::byKey('port', 'openzwave');
		if ($port != 'auto') {
			system::fuserk(jeedom::getUsbMapping($port));
		}
		sleep(1);
	}
	
	public static function syncconfOpenzwave($_background = true) {
		log::remove('openzwave_syncconf');
		log::add('openzwave_syncconf', 'info', 'Arrêt du démon en cours');
		self::deamon_stop();
		log::add('openzwave_syncconf', 'info', 'Arrêt du démon fait');
		$cmd = system::getCmdSudo() . ' /bin/bash ' . dirname(__FILE__) . '/../../resources/syncconf.sh >> ' . log::getPathToLog('openzwave_syncconf') . ' 2>&1';
		if ($_background) {
			$cmd .= ' &';
		}
		log::add('openzwave_syncconf', 'info', $cmd);
		shell_exec($cmd);
		self::deamon_start();
	}
	
	/*     * *********************Methode d'instance************************* */
	
	public function loadCmdFromConf($_update = false) {
		if (!is_file(dirname(__FILE__) . '/../config/devices/' . $this->getConfFilePath())) {
			return;
		}
		$device = is_json(file_get_contents(dirname(__FILE__) . '/../config/devices/' . $this->getConfFilePath()), array());
		if (!is_array($device) || !isset($device['commands'])) {
			return true;
		}
		if (isset($device['name']) && !$_update) {
			$this->setName('[' . $this->getLogicalId() . ']' . $device['name']);
		}
		$this->import($device);
		sleep(1);
		event::add('jeedom::alert', array(
			'level' => 'warning',
			'page' => 'openzwave',
			'message' => '',
		));
	}
	
	public function postSave() {
		try {
			$replace = array('/' => '');
			$location = '';
			$objet = $this->getObject();
			if (is_object($objet)) {
				$location = str_replace(array_keys($replace), $replace, $objet->getName());
			} else {
				$location = 'aucun';
			}
			$name = str_replace(array_keys($replace), $replace, $this->getName());
			$humanLocation = urlencode(trim($location));
			$humanName = urlencode(trim($name));
			self::callOpenzwave('/node?node_id=' . $this->getLogicalId() . '&type=setDeviceName&location=' . $humanLocation . '&name=' . $humanName . '&is_enable=' . $this->getIsEnable());
		} catch (Exception $e) {
			
		}
	}
	
	public function getConfFilePath($_all = false) {
		if ($_all) {
			$id = $this->getConfiguration('manufacturer_id') . '.' . $this->getConfiguration('product_type') . '.' . $this->getConfiguration('product_id');
			$return = ls(dirname(__FILE__) . '/../config/devices', $id . '_*.json', false, array('files', 'quiet'));
			foreach (ls(dirname(__FILE__) . '/../config/devices', '*', false, array('folders', 'quiet')) as $folder) {
				foreach (ls(dirname(__FILE__) . '/../config/devices/' . $folder, $id . '_*.json', false, array('files', 'quiet')) as $file) {
					$return[] = $folder . $file;
				}
			}
			return $return;
		}
		if (is_file(dirname(__FILE__) . '/../config/devices/' . $this->getConfiguration('fileconf'))) {
			return $this->getConfiguration('fileconf');
		}
		$id = $this->getConfiguration('manufacturer_id') . '.' . $this->getConfiguration('product_type') . '.' . $this->getConfiguration('product_id');
		$files = ls(dirname(__FILE__) . '/../config/devices', $id . '_*.json', false, array('files', 'quiet'));
		foreach (ls(dirname(__FILE__) . '/../config/devices', '*', false, array('folders', 'quiet')) as $folder) {
			foreach (ls(dirname(__FILE__) . '/../config/devices/' . $folder, $id . '_*.json', false, array('files', 'quiet')) as $file) {
				$files[] = $folder . $file;
			}
		}
		if (count($files) > 0) {
			return $files[0];
		}
		return false;
	}
	
	public function applyRecommended() {
		if (!$this->getIsEnable()) {
			return;
		}
		if (!is_file(dirname(__FILE__) . '/../config/devices/' . $this->getConfFilePath())) {
			return;
		}
		$device = is_json(file_get_contents(dirname(__FILE__) . '/../config/devices/' . $this->getConfFilePath()), array());
		if (!is_array($device) || !isset($device['recommended'])) {
			return true;
		}
		if (isset($device['recommended']['params'])) {
			foreach ($device['recommended']['params'] as $value) {
				openzwave::callOpenzwave('/node?node_id=' . $this->getLogicalId() . '&instance_id=0&cc_id=112&index=' . $value['index'] . '&type=setconfig&value=' . urlencode($value['value']) . '&size=0');
			}
		}
		if (isset($device['recommended']['groups'])) {
			foreach ($device['recommended']['groups'] as $value) {
				if ($value['value'] == 'add') {
					openzwave::callOpenzwave('/node?node_id=' . $this->getLogicalId() . '&type=association&action=add&group=' . $value['index'] . '&target_id=1&instance_id=0');
				} else if ($value['value'] == 'remove') {
					openzwave::callOpenzwave('/node?node_id=' . $this->getLogicalId() . '&type=association&action=remove&group=' . $value['index'] . '&target_id=1&instance_id=0');
				}
			}
		}
		if (isset($device['recommended']['wakeup'])) {
			openzwave::callOpenzwave('/node?node_id=' . $this->getLogicalId() . '&instance_id=0&cc_id=132&index=0&type=setvalue&value=' . $device['recommended']['wakeup']);
		}
		if (isset($device['recommended']['polling'])) {
			$pollinglist = $device['recommended']['polling'];
			foreach ($pollinglist as $value) {
				$instancepolling = $value['instanceId'];
				$indexpolling = 0;
				if (isset($value['index'])) {
					$indexpolling = $value['index'];
				}
				openzwave::callOpenzwave('/node?node_id=' . $this->getLogicalId() . '&instance_id=' . $instancepolling . '&cc_id=' . $value['class'] . '&index=' . $indexpolling . '&type=setPolling&frequency=1');
			}
		}
		if (isset($device['recommended']['needswakeup']) && $device['recommended']['needswakeup'] == true) {
			return "wakeup";
		}
		return;
	}
	
	public function getImgFilePath() {
		$id = $this->getConfiguration('manufacturer_id') . '.' . $this->getConfiguration('product_type') . '.' . $this->getConfiguration('product_id');
		$files = ls(dirname(__FILE__) . '/../config/devices', $id . '_*.{jpg,png}', false, array('files', 'quiet'));
		foreach (ls(dirname(__FILE__) . '/../config/devices', '*', false, array('folders', 'quiet')) as $folder) {
			foreach (ls(dirname(__FILE__) . '/../config/devices/' . $folder, $id . '_*{.jpg,png}', false, array('files', 'quiet')) as $file) {
				$files[] = $folder . $file;
			}
		}
		if (count($files) > 0) {
			return $files[0];
		}
		return false;
	}
	
	public function getImage() {
		return 'plugins/openzwave/core/config/devices/' . $this->getImgFilePath();
	}
	
	public function getAssistantFilePath() {
		$id = $this->getConfiguration('manufacturer_id') . '.' . $this->getConfiguration('product_type') . '.' . $this->getConfiguration('product_id');
		$files = ls(dirname(__FILE__) . '/../config/devices', $id . '_*.php', false, array('files', 'quiet'));
		foreach (ls(dirname(__FILE__) . '/../config/devices', '*', false, array('folders', 'quiet')) as $folder) {
			foreach (ls(dirname(__FILE__) . '/../config/devices/' . $folder, $id . '_*.php', false, array('files', 'quiet')) as $file) {
				$files[] = $folder . $file;
			}
		}
		if (count($files) > 0) {
			return $files[0];
		}
		return false;
	}
	
	public function createCommand($_update = false, $_data = null) {
		$return = array();
		if (!is_numeric($this->getLogicalId())) {
			return;
		}
		if (is_file(dirname(__FILE__) . '/../config/devices/' . $this->getConfFilePath())) {
			$this->loadCmdFromConf($_update);
			return;
		}
		event::add('jeedom::alert', array(
			'level' => 'warning',
			'page' => 'openzwave',
			'message' => __('Création des commandes en mode automatique', __FILE__),
		));
		if ($_data == null) {
			$results = self::callOpenzwave('/node?node_id=' . $this->getLogicalId() . '&type=info&info=all');
		} else {
			$results = $_data;
		}
		if (isset($results['instances']) && is_array($results['instances'])) {
			foreach ($results['instances'] as $instanceID => $instance) {
				if (isset($instance['commandClasses']) && is_array($instance['commandClasses'])) {
					foreach ($instance['commandClasses'] as $ccId => $commandClasses) {
						if (isset($commandClasses['data']) && is_array($commandClasses['data'])) {
							foreach ($commandClasses['data'] as $index => $data) {
								if (isset($data['genre']) && $data['genre'] != 'Config' && $data['genre'] != 'System') {
									$cmd_info = null;
									$cmd = null;
									if (count($results['instances']) > 2) {
										$cmd_name_number = $instanceID + 1;
										$cmd_name = $data['name'] . ' ' . $index . ' ' . $cmd_name_number;
									} else {
										$cmd_name = $data['name'] . ' ' . $index;
									}
									if (strpos($cmd_name, 'Unknown') !== false || strpos($cmd_name, 'Unused') !== false) {
										continue;
									}
									if (!$data['write_only']) {
										if ($data['read_only']) {
											$cmd_info = cmd::byEqLogicIdCmdName($this->getId(), $cmd_name);
										} else {
											$cmd_info = cmd::byEqLogicIdCmdName($this->getId(), 'Info ' . $cmd_name);
										}
										if (!is_object($cmd_info)) {
											$cmd_info = new openzwaveCmd();
										}
										$cmd_info->setType('info');
										$cmd_info->setEqLogic_id($this->getId());
										$cmd_info->setUnite($data['units']);
										if ($data['read_only']) {
											$cmd_info->setName($cmd_name);
										} else {
											$cmd_info->setName('Info ' . $cmd_name);
										}
										$cmd_info->setConfiguration('instance', $instanceID);
										$cmd_info->setConfiguration('class', $ccId);
										$cmd_info->setConfiguration('index', $index);
										switch ($data['type']) {
											case 'bool':
											$cmd_info->setSubType('binary');
											break;
											case 'int':
											$cmd_info->setSubType('numeric');
											$cmd_info->setIsHistorized(1);
											break;
											case 'float':
											$cmd_info->setSubType('numeric');
											$cmd_info->setIsHistorized(1);
											break;
											default:
											$cmd_info->setSubType('string');
											break;
										}
										$cmd_info->save();
									}
									if (!$data['read_only']) {
										switch ($data['type']) {
											case 'bool':
											if ($data['typeZW'] == 'Button') {
												$cmd = cmd::byEqLogicIdCmdName($this->getId(), $cmd_name);
											} else {
												$cmd = cmd::byEqLogicIdCmdName($this->getId(), $cmd_name . ' On');
											}
											if (!is_object($cmd)) {
												$cmd = new openzwaveCmd();
											}
											$cmd->setSubType('other');
											$cmd->setType('action');
											$cmd->setEqLogic_id($this->getId());
											$cmd->setConfiguration('instance', $instanceID);
											$cmd->setConfiguration('class', $ccId);
											$cmd->setConfiguration('index', $index);
											if ($data['typeZW'] == 'Button') {
												$cmd->setName($cmd_name);
												$cmd->setConfiguration('value', 'type=buttonaction&action=press');
											} else {
												$cmd->setName($cmd_name . ' On');
												$cmd->setConfiguration('value', 'type=setvalue&value=255');
											}
											if (is_object($cmd_info)) {
												$cmd->setValue($cmd_info->getId());
												$cmd->setTemplate('dashboard', 'light');
												$cmd->setTemplate('mobile', 'light');
												$cmd_info->setIsVisible(0);
												$cmd_info->save();
												
											}
											$cmd->save();
											if ($data['typeZW'] == 'Button') {
												$cmd = cmd::byEqLogicIdCmdName($this->getId(), $cmd_name . ' Stop');
											} else {
												$cmd = cmd::byEqLogicIdCmdName($this->getId(), $cmd_name . ' Off');
											}
											if (!is_object($cmd)) {
												$cmd = new openzwaveCmd();
											}
											$cmd->setSubType('other');
											$cmd->setType('action');
											$cmd->setEqLogic_id($this->getId());
											$cmd->setConfiguration('instance', $instanceID);
											$cmd->setConfiguration('class', $ccId);
											$cmd->setConfiguration('index', $index);
											if ($data['typeZW'] == 'Button') {
												$cmd->setName($cmd_name . ' Stop');
												$cmd->setIsVisible(0);
												$cmd->setConfiguration('value', 'type=buttonaction&action=release');
											} else {
												$cmd->setName($cmd_name . ' Off');
												$cmd->setConfiguration('value', 'type=setvalue&value=0');
											}
											if (is_object($cmd_info)) {
												$cmd->setValue($cmd_info->getId());
												$cmd->setTemplate('dashboard', 'light');
												$cmd->setTemplate('mobile', 'light');
												$cmd_info->setIsVisible(0);
												$cmd_info->save();
											}
											$cmd->save();
											break;
											case 'int':
											$cmd = cmd::byEqLogicIdCmdName($this->getId(), $cmd_name);
											if (!is_object($cmd)) {
												$cmd = new openzwaveCmd();
											}
											$cmd->setType('action');
											$cmd->setEqLogic_id($this->getId());
											$cmd->setName($cmd_name);
											$cmd->setConfiguration('instance', $instanceID);
											$cmd->setConfiguration('class', $ccId);
											$cmd->setConfiguration('index', $index);
											$cmd->setConfiguration('value', 'type=setvalue&value=#slider#');
											$cmd->setSubType('slider');
											if (is_object($cmd_info)) {
												$cmd->setValue($cmd_info->getId());
												$cmd_info->setIsVisible(0);
												$cmd_info->save();
											}
											$cmd->save();
											break;
											case 'float':
											$cmd = cmd::byEqLogicIdCmdName($this->getId(), $cmd_name);
											if (!is_object($cmd)) {
												$cmd = new openzwaveCmd();
											}
											$cmd->setType('action');
											$cmd->setEqLogic_id($this->getId());
											$cmd->setName($cmd_name);
											$cmd->setConfiguration('instance', $instanceID);
											$cmd->setConfiguration('class', $ccId);
											$cmd->setConfiguration('index', $index);
											$cmd->setConfiguration('value', 'type=setvalue&value=#slider#');
											$cmd->setSubType('slider');
											if (is_object($cmd_info)) {
												$cmd->setValue($cmd_info->getId());
												$cmd_info->setIsVisible(0);
												$cmd_info->save();
											}
											$cmd->save();
											break;
											case 'List':
											foreach (explode(';', $data['data_items']) as $value) {
												if (strpos($value, 'Unknown') !== false || strpos($cmd_name, 'Unused') !== false) {
													continue;
												}
												$cmd = cmd::byEqLogicIdCmdName($this->getId(), $cmd_name . ' ' . $value);
												if (!is_object($cmd)) {
													$cmd = new openzwaveCmd();
												}
												$cmd->setType('action');
												$cmd->setEqLogic_id($this->getId());
												$cmd->setName($cmd_name . ' ' . $value);
												$cmd->setConfiguration('instance', $instanceID);
												$cmd->setConfiguration('class', $ccId);
												$cmd->setConfiguration('index', $index);
												$cmd->setConfiguration('value', 'type=setvalue&value=' . $value);
												$cmd->setSubType('other');
												$cmd->save();
											}
											break;
										}
									}
								}
							}
						}
					}
				}
			}
		}
		event::add('jeedom::alert', array(
			'level' => 'warning',
			'page' => 'openzwave',
			'message' => '',
		));
	}
	
}

class openzwaveCmd extends cmd {
	/*     * ***********************Methode static*************************** */
	
	/*     * *********************Methode d'instance************************* */
	
	public function preSave() {
		if ($this->getConfiguration('instance') === '') {
			$this->setConfiguration('instance', '1');
		}
		if ($this->getConfiguration('index') === '') {
			$this->setConfiguration('index', '0');
		}
		if (strpos($this->getConfiguration('class'), '0x') !== false) {
			$this->setConfiguration('class', hexdec($this->getConfiguration('class')));
		}
		$this->setLogicalId($this->getConfiguration('instance') . '.' . $this->getConfiguration('class') . '.' . $this->getConfiguration('index'));
	}
	
	public function execute($_options = array()) {
		if ($this->getType() != 'action') {
			return;
		}
		$value = $this->getConfiguration('value');
		$request = '/node?node_id=' . $this->getEqLogic()->getLogicalId();
		switch ($this->getSubType()) {
			case 'slider':
			$value = str_replace('#slider#', $_options['slider'], $value);
			break;
			case 'color':
			if ($value == '#color#') {
				$value = str_replace('#color#', str_replace('#', '', $_options['color']), $value);
				return $this->setRGBColor($value);
			}
			if (strlen($_options['color']) == 7) {
				$_options['color'] .= '0000';
			}
			$value = str_replace('#color#', str_replace('#', '%23', $_options['color']), $value);
		}
		$request .= '&instance_id=' . $this->getConfiguration('instance', 1);
		$request .= '&cc_id=' . $this->getConfiguration('class');
		$request .= '&index=' . $this->getConfiguration('index');
		$request .= '&' . str_replace(' ', '%20', $value);
		openzwave::callOpenzwave($request);
	}
	
}

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

/* * ***************************Includes********************************* */

class openzwave extends eqLogic {
	/*     * *************************Attributs****************************** */

	private static $_nbZwaveServer = 1;
	private static $_listZwaveServer = null;
	public static $_excludeOnSendPlugin = array('openzwave.log');

	/*     * ***********************Methode static*************************** */

	public static function sick() {
		foreach (self::listServerZwave() as $serverID => $server) {
			if (isset($server['name'])) {
				try {
					echo "Server name : " . $server['name'] . "\n";
					echo "Server addr : " . $server['addr'] . "\n";
					echo "Port : " . $server['port'] . "\n";
					echo "Test connection to zwave server...";
					self::callOpenzwave('/ZWaveAPI/Run/network.GetControllerStatus()', $serverID);
					echo "OK\n";
				} catch (Exception $e) {
					echo "NOK\n";
					echo "Description : " . $e->getMessage();
					echo "\n";
				}
			}
		}
	}

	public static function listServerZwave() {
		if (self::$_listZwaveServer == null || count(self::$_listZwaveServer) == 0) {
			self::$_listZwaveServer = array();
			if (config::byKey('port', 'openzwave', 'none') != 'none' && config::byKey('allowStartDeamon', 'openzwave', 1) == 1) {
				self::$_listZwaveServer[0] = array(
					'id' => 0,
					'name' => 'Local',
					'addr' => '127.0.0.1',
					'port' => config::byKey('port_server', 'openzwave', 8083),
					'path' => 'plugins/openzwave/core/php/jeeZwaveProxy.php?server_id=0&request=',
				);
			}
			if (config::byKey('jeeNetwork::mode') == 'master') {
				foreach (jeeNetwork::byPlugin('openzwave') as $jeeNetwork) {
					if ($jeeNetwork->configByKey('port', 'openzwave', 'none') != 'none') {
						self::$_listZwaveServer[$jeeNetwork->getId()] = array(
							'id' => $jeeNetwork->getId(),
							'name' => $jeeNetwork->getName(),
							'addr' => $jeeNetwork->getRealIp(),
							'port' => $jeeNetwork->configByKey('port_server', 'openzwave', 8083),
							'path' => 'plugins/openzwave/core/php/jeeZwaveProxy.php?server_id=' . $jeeNetwork->getId() . '&request=',
						);
					}
				}
			}
		}
		return self::$_listZwaveServer;
	}

	public static function callOpenzwave($_url, $_serverId = 0, $_timeout = null, $_noError = false, $_data = null, $_async = false) {
		if (self::$_listZwaveServer == null) {
			self::listServerZwave();
		}
		if (!isset(self::$_listZwaveServer[$_serverId])) {
			self::listServerZwave();
		}
		if (!isset(self::$_listZwaveServer[$_serverId])) {
			return '';
		}
		$url = 'http://' . self::$_listZwaveServer[$_serverId]['addr'] . ':' . self::$_listZwaveServer[$_serverId]['port'] . str_replace(' ', '%20', $_url);
		if ($_async) {
			shell_exec('curl -s -u "token:' . config::byKey('api') . '" -G "' . $url . '" >> /dev/null 2>&1 &');
			return;
		}
		$ch = curl_init();
		curl_setopt_array($ch, array(
			CURLOPT_URL => $url,
			CURLOPT_HEADER => false,
			CURLOPT_RETURNTRANSFER => true,
		));
		if ($_timeout !== null) {
			curl_setopt($ch, CURLOPT_TIMEOUT_MS, $_timeout);
		}
		if ($_data !== null) {
			curl_setopt($ch, CURLOPT_POST, true);
			curl_setopt($ch, CURLOPT_POSTFIELDS, $_data);
		}
		curl_setopt($ch, CURLOPT_USERPWD, 'token:' . config::byKey('api'));
		$result = curl_exec($ch);
		if ($_noError) {
			curl_close($ch);
			return $result;
		}
		if (curl_errno($ch)) {
			$curl_error = curl_error($ch);
			curl_close($ch);
			throw new Exception(__('Echec de la requête http : ', __FILE__) . $url . ' Curl error : ' . $curl_error, 404);
		}
		curl_close($ch);
		if (is_json($result)) {
			return json_decode($result, true);
		} else {
			return $result;
		}
	}

	public static function getEqLogicByLogicalIdAndServerId($_logical_id, $_serverId = 0) {
		$eqLogics = self::byLogicalId($_logical_id, 'openzwave', true);
		if (is_array($eqLogics)) {
			foreach ($eqLogics as $eqLogic) {
				if ($eqLogic->getConfiguration('serverID', 0) == $_serverId) {
					return $eqLogic;
				}
			}
		}
		return null;
	}

	public static function syncEqLogicWithOpenZwave($_serverId = 0, $_logical_id = null) {
		try {
			$controlerState = self::callOpenzwave('/ZWaveAPI/Run/network.GetControllerStatus()', $_serverId);
			$state = $controlerState['result']['data']['networkstate']['value'];
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
			$eqLogic = self::getEqLogicByLogicalIdAndServerId($_logical_id, $_serverId);
			if (is_object($eqLogic)) {
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
			}
			$result = self::callOpenzwave('/ZWaveAPI/Run/devices[' . $_logical_id . ']', $_serverId);
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
			$eqLogic = new eqLogic();
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
			$eqLogic->setConfiguration('serverID', $_serverId);
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

		$results = self::callOpenzwave('/ZWaveAPI/Run/network.GetNodesList()', $_serverId);
		$findDevice = array();
		$include_device = '';
		if (count($results['devices']) < 1) {
			event::add('jeedom::alert', array(
				'level' => 'warning',
				'page' => 'openzwave',
				'message' => __('Le nombre de module trouvé est inférieure à 1', __FILE__),
			));
			return;
		}
		foreach ($results['devices'] as $nodeId => $result) {
			$findDevice[$nodeId] = $nodeId;
			if (!isset($result['product']['is_valid']) || !$result['product']['is_valid']) {
				continue;
			}
			$eqLogic = self::getEqLogicByLogicalIdAndServerId($nodeId, $_serverId);
			if (!is_object($eqLogic)) {
				$eqLogic = new eqLogic();
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
				$eqLogic->setConfiguration('serverID', $_serverId);
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
				if (!isset($findDevice[$eqLogic->getLogicalId()]) && $eqLogic->getConfiguration('serverID') == $_serverId) {
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

	public static function changeIncludeState($_mode, $_state, $_serverId = 0, $_secure = 0) {
		if ($_state == 0) {
			self::callOpenzwave('/ZWaveAPI/Run/controller.CancelCommand()', $_serverId);
			return;
		}
		try {
			$controlerState = self::callOpenzwave('/ZWaveAPI/Run/network.GetControllerStatus()', $_serverId);
			$isBusy = $controlerState['result']['data']['isBusy']['value'];
			$state = $controlerState['result']['data']['networkstate']['value'];
			$controlerState = $controlerState['result']['data']['mode']['value'];
		} catch (Exception $e) {
			$controlerState = 0;
			$state = 10;
		}
		if ($state < 7) {
			throw new Exception(__('Le contrôleur est en cours d\'initialisation veuillez réessayer dans quelques minutes', __FILE__));
		}
		if ($isBusy == 1) {
			throw new Exception(__('Le contrôleur est occupé, si vous êtes en inclusion ou exclusion veuillez d\'abord quitter ce mode', __FILE__));
		}
		if ($controlerState !== 0) {
			throw new Exception(__('Le contrôleur est déjà en inclusion ou exclusion', __FILE__));
		}
		if ($_mode == 1) {
			self::callOpenzwave('/ZWaveAPI/Run/controller.AddNodeToNetwork(' . $_state . ',' . $_secure . ')', $_serverId);
		} else {
			self::callOpenzwave('/ZWaveAPI/Run/controller.RemoveNodeFromNetwork(' . $_state . ')', $_serverId);
		}
	}

	public static function cronDaily() {
		if (config::byKey('jeeNetwork::mode') == 'master') {
			foreach (self::listServerZwave() as $serverID => $server) {
				try {
					$results = self::callOpenzwave('/ZWaveAPI/Run/network.RefreshAllBatteryLevel()', $serverID);
					foreach ($results as $node_id => $value) {
						if ($value['updateTime'] == null) {
							continue;
						}
						$eqLogic = self::getEqLogicByLogicalIdAndServerId($node_id, $serverID);
						$batteryStatusDate = date('Y-m-d H:i:s', $value['updateTime']);
						if (is_file(dirname(__FILE__) . '/../config/devices/' . $eqLogic->getConfFilePath())) {
							$content = file_get_contents(dirname(__FILE__) . '/../config/devices/' . $eqLogic->getConfFilePath());
							if (is_json($content)) {
								$device = json_decode($content, true);
								if (is_array($device) && isset($device['battery_type'])) {
									$eqLogic->setConfiguration('battery_type', $device['battery_type']);
								}
							}
						}
						$eqLogic->batteryStatus($value['value'], $batteryStatusDate);
					}
				} catch (Exception $e) {

				}
			}
			if (config::byKey('auto_health', 'openzwave') == 1 && (date('w') == 1 || date('w') == 4)) {
				sleep(3600);
				try {
					self::callOpenzwave('/ZWaveAPI/Run/controller.HealNetwork()', $serverID);
				} catch (Exception $e) {
				}
			}
			if (config::byKey('auto_updateConf', 'openzwave') == 1) {
				try {
					openzwave::syncconfOpenzwave();
				} catch (Exception $e) {
				}
			}
		}
	}

	public static function cron15() {
		if (config::byKey('jeeNetwork::mode') == 'master' && config::byKey('enabled_sanity_tests', 'openzwave') == 1) {
			foreach (self::listServerZwave() as $serverID => $server) {
				try {
					self::callOpenzwave('/ZWaveAPI/Run/network.PerformSanityChecks()', $serverID, null, false, null, true);
				} catch (Exception $e) {

				}
			}
		}
		$pathlog = log::getPathToLog('openzwaved');
		if (file_exists(log::getPathToLog('openzwaved')) && shell_exec('grep "Not enough space in stream buffer" ' . log::getPathToLog('openzwaved') . ' | wc -l') > 0) {
			self::deamon_stop();
			log::clear('openzwaved');
			try {
				$plugin = plugin::byId('openzwave');
				if (is_object($plugin)) {
					$plugin->deamon_start(false, true);
				}
			} catch (Exception $e) {

			}
		}
	}

	public static function getNetworkNameByServerId($_serverId = '') {
		if ($_serverId == 0) {
			return __('Local', __FILE__);
		} else {
			$jeeNetwork = jeeNetwork::byId($_serverId);
			if (is_object($jeeNetwork)) {
				return $jeeNetwork->getName();
			}
		}
		return $_serverId;
	}

	/*     * ********************************************************************** */
	/*     * ***********************OPENZWAVE MANAGEMENT*************************** */

	public static function dependancy_info() {
		$return = array();
		$return['log'] = 'openzwave_update';
		$return['progress_file'] = '/tmp/compilation_ozw_in_progress';
		$return['state'] = (self::compilationOk()) ? 'ok' : 'nok';
		if ($return['state'] == 'ok' && self::getVersion('openzwave') != -1 && version_compare(config::byKey('openzwave_version', 'openzwave'), self::getVersion('openzwave'), '>')) {
			$return['state'] = 'nok';
		}
		return $return;
	}

	public static function dependancy_install() {
		if (file_exists('/tmp/compilation_ozw_in_progress')) {
			return;
		}
		config::save('currentOzwVersion', config::byKey('openzwave_version', 'openzwave'), 'openzwave');
		log::remove('openzwave_update');
		$cmd = 'sudo /bin/bash ' . dirname(__FILE__) . '/../../resources/install.sh';
		$cmd .= ' >> ' . log::getPathToLog('openzwave_update') . ' 2>&1 &';
		exec($cmd);
	}

	public static function getVersion($_module = 'openzwave') {
		if ($_module == 'openzwave') {
			if (!file_exists('/opt/python-openzwave/openzwave/cpp/src/vers.cpp')) {
				return config::byKey('currentOzwVersion', 'openzwave');
			}
			$result = trim(str_replace(array('"', 'char', 'ozw_version_string', '[]', '=', ';'), '', shell_exec('cat /opt/python-openzwave/openzwave/cpp/src/vers.cpp | grep ozw_version_string')));
			$result = str_replace('-', '.', $result);
			$result = explode('.', str_replace('..', '.', $result));
			if (count($result) > 2) {
				$version = $result[0] . '.' . $result[1] . '.' . $result[2];
			} else {
				return config::byKey('currentOzwVersion', 'openzwave');
			}
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

	public static function syncconfOpenzwave($_background = true) {
		if (config::byKey('jeeNetwork::mode') == 'master') {
			foreach (jeeNetwork::byPlugin('openzwave') as $jeeNetwork) {
				try {
					$jeeNetwork->sendRawRequest('syncconfOpenzwave', array('plugin' => 'openzwave'));
				} catch (Exception $e) {

				}
			}
		}
		log::remove('openzwave_syncconf');
		$cmd = 'sudo /bin/bash ' . dirname(__FILE__) . '/../../resources/syncconf.sh';
		if ($_background) {
			$cmd .= ' >> ' . log::getPathToLog('openzwave_syncconf') . ' 2>&1 &';
		}
		log::add('openzwave_syncconf', 'info', $cmd);
		shell_exec($cmd);
		foreach (self::byType('openzwave') as $eqLogic) {
			$eqLogic->loadCmdFromConf(true);
		}
	}

	public static function deamon_info() {
		$return = array();
		$return['state'] = 'nok';
		$pid_file = '/tmp/openzwaved.pid';
		if (file_exists($pid_file)) {
			if (posix_getsid(trim(file_get_contents($pid_file)))) {
				$return['state'] = 'ok';
			} else {
				shell_exec('sudo rm -rf ' . $pid_file . ' 2>&1 > /dev/null;rm -rf ' . $pid_file . ' 2>&1 > /dev/null;');
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
				exec('sudo chmod 777 ' . $port . ' > /dev/null 2>&1');
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

		if (config::byKey('jeeNetwork::mode') == 'slave') {
			$serverId = config::byKey('jeeNetwork::slave::id');
			$callback = config::byKey('jeeNetwork::master::ip') . '/plugins/openzwave/core/php/jeeZwave.php';
			$apikey = config::byKey('jeeNetwork::master::apikey');
		} else {
			$serverId = 0;
			$callback = network::getNetworkAccess('internal', 'proto:127.0.0.1:port:comp') . '/plugins/openzwave/core/php/jeeZwave.php';
			$apikey = config::byKey('api');
		}
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
			if (!$eqLogic->getIsEnable() and $eqLogic->getConfiguration('serverID', 1) == $serverId) {
				$disabledNodes .= $eqLogic->getLogicalId() . ',';
			}
		}
		$disabledNodes = trim($disabledNodes, ',');

        $assumeAwake = 1;
        if (config::byKey('assume_awake', 'openzwave') == 0) {
            $assumeAwake = 0;
        }

		$cmd = '/usr/bin/python ' . $openzwave_path . '/openzwaved/openzwaved.py ';
		$cmd .= ' --pidfile=/tmp/openzwaved.pid';
		$cmd .= ' --device=' . $port;
		$cmd .= ' --loglevel=' . log::convertLogLevel(log::getLogLevel('openzwave'));
		$cmd .= ' --port=' . $port_server;
		$cmd .= ' --config_folder=' . $config_path;
		$cmd .= ' --data_folder=' . $data_path;
		$cmd .= ' --callback=' . $callback;
		$cmd .= ' --apikey=' . $apikey;
		$cmd .= ' --serverId=' . $serverId;
		$cmd .= ' --suppressRefresh=' . $suppressRefresh;
        $cmd .= ' --assumeAwake=' . $assumeAwake;
		if ($disabledNodes != '') {
			$cmd .= ' --disabledNodes=' . $disabledNodes;
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
				self::callOpenzwave('/ZWaveAPI/Run/network.Stop()', 0, 30000);
			} catch (Exception $e) {

			}
		}
		$pid_file = '/tmp/openzwaved.pid';
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

	/*     * *********************Methode d'instance************************* */

	public function loadCmdFromConf($_update = false) {
		if (!is_file(dirname(__FILE__) . '/../config/devices/' . $this->getConfFilePath())) {
			return;
		}
		$content = file_get_contents(dirname(__FILE__) . '/../config/devices/' . $this->getConfFilePath());
		if (!is_json($content)) {
			return;
		}
		$device = json_decode($content, true);
		if (!is_array($device) || !isset($device['commands'])) {
			return true;
		}
		$cmd_order = 0;
		$link_cmds = array();
		if (isset($device['name']) && !$_update) {
			$this->setName('[' . $this->getLogicalId() . ']' . $device['name']);
		}
		if (isset($device['configuration'])) {
			foreach ($device['configuration'] as $key => $value) {
				try {
					$this->setConfiguration($key, $value);
				} catch (Exception $e) {

				}
			}
		}
		if (isset($device['battery_type'])) {
			$this->setConfiguration('battery_type', $device['battery_type']);
		}
		event::add('jeedom::alert', array(
			'level' => 'warning',
			'page' => 'openzwave',
			'message' => __('Création des commandes à partir d\'une configuration', __FILE__),
		));
		$commands = $device['commands'];
		foreach ($commands as &$command) {
			if (!isset($command['configuration']['instanceId'])) {
				$command['configuration']['instanceId'] = 0;
			}
			if (!isset($command['configuration']['class'])) {
				$command['configuration']['class'] = '';
			}
			foreach ($this->getCmd(null, $command['configuration']['instanceId'] . '.' . $command['configuration']['class'], null, true) as $cmd) {
				if ($cmd->getConfiguration('value') == $command['configuration']['value']) {
					if ($cmd->getDisplay('generic_type') == '' && isset($command['display']['generic_type'])) {
						$cmd->setDisplay('generic_type', $command['display']['generic_type']);
						$cmd->save();
					}
					continue 2;
				}
			}
			try {
				$cmd = new openzwaveCmd();
				$cmd->setOrder($cmd_order);
				$cmd->setEqLogic_id($this->getId());
				utils::a2o($cmd, $command);
				if (isset($command['value'])) {
					$cmd->setValue(null);
				}
				$cmd->save();
				if (isset($command['value'])) {
					$link_cmds[$cmd->getId()] = $command['value'];
				}
				$cmd_order++;
			} catch (Exception $exc) {

			}
		}

		if (count($link_cmds) > 0) {
			foreach ($this->getCmd() as $eqLogic_cmd) {
				foreach ($link_cmds as $cmd_id => $link_cmd) {
					if ($link_cmd == $eqLogic_cmd->getName()) {
						$cmd = cmd::byId($cmd_id);
						if (is_object($cmd)) {
							$cmd->setValue($eqLogic_cmd->getId());
							$cmd->save();
						}
					}
				}
			}
		}
		$this->save();
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
			self::callOpenzwave('/ZWaveAPI/Run/devices[' . $this->getLogicalId() . '].SetDeviceName(' . $humanLocation . ',' . $humanName . ',' . $this->getIsEnable() . ')', $this->getConfiguration('serverID', 1));
		} catch (Exception $e) {

		}
	}

	public function sendNoOperation() {
		return self::callOpenzwave('/ZWaveAPI/Run/devices[' . $this->getLogicalId() . '].TestNode()', $this->getConfiguration('serverID', 1));
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
		$content = file_get_contents(dirname(__FILE__) . '/../config/devices/' . $this->getConfFilePath());
		if (!is_json($content)) {
			return;
		}
		$device = json_decode($content, true);
		if (!is_array($device) || !isset($device['recommended'])) {
			return true;
		}
		if (isset($device['recommended']['params'])) {
			$params = $device['recommended']['params'];
			foreach ($params as $value) {
				openzwave::callOpenzwave('/ZWaveAPI/Run/devices[' . $this->getLogicalId() . '].commandClasses[0x70].Set(' . $value['index'] . ',' . $value['value'] . ',1)', $this->getConfiguration('serverID', 1));
			}
		}
		if (isset($device['recommended']['groups'])) {
			$groups = $device['recommended']['groups'];
			foreach ($groups as $value) {
				if ($value['value'] == 'add') {
					openzwave::callOpenzwave('/ZWaveAPI/Run/devices[' . $this->getLogicalId() . '].instances[0].commandClasses[0x85].Add(' . $value['index'] . ',1)', $this->getConfiguration('serverID', 1));
				} else if ($value['value'] == 'remove') {
					openzwave::callOpenzwave('/ZWaveAPI/Run/devices[' . $this->getLogicalId() . '].instances[0].commandClasses[0x85].Remove(' . $value['index'] . ',1)', $this->getConfiguration('serverID', 1));
				}
			}
		}
		if (isset($device['recommended']['wakeup'])) {
			$wakeup = $device['recommended']['wakeup'];
			openzwave::callOpenzwave('/ZWaveAPI/Run/devices[' . $this->getLogicalId() . '].instances[0].commandClasses[0x84].data[0].Set(' . $wakeup . ')', $this->getConfiguration('serverID', 1));
		}
		if (isset($device['recommended']['polling'])) {
			$pollinglist = $device['recommended']['polling'];
			foreach ($pollinglist as $value) {
				$instancepolling = $value['instanceId'];
				$indexpolling = 0;
				if (isset($value['index'])) {
					$indexpolling = $value['index'];
				}
				$ccpolling = $value['class'];
				openzwave::callOpenzwave('/ZWaveAPI/Run/devices[' . $this->getLogicalId() . '].instances[' . $instancepolling . '].commandClasses[' . $ccpolling . '].data[' . $indexpolling . '].SetPolling(1)', $this->getConfiguration('serverID', 1));
			}
		}
		if (isset($device['recommended']['needswakeup']) && $device['recommended']['needswakeup'] == true) {
			return "wakeup";
		}
		return;
	}

	public function printPending() {
		if ($this->getIsEnable()) {
			$pendingresult = openzwave::callOpenzwave('/ZWaveAPI/Run/devices[' . $this->getLogicalId() . '].GetPendingChanges()', $this->getConfiguration('serverID', 1));
			if (isset($pendingresult['result']) && $pendingresult['result'] != true) {
				return $pendingresult['data'];
			}
		}
		return "ok";
	}

	public function getImgFilePath() {
		$id = $this->getConfiguration('manufacturer_id') . '.' . $this->getConfiguration('product_type') . '.' . $this->getConfiguration('product_id');
		$files = ls(dirname(__FILE__) . '/../config/devices', $id . '_*.jpg', false, array('files', 'quiet'));
		foreach (ls(dirname(__FILE__) . '/../config/devices', '*', false, array('folders', 'quiet')) as $folder) {
			foreach (ls(dirname(__FILE__) . '/../config/devices/' . $folder, $id . '_*.jpg', false, array('files', 'quiet')) as $file) {
				$files[] = $folder . $file;
			}
		}
		if (count($files) > 0) {
			return $files[0];
		}
		return false;
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
			$results = self::callOpenzwave('/ZWaveAPI/Run/devices[' . $this->getLogicalId() . ']', $this->getConfiguration('serverID', 1));
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
										$cmd_info = new openzwaveCmd();
										$cmd_info->setType('info');
										$cmd_info->setEqLogic_id($this->getId());
										$cmd_info->setUnite($data['units']);
										if ($data['read_only']) {
											$cmd_info->setName($cmd_name);
										} else {
											$cmd_info->setName('Info ' . $cmd_name);
										}
										$cmd_info->setConfiguration('instanceId', $instanceID);
										$cmd_info->setConfiguration('class', $ccId);
										$cmd_info->setConfiguration('value', 'data[' . $index . '].val');
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
												$cmd = new openzwaveCmd();
												$cmd->setSubType('other');
												$cmd->setType('action');
												$cmd->setEqLogic_id($this->getId());
												$cmd->setConfiguration('instanceId', $instanceID);
												$cmd->setConfiguration('class', $ccId);
												if ($data['typeZW'] == 'Button') {
													$cmd->setName($cmd_name);
													$cmd->setConfiguration('value', 'data[' . $index . '].PressButton()');
												} else {
													$cmd->setName($cmd_name . ' On');
													$cmd->setConfiguration('value', 'data[' . $index . '].Set(255)');
												}
												if (is_object($cmd_info)) {
													$cmd->setValue($cmd_info->getId());
													$cmd->setTemplate('dashboard', 'light');
													$cmd->setTemplate('mobile', 'light');
													$cmd_info->setIsVisible(0);
													$cmd_info->save();

												}
												$cmd->save();

												$cmd = new openzwaveCmd();
												$cmd->setSubType('other');
												$cmd->setType('action');
												$cmd->setEqLogic_id($this->getId());
												$cmd->setConfiguration('instanceId', $instanceID);
												$cmd->setConfiguration('class', $ccId);
												if ($data['typeZW'] == 'Button') {
													$cmd->setName($cmd_name . ' Stop');
													$cmd->setIsVisible(0);
													$cmd->setConfiguration('value', 'data[' . $index . '].ReleaseButton()');
												} else {
													$cmd->setName($cmd_name . ' Off');
													$cmd->setConfiguration('value', 'data[' . $index . '].Set(0)');
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
												$cmd = new openzwaveCmd();
												$cmd->setType('action');
												$cmd->setEqLogic_id($this->getId());
												$cmd->setName($cmd_name);
												$cmd->setConfiguration('instanceId', $instanceID);
												$cmd->setConfiguration('class', $ccId);
												$cmd->setConfiguration('value', 'data[' . $index . '].Set(#slider#)');
												$cmd->setSubType('slider');
												if (is_object($cmd_info)) {
													$cmd->setValue($cmd_info->getId());
													$cmd_info->setIsVisible(0);
													$cmd_info->save();
												}
												$cmd->save();
												break;
											case 'float':
												$cmd = new openzwaveCmd();
												$cmd->setType('action');
												$cmd->setEqLogic_id($this->getId());
												$cmd->setName($cmd_name);
												$cmd->setConfiguration('instanceId', $instanceID);
												$cmd->setConfiguration('class', $ccId);
												$cmd->setConfiguration('value', 'data[' . $index . '].Set(#slider#)');
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
													$cmd = new openzwaveCmd();
													$cmd->setType('action');
													$cmd->setEqLogic_id($this->getId());
													$cmd->setName($value);
													$cmd->setConfiguration('instanceId', $instanceID);
													$cmd->setConfiguration('class', $ccId);
													$cmd->setConfiguration('value', 'data[' . $index . '].Set(' . $value . ')');
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

	public static function handleResult($_val) {
		if (!is_array($_val)) {
			return '';
		}
		if (!isset($_val['value'])) {
			return '';
		}
		if (!isset($_val['type'])) {
			return $_val['value'];
		}
		$value = $_val['value'];
		switch ($_val['type']) {
			case 'float':
				$value = floatval($value);
				break;
			case 'int':
				$value = intval($value);
				break;
			case 'bool':
				$value = intval($value);
				break;
			case 'binary':
				if (is_array($_val['value'])) {
					$value = '';
					foreach ($_val['value'] as $ascii) {
						if ($ascii != 0) {
							$value .= $ascii;
						}
					}
				}
				break;
		}
		return $value;
	}

	/*     * *********************Methode d'instance************************* */

	public function handleUpdateValue($_result) {
		if (isset($_result['val'])) {
			$value = self::handleResult($_result['val']);
			if (isset($_result['val']['updateTime'])) {
				$this->setCollectDate(date('Y-m-d H:i:s', $_result['val']['updateTime']));
			}
		} else {
			$value = self::handleResult($_result);
			if (isset($_result['updateTime'])) {
				$this->setCollectDate(date('Y-m-d H:i:s', $_result['updateTime']));
			}
		}
		if ($value === '') {
			try {
				$value = $this->execute();
				$this->setCollectDate('');
			} catch (Exception $e) {
				return;
			}
		}
		$this->event($value, 0);
	}

	public function getRGBColor() {
		$eqLogic = $this->getEqLogic();
		$result = openzwave::callOpenzwave('/ZWaveAPI/Run/devices[' . $eqLogic->getLogicalId() . '].GetColor()', $eqLogic->getConfiguration('serverID', 1));
		$r = dechex($result['data']['red']);
		$g = dechex($result['data']['green']);
		$b = dechex($result['data']['blue']);
		$r = (strlen($r) == 1) ? '0' . $r : $r;
		$g = (strlen($g) == 1) ? '0' . $g : $g;
		$b = (strlen($b) == 1) ? '0' . $b : $b;
		return '#' . $r . $g . $b;
	}

	public function setRGBColor($_color) {
		if ($_color == '') {
			throw new Exception('Couleur non définie');
		}
		$eqLogic = $this->getEqLogic();
		$hex = str_replace("#", "", $_color);
		if (strlen($hex) == 3) {
			$r = hexdec(substr($hex, 0, 1) . substr($hex, 0, 1));
			$g = hexdec(substr($hex, 1, 1) . substr($hex, 1, 1));
			$b = hexdec(substr($hex, 2, 1) . substr($hex, 2, 1));
		} else {
			$r = hexdec(substr($hex, 0, 2));
			$g = hexdec(substr($hex, 2, 2));
			$b = hexdec(substr($hex, 4, 2));
		}
		openzwave::callOpenzwave('/ZWaveAPI/Run/devices[' . $eqLogic->getLogicalId() . '].SetColor(' . $r . ',' . $g . ',' . $b . ',0)', $eqLogic->getConfiguration('serverID', 1));
		return true;
	}

	public function getPilotWire() {
		$eqLogic = $this->getEqLogic();
		$request = '/ZWaveAPI/Run/devices[' . $this->getEqLogic()->getLogicalId() . ']';
		$info1 = openzwave::callOpenzwave($request . '.instances[0].commandClasses[0x25].data[0].val', $eqLogic->getConfiguration('serverID', 1));
		$info1 = ($info1 == 'True') ? 1 : 0;
		$info2 = openzwave::callOpenzwave($request . '.instances[1].commandClasses[0x25].data[0].val', $eqLogic->getConfiguration('serverID', 1));
		$info2 = ($info2 == 'True') ? 1 : 0;
		return intval($info1) * 2 + intval($info2);
	}

	public function preSave() {
		if ($this->getConfiguration('instanceId') === '') {
			$this->setConfiguration('instanceId', '0');
		}
		if (strpos($this->getConfiguration('class'), '0x') === false) {
			$this->setConfiguration('class', '0x' . dechex($this->getConfiguration('class')));
		}
		$this->setLogicalId($this->getConfiguration('instanceId') . '.' . $this->getConfiguration('class'));
	}

	public function sendZwaveResquest($_url, $_options = array()) {
		$eqLogic = $this->getEqLogic();
		if ($this->getType() == 'action') {
			openzwave::callOpenzwave($_url, $eqLogic->getConfiguration('serverID', 1));
			return;
		}
		$result = openzwave::callOpenzwave($_url, $eqLogic->getConfiguration('serverID', 1));
		if (is_array($result)) {
			$value = self::handleResult($result);
			if (isset($result['updateTime'])) {
				$this->setCollectDate(date('Y-m-d H:i:s', $result['updateTime']));
			}
		} else {
			$value = $result;
			if ($value === true) {
				return 1;
			}
			if ($value === false) {
				return 0;
			}
			if (is_numeric($value)) {
				return round($value, 2);
			}
		}
		return $value;
	}

	public function postInsert() {
		if ($this->getType() == 'info') {
			$this->event($this->execute());
		}
	}

	public function execute($_options = array()) {
		if ($this->getLogicalId() == 'pilotWire' || $this->getConfiguration('value') == 'pilotWire') {
			return $this->getPilotWire();
		}
		$value = $this->getConfiguration('value');
		$request = '/ZWaveAPI/Run/devices[' . $this->getEqLogic()->getLogicalId() . ']';
		switch ($this->getType()) {
			case 'action':
				switch ($this->getSubType()) {
					case 'slider':
						$value = str_replace('#slider#', $_options['slider'], $value);
						break;
					case 'color':
					case 'color':
						if ($value == '#color#') {
							$value = str_replace('#color#', str_replace('#', '', $_options['color']), $value);
							return $this->setRGBColor($value);
						}
						if (strlen($_options['color']) == 7) {
							$_options['color'] .= '0000';
						}
						$_options['color'] = str_replace('#', '%23', $_options['color']);

						$value = str_replace('#color#', $_options['color'], $value);
				}
				break;
		}
		if (strpos($this->getConfiguration('instanceId'), '&&') !== false || strpos($value, '&&') !== false) {
			$lastInstanceId = $this->getConfiguration('instanceId');
			$instancesId = explode('&&', $this->getConfiguration('instanceId'));
			$lastValue = $value;
			$values = explode('&&', $value);
			$totalRequest = max(count($values), count($instancesId));
			$result = '';
			for ($i = 0; $i < $totalRequest; $i++) {
				if (strpos($values[$i], 'sleep(') !== false) {
					$duration = str_replace(array('sleep(', ')'), '', $values[$i]);
					if ($duration != '' && is_numeric($duration)) {
						sleep($duration);
					}
				} else {
					$request_http = $request;
					$value = $lastValue;
					if (isset($values[$i]) && $values[$i] != '') {
						$value = $values[$i];
						$lastValue = $value;
					}

					$instanceId = $lastInstanceId;
					if (isset($instancesId[$i])) {
						$instanceId = $instancesId[$i];
						$lastInstanceId = $instanceId;
					}
					if ($instanceId != '') {
						$request_http .= '.instances[' . $instanceId . ']';
					} else {
						$request_http .= '.instances[0]';
					}
					$request_http .= '.commandClasses[' . $this->getConfiguration('class') . ']';
					$request_http .= '.' . $value;
					$result .= $this->sendZwaveResquest($request_http, $_options);
				}
			}
			return $result;
		}
		if ($this->getConfiguration('instanceId') != '' && ($this->getConfiguration('class') != '0x70')) {
			$request .= '.instances[' . $this->getConfiguration('instanceId') . ']';
		} else {
			$request .= '.instances[0]';
		}
		$request .= '.commandClasses[' . $this->getConfiguration('class') . ']';
		$request .= '.' . str_replace(' ', '%20', str_replace(',', '%2C', $value));
		return $this->sendZwaveResquest($request, $_options);
	}

}

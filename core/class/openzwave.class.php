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

	private static $_curl = null;
	private static $_nbZwaveServer = 1;
	private static $_listZwaveServer = null;

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

	public static function listServerZwave($_autofix = true) {
		if (self::$_listZwaveServer == null || count(self::$_listZwaveServer) == 0) {
			self::$_listZwaveServer = array();
			if (config::byKey('port', 'openzwave', 'none') != 'none' && config::byKey('allowStartDeamon', 'openzwave', 1) == 1) {
				self::$_listZwaveServer[0] = array(
					'id' => 0,
					'name' => 'Local',
					'addr' => '127.0.0.1',
					'port' => config::byKey('port_server', 'openzwave', 8083),
				);
				if ($_autofix & config::byKey('urlPath0', 'openzwave') == '') {
					self::updateNginxRedirection();
				}
				self::$_listZwaveServer[0]['path'] = '/' . config::byKey('urlPath0', 'openzwave');
			}
			if (config::byKey('jeeNetwork::mode') == 'master') {
				foreach (jeeNetwork::byPlugin('openzwave') as $jeeNetwork) {
					if ($jeeNetwork->configByKey('port', 'openzwave', 'none') != 'none') {
						self::$_listZwaveServer[$jeeNetwork->getId()] = array(
							'id' => $jeeNetwork->getId(),
							'name' => $jeeNetwork->getName(),
							'addr' => $jeeNetwork->getRealIp(),
							'port' => $jeeNetwork->configByKey('port_server', 'openzwave', 8083),
						);
						if ($_autofix && config::byKey('urlPath' . $jeeNetwork->getId(), 'openzwave') == '') {
							self::updateNginxRedirection();
						}
						self::$_listZwaveServer[$jeeNetwork->getId()]['path'] = '/' . config::byKey('urlPath' . $jeeNetwork->getId(), 'openzwave');
					}
				}
			}
		}
		return self::$_listZwaveServer;
	}

	public static function health() {
		$return = array();
		$demon_state = self::deamonRunning();
		$return[] = array(
			'test' => __('Démon local', __FILE__),
			'result' => ($demon_state) ? __('OK', __FILE__) : __('NOK', __FILE__),
			'advice' => ($demon_state) ? '' : __('Peut être normal si vous êtes en déporté', __FILE__),
			'state' => $demon_state,
		);
		$version = openzwave::getVersion('openzwave');
		$return[] = array(
			'test' => __('Version d\'openzwave', __FILE__),
			'result' => $version,
			'advice' => ($demon_state) ? '' : __('Mettez à jour les dépendances', __FILE__),
			'state' => version_compare(config::byKey('openzwave_version', 'openzwave'), $version, '<='),
		);
		$compilation = openzwave::compilationOk();
		$return[] = array(
			'test' => __('Compilation', __FILE__),
			'result' => ($compilation) ? __('OK', __FILE__) : __('NOK', __FILE__),
			'advice' => ($compilation) ? '' : __('Mettez à jour les dépendances', __FILE__),
			'state' => $compilation,
		);
		if (config::byKey('jeeNetwork::mode') == 'master') {
			foreach (jeeNetwork::byPlugin('openzwave') as $jeeNetwork) {
				try {
					$demon_state = $jeeNetwork->sendRawRequest('deamonRunning', array('plugin' => 'openzwave'));
				} catch (Exception $e) {
					$demon_state = false;
				}
				$return[] = array(
					'test' => __('Démon sur ', __FILE__) . $jeeNetwork->getName(),
					'result' => ($demon_state) ? __('OK', __FILE__) : __('NOK', __FILE__),
					'advice' => '',
					'state' => $demon_state,
				);
				$version = $jeeNetwork->sendRawRequest('getVersion', array('plugin' => 'openzwave', 'module' => 'openzwave'));
				$return[] = array(
					'test' => __('Version d\'openzwave sur ', __FILE__) . $jeeNetwork->getName(),
					'result' => $version,
					'advice' => ($demon_state) ? '' : __('Mettez à jour les dépendances', __FILE__),
					'state' => version_compare(config::byKey('openzwave_version', 'openzwave'), $version, '<='),
				);
				$compilation = $jeeNetwork->sendRawRequest('compilationOk', array('plugin' => 'openzwave'));
				$return[] = array(
					'test' => __('Compilation sur', __FILE__) . $jeeNetwork->getName(),
					'result' => ($compilation) ? __('OK', __FILE__) : __('NOK', __FILE__),
					'advice' => ($compilation) ? '' : __('Mettez à jour les dépendances', __FILE__),
					'state' => $compilation,
				);
			}
		}
		return $return;
	}

	public static function updateNginxRedirection() {
		foreach (self::listServerZwave(false) as $zwave) {
			if (trim($zwave['addr']) == '' || trim($zwave['port']) == '') {
				continue;
			}
			$urlPath = config::byKey('urlPath' . $zwave['id'], 'openzwave');
			if ($urlPath == '') {
				$urlPath = 'openzwave_' . $zwave['id'] . '_' . config::genKey(30);
				config::save('urlPath' . $zwave['id'], $urlPath, 'openzwave');
			}
			$rules = array(
				"location /" . $urlPath . "/ {\n" .
				"proxy_pass http://" . $zwave['addr'] . ":" . $zwave['port'] . "/;\n" .
				"proxy_redirect off;\n" .
				"proxy_set_header Host \$host:\$server_port;\n" .
				"proxy_set_header X-Real-IP \$remote_addr;\n" .
				"}",
			);
			network::nginx_saveRule($rules);
		}
	}

	public static function removeNginxRedirection() {
		foreach (self::listServerZwave(false) as $zwave) {
			$urlPath = config::byKey('urlPath' . $zwave['id'], 'openzwave');
			$rules = array(
				"location /" . $urlPath . "/ {\n",
			);
			network::nginx_removeRule($rules);
			config::save('urlPath' . $zwave['id'], '', 'openzwave');
		}
	}

	public static function callOpenzwave($_url, $_serverId = 0, $_timeout = null, $_noError = false) {
		if (self::$_curl == null) {
			self::$_curl = curl_init();
		}
		if (self::$_listZwaveServer == null) {
			self::listServerZwave();
		}
		$url = 'http://' . self::$_listZwaveServer[$_serverId]['addr'] . ':' . self::$_listZwaveServer[$_serverId]['port'] . $_url;
		$ch = self::$_curl;
		curl_setopt_array($ch, array(
			CURLOPT_URL => $url,
			CURLOPT_HEADER => false,
			CURLOPT_RETURNTRANSFER => true,
		));
		if ($_timeout !== null) {
			curl_setopt($ch, CURLOPT_TIMEOUT_MS, $_timeout);
		}
		$result = curl_exec($ch);
		if ($_noError) {
			return $result;
		}
		if (curl_errno($ch)) {
			$curl_error = curl_error($ch);
			throw new Exception(__('Echec de la requete http : ', __FILE__) . $url . ' Curl error : ' . $curl_error, 404);
		}
		if (is_json($result)) {
			return json_decode($result, true);
		} else {
			return $result;
		}
	}

	public static function backup($_path) {
		exec('cp /opt/python-openzwave/zwcfg_*.xml ' . $_path);
		if (file_exists('/opt/python-openzwave/xml_backups')) {
			exec('cp -R /opt/python-openzwave/xml_backups ' . $_path);
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
			nodejs::pushUpdate('jeedom::alert', array(
				'level' => 'warning',
				'message' => __('Le controleur est occupé veuillez réessayer plus tard', __FILE__),
			));
			return;
		}
		if ($_logical_id !== null) {
			$eqLogic = self::getEqLogicByLogicalIdAndServerId($_logical_id, $_serverId);
			if (is_object($eqLogic)) {
				if (config::byKey('autoRemoveExcludeDevice', 'openzwave') == 1) {
					$eqLogic->remove();
					nodejs::pushUpdate('zwave::includeDevice', '');
				}
				nodejs::pushUpdate('jeedom::alert', array(
					'level' => 'warning',
					'message' => '',
				));
				return;
			}
			$result = self::callOpenzwave('/ZWaveAPI/Run/devices[' . $_logical_id . ']', $_serverId);
			if (count($result) == 0) {
				nodejs::pushUpdate('jeedom::alert', array(
					'level' => 'danger',
					'message' => __('Aucun module trouvé correspondant à cette ID : ', __FILE__) . $_logical_id,
				));
				return;
			}
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
			$include_device = $eqLogic->getId();
			$eqLogic->createCommand(false, $result);
			nodejs::pushUpdate('zwave::includeDevice', $include_device);
			nodejs::pushUpdate('jeedom::alert', array(
				'level' => 'warning',
				'message' => '',
			));
			return;
		}

		$results = self::callOpenzwave('/ZWaveAPI/Run/network.GetNodesList()', $_serverId);
		$findDevice = array();
		$include_device = '';
		if (count($results['devices']) < 2) {
			nodejs::pushUpdate('jeedom::alert', array(
				'level' => 'warning',
				'message' => __('Le nombre de module trouvé est inférieure à 2', __FILE__),
			));
			return;
		}
		foreach ($results['devices'] as $nodeId => $result) {
			$findDevice[$nodeId] = $nodeId;
			if (isset($result['description']['is_static_controller']) && $result['description']['is_static_controller']) {
				continue;
			}
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
		nodejs::pushUpdate('zwave::includeDevice', $include_device);
		nodejs::pushUpdate('jeedom::alert', array(
			'level' => 'warning',
			'message' => '',
		));
	}

	public static function changeIncludeState($_mode, $_state, $_serverId = 0) {
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
			throw new Exception(__('Le controleur est en cours d\'initialisation veuillez reesayer dans quelques minutes', __FILE__));
		}
		if ($isBusy == 1) {
			throw new Exception(__('Le controleur est occupé, si vous etes en inclusion ou exclusion veuillez d\'abord quitter ce mode', __FILE__));
		}
		if ($controlerState !== 0) {
			throw new Exception(__('Le controleur est deja en inclusion ou exclusion', __FILE__));
		}
		if ($_mode == 1) {
			self::callOpenzwave('/ZWaveAPI/Run/controller.AddNodeToNetwork(' . $_state . ',0)', $_serverId);
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
						$batteryStatusDate = date('Y-m-d H:i:s');
						$eqLogic = self::getEqLogicByLogicalIdAndServerId($node_id, $serverID);
						if (is_object($eqLogic) && $eqLogic->getConfiguration('noBatterieCheck', 0) != 1) {
							if ($value['updateTime'] !== null) {
								$batteryStatusDate = date('Y-m-d H:i:s', $value['updateTime']);
							}
							$eqLogic->batteryStatus($value['value'], $batteryStatusDate);
						}
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
		}
	}

/*     * ********************************************************************** */
/*     * ***********************OPENZWAVE MANAGEMENT*************************** */

	public static function getVersion($_module) {
		if ($_module == 'openzwave') {
			if (!file_exists('/opt/python-openzwave/openzwave/cpp/src/vers.cpp')) {
				return config::byKey('openzwave_version', 'openzwave');
			}
			$result = trim(str_replace(array('"', 'char', 'ozw_version_string', '[]', '=', ';'), '', shell_exec('cat /opt/python-openzwave/openzwave/cpp/src/vers.cpp | grep ozw_version_string')));
			$result = str_replace('-', '.', $result);
			$result = explode('.', str_replace('..', '.', $result));
			if (count($result) > 2) {
				return $result[0] . '.' . $result[1] . '.' . $result[2];
			}
		}
	}

	public static function compilationOk() {
		if (shell_exec('ls /usr/local/lib/python2.*/dist-packages/openzwave*.egg/libopenzwave.so | wc -l') == 0) {
			return false;
		}
		return true;
	}

	public static function updateOpenzwave($_background = true) {
		try {
			self::stopDeamon();
		} catch (Exception $e) {

		}
		log::remove('openzwave_update');
		$cmd = 'sudo /bin/bash ' . dirname(__FILE__) . '/../../ressources/install.sh';
		if ($_background) {
			$cmd .= ' >> ' . log::getPathToLog('openzwave_update') . ' 2>&1 &';
		}
		exec($cmd);
	}

	public static function cron15() {
		if (config::byKey('allowStartDeamon', 'openzwave', 1) == 1 && config::byKey('port', 'openzwave', 'none') != 'none' && !self::deamonRunning()) {
			self::runDeamon();
		}
	}

	public static function start() {
		if (config::byKey('allowStartDeamon', 'openzwave', 1) == 1 && config::byKey('port', 'openzwave', 'none') != 'none' && !self::deamonRunning()) {
			$continue = 0;
			while ($continue < 4) {
				self::runDeamon();
				if (!self::deamonRunning()) {
					$continue++;
					sleep(60);
				} else {
					$continue = 99;
				}
			}
		}
	}

	public static function runDeamon($_debug = false) {
		if (config::byKey('allowStartDeamon', 'openzwave', 1) == 0) {
			return;
		}
		try {
			self::stop();
			self::stopDeamon();
		} catch (Exception $e) {

		}
		log::add('openzwave', 'info', 'Lancement du démon openzwave');
		$port = config::byKey('port', 'openzwave');
		if ($port != 'auto') {
			$port = jeedom::getUsbMapping($port, true);
			if (@!file_exists($port)) {
				throw new Exception(__('Le port : ', __FILE__) . print_r($port, true) . __(' n\'existe pas', __FILE__));
			}
			exec('sudo chmod 777 ' . $port . ' > /dev/null 2>&1');
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
		$openzwave_path = realpath(dirname(__FILE__) . '/../../ressources/zwaveserver');
		$config_path = realpath(dirname(__FILE__) . '/../../ressources/openzwave/config');
		$log = ($_debug) ? 'Debug' : 'Info';
		$cmd = '/usr/bin/python ' . $openzwave_path . '/openZWave.py ';
		$cmd .= ' --pidfile=/tmp/openzwave.pid';
		$cmd .= ' --device=' . $port;
		$cmd .= ' --log=' . $log;
		$cmd .= ' --port=' . $port_server;
		$cmd .= ' --config=' . $config_path;
		$cmd .= ' --callback=' . $callback;
		$cmd .= ' --apikey=' . $apikey;
		$cmd .= ' --serverId=' . $serverId;

		log::add('openzwave', 'info', 'Lancement démon openzwave : ' . $cmd);
		$result = exec($cmd . ' >> ' . log::getPathToLog('openzwave') . ' 2>&1 &');
		if (strpos(strtolower($result), 'error') !== false || strpos(strtolower($result), 'traceback') !== false) {
			log::add('openzwave', 'error', $result);
			return false;
		}
		$i = 0;
		while ($i < 30) {
			if (self::deamonRunning()) {
				break;
			}
			sleep(1);
			$i++;
		}
		if ($i >= 10) {
			log::add('openzwave', 'error', 'Impossible de lancer le démon openzwave, vérifiez le port', 'unableStartDeamon');
			return false;
		}
		message::removeAll('openzwave', 'unableStartDeamon');
		log::add('openzwave', 'info', 'Démon openzwave lancé');
	}

	public static function deamonRunning() {
		$pid_file = '/tmp/openzwave.pid';
		if (!file_exists($pid_file)) {
			return false;
		}
		$pid = trim(file_get_contents($pid_file));
		if (posix_getsid($pid)) {
			return true;
		}
		unlink($pid_file);
		return false;
	}

	public static function stop() {
		if (self::deamonRunning()) {
			try {
				self::callOpenzwave('/ZWaveAPI/Run/network.Stop()');
			} catch (Exception $e) {

			}
		}
	}

	public static function stopDeamon() {
		self::stop();
		$pid_file = '/tmp/openzwave.pid';
		if (file_exists($pid_file)) {
			$pid = intval(trim(file_get_contents($pid_file)));
			posix_kill($pid, 15);
			if (self::deamonRunning()) {
				sleep(1);
				posix_kill($pid, 9);
			}
			if (self::deamonRunning()) {
				sleep(1);
				exec('kill -9 ' . $pid . ' > /dev/null 2>&1');
			}
		}
		exec('fuser -k ' . config::byKey('port_server', 'openzwave', 8083) . '/tcp > /dev/null 2>&1');
		exec('sudo fuser -k ' . config::byKey('port_server', 'openzwave', 8083) . '/tcp > /dev/null 2>&1');
		exec("ps aux | grep -ie 'openZWave.py' | awk '{print $2}' | xargs kill -9 > /dev/null 2>&1");
		return self::deamonRunning();
	}

	/*     * *********************Methode d'instance************************* */

	public function ping() {
		return true;
	}

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
		nodejs::pushUpdate('jeedom::alert', array(
			'level' => 'warning',
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

		nodejs::pushUpdate('jeedom::alert', array(
			'level' => 'warning',
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
			self::callOpenzwave('/ZWaveAPI/Run/devices[' . $this->getLogicalId() . '].SetDeviceName(' . $humanLocation . ',' . $humanName . ')', $this->getConfiguration('serverID', 1));
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
		nodejs::pushUpdate('jeedom::alert', array(
			'level' => 'warning',
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
		nodejs::pushUpdate('jeedom::alert', array(
			'level' => 'warning',
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
				$value = round(floatval($value), 2);
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
		log::add('openzwave', 'debug', '/ZWaveAPI/Run/devices[' . $eqLogic->getLogicalId() . '].SetColor(' . $r . ',' . $g . ',' . $b . ',0)');
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
		$this->setEventOnly(1);
	}

	public function sendZwaveResquest($_url, $_options = array()) {
		$eqLogic = $this->getEqLogic();
		if ($this->getType() == 'action') {
			if (isset($_options['speedAndNoErrorReport']) && $_options['speedAndNoErrorReport'] == true) {
				openzwave::callOpenzwave($_url, $eqLogic->getConfiguration('serverID', 1), 1, true);
			} else {
				openzwave::callOpenzwave($_url, $eqLogic->getConfiguration('serverID', 1));
			}
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
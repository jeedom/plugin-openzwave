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
	private static $_zwaveUpdatetime = array();

	/*     * ***********************Methode static*************************** */

	public static function sick() {
		foreach (self::listServerZwave() as $serverID => $server) {
			if (isset($server['name'])) {
				try {
					echo "Server name : " . $server['name'] . "\n";
					echo "Server addr : " . $server['addr'] . "\n";
					echo "Port : " . $server['port'] . "\n";
					echo "Test connection to zwave server...";
					self::callRazberry('/ZWaveAPI/Data/0', $serverID);
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
		if (self::$_listZwaveServer == null) {
			self::$_listZwaveServer = array();
			if (config::byKey('port', 'openzwave', 'none') != 'none') {
				self::$_listZwaveServer[0] = array(
					'id' => 0,
					'name' => 'Local',
					'addr' => '127.0.0.1',
					'port' => config::byKey('port_server', 'openzwave', 8083),
					'path' => network::getNetworkAccess('external', 'prot:ip:port') . '/' . config::byKey('urlPath0', 'openzwave'),
				);
				if (self::$_listZwaveServer[0]['path'] == '') {
					self::updateNginxRedirection();
				}
				self::$_listZwaveServer[0]['path'] = network::getNetworkAccess('auto', 'prot:ip:port') . '/' . config::byKey('urlPath0', 'openzwave');
			}
			if (config::byKey('jeeNetwork::mode') == 'master') {
				foreach (jeeNetwork::byPlugin('openzwave') as $jeeNetwork) {
					self::$_listZwaveServer[$jeeNetwork->getId()] = array(
						'id' => $jeeNetwork->getId(),
						'name' => $jeeNetwork->getName(),
						'addr' => $jeeNetwork->getRealIp(),
						'port' => $jeeNetwork->configByKey('port_server', 'openzwave', 8083),
						'path' => network::getNetworkAccess('auto', 'prot:ip:port') . '/' . config::byKey('urlPath' . $jeeNetwork->getId(), 'openzwave'),
					);
					if (self::$_listZwaveServer[$jeeNetwork->getId()]['path'] == '') {
						self::updateNginxRedirection();
					}
					self::$_listZwaveServer[$jeeNetwork->getId()]['path'] = network::getNetworkAccess('external', 'prot:ip:port') . '/' . config::byKey('urlPath' . $jeeNetwork->getId(), 'openzwave');
				}

			}

		}
		return self::$_listZwaveServer;
	}

	public static function updateNginxRedirection() {
		foreach (self::listServerZwave() as $zwave) {
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

	public static function callRazberry($_url, $_serverId = 0) {
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
		$result = curl_exec($ch);
		if (curl_errno($ch)) {
			$curl_error = curl_error($ch);
			throw new Exception(__('Echec de la requete http : ', __FILE__) . $url . ' Curl error : ' . $curl_error, 404);
		}
		if (strpos($result, 'Error 500: Server Error') === 0 || strpos($result, 'Error 500: Internal Server Error') === 0) {
			if (strpos($result, 'Code took too long to return result') === false) {
				throw new Exception('Echec de la commande : ' . $_url . '. Erreur : ' . $result, 500);
			}
		}
		if (is_json($result)) {
			return json_decode($result, true);
		} else {
			return $result;
		}
	}

	public static function getZwaveInfo($_path, $_serverId = 0) {
		$results = self::callRazberry('/ZWaveAPI/Data/0', $_serverId);
		if ($_path != '') {
			$paths = explode('::', $_path);
			foreach ($paths as $path) {
				if (isset($results[$path])) {
					$results = $results[$path];
				} else {
					return null;
				}
			}
		}
		return $results;
	}

	public static function pull() {
		foreach (self::listServerZwave() as $serverID => $server) {
			if (!isset($server['name'])) {
				continue;
			}
			if (!isset(self::$_zwaveUpdatetime[$serverID])) {
				$cache = cache::byKey('openzwave::lastUpdate' . $serverID);
				self::$_zwaveUpdatetime[$serverID] = $cache->getValue(0);
			}
			$results = self::callRazberry('/ZWaveAPI/Data/' . self::$_zwaveUpdatetime[$serverID], $serverID);
			if (!is_array($results)) {
				continue;
			}
			foreach ($results as $key => $result) {
				if ($key == 'controller.data.controllerState') {
					nodejs::pushUpdate('zwave::' . $key, array('name' => $server['name'], 'state' => $result['value'], 'serverId' => $serverID));
				} else if ($key == 'controller.data.lastExcludedDevice') {
					if ($result['value'] != null) {
						nodejs::pushUpdate('zwave::' . $key, array('name' => $server['name'], 'state' => 0, 'serverId' => $serverID));
						nodejs::pushUpdate('jeedom::alert', array(
							'level' => 'warning',
							'message' => __('Un périphérique Z-Wave vient est en cours d\'exclusion. Logical ID : ', __FILE__) . $result['value'],
						));
						sleep(5);
						self::syncEqLogicWithRazberry($serverID);
						nodejs::pushUpdate('jeedom::alert', array(
							'level' => 'warning',
							'message' => '',
						));
					}
				}if ($key == 'controller') {
					if (isset($result['controllerState'])) {
						nodejs::pushUpdate('zwave::controller.data.controllerState', array('name' => $server['name'], 'state' => $result['controllerState']['value'], 'serverId' => $serverID));
					}
				} else if ($key == 'controller.data.lastIncludedDevice') {
					if ($result['value'] != null) {
						nodejs::pushUpdate('zwave::' . $key, array('name' => $server['name'], 'state' => 0, 'serverId' => $serverID));
						$eqLogic = self::getEqLogicByLogicalIdAndServerId($result['value'], $serverID);
						if (!is_object($eqLogic)) {
							nodejs::pushUpdate('jeedom::alert', array(
								'level' => 'warning',
								'message' => __('Nouveau module Z-Wave détecté. Début de l\'intégration', __FILE__),
							));
							sleep(5);
							for ($i = 0; $i < 30; $i++) {
								nodejs::pushUpdate('jeedom::alert', array(
									'level' => 'warning',
									'message' => __('Pause de ', __FILE__) . (30 - $i) . __(' pour synchronisation avec le module', __FILE__),
								));
								sleep(1);
							}
							nodejs::pushUpdate('jeedom::alert', array(
								'level' => 'warning',
								'message' => __('Inclusion en cours...', __FILE__),
							));
							self::syncEqLogicWithRazberry($serverID);
						}
					}
				} else {
					$explodeKey = explode('.', $key);
					if (!isset($explodeKey[1])) {
						continue;
					}
					if ($explodeKey[1] == 1) {
						if (isset($results['devices.1.instances.0.commandClasses.' . $explodeKey[5] . '.data.srcNodeId'])) {
							$explodeKey[1] = $results['devices.1.instances.0.commandClasses.' . $explodeKey[5] . '.data.srcNodeId']['value'];
							$eqLogic = self::getEqLogicByLogicalIdAndServerId($results['devices.1.instances.0.commandClasses.' . $explodeKey[5] . '.data.srcNodeId']['value'], $serverID);
							if (is_object($eqLogic)) {
								foreach ($eqLogic->getCmd('info') as $cmd) {
									if ($cmd->getConfiguration('instanceId') == $explodeKey[3]) {
										try {
											$cmd->forceUpdate();
										} catch (Exception $e) {

										}
									}
								}
							}
						}
					}
					$eqLogic = self::getEqLogicByLogicalIdAndServerId($explodeKey[1], $serverID);
					if (is_object($eqLogic)) {
						if (isset($value['hasCode'])) {
							foreach ($eqLogic->searchCmdByConfiguration('code', 'info') as $cmd) {
								$cmd->event($cmd->execute(), 0);
								break;
							}
							continue;
						}
						if (count($explodeKey) == 5) {
							foreach ($result as $class => $value) {
								if ($eqLogic->getConfiguration('device') == 'fibaro.fgs221.pilote') {
									foreach ($eqLogic->searchCmdByConfiguration('pilotWire', 'info') as $cmd) {
										$cmd->event($cmd->getPilotWire(), 0);
										break;
									}
									continue;
								}
								foreach ($eqLogic->getCmd('info') as $cmd) {
									foreach ($eqLogic->getCmd('info', $explodeKey[3] . '.0x' . dechex($explodeKey[5]), null, true) as $cmd) {
										$configurationValues = explode('.', str_replace(array(']', '['), array('', '.'), $cmd->getConfiguration('value')));
										foreach ($configurationValues as $configurationValue) {
											if (isset($value[$configurationValue])) {
												$value = [$configurationValue];
											}
										}
										$cmd->handleUpdateValue($value);
									}
								}
							}
						} else if (count($explodeKey) > 5) {
							if ($eqLogic->getConfiguration('device') == 'fibaro.fgs221.pilote') {
								foreach ($eqLogic->searchCmdByConfiguration('pilotWire', 'info') as $cmd) {
									$cmd->event($cmd->getPilotWire(), 0);
									break;
								}
								continue;
							}
							$attribut = implode('.', array_slice($explodeKey, 6));
							foreach ($eqLogic->getCmd('info', $explodeKey[3] . '.0x' . dechex($explodeKey[5]), null, true) as $cmd) {
								if (strpos(str_replace(array(']', '['), array('', '.'), $cmd->getConfiguration('value')), $attribut) !== false) {
									$cmd->handleUpdateValue($result);
								}
							}
						}
					}
				}
			}
			if (isset($results['updateTime'])) {
				self::$_zwaveUpdatetime[$serverID] = $results['updateTime'];
				cache::set('openzwave::lastUpdate' . $serverID, $results['updateTime'], 0);
			} else {
				self::$_zwaveUpdatetime[$serverID] = 0;
				cache::set('openzwave::lastUpdate' . $serverID, 0, 0);
			}
		}
	}

	public static function getEqLogicByLogicalIdAndServerId($_logical_id, $_serverId = 0) {
		foreach (self::byLogicalId($_logical_id, 'openzwave', true) as $eqLogic) {
			if ($eqLogic->getConfiguration('serverID', 0) == $_serverId) {
				return $eqLogic;
			}
		}
		return null;
	}

	public static function syncEqLogicWithRazberry($_serverId = 0) {
		$results = self::callRazberry('/ZWaveAPI/Data/0', $_serverId);
		$findDevice = array();
		$include_device = '';
		$controller_id = openzwave::getZwaveInfo('controller::data::nodeId::value', $_serverId);
		foreach ($results['devices'] as $nodeId => $result) {
			if ($nodeId == $controller_id) {
				continue;
			}
			$findDevice[$nodeId] = $nodeId;
			$eqLogic = self::getEqLogicByLogicalIdAndServerId($nodeId, $_serverId);
			if (!is_object($eqLogic)) {
				$eqLogic = new eqLogic();
				$eqLogic->setEqType_name('openzwave');
				$eqLogic->setIsEnable(1);
				if (isset($result['data']['name']['value']) && trim($result['data']['name']['value']) != '') {
					$eqLogic->setName('[' . $eqLogic->getLogicalId() . ']' . $result['data']['name']['value']);
					$eqLogic->setConfiguration('product_name', strtolower(str_replace(' ', '.', $result['data']['name']['value'])));
				} else {
					$eqLogic->setName('Device ' . $nodeId);
				}
				$eqLogic->setLogicalId($nodeId);
				$eqLogic->setConfiguration('serverID', $_serverId);
				$eqLogic->setIsVisible(1);
				$eqLogic->save();
				$eqLogic = openzwave::byId($eqLogic->getId());
				$include_device = $eqLogic->getId();
				$eqLogic->createCommand();
			} else {
				if (isset($result['data']['name']['value'])) {
					$eqLogic->setConfiguration('product_name', strtolower(str_replace(' ', '.', $result['data']['name']['value'])));
					$eqLogic->setConfiguration('manufacturer_id', strtolower(str_replace(' ', '.', $result['data']['manufacturerId']['value'])));
					$eqLogic->setConfiguration('product_type', strtolower(str_replace(' ', '.', $result['data']['manufacturerProductType']['value'])));
					$eqLogic->setConfiguration('product_id', strtolower(str_replace(' ', '.', $result['data']['manufacturerProductId']['value'])));
					$eqLogic->save();
				}
			}
		}
		if (config::byKey('autoRemoveExcludeDevice', 'openzwave') == 1 && count($findDevice) > 1) {
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
			self::callRazberry('/ZWaveAPI/Run/CancelCommand()', $_serverId);
			return;
		}
		if ($_mode == 1) {
			self::callRazberry('/ZWaveAPI/Run/controller.AddNodeToNetwork(' . $_state . ')', $_serverId);
		} else {
			self::callRazberry('/ZWaveAPI/Run/controller.RemoveNodeFromNetwork(' . $_state . ')', $_serverId);
		}
	}

	public static function cronDaily() {
		foreach (self::byType('zwave') as $eqLogic) {
			if ($eqLogic->getConfiguration('noBatterieCheck', 0) != 1) {
				try {
					$info = $eqLogic->getInfo();
					if (isset($info['battery']) && $info['battery'] !== '') {
						$eqLogic->batteryStatus($info['battery']['value'], $info['battery']['datetime']);
					}
				} catch (Exception $exc) {

				}
			}
		}
	}

	public static function updateConf() {
		foreach (self::byType('openzwave') as $openzwave) {
			if (!file_exists(dirname(__FILE__) . '/../config/devices/' . $openzwave->getConfiguration('product_name') . '.json')) {
				continue;
			}
			$content = file_get_contents(dirname(__FILE__) . '/../config/devices/' . $openzwave->getConfiguration('product_name') . '.json');
			if (!is_json($content)) {
				continue;
			}
			$device = json_decode($content, true);
			if (!isset($device['configuration']) || !isset($device['configuration']['conf_version'])) {
				continue;
			}
			if ($device['configuration']['conf_version'] <= $openzwave->getConfiguration('conf_version')) {
				continue;
			}
			$openzwave->createCommand(true);
		}
	}

/*     * ********************************************************************** */
/*     * ***********************OPENZWAVE MANAGEMENT*************************** */
	public static function updateOpenzwave() {
		log::remove('openzwave_update');
		$cmd = 'sudo /bin/bash ' . dirname(__FILE__) . '/../../ressources/install.sh';
		$cmd .= ' >> ' . log::getPathToLog('openzwave_update') . ' 2>&1 &';
		exec($cmd);
	}

	public static function cron() {
		$port = config::byKey('port', 'openzwave', 'none');
		if ($port != 'none') {
			if ($port == 'auto' || file_exists(jeedom::getUsbMapping($port))) {
				if (!self::deamonRunning()) {
					self::runDeamon();
				}
				message::removeAll('openzwave', 'noOpenzwaveComPort');
			} else {
				log::add('rfxcom', 'error', __('Le port du openZwave est vide ou n\'existe pas', __FILE__), 'noOpenzwaveComPort');
			}
		}
	}

	public static function runDeamon($_debug = false) {
		self::stopDeamon();
		log::add('openzwave', 'info', 'Lancement du démon openzwave');
		$port = config::byKey('port', 'openzwave');
		if ($port != 'auto') {
			$port = jeedom::getUsbMapping($port);
			if (@!file_exists($port)) {
				throw new Exception(__('Le port : ', __FILE__) . print_r($port, true) . __(' n\'existe pas', __FILE__));
			}
			exec('sudo chmod 777 ' . $port . ' > /dev/null 2>&1');
		}
		$port_server = config::byKey('port_server', 'openzwave', 8083);
		$openzwave_path = realpath(dirname(__FILE__) . '/../../ressources/zwaveserver');
		if ($_debug) {
			$cmd = 'nice -n 19 /usr/bin/python ' . $openzwave_path . '/rest-server.py --device=' . $port . ' --log=Debug --port=' . $port_server;
		} else {
			$cmd = 'nice -n 19 /usr/bin/python ' . $openzwave_path . '/rest-server.py --device=' . $port . ' --log=Info --port=' . $port_server;
		}
		log::add('openzwave', 'info', 'Lancement démon openzwave : ' . $cmd);
		$result = exec('nohup ' . $cmd . ' >> ' . log::getPathToLog('openzwave') . ' 2>&1 &');
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
		if ($i >= 30) {
			log::add('openzwave', 'error', 'Impossible de lancer le démon openzwave, vérifiez le port', 'unableStartDeamon');
			return false;
		}
		message::removeAll('openzwave', 'unableStartDeamon');
		log::add('openzwave', 'info', 'Démon openzwave lancé');
	}

	public static function deamonRunning() {
		//$result = exec('ps e | grep "rest-server.py" | wc -l');
		$result = exec("ps -eo pid,command | grep 'rest-server.py' | grep -v grep | awk '{print $1}'");
		if ($result == 0) {
			return false;
		}
		return true;
	}

	public static function stopDeamon() {
		if (!self::deamonRunning()) {
			return true;
		}
		$pid = exec("ps -eo pid,command | grep 'rest-server.py' | grep -v grep | awk '{print $1}'");
		posix_kill($pid, 15);
		if (self::deamonRunning()) {
			sleep(1);
			posix_kill($pid, 9);
		}
		if (self::deamonRunning()) {
			sleep(1);
			exec('kill -9 ' . $pid . ' > /dev/null 2>&1');
		}
		exec('fuser -k ' . config::byKey('port_server', 'openzwave', 8083) . '/tcp > /dev/null 2>&1');
		exec('sudo fuser -k ' . config::byKey('port_server', 'openzwave', 8083) . '/tcp > /dev/null 2>&1');
		return self::deamonRunning();
	}

	/*     * *********************Methode d'instance************************* */

	public function ping() {
		$info = $this->getInfo();
		if ($info['state']['value'] == __('Réveillé', __FILE__) || $info['state']['value'] == __('Actif', __FILE__)) {
			$cmds = $this->getCmd('info');
			$cmds[0]->forceUpdate();
			if (strtotime($this->getStatus('lastCommunication', date('Y-m-d H:i:s'))) < (strtotime('now') - 120)) {
				sleep(5);
			}
			if (strtotime($this->getStatus('lastCommunication', date('Y-m-d H:i:s'))) < (strtotime('now') - 120)) {
				echo 'je passe';
				return false;
			}
		} else {
			if ($this->getStatus('lastCommunication', date('Y-m-d H:i:s')) < date('Y-m-d H:i:s', strtotime('-' . $this->getTimeout() . ' minutes' . date('Y-m-d H:i:s')))) {
				return false;
			}
		}
		return true;
	}

	public function getInfo() {
		$return = array();
		if (!is_numeric($this->getLogicalId())) {
			return $return;
		}
		$results = self::callRazberry('/ZWaveAPI/Run/devices[' . $this->getLogicalId() . ']', $this->getConfiguration('serverID', 1));
		if ($this->getConfiguration('noBatterieCheck') != 1 && isset($results['instances']) && isset($results['instances'][0]) &&
			isset($results['instances'][0]['commandClasses']) && isset($results['instances'][0]['commandClasses'][128]) &&
			isset($results['instances'][0]['commandClasses'][128]['data']['supported']) && $results['instances'][0]['commandClasses'][128]['data']['supported']['value'] === true) {
			$return['battery'] = array(
				'value' => $results['instances'][0]['commandClasses'][128]['data']['last']['value'],
				'datetime' => date('Y-m-d H:i:s', $results['instances'][0]['commandClasses'][128]['data']['last']['updateTime']),
				'unite' => '%',
			);
		}

		if (isset($results['data'])) {
			if (isset($results['data']['isAwake'])) {
				$return['state'] = array(
					'value' => ($results['data']['isAwake']['value']) ? __('Réveillé', __FILE__) : __('Endormi', __FILE__),
					'datetime' => date('Y-m-d H:i:s', $results['data']['isAwake']['updateTime']),
				);
			}
			if (isset($results['data']['isFailed'])) {
				$return['state']['value'] = ($results['data']['isFailed']['value']) ? 'Dead' : $return['state']['value'];
			}
			if (isset($results['data']['vendorString'])) {
				$return['brand'] = array(
					'value' => $results['data']['vendorString']['value'],
					'datetime' => '',
				);
			}

			if (isset($results['data']['lastReceived'])) {
				$return['lastReceived'] = array(
					'value' => date('Y-m-d H:i', $results['data']['lastReceived']['updateTime']),
					'datetime' => date('Y-m-d H:i:s', $results['data']['lastReceived']['updateTime']),
				);
			}

			if ((isset($return['battery']) && $return['battery']['value'] != '') || (isset($return['state']) && $return['state']['value'] == __('Endormi', __FILE__))) {
				$return['powered'] = array(
					'value' => false,
					'datetime' => date('Y-m-d H:i:s'),
				);
			} else {
				$return['powered'] = array(
					'value' => true,
					'datetime' => date('Y-m-d H:i:s'),
				);
			}
		}
		return $return;
	}

	public function loadCmdFromConf($_update = false) {
		if (!file_exists(dirname(__FILE__) . '/../config/devices/' . $this->getConfFilePath())) {
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
			$cmd = null;
			foreach ($this->getCmd() as $liste_cmd) {
				if ($liste_cmd->getConfiguration('instanceId', 0) == $command['configuration']['instanceId'] &&
					$liste_cmd->getConfiguration('class') == $command['configuration']['class'] &&
					$liste_cmd->getConfiguration('value') == $command['configuration']['value']) {
					$cmd = $liste_cmd;
					break;
				}
				if ($liste_cmd->getName() == $command['name']) {
					$cmd = $liste_cmd;
					break;
				}
			}
			try {
				if ($cmd == null || !is_object($cmd)) {
					$cmd = new openzwaveCmd();
					$cmd->setOrder($cmd_order);
					$cmd->setEqLogic_id($this->getId());
				} else {
					$command['name'] = $cmd->getName();
					if (isset($command['display'])) {
						unset($command['display']);
					}
				}
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

	public function getConfFilePath() {
		$id = $this->getConfiguration('manufacturer_id') . '.' . $this->getConfiguration('product_type') . '.' . $this->getConfiguration('product_id');
		$files = ls(dirname(__FILE__) . '/../config/devices', $id . '_*.json', false, array('files', 'quiet'));
		if (count($files) > 0) {
			return $files[0];
		}
		return false;
	}

	public function getImgFilePath() {
		$id = $this->getConfiguration('manufacturer_id') . '.' . $this->getConfiguration('product_type') . '.' . $this->getConfiguration('product_id');
		$files = ls(dirname(__FILE__) . '/../img/devices', $id . '_*.jpg', false, array('files', 'quiet'));
		if (count($files) > 0) {
			return $files[0];
		}
		return false;
	}

	public function getAssistantFilePath() {
		$id = $this->getConfiguration('manufacturer_id') . '.' . $this->getConfiguration('product_type') . '.' . $this->getConfiguration('product_id');
		$files = ls(dirname(__FILE__) . '/../config/devices', $id . '_*.php', false, array('files', 'quiet'));
		if (count($files) > 0) {
			return $files[0];
		}
		return false;
	}

	public function createCommand() {
		$return = array();
		if (!is_numeric($this->getLogicalId())) {
			return;
		}

		if (file_exists(dirname(__FILE__) . '/../config/devices/' . $this->getConfFilePath())) {
			$this->loadCmdFromConf();
			return;
		}
		nodejs::pushUpdate('jeedom::alert', array(
			'level' => 'warning',
			'message' => __('Création des commandes en mode automatique', __FILE__),
		));
		$results = self::callRazberry('/ZWaveAPI/Run/devices[' . $this->getLogicalId() . ']', $this->getConfiguration('serverID', 1));
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
										$cmd_name = $data['name'] . ' ' . $cmd_name_number;
									} else {
										$cmd_name = $data['name'];
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
										}
										try {
											$cmd_info->save();
										} catch (Exception $e) {
											ajax::error(displayExeption($e), $e->getCode());
										}
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
												try {
													$cmd->save();
												} catch (Exception $e) {
													ajax::error(displayExeption($e), $e->getCode());
												}
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
												try {
													$cmd->save();
												} catch (Exception $e) {
													ajax::error(displayExeption($e), $e->getCode());
												}
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
												}
												try {
													$cmd->save();
												} catch (Exception $e) {
													ajax::error(displayExeption($e), $e->getCode());
												}
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
												}
												try {
													$cmd->save();
												} catch (Exception $e) {
													ajax::error(displayExeption($e), $e->getCode());
												}
												break;
											case 'List':
												foreach (explode(';', $data['data_items']) as $value) {
													$cmd = new openzwaveCmd();
													$cmd->setType('action');
													$cmd->setEqLogic_id($this->getId());
													$cmd->setName($value);
													$cmd->setConfiguration('instanceId', $instanceID);
													$cmd->setConfiguration('class', $ccId);
													$cmd->setConfiguration('value', 'data[' . $index . '].Set(' . $value . ')');
													$cmd->setSubType('other');
													try {
														$cmd->save();
													} catch (Exception $e) {
														ajax::error(displayExeption($e), $e->getCode());
													}
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
		$value = $_val['value'];
		switch ($_val['type']) {
			case 'float':
				$value = round(floatval($value), 2);
				break;
			case 'int':
				$value = intval($value);
				break;
			case 'bool':
				if ($value === true || $value == 'true') {
					$value = 1;
				} else {
					$value = 0;
				}
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
		$updateTime = null;
		if (isset($_result['val'])) {
			$value = self::handleResult($_result['val']);
			if (isset($_result['val']['updateTime'])) {
				$updateTime = $_result['val']['updateTime'];
			}
		} else if (isset($_result['level'])) {
			$value = self::handleResult($_result['level']);
			if (isset($_result['level']['updateTime'])) {
				$updateTime = $_result['level']['updateTime'];
			}
		} else {
			$value = self::handleResult($_result);
			if (isset($_result['updateTime'])) {
				$updateTime = $_result['updateTime'];
			}
		}
		if ($updateTime != null) {
			$this->setCollectDate(date('Y-m-d H:i:s', $updateTime));
		}
		if ($value === '') {
			try {
				$value = $this->execute();
			} catch (Exception $e) {
				return;
			}
		}
		$this->event($value, 0);
	}

	public function setRGBColor($_color) {
		if ($_color == '') {
			throw new Exception('Couleur non définie');
		}
		$eqLogic = $this->getEqLogic();
		$request = '/ZWaveAPI/Run/devices[' . $eqLogic->getLogicalId() . ']';

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

		//Convertion pour sur une echelle de 0-99
		$r = ($r / 255) * 99;
		$g = ($g / 255) * 99;
		$b = ($b / 255) * 99;

		if ($eqLogic->getConfiguration('device') == 'fibaro.fgrgb101') {
			/* Set GREEN color */
			openzwave::callRazberry($request . '.instances[3].commandClasses[0x26].Set(' . str_replace(',', '%2C', $g) . ')', $eqLogic->getConfiguration('serverID', 1));
			/* Set BLUE color */
			openzwave::callRazberry($request . '.instances[4].commandClasses[0x26].Set(' . str_replace(',', '%2C', $b) . ')', $eqLogic->getConfiguration('serverID', 1));
			/* Set RED color */
			openzwave::callRazberry($request . '.instances[2].commandClasses[0x26].Set(' . str_replace(',', '%2C', $r) . ')', $eqLogic->getConfiguration('serverID', 1));
		} else {
			openzwave::callRazberry($request . '.instances[0].commandClasses[0x33].Set(0,0)', $eqLogic->getConfiguration('serverID', 1));
			openzwave::callRazberry($request . '.instances[0].commandClasses[0x33].Set(1,0)', $eqLogic->getConfiguration('serverID', 1));
			/* Set GREEN color */
			openzwave::callRazberry($request . '.instances[0].commandClasses[0x33].Set(3,' . str_replace(',', '%2C', $g) . ')', $eqLogic->getConfiguration('serverID', 1));
			/* Set BLUE color */
			openzwave::callRazberry($request . '.instances[0].commandClasses[0x33].Set(4,' . str_replace(',', '%2C', $b) . ')', $eqLogic->getConfiguration('serverID', 1));
			/* Set RED color */
			openzwave::callRazberry($request . '.instances[0].commandClasses[0x33].Set(2,' . str_replace(',', '%2C', $r) . ')', $eqLogic->getConfiguration('serverID', 1));
			openzwave::callRazberry($request . '.instances[0].commandClasses[0x26].Set(255)', $eqLogic->getConfiguration('serverID', 1));
		}
		return true;
	}

	public function getRGBColor() {
		$eqLogic = $this->getEqLogic();
		$request = '/ZWaveAPI/Run/devices[' . $eqLogic->getLogicalId() . ']';
		/* Get RED color */
		$r = openzwave::callRazberry($request . '.instances[2].commandClasses[0x26].data.level.value', $eqLogic->getConfiguration('serverID', 1));
		/* Get GREEN color */
		$g = openzwave::callRazberry($request . '.instances[3].commandClasses[0x26].data.level.value', $eqLogic->getConfiguration('serverID', 1));
		/* Get BLUE color */
		$b = openzwave::callRazberry($request . '.instances[4].commandClasses[0x26].data.level.value', $eqLogic->getConfiguration('serverID', 1));
		//Convertion pour sur une echelle de 0-255
		$r = dechex(($r / 99) * 255);
		$g = dechex(($g / 99) * 255);
		$b = dechex(($b / 99) * 255);
		if (strlen($r) == 1) {
			$r = '0' . $r;
		}
		if (strlen($g) == 1) {
			$g = '0' . $g;
		}
		if (strlen($b) == 1) {
			$b = '0' . $b;
		}
		return '#' . $r . $g . $b;
	}

	public function getPilotWire() {
		$eqLogic = $this->getEqLogic();
		$request = '/ZWaveAPI/Run/devices[' . $this->getEqLogic()->getLogicalId() . ']';
		$instancesId = explode('&&', $this->getConfiguration('instanceId'));
		if (!isset($instancesId[0])) {
			$instancesId[0] = 0;
		}
		if (!isset($instancesId[1])) {
			$instancesId[1] = 1;
		}
		$info1 = self::handleResult(openzwave::callRazberry($request . '.instances[' . $instancesId[0] . '].commandClasses[0x25].data.level', $eqLogic->getConfiguration('serverID', 1)));
		$info2 = self::handleResult(openzwave::callRazberry($request . '.instances[' . $instancesId[1] . '].commandClasses[0x25].data.level', $eqLogic->getConfiguration('serverID', 1)));
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

	public function forceUpdate() {
		$eqLogic = $this->getEqLogic();
		openzwave::callRazberry('/ZWaveAPI/Run/devices[' . $this->getEqLogic()->getLogicalId() . '].instances[' . $this->getConfiguration('instanceId', 0) . '].commandClasses[' . $this->getConfiguration('class') . '].Get()', $eqLogic->getConfiguration('serverID', 1));
	}

	public function sendZwaveResquest($_url) {
		$eqLogic = $this->getEqLogic();
		$result = openzwave::callRazberry($_url, $eqLogic->getConfiguration('serverID', 1));
		if ($this->getType() == 'action') {
			return;
		}
		if (is_array($result)) {
			$value = self::handleResult($result);
			if (isset($result['updateTime'])) {
				$this->setCollectDate(date('Y-m-d H:i:s', $result['updateTime']));
			}
		} else {
			$value = $result;
			if ($value === true || $value == 'true') {
				return 1;
			}
			if ($value === false || $value == 'false') {
				return 0;
			}
			if (is_numeric($value)) {
				return round($value, 1);
			}
		}
		return $value;
	}

	public function execute($_options = null) {
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
						$value = str_replace('#color#', $_options['color'], $value);
						return $this->setRGBColor($value);
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
					}
					$request_http .= '.commandClasses[' . $this->getConfiguration('class') . ']';
					$request_http .= '.' . $value;
					$result .= $this->sendZwaveResquest($request_http);
				}
			}
			return $result;
		}
		if ($this->getConfiguration('instanceId') != '' && ($this->getConfiguration('class') != '0x70')) {
			$request .= '.instances[' . $this->getConfiguration('instanceId') . ']';
		}
		$request .= '.commandClasses[' . $this->getConfiguration('class') . ']';
		$request .= '.' . str_replace(',', '%2C', $value);
		return $this->sendZwaveResquest($request);
	}

}

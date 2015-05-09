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

	/*     * ***********************Methode static*************************** */

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

	public static function runDeamon() {
		self::stopDeamon();
		log::add('openzwave', 'info', 'Lancement du démon openzwave');

		$port = config::byKey('port', 'openzwave');
		if ($port != 'auto') {
			$port = jeedom::getUsbMapping($port);
			if (@!file_exists($port)) {
				throw new Exception(__('Le port : ', __FILE__) . print_r($port, true) . __(' n\'existe pas', __FILE__));
			}
		}

		$port_server = config::byKey('port_server', 'openzwave', 8083);

		if (!file_exists($port)) {
			config::save('port', '', 'openzwave');
			throw new Exception(__('Le port : ', __FILE__) . $port . __(' n\'éxiste pas', __FILE__));
		}
		$openzwave_path = realpath(dirname(__FILE__) . '/../../ressources/zwaveserver');

		$enable_logging = 0;
		if (config::byKey('enableLogging', 'openzwave', 0) == 1) {
			$enable_logging = 1;
		}

		if ($enable_logging == 1) {
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
		sleep(2);
		if (!self::deamonRunning()) {
			sleep(10);
			if (!self::deamonRunning()) {
				log::add('openzwave', 'error', 'Impossible de lancer le démon openzwave, vérifiez le port', 'unableStartDeamon');
				return false;
			}
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
	/*     * ********************************************************************** */
	/*     * ********************************************************************** */
	/*     * ********************************************************************** */

	/*     * *********************Methode d'instance************************* */
}

class openzwaveCmd extends cmd {
	/*     * ***********************Methode static*************************** */

	/*     * *********************Methode d'instance************************* */

}

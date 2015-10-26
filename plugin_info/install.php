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

function openzwave_update() {
	if (!file_exists(dirname(__FILE__) . '/../data')) {
		mkdir(dirname(__FILE__) . '/../data');
	}
	shell_exec('cp -R /opt/python-openzwave/xml_backups ' . dirname(__FILE__) . '/../data');
	shell_exec('cp -R /opt/python-openzwave/zwcfg_*.xml ' . dirname(__FILE__) . '/../data');
	shell_exec('rm -rf /opt/python-openzwave/xml_backups');
	shell_exec('rm -rf /opt/python-openzwave/zwcfg_*.xml');
	config::save('allowStartDeamon', 0, 'openzwave');
	echo 'Stop zwave network...';
	openzwave::stop();
	openzwave::stopDeamon();
	echo "OK\n";
	echo 'Stop cron...';
	$cron = cron::byClassAndFunction('openzwave', 'pull');
	if (is_object($cron)) {
		$cron->remove();
	}
	echo "OK\n";

	echo 'Check zwave system...';
	if (count(eqLogic::byType('zwave')) > 0) {
		log::add('openzwave', 'error', 'Attention vous etes sur la nouvelle version d\'openzwave, des actions de votre part sont necessaire merci d\'aller voir https://jeedom.fr/blog/?p=1576');
	}
	if (config::byKey('port', 'openzwave', 'none') != 'none') {
		if (method_exists('openzwave', 'getVersion')) {
			if (version_compare(config::byKey('openzwave_version', 'openzwave'), openzwave::getVersion('openzwave'), '>')) {
				if (jeedom::getHardwareName() == 'Jeedomboard') {
					openzwave::updateOpenzwave(false);
				} else {
					log::add('openzwave', 'error', __('Attention votre version d\'openzwave est dépassée sur le démon local, il faut ABSOLUMENT la mettre à jour', __FILE__));
				}
			}
		}
	}
	if (config::byKey('jeeNetwork::mode') == 'master') {
		foreach (jeeNetwork::byPlugin('openzwave') as $jeeNetwork) {
			try {
				if ($jeeNetwork->configByKey('port', 'openzwave', 'none') != 'none') {
					if (version_compare($jeeNetwork->sendRawRequest('getVersion', array('plugin' => 'openzwave', 'module' => 'openzwave')), openzwave::getVersion('openzwave'), '>')) {
						log::add('openzwave', 'error', __('Attention votre version d\'openzwave est dépassée sur', __FILE__) . ' ' . $jeeNetwork->getName() . ' ' . __('il faut ABSOLUMENT la mettre à jour', __FILE__));
					}
				}
			} catch (Exception $e) {

			}
		}
	}
	echo "OK\n";
	echo 'Redemarrage zwave network...';
	try {
		config::save('allowStartDeamon', 1, 'openzwave');
		openzwave::runDeamon();
	} catch (Exception $e) {

	}
	echo "OK\n";
}

function openzwave_remove() {
	if (openzwave::deamonRunning()) {
		openzwave::stopDeamon();
	}
	$cron = cron::byClassAndFunction('openzwave', 'pull');
	if (is_object($cron)) {
		$cron->remove();
	}
}

?>
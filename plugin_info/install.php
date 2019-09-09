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

function openzwave_install() {
	if (config::byKey('api::openzwave::mode') == '') {
		config::save('api::openzwave::mode', 'localhost');
	}
}

function openzwave_update() {
	if (config::byKey('api::openzwave::mode') == '') {
		config::save('api::openzwave::mode', 'localhost');
	}
	if (!file_exists(dirname(__FILE__) . '/../data')) {
		mkdir(dirname(__FILE__) . '/../data');
		if (file_exists('/opt/python-openzwave/xml_backups')) {
			shell_exec('cp -R /opt/python-openzwave/xml_backups ' . dirname(__FILE__) . '/../data');
			shell_exec('cp -R /opt/python-openzwave/zwcfg_*.xml ' . dirname(__FILE__) . '/../data');
			shell_exec('rm -rf /opt/python-openzwave/xml_backups');
			shell_exec('rm -rf /opt/python-openzwave/zwcfg_*.xml');
		}
	}
	$cron = cron::byClassAndFunction('openzwave', 'pull');
	if (is_object($cron)) {
		$cron->remove();
	}
	if (count(eqLogic::byType('zwave')) > 0) {
		log::add('openzwave', 'error', 'Attention vous etes sur la nouvelle version d\'openzwave, des actions de votre part sont necessaire merci d\'aller voir https://jeedom.fr/blog/?p=1576');
	}
	foreach (eqLogic::byType('openzwave') as $eqLogic) {
		foreach ($eqLogic->getCmd() as $cmd) {
			if (strpos($cmd->getConfiguration('class'), '0x') === false) {
				continue;
			}
			$cmd->setConfiguration('class', hexdec($cmd->getConfiguration('class')));
			$cmd->setConfiguration('instance', $cmd->getConfiguration('instanceId') + 1);
			$matches = array();
			preg_match_all('/data\[(.*)\]\.(.*)/', $cmd->getConfiguration('value'), $matches);
			if (count($matches[1]) == 1 && count($matches[2]) == 1) {
				$cmd->setConfiguration('index', $matches[1][0]);
				if ($matches[2][0] == 'val') {
					$matches[2][0] = '';
				}
				$matches[2][0] = str_replace('Set', 'set', $matches[2][0]);
				$matches[2][0] = str_replace('PressButton()', 'button(press)', $matches[2][0]);
				$matches[2][0] = str_replace('ReleaseButton()', 'button(release)', $matches[2][0]);
				$cmd->setConfiguration('value', $matches[2][0]);
			}
			if ($cmd->getConfiguration('value') == 'button(press)') {
				$cmd->setConfiguration('value', 'type=buttonaction&action=press');
			} else if ($cmd->getConfiguration('value') == 'button(release)') {
				$cmd->setConfiguration('value', 'type=buttonaction&action=release');
			} else if (strpos($cmd->getConfiguration('value'), '.val') !== false) {
				$cmd->setConfiguration('value', '');
			} else if (strpos($cmd->getConfiguration('value'), '.val') !== false || $cmd->getConfiguration('value') == 'Get()') {
				$cmd->setConfiguration('value', 'type=refreshData');
			} else if ($cmd->getConfiguration('value') == 'ForceRefresh()') {
				$cmd->setConfiguration('value', 'type=refreshData');
			} else {
				preg_match_all('/set\((.*),(.*),(.*)\)/', $cmd->getConfiguration('value'), $matches);
				if (isset($matches[1][0])) {
					$cmd->setConfiguration('index', $matches[1][0]);
					$cmd->setConfiguration('value', 'type=setconfig&value=' . urlencode($matches[2][0]) . '&size=' . urlencode($matches[3][0]));
				} else {
					preg_match_all('/set\((.*)\)/', $cmd->getConfiguration('value'), $matches);
					if (isset($matches[1][0])) {
						$cmd->setConfiguration('value', 'type=setvalue&value=' . urlencode($matches[1][0]));
					} else {
						preg_match_all('/SwitchAll\((.*)\)/', $cmd->getConfiguration('value'), $matches);
						if (isset($matches[1][0])) {
							$cmd->setConfiguration('value', 'type=switchall&value=' . urlencode($matches[1][0]));
						} else {

						}
					}
				}
			}
			$cmd->setConfiguration('value', str_replace('%23', '#', $cmd->getConfiguration('value')));
			$cmd->save();
		}
	}
}

function openzwave_remove() {

}

?>

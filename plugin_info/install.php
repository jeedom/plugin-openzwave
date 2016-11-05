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

function openzwave_update() {
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
			if (strpos('0x', $cmd->getConfiguration('class')) !== false) {
				$cmd->setConfiguration('class', hexdec($cmd->getConfiguration('class')));
			}
			$cmd->setConfiguration('instance', $cmd->getConfiguration('instanceId'));
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
			$cmd->save();
		}
	}
	openzwave::syncconfOpenzwave();
}

function openzwave_remove() {

}

?>
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
	sleep(2);
	if (openzwave::deamonRunning()) {
		openzwave::runDeamon();
	}
}

function openzwave_remove() {
	config::save('allowStartDeamon', 0, 'openzwave');
	if (openzwave::deamonRunning()) {
		openzwave::stopDeamon();
	}
}

?>
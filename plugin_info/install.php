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

function openzwave_install() {
	if (config::byKey('jeeNetwork::mode') != 'slave') {
		$cron = cron::byClassAndFunction('openzwave', 'pull');
		if (!is_object($cron)) {
			$cron = new cron();
			$cron->setClass('openzwave');
			$cron->setFunction('pull');
			$cron->setEnable(1);
			$cron->setDeamon(1);
			$cron->setDeamonSleepTime(0.5);
			$cron->setTimeout(1440);
			$cron->setSchedule('* * * * *');
			$cron->save();
		}
	}
}

function openzwave_update() {
	if (openzwave::deamonRunning()) {
		openzwave::stopDeamon();
	}
	$cron = cron::byClassAndFunction('openzwave', 'pull');
	if (config::byKey('jeeNetwork::mode') != 'slave') {
		if (!is_object($cron)) {
			$cron = new cron();
		}
		$cron->setClass('openzwave');
		$cron->setFunction('pull');
		$cron->setEnable(1);
		$cron->setDeamon(1);
		$cron->setDeamonSleepTime(0.5);
		$cron->setTimeout(1440);
		$cron->setSchedule('* * * * *');
		$cron->save();
		$cron->stop();
	} else {
		if (is_object($cron)) {
			$cron->remove();
		}
	}
	openzwave::updateConf();
	if (count(eqLogic::byType('zwave')) > 0) {
		log::add('openzwave', 'error', 'Attention vous etes sur la nouvelle version d\'openzwave, des actions de votre part sont necessaire merci d\'aller voir https://jeedom.fr/blog/?p=1576');
	}
}

function openzwave_remove() {
	if (openzwave::deamonRunning()) {
		openzwave::stopDeamon();
	}
	$cron = cron::byClassAndFunction('zwave', 'pull');
	if (is_object($cron)) {
		$cron->remove();
	}
}

?>
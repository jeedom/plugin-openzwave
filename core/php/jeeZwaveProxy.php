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
require_once dirname(__FILE__) . "/../../../../core/php/core.inc.php";
include_file('core', 'authentification', 'php');
if (!isConnect('admin')) {
    echo '401 - Accès non autorisé';
    die();
}
ajax::init();
try {
    if (strpos(init('request'), '/ZWaveAPI/Run/network.SaveZWConfig()') !== false) {
        $data_path = dirname(__FILE__) . '/../../data';
        if (!file_exists($data_path)) {
            exec('mkdir ' . $data_path . ' && chmod 775 -R ' . $data_path . ' && chown -R www-data:www-data ' . $data_path);
        }
        if (file_exists($data_path . '/zwcfg_new.xml')) {
            unlink($data_path . '/zwcfg_new.xml');
        }
        if (file_exists($data_path . '/zwcfg_new.xml')) {
            exec('sudo rm -rf ' . $data_path . '/zwcfg_new.xml');
        }
        file_put_contents($data_path . '/zwcfg_new.xml', init('data'));
        echo json_encode(openzwave::callOpenzwave(str_replace('//', '/', init('request')), init('server_id')));
    } else {
        echo json_encode(openzwave::callOpenzwave(str_replace('//', '/', init('request')), init('server_id')));
    }
} catch (Exception $e) {
    http_response_code(500);
    die($e->getMessage());
}

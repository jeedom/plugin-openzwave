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

if (!isConnect('admin')) {
	throw new Exception('401 Unauthorized');
}
?>
<span class='pull-right'>
    <a class="btn btn-default pull-right" id="bt_refreshHealth"><i class="fas fa-sync-alt"></i> {{Rafraichir}}</a>
    <a class="btn btn-primary pull-right" id="bt_pingAllDevice"><i class="fa fa-eye"></i> {{Ping de tous}}</a>
</span>
<br/><br/>
<div id='div_networkHealthAlert' style="display: none;"></div>
<table class="table table-condensed" id="table_healthNetwork">
    <thead>
        <tr>
            <th>{{Module}}</th>
            <th>{{ID}}</th>
            <th width="50"></th>
            <th>{{Groupes}}</th>
            <th>{{Constructeur}}</th>
            <th>{{Voisins}}</th>
            <th>{{Configuration}}</th>
            <th>{{Statut}}</th>
            <th>{{Batterie}}</th>
            <th>{{Wakeup time}}</th>
            <th>{{Paquet total}}</th>
            <th>{{% OK}}</th>
            <th>{{Temporisation}}</th>
            <th>{{Dernière notification}}</th>
            <th>{{Ping}}</th>
        </tr>
    </thead>
    <tbody>

    </tbody>
</table>
<?php include_file('core', 'openzwave', 'class.js', 'openzwave');?>
<?php include_file('desktop', 'health', 'js', 'openzwave');?>
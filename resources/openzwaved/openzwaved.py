#!flask/bin/python
# This file is part of Jeedom.
#
# Jeedom is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Jeedom is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Jeedom. If not, see <http://www.gnu.org/licenses/>.
import sys
import argparse

from ozwave import globals,utils,network_utils,node_utils,dispatcher_utils,server_utils,manager_utils,value_utils

try:
	from tornado.wsgi import WSGIContainer
	from tornado.httpserver import HTTPServer
	from tornado.ioloop import IOLoop
except Exception as e:
	print(globals.MSG_CHECK_DEPENDENCY, 'error')
	print("Error: %s" % str(e), 'error')
	sys.exit(1)

try:
	from flask import Flask, jsonify, abort, request, make_response, redirect, url_for
	from flask_httpauth import HTTPBasicAuth
except Exception as e:
	print(globals.MSG_CHECK_DEPENDENCY, 'error')
	print("Error: %s" % str(e), 'error')
	sys.exit(1)

try:
	import logging
	import os.path
	import shutil
	import platform
	import datetime
	import binascii
	import threading
	from threading import Event, Thread
	from lxml import etree
	import signal

except Exception as e:
	print(globals.MSG_CHECK_DEPENDENCY, 'error')
	print("Error: %s" % str(e), 'error')
	sys.exit(1)

if not os.path.exists('/tmp/python-openzwave-eggs'):
	os.makedirs('/tmp/python-openzwave-eggs')
os.environ['PYTHON_EGG_CACHE'] = '/tmp/python-openzwave-eggs'

auth = HTTPBasicAuth()

parser = argparse.ArgumentParser(description='Ozw Daemon for Jeedom plugin')
parser.add_argument("--device", help="Device", type=str)
parser.add_argument("--port", help="Port for OZW server", type=str)
parser.add_argument("--loglevel", help="Log Level for the daemon", type=str)
parser.add_argument("--config_folder", help="Read or Write", type=str)
parser.add_argument("--data_folder", help="Handle to read or write", type=str)
parser.add_argument("--pidfile", help="Value to write", type=str)
parser.add_argument("--callback", help="Value to write", type=str)
parser.add_argument("--apikey", help="Value to write", type=str)
parser.add_argument("--suppressRefresh", help="Value to write", type=str)
parser.add_argument("--disabledNodes", help="Value to write", type=str)
args = parser.parse_args()

if args.device:
	globals.device = args.device
if args.port:
	globals.port_server = args.port
if args.loglevel:
	globals.log_level = args.loglevel
if args.config_folder:
	globals.config_folder = args.config_folder
if args.data_folder:
	globals.data_folder = args.data_folder
if args.pidfile:
	globals.pidfile = args.pidfile
if args.callback:
	globals.callback = args.callback
if args.apikey:
	globals.apikey = args.apikey
if args.suppressRefresh:
	globals.suppress_refresh = args.suppressRefresh
if args.disabledNodes:
	if args.disabledNodes != '':
		globals.disabled_nodes = [int(disabled_node_id) for disabled_node_id in args.disabledNodes.split(',')]

cycle = float(globals.cycle)

server_utils.set_log_level()

logging.info('Start openzwaved')
logging.info('Log level : ' + str(globals.log_level))
logging.debug('PID file : ' + str(globals.pidfile))
logging.info('Device : ' + str(globals.device))
logging.debug('Apikey : ' + str(globals.apikey))
logging.info('Callback : ' + str(globals.callback))
logging.info('Cycle : ' + str(globals.cycle))

logging.debug('Initial disabled nodes list: ' + str(globals.disabled_nodes))

server_utils.init_jeedom_com()

if not globals.jeedom_com.test():
	logging.error('Network communication issues. Please fixe your Jeedom network configuration.')
	sys.exit(1)

reload(sys)
sys.setdefaultencoding('utf8')

logging.info("Check Openzwave")
from ozwave.utilities.NetworkExtend import *
from ozwave.utilities.NodeExtend import *
from ozwave.utilities.Constants import *
from ozwave.utilities.FilesManager import FilesManager

logging.info("--> pass")

server_utils.check_start_server()
manager_utils.init_manager()

app = Flask(__name__, static_url_path='/static')
# Create a network object
network_utils.create_network()
dispatcher_utils.connect_dispatcher()
network_utils.start_network()
logging.info('OpenZwave Library Version %s' % (globals.network.manager.getOzwLibraryVersionNumber(),))
logging.info('Python-OpenZwave Wrapper Version %s' % (globals.network.manager.getPythonLibraryVersionNumber(),))
# We wait for the network.
logging.info('Waiting for network to become ready')

def mark_pending_change(my_value, data, wake_up_time=0):
	if my_value is not None and not my_value.is_write_only:
		globals.pending_configurations[my_value.id_on_network] = PendingConfiguration(data, wake_up_time)

def check_pending_changes(node_id):
	my_node = globals.network.nodes[node_id]
	pending_changes = 0
	for val in my_node.get_values():
		my_value = my_node.values[val]
		if my_value.command_class is None:
			continue
		if my_value.is_write_only:
			continue
		if my_value.is_read_only:
			continue
		pending_state = None
		if my_value.id_on_network in globals.pending_configurations:
			pending_configuration = globals.pending_configurations[my_value.id_on_network]
			if pending_configuration is not None:
				pending_state = pending_configuration.state

		if pending_state is None or pending_state == 1:
			continue
		pending_changes += 1
	if my_node.node_id in globals.pending_associations:
		pending_associations = globals.pending_associations[my_node.node_id]
		for index_group in list(pending_associations):
			pending_association = pending_associations[index_group]
			pending_state = None
			if pending_association is not None:
				pending_state = pending_association.state
			if pending_state is None or pending_state == 1:
				continue
			pending_changes += 1
	return pending_changes

def serialize_neighbour_to_json(node_id):
	json_result = {}
	if node_id in globals.network.nodes:
		my_node = globals.network.nodes[node_id]
		json_result['data'] = {}
		json_result['data']['product_name'] = {'value': my_node.product_name}
		json_result['data']['location'] = {'value': my_node.location}
		node_name = my_node.name
		if globals.network.controller.node_id == node_id:
			node_name = my_node.product_name
		if utils.is_none_or_empty(node_name):
			node_name = my_node.product_name
		if utils.is_none_or_empty(node_name):
			node_name = 'Unknown'
		json_result['data']['name'] = {'value': node_name}
		json_result['data']['isPrimaryController'] = {'value': globals.network.controller.node_id == node_id}
		neighbour_is_enabled = my_node.generic != 1 # not a remote control
		if my_node.generic == 8 and not my_node.is_listening_device:
			neighbour_is_enabled = len(my_node.neighbors) > 0
		json_result['data']['neighbours'] = {'value': list(my_node.neighbors), 'enabled': neighbour_is_enabled}
		json_result['data']['isDead'] = {'value': my_node.is_failed}
		json_result['data']['type'] = {'basic': my_node.basic, 'generic': my_node.generic, 'specific': my_node.specific}
		json_result['data']['state'] = {'value': utils.convert_query_stage_to_int(my_node.query_stage)}
		json_result['data']['isListening'] = {'value': my_node.is_listening_device}
		json_result['data']['isRouting'] = {'value': my_node.is_routing_device}
	else:
		logging.warning('This network does not contain any node with the id %s' % (node_id,))
	return json_result

def serialize_node_to_json(node_id):
	json_result = {}
	if node_id not in globals.network.nodes or node_id in globals.not_supported_nodes:
		return json_result
	my_node = globals.network.nodes[node_id]
	try:
		timestamp = int(my_node.last_update)
	except TypeError:
		timestamp = int(1)
	try:
		manufacturer_id = int(my_node.manufacturer_id, 16)
	except ValueError:
		manufacturer_id = None
	try:
		product_id = int(my_node.product_id, 16)
	except ValueError:
		product_id = None
	try:
		product_type = int(my_node.product_type, 16)
	except ValueError:
		product_type = None
	json_result['data'] = {}
	node_name = my_node.name
	if globals.network.controller.node_id == node_id:
		node_name = my_node.product_name
	if utils.is_none_or_empty(node_name):
		node_name = 'Unknown'
	json_result['data']['description'] = {'name': node_name, 'location': my_node.location,'product_name': my_node.product_name}
	json_result['data']['manufacturerId'] = {'value': manufacturer_id, 'hex': my_node.manufacturer_id}
	json_result['data']['vendorString'] = {'value': my_node.manufacturer_name}
	json_result['data']['manufacturerProductId'] = {'value': product_id, 'hex': my_node.product_id}
	json_result['data']['product_name'] = {'value': my_node.product_name}
	json_result['data']['location'] = {'value': my_node.location}
	json_result['data']['name'] = {'value': my_node.name}
	json_result['data']['version'] = {'value': my_node.version}
	json_result['data']['manufacturerProductType'] = {'value': product_type, 'hex': my_node.product_type}
	json_result['data']['neighbours'] = {'value': list(my_node.neighbors)}
	json_result['data']['isVirtual'] = {'value': ''}
	if globals.network.controller.node_id == node_id and my_node.basic == 1:
		json_result['data']['basicType'] = {'value': 2}
	else:
		json_result['data']['basicType'] = {'value': my_node.basic}
	json_result['data']['genericType'] = {'value': my_node.generic}
	json_result['data']['specificType'] = {'value': my_node.specific}
	json_result['data']['type'] = {'value': my_node.type}
	json_result['data']['state'] = {'value': str(my_node.query_stage)}
	json_result['data']['isAwake'] = {'value': my_node.is_awake, "updateTime": timestamp}
	json_result['data']['isReady'] = {'value': my_node.is_ready, "updateTime": timestamp}
	json_result['data']['isEnable'] = {'value': int(node_id) not in globals.disabled_nodes}
	json_result['data']['isInfoReceived'] = {'value': my_node.is_info_received}
	try:
		can_wake_up = my_node.can_wake_up()
	except RuntimeError:
		can_wake_up = False
	json_result['data']['can_wake_up'] = {'value': can_wake_up}
	json_result['data']['battery_level'] = {'value': my_node.get_battery_level()}
	json_result['last_notification'] = {}
	next_wake_up = None
	if node_id in globals.node_notifications:
		notification = globals.node_notifications[node_id]
		next_wake_up = notification.next_wake_up
		json_result['last_notification'] = {"receiveTime": notification.receive_time,"description": notification.description,"help": notification.help}
	json_result['data']['wakeup_interval'] = {'value': node_utils.get_wake_up_interval(node_id), 'next_wakeup': next_wake_up}
	json_result['data']['isFailed'] = {'value': my_node.is_failed}
	json_result['data']['isListening'] = {'value': my_node.is_listening_device}
	json_result['data']['isRouting'] = {'value': my_node.is_routing_device}
	json_result['data']['isSecurity'] = {'value': my_node.is_security_device}
	json_result['data']['isBeaming'] = {'value': my_node.is_beaming_device}
	json_result['data']['isFrequentListening'] = {'value': my_node.is_frequent_listening_device}
	json_result['data']['security'] = {'value': my_node.security}
	json_result['data']['lastReceived'] = {'updateTime': timestamp}
	json_result['data']['maxBaudRate'] = {'value': my_node.max_baud_rate}
	json_result['data']['is_enable'] = {'value': int(node_id) not in globals.disabled_nodes}
	json_result['data']['isZwavePlus'] = {'value': my_node.is_zwave_plus}
	statistics = globals.network.manager.getNodeStatistics(globals.network.home_id, node_id)
	send_total = statistics['sentCnt'] + statistics['sentFailed']
	percent_delivered = 0
	if send_total > 0:
		percent_delivered = (statistics['sentCnt'] * 100) / send_total
	average_request_rtt = statistics['averageRequestRTT']
	json_result['data']['statistics'] = {'total': send_total, 'delivered': percent_delivered,'deliveryTime': average_request_rtt}
	have_group = False
	query_stage_index = utils.convert_query_stage_to_int(my_node.query_stage)
	if my_node.groups and query_stage_index >= 12 and my_node.generic != 2:
		check_for_group = len(my_node.groups) > 0
		if check_for_group :
			have_group = check_primary_controller(my_node)
	else:
		check_for_group = False
	json_result['data']['is_groups_ok'] = {'value': have_group, 'enabled': check_for_group}
	is_neighbours_ok = query_stage_index > 13
	if my_node.generic == 1:
		is_neighbours_ok = False
	if my_node.generic == 8 and not my_node.is_listening_device:
		is_neighbours_ok = False
	json_result['data']['is_neighbours_ok'] = {'value': len(my_node.neighbors) > 0,'neighbors': len(my_node.neighbors), 'enabled': is_neighbours_ok}
	json_result['data']['is_manufacturer_specific_ok'] = {'value': my_node.manufacturer_id != 0 and my_node.product_id != 0 and my_node.product_type != 0,'enabled': query_stage_index >= 7} 
	is_secured = value_utils.get_value_by_label(node_id, COMMAND_CLASS_SECURITY, 1, 'Secured', False)
	json_result['data']['isSecured'] = {'value': is_secured is not None and is_secured.data, 'enabled' : is_secured is not None}
	pending_changes = 0
	json_result['instances'] = {"updateTime": timestamp}
	json_result['groups'] = {"updateTime": timestamp}
	for groupIndex in list(my_node.groups):
		group = my_node.groups[groupIndex]
		pending_state = 1
		if my_node.node_id in globals.pending_associations:
			pending_associations = globals.pending_associations[my_node.node_id]
			if groupIndex in pending_associations:
				pending_association = pending_associations[groupIndex]
				if pending_association.state is not None:
					pending_state = pending_association.state
					if pending_state is not None and pending_state > 1:
						pending_changes += 1
		json_result['groups'][groupIndex] = {"label": group.label, "maximumAssociations": group.max_associations,"associations": list(group.associations_instances),"pending": pending_state}
	json_result['associations'] = serialize_associations(node_id)
	if node_id in globals.node_notifications:
		notification = globals.node_notifications[node_id]
		json_result['last_notification'] = {"receiveTime": notification.receive_time,"code": notification.code,"description": notification.description,"help": notification.help,"next_wakeup": notification.next_wake_up}
	else:
		json_result['last_notification'] = {}
	json_result['command_classes'] = {}
	for command_class in my_node.command_classes:
		json_result['command_classes'][command_class] = {'name': my_node.get_command_class_as_string(command_class),'hex': '0x' + utils.convert_user_code_to_hex(command_class)}
	instances = []
	for val in my_node.get_values():
		my_value = my_node.values[val]
		if my_value.command_class is None or (my_value.instance > 1 and my_value.command_class in [COMMAND_CLASS_ZWAVEPLUS_INFO,COMMAND_CLASS_VERSION]):
			continue
		try:
			label = my_value.label
		except Exception, exception:
			label = exception.message
			logging.error('Value label contains unsupported text: %s' % (str(exception),))
		try:
			value_help = my_value.help
		except Exception, exception:
			value_help = exception.message
			logging.error('Value help contains unsupported text: %s' % (str(exception),))
		if label == 'Temperature' and my_value.units == 'F':
			value_units = 'C'
		else:
			value_units = my_value.units
		if my_value.genre != 'Basic':
			standard_type = utils.get_standard_value_type(my_value.type)
		else:
			standard_type = 'int'
		if my_value.is_write_only:
			value2 = None
		else:
			if my_value.type == 'Short':
				value2 = utils.normalize_short_value(my_value.data)
			else:
				value2 = value_utils.extract_data(my_value)
		instance2 = utils.change_instance(my_value)
		if my_value.index:
			index2 = my_value.index
		else:
			index2 = 0
		pending_state = None
		expected_data = None
		data_items = utils.concatenate_list(my_value.data_items)
		if my_value.id_on_network in globals.pending_configurations:
			pending = globals.pending_configurations[my_value.id_on_network]
			if pending is not None:
				pending_state = pending.state
				expected_data = pending.expected_data
				if pending_state is not None and pending_state > 1:
					pending_changes += 1
		try:
			timestamp = int(my_value.last_update)
		except TypeError:
			timestamp = int(1)
		if my_value.genre == 'User' and not my_value.instance in instances:
			instances.append(my_node.values[val].instance)
		if instance2 not in json_result['instances']:
			json_result['instances'][instance2] = {"updateTime": timestamp}
			json_result['instances'][instance2]['commandClasses'] = {"updateTime": timestamp}
			json_result['instances'][instance2]['commandClasses']['data'] = {"updateTime": timestamp}
			serialize_command_class_info(instance2, json_result, my_node, my_value, timestamp)
			serialize_command_class_data(data_items, expected_data, index2, instance2, json_result, label, my_value, pending_state, standard_type, timestamp, value2, value_help, value_units)
		elif my_value.command_class not in json_result['instances'][instance2]['commandClasses']:
			json_result['instances'][instance2]['commandClasses'][my_value.command_class] = {"updateTime": timestamp}
			serialize_command_class_info(instance2, json_result, my_node, my_value, timestamp)
			serialize_command_class_data(data_items, expected_data, index2, instance2, json_result, label, my_value,pending_state, standard_type, timestamp, value2, value_help, value_units)
		elif index2 not in json_result['instances'][instance2]['commandClasses'][my_value.command_class]['data']:
			serialize_command_class_data(data_items, expected_data, index2, instance2, json_result, label, my_value,pending_state, standard_type, timestamp, value2, value_help, value_units)
	json_result['data']['pending_changes'] = {'count': pending_changes}
	json_result['multi_instance'] = {'support': COMMAND_CLASS_MULTI_CHANNEL in my_node.command_classes,'instances': len(instances)}
	return json_result

def serialize_command_class_data(data_items, expected_data, index2, instance2, json_result, label, my_value,pending_state, standard_type, timestamp, value2, value_help, value_units):
	json_result['instances'][instance2]['commandClasses'][my_value.command_class]['data'][index2] = {"val": value2,
																									 "name": label,
																									 "help": value_help,
																									 "type": standard_type,
																									 "typeZW": my_value.type,
																									 "units": value_units,
																									 "data_items": data_items,
																									 "read_only": my_value.is_read_only,
																									 "write_only": my_value.is_write_only,
																									 "updateTime": timestamp,
																									 "genre": my_value.genre,
																									 "value_id": my_value.value_id,
																									 "poll_intensity": my_value.poll_intensity,
																									 "pendingState": pending_state,
																									 "expected_data": expected_data}


def serialize_command_class_info(instance2, json_result, my_node, my_value, timestamp):
	json_result['instances'][instance2]['commandClasses'][my_value.command_class] = {"name": my_node.get_command_class_as_string(my_value.command_class)}
	json_result['instances'][instance2]['commandClasses'][my_value.command_class]['data'] = {"updateTime": timestamp}

def check_primary_controller(my_node):
	for groupIndex in list(my_node.groups):
		group = my_node.groups[groupIndex]
		if len(group.associations_instances) > 0:
			for associations_instance in group.associations_instances:
				for node_instance in associations_instance:
					if globals.network.controller.node_id == node_instance:
						return True
					break
	return False

def serialize_controller_to_json():
	json_result = {'data': {}}
	json_result['data']['roles'] = {'isPrimaryController': globals.network.controller.is_primary_controller, 'isStaticUpdateController': globals.network.controller.is_static_update_controller, 'isBridgeController': globals.network.controller.is_bridge_controller}
	json_result['data']['nodeId'] = {'value': globals.network.controller.node_id}
	json_result['data']['mode'] = {'value': network_utils.get_network_mode()}
	json_result['data']['softwareVersion'] = {'ozw_library': globals.network.controller.ozw_library_version, 'python_library': globals.network.controller.python_library_version}
	json_result['data']['notification'] = globals.network_information.last_controller_notifications[0]
	json_result['data']['isBusy'] = {"value": globals.network_information.controller_is_busy}
	json_result['data']['networkstate'] = {"value": globals.network.state}
	return json_result

def serialize_associations(node_id):
	json_result = {}
	for other_node_id in list(globals.network.nodes):
		other_node = globals.network.nodes[other_node_id]
		if other_node.groups:
			for group in list(other_node.groups):
				if node_id in other_node.groups[group].associations:
					value = {'index': other_node.groups[group].index, 'label': other_node.groups[group].label}
					try:
						json_result[other_node_id].append(value)
					except KeyError:
						json_result[other_node_id] = [value]
	return json_result

def changes_value_polling(intensity, value):
	if intensity == 0:  # disable the value polling for any value
		if value.poll_intensity > 0:
			value.disable_poll()
	elif value.genre == "User" and not value.is_write_only:  # we activate the value polling only on user genre value and is not a writeOnly
		if intensity > globals.maximum_poll_intensity:
			intensity = globals.maximum_poll_intensity
		value.enable_poll(intensity)

def set_value(node_id, value_id, data):
	utils.check_node_exist(node_id)
	logging.debug("set a value for nodeId:%s valueId:%s data:%s" % (node_id, value_id, data,))
	my_node = globals.network.nodes[node_id]
	if not my_node.is_ready:
		return utils.format_json_result(False, 'The node must be Ready', 'debug')
	for value in my_node.get_values():
		if value == value_id:
			zwave_value = my_node.values[value]
			# cast data in desired type
			data = zwave_value.check_data(data=data)
			if data is None:
				return jsonify({'result': False, 'reason': 'cant convert in desired dataType'})
			my_result = globals.network.manager.setValue(zwave_value.value_id, data)
			if my_result == 0:
				result_message = 'fails'
			elif my_result == 1:
				result_message = 'succeed'
			elif my_result == 2:
				result_message = 'fails (valueId not exist)'
			else:
				result_message = 'fails (unknown error)'
			if my_result == 1:
				return utils.format_json_result()
			return utils.format_json_result(False, result_message, 'warning')
	return utiils.format_json_result(False, 'valueId not exist', 'warning')

refresh_workers = {}

def create_worker(node_id, value_id, target_value, starting_value, counter, motor):
	# create a new refresh worker
	refresh_interval = globals.refresh_interval
	if motor :
		# a full operation take time, wait longer on each refresh
		refresh_interval = globals.refresh_interval * 5
	worker = threading.Timer(interval=refresh_interval, function=refresh_background,
							 args=(node_id, value_id, target_value, starting_value, counter, motor))
	# save worker
	refresh_workers[value_id] = worker
	# start refresh timer
	worker.start()

def prepare_refresh(node_id, value_id, target_value=None, motor=False):
	if globals.suppress_refresh:
		return
	# logging.debug("prepare_refresh for nodeId:%s valueId:%s data:%s" % (node_id, value_id, target_value,))
	stop_refresh(node_id, value_id)
	starting_value = globals.network.nodes[node_id].values[value_id].data
	create_worker(node_id, value_id, target_value, starting_value, 0, motor)
	globals.network.nodes[node_id].values[value_id].start_refresh_time = int(time.time())

def refresh_background(node_id, value_id, target_value, starting_value, counter, motor):
	do_refresh = True
	actual_value = globals.network.nodes[node_id].values[value_id].data
	if target_value is not None:
		if isinstance(target_value, basestring):
			# color CC test
			actual_value = actual_value.lower()
			target_value = target_value.lower()
			do_refresh = actual_value != target_value
			# if do_refresh:
			# logging.debug("delta %s: %s" % (actual_value, target_value,))
		else:
			# check if target is reported
			delta = abs(actual_value - target_value)
			# logging.debug("delta for nodeId:%s valueId:%s is: %s" % (node_id, value_id, delta,))
			if delta < 2:
				# if delta is too small don't refresh
				do_refresh = False
				# logging.debug("delta is too small don't refresh")
	if do_refresh:
		# logging.debug("check for changes, actual: %s , starting: %s (retry %s)" % (actual_value, starting_value, counter,))
		# check if won't changes
		if starting_value == actual_value:
			counter += 1
			if counter > 2:
				do_refresh = False
		else:
			counter = 0
			starting_value = actual_value
	if do_refresh:
		# logging.debug("refresh")
		globals.network.nodes[node_id].values[value_id].refresh()
		# check if someone stop this refresh or we reach the timeout
		timeout = int(time.time()) - globals.network.nodes[node_id].values[value_id].start_refresh_time
		if timeout < globals.refresh_timeout:
			# I will start again a refresh timer
			create_worker(node_id, value_id, target_value, starting_value, counter, motor)
	else:
		# remove worker the flag is set
		del refresh_workers[value_id]

def stop_refresh(node_id, value_id):
	# check if for a existing worker
	worker = refresh_workers.get(value_id)
	if worker is not None:
		# logging.debug("Stop the timer")
		# Stop the timer, and cancel the execution of the timer action. This will only work if the timer is still in its waiting stage.
		worker.cancel()
		# remove worker
		del refresh_workers[value_id]
	# reset start time if refresh is running to avoid start again
	globals.network.nodes[node_id].values[value_id].start_refresh_time = 0

def refresh_switch_binary(node_id, value_id, target_value):
	if node_id in globals.network.nodes:
		my_value = globals.network.nodes[node_id].values[value_id]
		if my_value is not None:
			if my_value.data != target_value:
				logging.debug("Force refresh switch binary")
				my_value.refresh()

def send_command_zwave(_node_id, _cc_id, _instance_id, _index, _value):
	logging.info("Send command to "+str(_node_id)+" on "+str(_cc_id)+" instance "+str(_instance_id)+" index "+str(_index)+" value "+str(_value))
	utils.check_node_exist(_node_id)
	if _cc_id == hex(COMMAND_CLASS_NO_OPERATION):
		return test_node(_node_id, 1)
	if _cc_id == str(COMMAND_CLASS_WAKE_UP):
		arr = _value.split(",")
		wake_up_time = int(arr[0])
		return set_wake_up(_node_id, wake_up_time)
	if _cc_id == '0x85':
		arr = _value.split(",")
		group = int(arr[0])
		target_node = int(arr[1])
		try:
			return add_assoc(_node_id, group, target_node)
		except ValueError:
			raise Exception('Node is not Ready for associations')
	for val in globals.network.nodes[_node_id].get_values(class_id=int(_cc_id, 16), genre='All', type='All', readonly='All', writeonly='All'):
		if globals.network.nodes[_node_id].values[val].instance - 1 == _instance_id and (_index is None or globals.network.nodes[_node_id].values[val].index == _index):
			if _cc_id == hex(COMMAND_CLASS_SWITCH_MULTILEVEL) and _value > 99:
				logging.debug("Switch light ON to dim level that was last known")
				_value = 255
			globals.network.nodes[_node_id].values[val].data = _value
			if globals.network.nodes[_node_id].values[val].genre == 'System':
				if globals.network.nodes[_node_id].values[val].type == 'Bool':
					if _value == 0:
						_value = False
					else:
						_value = True
				mark_pending_change(globals.network.nodes[_node_id].values[val], _value)
			if _cc_id == hex(COMMAND_CLASS_SWITCH_MULTILEVEL) and _value <= 99:
				prepare_refresh(_node_id, val, _value, utils.is_motor(_node_id))
			if int(_cc_id, 16) == COMMAND_CLASS_THERMOSTAT_SETPOINT:
				logging.debug("COMMAND_CLASS_THERMOSTAT_SETPOINT")
				node_utils.save_node_value_event(_node_id, int(time.time()), COMMAND_CLASS_THERMOSTAT_SETPOINT, _index, utils.get_standard_value_type(globals.network.nodes[_node_id].values[val].type), _value, _instance_id + 10)
			if _cc_id == hex(COMMAND_CLASS_SWITCH_BINARY):
				if _value == 0:
					_value = False
				else:
					_value = True
				worker = threading.Timer(interval=0.5, function=refresh_switch_binary, args=(_node_id, val, _value))
				worker.start()
			return True
	raise Exception('Value not found')

def set_config(_node_id, _index_id, _value, _size):
	if globals.network_information.controller_is_busy:
		raise Exception('Controller is bussy')
	utils.check_node_exist(_node_id)
	logging.info('Set_config for nodeId : '+str(_node_id)+' index : '+str(_index_id)+', value : '+str(_value)+', size : '+str(_size))	
	if type(_value) == str:
		for value_id in globals.network.nodes[_node_id].get_values(class_id=COMMAND_CLASS_CONFIGURATION, genre='All', type='All', readonly='All', writeonly='All'):
			if globals.network.nodes[_node_id].values[value_id].index == _index_id:
				_value = _value.replace("@", "/")
				my_value = globals.network.nodes[_node_id].values[value_id]
				if my_value.type == 'Button':
					if _value.lower() == 'true':
						globals.network.manager.pressButton(my_value.value_id)
					else:
						globals.network.manager.releaseButton(my_value.value_id)
				elif my_value.type == 'List':
					globals.network.manager.setValue(value_id, _value)
					mark_pending_change(my_value, _value)
				elif my_value.type == 'Bool':
					if _value.lower() == 'true':
						_value = True
					else:
						_value = False
					globals.network.manager.setValue(value_id, _value)
					mark_pending_change(my_value, _value)
				return
			raise Exception('Configuration index : '+str(_index_id)+' not found')
	if _size == 0:
		_size = 2
	if _size > 4:
		_size = 4
	_value = int(_value)
	my_value = value_utils.get_value_by_index(_node_id, COMMAND_CLASS_CONFIGURATION, 1, _index_id)
	result = globals.network.nodes[_node_id].set_config_param(_index_id, _value, _size)
	if my_value is not None and my_value.type != 'List':
		mark_pending_change(my_value, _value)
	return result

'''
default routes
'''

@app.errorhandler(Exception)
def all_exception_handler(error):
	return utils.format_json_result(False, str(error))

@app.before_first_request
def _run_on_start():
	pass

@app.route('/', methods=['GET'])
def default_index():
	with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'index.html')), 'rb') as f:
		content = f.read()
	return content


@app.errorhandler(400)
def not_found400(error):
	logging.error('%s %s' % (error, request.url))
	return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(404)
def not_found404(error):
	logging.error('%s %s' % (error, request.url))
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.teardown_appcontext
def close_network(error):
	if error is not None:
		logging.error('%s %s' % (error, 'teardown'))

@app.errorhandler(Exception)
def unhandled_exception(exception):
	message = 'Unhandled Exception: %s' % (exception.message,)
	logging.info(message)
	return make_response(jsonify({'error': message}), 500)

@auth.verify_password
def verify_password(username, password):
	return password == globals.apikey

'''
devices routes
'''

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[0].commandClasses[133].Get()', methods=['GET'])
@auth.login_required
def refresh_assoc(node_id):
	utils.check_node_exist(node_id)
	logging.debug("refresh_assoc for nodeId: %s" % (node_id,))
	for val in globals.network.nodes[node_id].get_values(class_id=COMMAND_CLASS_ASSOCIATION):
		globals.network.nodes[node_id].values[val].refresh()
	return utils.format_json_result()
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[0].commandClasses[133].data', methods=['GET'])
@auth.login_required
def get_assoc(node_id):
	utils.check_node_exist(node_id)
	logging.debug("get_assoc for nodeId: %s" % (node_id,))
	config = {}
	if globals.network.nodes[node_id].groups:
		config['supported'] = {'value': True}
		for group in list(globals.network.nodes[node_id].groups):
			config[globals.network.nodes[node_id].groups[group].index] = {}
			config[globals.network.nodes[node_id].groups[group].index]['nodes'] = {'value': list(globals.network.nodes[node_id].groups[group].associations), 'updateTime': int(time.time()), 'invalidateTime': 0}
	return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[0].commandClasses[0x85].Remove(<int:group_index>,<int:target_node_id>)', methods=['GET'])
@auth.login_required
def remove_assoc(node_id, group_index, target_node_id):
	if globals.network_information.controller_is_busy:
		raise Exception('Controller is bussy')
	utils.check_node_exist(node_id)
	logging.info("remove_assoc to nodeId: %s in group %s with nodeId: %s" % (node_id, group_index, target_node_id,))
	my_node = globals.network.nodes[node_id]
	if my_node.node_id not in globals.pending_associations:
		globals.pending_associations[my_node.node_id] = dict()
	globals.pending_associations[my_node.node_id][group_index] = PendingAssociation(pending_added=None, pending_removed=target_node_id, timeout=0)
	globals.network.manager.removeAssociation(globals.network.home_id, node_id, group_index, target_node_id)
	return utils.format_json_result()
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[0].commandClasses[0x85].Add(<int:group_index>,<int:target_node_id>)', methods=['GET'])
@auth.login_required
def add_assoc(node_id, group_index, target_node_id):
	if globals.network_information.controller_is_busy:
		raise Exception('Controller is bussy')
	utils.check_node_exist(node_id)
	logging.info("add_assoc to nodeId: %s in group %s with nodeId: %s" % (node_id, group_index, target_node_id,))
	my_node = globals.network.nodes[node_id]
	if not (target_node_id in my_node.groups[group_index].associations):
		if my_node.node_id not in globals.pending_associations:
			globals.pending_associations[my_node.node_id] = dict()
	globals.pending_associations[my_node.node_id][group_index] = PendingAssociation(pending_added=target_node_id, pending_removed=None, timeout=0)
	globals.network.manager.addAssociation(globals.network.home_id, node_id, group_index, target_node_id)
	return utils.format_json_result()

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].Associations[<int:group_index>].Remove(<int:target_node_id>,<int:target_node_instance>)', methods=['GET'])
@auth.login_required
def remove_association(node_id, group_index, target_node_id, target_node_instance):
	if globals.network_information.controller_is_busy:
		raise Exception('Controller is bussy')
	utils.check_node_exist(node_id)
	logging.info("remove_association to nodeId: %s in group %s with nodeId: %s instance %s" % (node_id, group_index, target_node_id, target_node_instance,))
	my_node = globals.network.nodes[node_id]
	if my_node.node_id not in globals.pending_associations:
		globals.pending_associations[my_node.node_id] = dict()
	globals.pending_associations[my_node.node_id][group_index] = PendingAssociation(pending_added=None, pending_removed=target_node_id, timeout=0)
	globals.network.manager.removeAssociation(globals.network.home_id, node_id, group_index, target_node_id, target_node_instance)
	return utils.format_json_result()
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].Associations[<int:group_index>].Add(<int:target_node_id>,<int:target_node_instance>)', methods=['GET'])
@auth.login_required
def add_association(node_id, group_index, target_node_id, target_node_instance):
	if globals.network_information.controller_is_busy:
		raise Exception('Controller is bussy')
	utils.check_node_exist(node_id)
	logging.info("add_association to nodeId: %s in group %s with nodeId: %s instance %s" % (
	node_id, group_index, target_node_id, target_node_instance,))
	my_node = globals.network.nodes[node_id]
	if not (target_node_id in my_node.groups[group_index].associations):
		if my_node.node_id not in globals.pending_associations:
			globals.pending_associations[my_node.node_id] = dict()
	globals.pending_associations[my_node.node_id][group_index] = PendingAssociation(pending_added=target_node_id, pending_removed=None, timeout=0)
	globals.network.manager.addAssociation(globals.network.home_id, node_id, group_index, target_node_id, target_node_instance)
	return utils.format_json_result()
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].SetPolling(<int:value_id>,<frequency>)', methods=['GET'])
@auth.login_required
def set_polling2(node_id, value_id, frequency):
	utils.check_node_exist(node_id)
	logging.info("set_polling for nodeId: %s ValueId %s at: %s" % (node_id, value_id, frequency,))
	my_node = globals.network.nodes[node_id]
	for val in my_node.get_values():
		my_value = my_node.values[val]
		if my_value.value_id == value_id:
			changes_value_polling(frequency, my_value)
			for value_id in my_node.get_values(class_id=my_value.command_class):
				if my_node.values[value_id].instance == my_value.instance and my_node.values[
					value_id].index != my_value.index_id:
					changes_value_polling(0, value_id)
			return utils.format_json_result()
	return utils.format_json_result(False, 'valueId: %s not found' % (value_id,), 'warning')
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].SetPolling(<int:frequency>)', methods=['GET'])
@auth.login_required
def set_polling_value(node_id, instance_id, cc_id, index, frequency):
	utils.check_node_exist(node_id)
	logging.info("set_polling_value for nodeId: %s instance: %s cc:%s index:%s at: %s" % (node_id, instance_id, cc_id, index, frequency,))
	for val in globals.network.nodes[node_id].get_values(class_id=int(cc_id, 16)):
		if globals.network.nodes[node_id].values[val].instance - 1 == instance_id:
			my_value = globals.network.nodes[node_id].values[val]
			if frequency == 0 & my_value.poll_intensity > 0:
				my_value.disable_poll()
			else:
				if globals.network.nodes[node_id].values[val].index == index:
					changes_value_polling(frequency, my_value)
				else:
					if my_value.poll_intensity > 0:
						my_value.disable_poll()
	write_config()
	return utils.format_json_result()

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].SetPolling(<int:frequency>)', methods=['GET'])
@auth.login_required
def set_polling_instance(node_id, instance_id, cc_id, frequency):
	utils.check_node_exist(node_id)
	logging.info("set_polling_instance for nodeId: %s instance: %s cc:%s at: %s" % (node_id, instance_id, cc_id, frequency,))
	polling_apply = False
	for val in globals.network.nodes[node_id].get_values(class_id=int(cc_id, 16)):
		if globals.network.nodes[node_id].values[val].instance - 1 == instance_id:
			my_value = globals.network.nodes[node_id].values[val]
			if frequency == 0 & my_value.poll_intensity > 0:
				my_value.disable_poll()
			else:
				if not polling_apply:
					polling_apply = True
					changes_value_polling(frequency, my_value)
				else:
					if my_value.poll_intensity > 0:
						my_value.disable_poll()
	write_config()
	return utils.format_json_result()
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].SetWakeup(<wake_up_time>)', methods=['GET'])
@auth.login_required
def set_wake_up(node_id, wake_up_time):
	utils.check_node_exist(node_id)
	logging.info("set wakeup interval for nodeId %s at: %s" % (node_id, wake_up_time,))
	for val in globals.network.nodes[node_id].get_values(class_id=COMMAND_CLASS_WAKE_UP):
		my_value = globals.network.nodes[node_id].values[val]
		if my_value.label == "Wake-up Interval":
			return utils.format_json_result(set_value(node_id, my_value.value_id, int(wake_up_time)))
	return utils.format_json_result(False, 'Wake-up Interval not found', 'warning')
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].Refresh()', methods=['GET'])
@auth.login_required
def request_all_config_params(node_id):
	utils.check_node_exist(node_id)
	logging.info("Request the values of all known configurable parameters from nodeId %s" % (node_id,))
	for val in globals.network.nodes[node_id].get_values(class_id=COMMAND_CLASS_CONFIGURATION):
		configuration_item = globals.network.nodes[node_id].values[val]
		if configuration_item.id_on_network in globals.pending_configurations:
			del globals.pending_configurations[configuration_item.id_on_network]
	globals.network.manager.requestAllConfigParams(globals.network.home_id, node_id)
	return utils.format_json_result()
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].Get(<int:index_id>)', methods=['GET'])
@auth.login_required
def refresh_config(node_id, index_id):
	utils.check_node_exist(node_id)
	logging.debug("refresh_config for nodeId:%s index_id:%s" % (node_id, index_id,))
	for val in globals.network.nodes[node_id].get_values(class_id=COMMAND_CLASS_CONFIGURATION):
		if globals.network.nodes[node_id].values[val].index == index_id:
			globals.network.nodes[node_id].values[val].refresh()
	return utils.format_json_result()
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].SetDeviceName(<string:location>,<string:name>,<int:is_enable>)', methods=['GET'])
@auth.login_required
def set_device_name(node_id, location, name, is_enable):
	utils.check_node_exist(node_id)
	logging.info("set_device_name node_id:%s new name ; '%s'. Is enable: %s" % (node_id, name, is_enable,))
	if node_id in globals.disabled_nodes and is_enable:
		globals.disabled_nodes.remove(node_id)
	elif node_id not in globals.disabled_nodes and not is_enable:
		globals.disabled_nodes.append(node_id)
	name = name.encode('utf8')
	name = name.replace('+', ' ')
	globals.network.nodes[node_id].set_field('name', name)
	location = location.encode('utf8')
	location = location.replace('+', ' ')
	globals.network.nodes[node_id].set_field('location', location)
	return utils.format_json_result()

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].data', methods=['GET'])
@auth.login_required
def get_config(node_id):
	utils.check_node_exist(node_id)
	logging.debug("get_config for nodeId:%s" % (node_id,))
	config = {}
	for val in globals.network.nodes[node_id].values:
		list_values = []
		my_value = globals.network.nodes[node_id].values[val]
		if my_value.command_class == COMMAND_CLASS_CONFIGURATION:
			config[globals.network.nodes[node_id].values[val].index] = {}
			if my_value.type == "List" and not my_value.is_read_only:
				result_data = globals.network.manager.getValueListSelectionNum(my_value.value_id)
				values = my_value.data_items
				for index_item, value_item in enumerate(values):
					list_values.append(value_item)
					if value_item == my_value.data_as_string:
						result_data = index_item
			elif my_value.type == "Bool" and not my_value.data:
				result_data = 0
			elif my_value.type == "Bool" and my_value.data:
				result_data = 1
			else:
				result_data = my_value.data
			config[my_value.index]['val'] = {'value2': my_value.data, 'value': result_data,'value3': my_value.label, 'value4': sorted(list_values),'updateTime': int(time.time()), 'invalidateTime': 0}
	return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:source_id>].CopyConfigurations(<int:target_id>)', methods=['GET'])
@auth.login_required
def copy_configuration(source_id, target_id):
	if globals.network_information.controller_is_busy:
		raise Exception('Controller is bussy')
	logging.info("copy_configuration from source_id:%s to target_id:%s" % (source_id, target_id,))
	items = 0
	utils.check_node_exist(source_id)
	utils.check_node_exist(target_id)
	source = globals.network.nodes[source_id]
	target = globals.network.nodes[target_id]
	if source.manufacturer_id == target.manufacturer_id and source.product_type == target.product_type and source.product_id == target.product_id:
		for val in source.get_values():
			configuration_value = source.values[val]
			if configuration_value.genre == 'Config':
				if configuration_value.type == 'Button':
					continue
				if configuration_value.is_write_only:
					continue
				try:
					target_value = value_utils.get_value_by_index(target_id, COMMAND_CLASS_CONFIGURATION, 1,configuration_value.index)
					if target_value is not None:
						if configuration_value.type == 'List':
							globals.network.manager.setValue(target_value.value_id, configuration_value.data)
							accepted = True
						else:
							accepted = target.set_config_param(configuration_value.index,configuration_value.data)
						if accepted:
							items += 1
							mark_pending_change(target_value, configuration_value.data)
				except Exception as error:
					logging.error('Copy configuration %s (index:%s): %s' % (
					configuration_value.label, configuration_value.index, str(error),))
		my_result = items != 0
	else:
		return utils.format_json_result(False,'The two nodes must be with same: manufacturer_id, product_type and product_id','warning')
	return jsonify({'result': my_result, 'copied_configuration_items': items})

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[0x70].data[<int:index_id2>].Set(<int:index_id>,<string:value>,<int:size>)', methods=['GET'])
@auth.login_required
def set_config5(node_id, instance_id, index_id2, index_id, value, size):
	return utils.format_json_result(set_config(node_id, index_id, value, size))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[0x70].data[<int:index_id2>].Set(<int:index_id>,<float:value>,<int:size>)', methods=['GET'])
@auth.login_required
def set_config6(node_id, instance_id, index_id2, index_id, value, size):
	return utils.format_json_result(set_config(node_id, index_id, value, size))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[0x70].data[<int:index_id2>].Set(<int:index_id>,<int:value>,<int:size>)', methods=['GET'])
@auth.login_required
def set_config4(node_id, instance_id, index_id2, index_id, value, size):
	return utils.format_json_result(set_config(node_id, index_id, value, size))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].Set(<int:index_id>,<string:value>,<int:size>)', methods=['GET'])
@auth.login_required
def set_config2(node_id, index_id, value, size):
	return utils.format_json_result(set_config(node_id, index_id, value, size))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].Set(<int:index_id>,<float:value>,<int:size>)', methods=['GET'])
@auth.login_required
def set_config3(node_id, index_id, value, size):
	return utils.format_json_result(set_config(node_id, index_id, value, size))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].Set(<int:index_id>,<int:value>,<int:size>)', methods=['GET'])
@auth.login_required
def set_config1(node_id, index_id, value, size):
	return utils.format_json_result(set_config(node_id, index_id, value, size))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses', methods=['GET'])
@auth.login_required
def get_command_classes(node_id):
	my_result = {}
	logging.debug("get_command_classes for nodeId:%s" % (node_id,))
	utils.check_node_exist(node_id)
	for val in globals.network.nodes[node_id].get_values():
		my_result[globals.network.nodes[node_id].values[val].command_class] = {}
	return jsonify(my_result)

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].RequestNodeDynamic()', methods=['GET'])
@auth.login_required
def request_node_dynamic(node_id):
	utils.check_node_exist(node_id)
	globals.network.manager.requestNodeDynamic(globals.network.home_id, node_id)
	globals.network.nodes[node_id].last_update = time.time()
	logging.info("Fetch the dynamic command class data for the node %s" % (node_id,))
	return utils.format_json_result()

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].Get()', methods=['GET'])
@auth.login_required
def get_value(node_id, instance_id, cc_id):
	utils.check_node_exist(node_id)
	try:
		globals.network.nodes[node_id].last_update
	except NameError:
		globals.network.nodes[node_id].last_update = time.time()
	now = datetime.datetime.now()
	if isinstance(globals.network.nodes[node_id].last_update, float):
		last_update = datetime.datetime.fromtimestamp(globals.network.nodes[node_id].last_update)
	else:
		last_update = datetime.datetime.now()
		globals.network.nodes[node_id].last_update = time.time()
	last_delta = last_update + datetime.timedelta(seconds=30)
	if now > last_delta and globals.network.nodes[node_id].is_listening_device and globals.network.nodes[node_id].is_ready:
		globals.network.manager.requestNodeDynamic(globals.network.home_id, globals.network.nodes[node_id].node_id)
		globals.network.nodes[node_id].last_update = time.time()
		logging.debug("Fetch the dynamic command class data for the node %s" % (node_id,))
	return utils.format_json_result()

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].val', methods=['GET'])
@auth.login_required
def get_value6(node_id, instance_id, index, cc_id):
	utils.check_node_exist(node_id)
	for val in globals.network.nodes[node_id].get_values(class_id=int(cc_id, 16)):
		if globals.network.nodes[node_id].values[val].instance - 1 == instance_id and globals.network.nodes[node_id].values[
			val].index == index:
			if globals.network.nodes[node_id].values[val].units == 'F':
				return str(utils.convert_fahrenheit_celsius(globals.network.nodes[node_id].values[val]))
			else:
				return str(globals.network.nodes[node_id].values[val].data)
	return jsonify({})

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].ForceRefresh()', methods=['GET'])
@auth.login_required
def force_refresh_one_value(node_id, instance_id, index, cc_id):
	return refresh_one_value(node_id, instance_id, index, int(cc_id, 16))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<int:cc_id>].data[<int:index>].Refresh()', methods=['GET'])
@auth.login_required
def refresh_one_value(node_id, instance_id, index, cc_id):
	utils.check_node_exist(node_id)
	for val in globals.network.nodes[node_id].get_values(class_id=cc_id):
		if globals.network.nodes[node_id].values[val].instance - 1 == instance_id and globals.network.nodes[node_id].values[val].index == index:
			globals.network.nodes[node_id].values[val].refresh()
			return utils.format_json_result()
	return utils.format_json_result(False, 'This device does not contain the specified value', 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[0x63].data[<int:index>].code', methods=['GET'])
@auth.login_required
def get_user_code(node_id, instance_id, index):
	utils.check_node_exist(node_id)
	logging.debug("getValueRaw nodeId:%s instance:%s commandClasses:%s index:%s" % (
	node_id, instance_id, hex(COMMAND_CLASS_USER_CODE), index))
	my_result = {}
	my_node = globals.network.nodes[node_id]
	for val in my_node.get_values(class_id=COMMAND_CLASS_USER_CODE):
		my_value = my_node.values[val]
		if my_value.instance - 1 == instance_id and my_value.index == index:
			user_code = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			timestamp = int(1)
			raw_data = value_utils.extract_data(my_value)
			if raw_data != '00000000000000000000':
				try:
					timestamp = int(my_value.last_update)
					chunks, chunk_size = len(raw_data), len(raw_data) / 10
					user_code = [int(raw_data[i:i + chunk_size], 16) for i in range(0, chunks, chunk_size)]
				except TypeError:
					timestamp = int(1)
			my_result = {'invalidateTime': int(time.time() - datetime.timedelta(seconds=30).total_seconds()), 'type': utils.get_standard_value_type(my_value.type),'value': user_code,'updateTime': timestamp}
			break
	return jsonify(my_result)

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[0x63].data', methods=['GET'])
@auth.login_required
def get_user_codes(node_id, instance_id):
	utils.check_node_exist(node_id)
	logging.debug("getValueAllRaw nodeId:%s instance:%s commandClasses:%s" % (node_id, instance_id, hex(COMMAND_CLASS_USER_CODE),))
	result_value = {}
	my_node = globals.network.nodes[node_id]
	for val in my_node.get_values(class_id=COMMAND_CLASS_USER_CODE):
		my_value = my_node.values[val]
		if my_value.instance - 1 == instance_id:
			if my_value.index == 0:
				continue
			if my_value.index > 10:
				continue
			raw_data = value_utils.extract_data(my_value)
			if raw_data == '00000000000000000000':
				result_value[my_value.index] = None
			else:
				result_value[my_value.index] = {}
	return jsonify(result_value)

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].UserCode.SetRaw(<int:slot_id>,[<string:value>],1)', methods=['GET'])
@auth.login_required
def set_user_code(node_id, slot_id, value):
	utils.check_node_exist(node_id)
	logging.info("set_user_code nodeId:%s slot:%s user code:%s" % (node_id, slot_id, value,))
	result_value = {}
	for val in globals.network.nodes[node_id].get_values(class_id=COMMAND_CLASS_USER_CODE):
		if globals.network.nodes[node_id].values[val].index == slot_id:
			result_value['data'] = {}
			original_value = value
			value = binascii.a2b_hex(value)
			globals.network.nodes[node_id].values[val].data = value
			result_value['data'][val] = {'device': node_id, 'slot': slot_id, 'val': original_value}
			return jsonify(result_value)
	return jsonify(result_value)

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[0].commandClasses[0x63].SetRaw(<int:slot_id>,[<value1>,<value2>,<value3>,<value4>,<value5>,<value6>,<value7>,<value8>,<value9>,<value10>],1)', methods=['GET'])
@auth.login_required
def set_user_code2(node_id, slot_id, value1, value2, value3, value4, value5, value6, value7, value8, value9, value10):
	utils.check_node_exist(node_id)
	logging.info("set_user_code2 nodeId:%s slot:%s user code:%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (node_id, slot_id, value1, value2, value3, value4, value5, value6, value7, value8, value9, value10,))
	result_value = {}
	for val in globals.network.nodes[node_id].get_values(class_id=COMMAND_CLASS_USER_CODE):
		if globals.network.nodes[node_id].values[val].index == slot_id:
			result_value['data'] = {}
			value = utils.convert_user_code_to_hex(value1) + utils.convert_user_code_to_hex(value2) + utils.convert_user_code_to_hex(value3) + utils.convert_user_code_to_hex(value4) + utils.convert_user_code_to_hex(value5) + utils.convert_user_code_to_hex(value6) + utils.convert_user_code_to_hex(value7) + utils.convert_user_code_to_hex(value8) + utils.convert_user_code_to_hex(value9) + utils.convert_user_code_to_hex(value10)
			original_value = value
			value = binascii.a2b_hex(value)
			globals.network.nodes[node_id].values[val].data = value
			result_value['data'][val] = {'device': node_id, 'slot': slot_id, 'val': original_value}
			return jsonify(result_value)
	return jsonify(result_value)

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].Set(<float:value>)', methods=['GET'])
@auth.login_required
def set_value8(node_id, instance_id, cc_id, index, value):
	return utils.format_json_result(True, send_command_zwave(node_id, cc_id, instance_id, index, value))
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].Set(<string:value>)', methods=['GET'])
@auth.login_required
def set_value6(node_id, instance_id, cc_id, value):
	return utils.format_json_result(True, send_command_zwave(node_id, cc_id, instance_id, None, value))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].Set(<int:value>)', methods=['GET'])
@auth.login_required
def set_value7(node_id, instance_id, cc_id, index, value):
	return utils.format_json_result(True, send_command_zwave(node_id, cc_id, instance_id, index, value))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].Set(<string:value>)', methods=['GET'])
@auth.login_required
def set_value9(node_id, instance_id, cc_id, index, value):
	return utils.format_json_result(True, send_command_zwave(node_id, cc_id, instance_id, index, value))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].GetColor()', methods=['GET'])
@auth.login_required
def get_color(node_id):
	utils.check_node_exist(node_id)
	logging.debug("get_color nodeId:%s" % (node_id,))
	my_result = {}
	red_level = 0
	green_level = 0
	blue_level = 0
	white_level = 0
	for val in globals.network.nodes[node_id].get_values(class_id=COMMAND_CLASS_SWITCH_MULTILEVEL, genre='User', type='Byte', readonly='All', writeonly=False):
		my_value = globals.network.nodes[node_id].values[val]
		if my_value.label != 'Level':
			continue
		if my_value.instance < 2:
			continue
		if my_value.instance == 3:
			red_level = utils.convert_level_to_color(my_value.data)
		elif my_value.instance == 4:
			green_level = utils.convert_level_to_color(my_value.data)
		elif my_value.instance == 5:
			blue_level = utils.convert_level_to_color(my_value.data)
		elif my_value.instance == 6:
			white_level = utils.convert_level_to_color(my_value.data)
	my_result['data'] = {'red': red_level, 'green': green_level, 'blue': blue_level, 'white': white_level}
	return jsonify(my_result)

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].SetColor(<int:red_level>,<int:green_level>,<int:blue_level>,<int:white_level>)', methods=['GET'])
@auth.login_required
def set_color(node_id, red_level, green_level, blue_level, white_level):
	utils.check_node_exist(node_id)
	logging.info("set_color nodeId:%s red:%s green:%s blue:%s white:%s" % (node_id, red_level, green_level, blue_level, white_level,))
	my_result = False
	intensity_value = None
	red_value = None
	green_value = None
	blue_value = None
	for val in globals.network.nodes[node_id].get_values(class_id=COMMAND_CLASS_SWITCH_MULTILEVEL, genre='User', type='Byte', readonly='All', writeonly=False):
		my_value = globals.network.nodes[node_id].values[val]
		if my_value.label != 'Level':
			continue
		if my_value.instance == 2:
			continue
		if my_value.instance == 1:
			intensity_value = val
		elif my_value.instance == 3:
			red_value = val
			my_value.data = utils.convert_color_to_level(red_level)
		elif my_value.instance == 4:
			green_value = val
			my_value.data = utils.convert_color_to_level(green_level)
		elif my_value.instance == 5:
			blue_value = val
			my_value.data = utils.convert_color_to_level(blue_level)
		elif my_value.instance == 6:
			my_value.data = utils.convert_color_to_level(white_level)
	if red_value is not None and green_value is not None and blue_value is not None:
		prepare_refresh(node_id, intensity_value, None)
		my_result = True
	return utils.format_json_result(my_result)

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].PressButton()', methods=['GET'])
@auth.login_required
def press_button(node_id, instance_id, cc_id, index):
	utils.check_node_exist(node_id)
	logging.info("press_button nodeId:%s, instance:%s, cc:%s, index:%s" % (node_id, instance_id, cc_id, index,))
	for val in globals.network.nodes[node_id].get_values(class_id=int(cc_id, 16), genre='All', type='All', readonly='All', writeonly='All'):
		if globals.network.nodes[node_id].values[val].instance - 1 == instance_id and globals.network.nodes[node_id].values[
			val].index == index:
			globals.network.manager.pressButton(globals.network.nodes[node_id].values[val].value_id)
			if cc_id == hex(COMMAND_CLASS_SWITCH_MULTILEVEL) and globals.network.nodes[node_id].values[val].label in ['Bright', 'Dim', 'Open', 'Close']:
				value = 1
				if globals.network.nodes[node_id].values[val].label in ['Bright', 'Open']:
					value = 99
				elif globals.network.nodes[node_id].values[val].label in ['Close']:
					value = 0
				value_level = value_utils.get_value_by_label(node_id, COMMAND_CLASS_SWITCH_MULTILEVEL,
                                                 globals.network.nodes[node_id].values[val].instance, 'Level')
				if value_level:
					prepare_refresh(node_id, value_level.value_id, value, utils.is_motor(node_id))
			return utils.format_json_result()
	return utils.format_json_result(False, 'button not found', 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].ReleaseButton()', methods=['GET'])
@auth.login_required
def release_button(node_id, instance_id, cc_id, index):
	utils.check_node_exist(node_id)
	for val in globals.network.nodes[node_id].get_values(class_id=int(cc_id, 16), genre='All', type='All', readonly='All', writeonly='All'):
		if globals.network.nodes[node_id].values[val].instance - 1 == instance_id and globals.network.nodes[node_id].values[
			val].index == index:
			globals.network.manager.releaseButton(globals.network.nodes[node_id].values[val].value_id)
			# stop refresh if running in background
			if cc_id == hex(COMMAND_CLASS_SWITCH_MULTILEVEL):
				value_level = value_utils.get_value_by_label(node_id, COMMAND_CLASS_SWITCH_MULTILEVEL,
                                                 globals.network.nodes[node_id].values[val].instance, 'Level')
				if value_level:
					stop_refresh(node_id, value_level.value_id)

			return utils.format_json_result()
	return utils.format_json_result(False, 'button not found', 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[0].commandClasses[0xF0].SwitchAll(<int:state>)', methods=['GET'])
@auth.login_required
def switch_all(node_id, state):
	if state == 0:
		logging.info("SwitchAll Off")
		globals.network.switch_all(False)
	else:
		logging.info("SwitchAll On")
		globals.network.switch_all(True)
	for node_id in globals.network.nodes:
		my_node = globals.network.nodes[node_id]
		if my_node.is_failed:
			continue
		value_ids = my_node.get_switches_all()
		if value_ids is not None and len(value_ids) > 0:
			for value_id in value_ids:
				if my_node.values[value_id].data == "Disabled":
					continue
				elif my_node.values[value_id].data == "On and Off Enabled":
					pass
				if my_node.values[value_id].data == "Off Enabled" and state != 0:
					continue
				if my_node.values[value_id].data == "On Enabled" and state == 0:
					continue
				for switch in my_node.get_switches():
					my_node.values[switch].refresh()
				for dimmer in my_node.get_dimmers():
					my_node.values[dimmer].refresh()
	return utils.format_json_result()

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].RequestNodeNeighbourUpdate()', methods=['GET'])
@auth.login_required
def request_node_neighbour_update(node_id):
	if not network_utils.can_execute_network_command():
		raise Exception('Controller is bussy')
	utils.check_node_exist(node_id,True)
	logging.info("request_node_neighbour_update for node %s" % (node_id,))
	return utils.format_json_result(globals.network.manager.requestNodeNeighborUpdate(globals.network.home_id, node_id), 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].RemoveFailedNode()', methods=['GET'])
@auth.login_required
def remove_failed_node(node_id):
	utils.check_node_exist(node_id)
	if not network_utils.can_execute_network_command(0):
		raise Exception('Controller is bussy')
	logging.info("Remove a failed node %s" % (node_id,))
	return utils.format_json_result(globals.network.manager.removeFailedNode(globals.network.home_id, node_id))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].HealNode()', methods=['GET'])
@auth.login_required
def heal_node(node_id, perform_return_routes_initialization=False):
	if not network_utils.can_execute_network_command():
		raise Exception('Controller is bussy')
	utils.check_node_exist(node_id,True)
	logging.info("Heal network node (%s) by requesting the node rediscover their neighbors" % (node_id,))
	globals.network.manager.healNetworkNode(globals.network.home_id, node_id, perform_return_routes_initialization)
	return utils.format_json_result()

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].AssignReturnRoute()', methods=['GET'])
@auth.login_required
def assign_return_route(node_id):
	if not network_utils.can_execute_network_command():
		raise Exception('Controller is bussy')
	utils.check_node_exist(node_id)
	logging.info("Ask Node (%s) to update its Return Route to the Controller" % (node_id,))
	return utils.format_json_result(globals.network.manager.assignReturnRoute(globals.network.home_id, node_id))
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>]', methods=['GET'])
def get_serialized_device(node_id):
	utils.check_node_exist(node_id)
	return jsonify(serialize_node_to_json(node_id))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].ReplaceFailedNode()', methods=['GET'])
@auth.login_required
def replace_failed_node(node_id):
	if not network_utils.can_execute_network_command():
		raise Exception('Controller is bussy')
	utils.check_node_exist(node_id,True)
	logging.info("replace_failed_node node %s" % (node_id,))
	return utils.format_json_result(globals.network.manager.replaceFailedNode(globals.network.home_id, node_id))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].SendNodeInformation()', methods=['GET'])
@auth.login_required
def send_node_information(node_id):
	if not network_utils.can_execute_network_command():
		raise Exception('Controller is bussy')
	utils.check_node_exist(node_id,True)
	logging.info("send_node_information node %s" % (node_id,))
	return utils.format_json_result(globals.network.manager.sendNodeInformation(globals.network.home_id, node_id))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].HasNodeFailed()', methods=['GET'])
@auth.login_required
def has_node_failed(node_id):
	if not network_utils.can_execute_network_command():
		raise Exception('Controller is bussy')
	utils.check_node_exist(node_id,True)
	logging.info("has_node_failed node %s" % (node_id,))
	return utils.format_json_result(globals.network.manager.hasNodeFailed(globals.network.home_id, node_id))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].RefreshNodeInfo()', methods=['GET'])
@auth.login_required
def refresh_node_info(node_id):
	if not network_utils.can_execute_network_command():
		raise Exception('Controller is bussy')
	utils.check_node_exist(node_id,True)
	logging.info("refresh_node_info node %s" % (node_id,))
	return utils.format_json_result(globals.network.manager.refreshNodeInfo(globals.network.home_id, node_id))
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].RefreshAllValues()', methods=['GET'])
@auth.login_required
def refresh_all_values(node_id):
	utils.check_node_exist(node_id,True)
	current_node = globals.network.nodes[node_id]
	counter = 0
	logging.info("refresh_all_values node %s" % (node_id,))
	for val in current_node.get_values():
		current_value = current_node.values[val]
		if current_value.type == 'Button':
			continue
		if current_value.is_write_only:
			continue
		current_value.refresh()
		counter += 1
	message = 'Refreshed values count: %s' % (counter,)
	return utils.format_json_result(True, message)

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].TestNode()', methods=['GET'])
@auth.login_required
def test_node(node_id=0, count=3):
	if not network_utils.can_execute_network_command():
		raise Exception('Controller is bussy')
	utils.check_node_exist(node_id,True)
	globals.network.manager.testNetworkNode(globals.network.home_id, node_id, count)
	return utils.format_json_result()
		
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].GetNodeStatistics()', methods=['GET'])
@auth.login_required
def get_node_statistics(node_id):
	utils.check_node_exist(node_id,True)
	query_stage_description = globals.network.manager.getNodeQueryStage(globals.network.home_id, node_id)
	query_stage_code = globals.network.manager.getNodeQueryStageCode(query_stage_description)
	return jsonify({'statistics': globals.network.manager.getNodeStatistics(globals.network.home_id, node_id), 'queryStageCode': query_stage_code, 'queryStageDescription': query_stage_description})

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].RemoveDeviceZWConfig(<int:identical>)', methods=['GET'])
@auth.login_required
def remove_device_openzwave_config(node_id, identical):
	utils.check_node_exist(node_id)
	my_node = globals.network.nodes[node_id]
	manufacturer_id = my_node.manufacturer_id
	product_id = my_node.product_id
	product_type = my_node.product_type
	list_to_remove = [node_id]
	if identical != 0:
		for child_id in list(globals.network.nodes):
			node = globals.network.nodes[child_id]
			if child_id != node_id and node.manufacturer_id == manufacturer_id and node.product_id == product_id and node.product_type == product_type:
				list_to_remove.append(child_id)
	globals.network_is_running = False
	globals.network.stop()
	logging.info('ZWave network is now stopped')
	time.sleep(5)
	filename = globals.data_folder + "/zwcfg_" + globals.network.home_id_str + ".xml"
	tree = etree.parse(filename)
	for child_id in list_to_remove:
		logging.info("Remove xml element for node %s" % (child_id,))
		node = tree.find("{http://code.google.com/p/open-zwave/}Node[@id='" + str(child_id) + "']")
		tree.getroot().remove(node)
	working_file = open(filename, "w")
	working_file.write('<?xml version="1.0" encoding="utf-8" ?>\n')
	working_file.writelines(etree.tostring(tree, pretty_print=True))
	working_file.close()
	network_utils.start_network()
	return utils.format_json_result()
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].GhostKiller()', methods=['GET'])
@auth.login_required
def ghost_killer(node_id):
	if not network_utils.can_execute_network_command(0):
		raise Exception('Controller is bussy')
	logging.info('Remove cc 0x84 (wake_up) for a ghost device: %s' % (node_id,))
	filename = globals.data_folder + "/zwcfg_" + globals.network.home_id_str + ".xml"
	globals.network_is_running = False
	globals.network.stop()
	logging.info('ZWave network is now stopped')
	time.sleep(5)
	found = False
	message = None
	tree = etree.parse(filename)
	namespace = tree.getroot().tag[1:].split("}")[0]
	node = tree.find("{%s}Node[@id='%s']" % (namespace, node_id,))
	if node is None:
		message = 'node not found'
	else:
		command_classes = node.find(".//{%s}CommandClasses" % namespace)
		if command_classes is None:
			message = 'commandClasses not found'
		else:
			for command_Class in command_classes.findall(".//{%s}CommandClass" % namespace):
				if int(command_Class.get("id")[:7]) == COMMAND_CLASS_WAKE_UP:
					command_classes.remove(command_Class)
					found = True
					break
			if found:
				config_file = open(filename, "w")
				config_file.write('<?xml version="1.0" encoding="utf-8" ?>\n')
				config_file.writelines(etree.tostring(tree, pretty_print=True))
				config_file.close()
			else:
				message = 'commandClass wake_up not found'
		globals.ghost_node_id = node_id
	return utils.format_json_result(found, message)
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].GetPendingChanges()', methods=['GET'])
@auth.login_required
def get_pending_changes(node_id):
	utils.check_node_exist(node_id)
	pending_changes = check_pending_changes(node_id)
	if pending_changes == 0:
		return utils.format_json_result()
	return utils.format_json_result(False, str(pending_changes))
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].GetHealth()', methods=['GET'])
@auth.login_required
def get_node_health(node_id):
	utils.check_node_exist(node_id)
	return jsonify(serialize_node_to_json(node_id))
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].GetLastNotification()', methods=['GET'])
@auth.login_required
def get_node_last_notification(node_id):
	utils.check_node_exist(node_id)
	return jsonify(node_utils.serialize_node_notification(node_id))
	
"""
controllers routes
"""
@app.route('/ZWaveAPI/Run/controller.AddNodeToNetwork(<int:state>,<int:do_security>)', methods=['GET'])
@auth.login_required
def start_node_inclusion(state, do_security):
	if globals.network_information.controller_is_busy:
		raise Exception('Controller is bussy')
	if state == 1:
		if not network_utils.can_execute_network_command(0):
			raise Exception('Controller is bussy')
		if do_security == 1:
			do_security = True
			logging.info(
				"Start the Inclusion Process to add a Node to the Network with Security CC if the node is supports it")
		else:
			do_security = False
			logging.info("Start the Inclusion Process to add a Node to the Network")
		execution_result = globals.network.manager.addNode(globals.network.home_id, do_security)
		if execution_result:
			globals.network_information.actual_mode = ControllerMode.AddDevice
		return utils.format_json_result(execution_result)
	elif state == 0:
		logging.info("Start the Inclusion (Cancel)")
		globals.network.manager.cancelControllerCommand(globals.network.home_id)
		return utils.format_json_result()

@app.route('/ZWaveAPI/Run/controller.RemoveNodeFromNetwork(<int:state>)', methods=['GET'])
@auth.login_required
def start_node_exclusion(state):
	if globals.network_information.controller_is_busy:
		raise Exception('Controller is bussy')
	if state == 1:
		if not network_utils.can_execute_network_command(0):
			raise Exception('Controller is bussy')
		logging.info("Remove a Device from the Z-Wave Network (Started)")
		execution_result = globals.network.manager.removeNode(globals.network.home_id)
		if execution_result:
			globals.network_information.actual_mode = ControllerMode.RemoveDevice
		return utils.format_json_result(execution_result)
	elif state == 0:
		logging.info("Remove a Device from the Z-Wave Network (Cancel)")
		globals.network.manager.cancelControllerCommand(globals.network.home_id)
		return utils.format_json_result()

@app.route('/ZWaveAPI/Run/controller.CancelCommand()', methods=['GET'])
@auth.login_required
def cancel_command():
	logging.info("Cancels any in-progress command running on a controller.")
	execution_result = globals.network.manager.cancelControllerCommand(globals.network.home_id)
	if execution_result:
		globals.network_information.controller_is_busy = False
	return utils.format_json_result(execution_result)

@app.route('/ZWaveAPI/Run/controller.RequestNetworkUpdate(<node_id>)', methods=['GET'])
@auth.login_required
def request_network_update(node_id):
	if not network_utils.can_execute_network_command(0):
		raise Exception('Controller is bussy')
	utils.check_node_exist(node_id)
	logging.info("Update the controller (%s) with network information from the SUC/SIS" % (node_id,))
	execution_result = globals.network.manager.requestNetworkUpdate(globals.network.home_id, node_id)
	return utils.format_json_result(execution_result)

@app.route('/ZWaveAPI/Run/controller.ReplicationSend(<node_id>)', methods=['GET'])
@auth.login_required
def replication_send(node_id):
	if not network_utils.can_execute_network_command(0):
		raise Exception('Controller is bussy')
	utils.check_node_exist(node_id)
	logging.info('Send information from primary to secondary %s' % (node_id,))
	return utils.format_json_result(globals.network.manager.replicationSend(globals.network.home_id, node_id))
	
@app.route('/ZWaveAPI/Run/controller.HealNetwork()', methods=['GET'])
@auth.login_required
def heal_network(perform_return_routes_initialization=False):
	if not network_utils.can_execute_network_command(0):
		raise Exception('Controller is bussy')
	logging.info("Heal network by requesting node's rediscover their neighbors")
	for node_id in list(globals.network.nodes):
		if node_id in globals.not_supported_nodes:
			logging.debug("skip not supported (nodeId: %s)" % (node_id,))
			continue
		if globals.network.nodes[node_id].is_failed:
			logging.debug("skip presume dead (nodeId: %s)" % (node_id,))
			continue
		if globals.network.nodes[node_id].query_stage != "Complete":
			logging.debug("skip query stage not complete (nodeId: %s)" % (node_id,))
			continue
		if globals.network.nodes[node_id].generic == 1:
			logging.debug("skip Remote controller (nodeId: %s) (they don't have neighbors)" % (node_id,))
			continue
		if node_id in globals.disabled_nodes:
			continue
		globals.network.manager.healNetworkNode(globals.network.home_id, node_id, perform_return_routes_initialization)
	return utils.format_json_result()

@app.route('/ZWaveAPI/Run/controller.SerialAPISoftReset()', methods=['GET'])
@auth.login_required
def soft_reset():
	logging.info("Resets a controller without erasing its network configuration settings")
	globals.network.controller.soft_reset()
	return utils.format_json_result()

@app.route('/ZWaveAPI/Run/controller.TestNetwork()', methods=['GET'])
@auth.login_required
def test_network(count=3):
	if not network_utils.can_execute_network_command():
		raise Exception('Controller is bussy')
	logging.info("Sends a series of messages to a network node for testing network reliability")
	for node_id in list(globals.network.nodes):
		if node_id in globals.not_supported_nodes:
			logging.debug("skip not supported (nodeId: %s)" % (node_id,))
			continue
		if node_id in globals.disabled_nodes:
			continue
		globals.network.manager.testNetworkNode(globals.network.home_id, node_id, count)
	return utils.format_json_result()

@app.route('/ZWaveAPI/Run/controller.CreateNewPrimary()', methods=['GET'])
@auth.login_required
def create_new_primary():
	if not network_utils.can_execute_network_command(0):
		raise Exception('Controller is bussy')
	logging.info("Add a new controller to the Z-Wave network")
	return utils.format_json_result(globals.network.manager.createNewPrimary(globals.network.home_id))

@app.route('/ZWaveAPI/Run/controller.TransferPrimaryRole()', methods=['GET'])
@auth.login_required
def transfer_primary_role():
	if not network_utils.can_execute_network_command(0):
		raise Exception('Controller is bussy')
	logging.info("Transfer Primary Role")
	return utils.format_json_result(globals.network.manager.transferPrimaryRole(globals.network.home_id))

@app.route('/ZWaveAPI/Run/controller.ReceiveConfiguration()', methods=['GET'])
@auth.login_required
def receive_configuration():
	if not network_utils.can_execute_network_command(0):
		raise Exception('Controller is bussy')
	logging.info("Receive Configuration")
	return utils.format_json_result(globals.network.manager.receiveConfiguration(globals.network.home_id))

@app.route('/ZWaveAPI/Run/controller.HardReset()', methods=['GET'])
@auth.login_required
def hard_reset():
	logging.info("Resets a controller and erases its network configuration settings")
	globals.network.controller.hard_reset()
	logging.info('The controller becomes a primary controller ready to add devices to a new network')
	time.sleep(3)
	network_utils.start_network()
	return utils.format_json_result()

"""
network routes
"""
@app.route('/ZWaveAPI/Run/network.Start()', methods=['GET'])
@auth.login_required
def network_start():
	logging.info('******** The ZWave network is being started ********')
	network_utils.start_network()
	return utils.format_json_result()
	

@app.route('/ZWaveAPI/Run/network.Stop()', methods=['GET'])
@auth.login_required
def stop_network():
	network_utils.graceful_stop_network()
	return utils.format_json_result()

@app.route('/ZWaveAPI/Run/network.GetStatus()', methods=['GET'])
@auth.login_required
def get_network_status():
	if globals.network is not None and globals.network.state >= globals.network.STATE_STARTED and globals.network_is_running:
		json_result = {'nodesCount': globals.network.nodes_count, 'sleepingNodesCount': utils.get_sleeping_nodes_count(),
                       'scenesCount': globals.network.scenes_count, 'pollInterval': globals.network.manager.getPollInterval(),
                       'isReady': globals.network.is_ready, 'stateDescription': globals.network.state_str, 'state': globals.network.state,
                       'controllerCapabilities': utils.concatenate_list(globals.network.controller.capabilities),
                       'controllerNodeCapabilities': utils.concatenate_list(globals.network.controller.node.capabilities),
					   'outgoingSendQueue': globals.network.controller.send_queue_count,
					   'controllerStatistics': globals.network.controller.stats, 'devicePath': globals.network.controller.device,
					   'OpenZwaveLibraryVersion': globals.network.manager.getOzwLibraryVersionNumber(),
					   'PythonOpenZwaveLibraryVersion': globals.network.manager.getPythonLibraryVersionNumber(),
					   'neighbors': utils.concatenate_list(globals.network.controller.node.neighbors),
					   'notifications': list(globals.network_information.last_controller_notifications),
					   'isBusy': globals.network_information.controller_is_busy, 'startTime': globals.network_information.start_time,
					   'isPrimaryController': globals.network.controller.is_primary_controller,
					   'isStaticUpdateController': globals.network.controller.is_static_update_controller,
					   'isBridgeController': globals.network.controller.is_bridge_controller,
					   'awakedDelay': globals.network_information.controller_awake_delay, 'mode': network_utils.get_network_mode()
                       }
	else:
		json_result = {}
	return jsonify(json_result)

@app.route('/ZWaveAPI/Run/network.GetNeighbours()', methods=['GET'])
@auth.login_required
def get_network_neighbours():
	neighbours = {'updateTime': int(time.time())}
	nodes_data = {}
	if globals.network is not None and globals.network.state >= globals.network.STATE_STARTED and globals.network_is_running:
		for node_id in list(globals.network.nodes):
			if node_id not in globals.disabled_nodes:
				nodes_data[node_id] = serialize_neighbour_to_json(node_id)
	neighbours['devices'] = nodes_data
	return jsonify(neighbours)


@app.route('/ZWaveAPI/Run/network.GetHealth()', methods=['GET'])
@auth.login_required
def get_network_health():
	network_health = {'updateTime': int(time.time())}
	nodes_data = {}
	if globals.network is not None and globals.network.state >= globals.network.STATE_STARTED and globals.network_is_running:
		for node_id in list(globals.network.nodes):
			nodes_data[node_id] = serialize_node_to_json(node_id)
	network_health['devices'] = nodes_data
	return jsonify(network_health)

@app.route('/ZWaveAPI/Run/network.GetNodesList()', methods=['GET'])
@auth.login_required
def get_nodes_list():
	nodes_list = {'updateTime': int(time.time())}
	nodes_data = {}
	for node_id in list(globals.network.nodes):
		my_node = globals.network.nodes[node_id]
		json_node = {}
		try:
			manufacturer_id = int(my_node.manufacturer_id, 16)
		except ValueError:
			manufacturer_id = None
		try:
			product_id = int(my_node.product_id, 16)
		except ValueError:
			product_id = None
		try:
			product_type = int(my_node.product_type, 16)
		except ValueError:
			product_type = None
		node_name = my_node.name
		node_location = my_node.location
		if utils.is_none_or_empty(node_name):
			node_name = 'Unknown'
		if globals.network.controller.node_id == node_id:
			node_name = my_node.product_name
			node_location = 'Jeedom'
		json_node['description'] = {'name': node_name, 'location': node_location,'product_name': my_node.product_name,'is_static_controller': my_node.basic == 2,'is_enable': int(node_id) not in globals.disabled_nodes}
		json_node['product'] = {'manufacturer_id': manufacturer_id,'product_type': product_type,'product_id': product_id,'is_valid': manufacturer_id is not None and product_id is not None and product_type is not None}
		instances = []
		for val in my_node.get_values(genre='User'):
			if my_node.values[val].instance in instances:
				continue
			instances.append(my_node.values[val].instance)
		json_node['multi_instance'] = {'support': COMMAND_CLASS_MULTI_CHANNEL in my_node.command_classes,'instances': len(instances)}
		json_node['capabilities'] = {'isListening': my_node.is_listening_device,'isRouting': my_node.is_routing_device,'isBeaming': my_node.is_beaming_device,'isFlirs': my_node.is_frequent_listening_device}
		nodes_data[node_id] = json_node
	nodes_list['devices'] = nodes_data
	return jsonify(nodes_list)

@app.route('/ZWaveAPI/Run/network.GetControllerStatus()', methods=['GET'])
@auth.login_required
def get_controller_status():
	controller_status = {}
	if globals.network is not None and globals.network.state >= globals.network.STATE_STARTED and globals.network_is_running:
		if globals.network.controller:
			controller_status = serialize_controller_to_json()
	return jsonify({'result': controller_status})

@app.route('/ZWaveAPI/Run/network.GetOZLogs()', methods=['GET'])
@auth.login_required
def get_openzwave_logs():
	std_in, std_out = os.popen2("tail -n 1000 " + globals.data_folder + "/openzwave.log")
	std_in.close()
	lines = std_out.readlines()
	std_out.close()
	return jsonify({'result': lines})

@app.route('/ZWaveAPI/Run/network.GetZWConfig()', methods=['GET'])
@auth.login_required
def get_openzwave_config():
	write_config()
	filename = globals.data_folder + "/zwcfg_" + globals.network.home_id_str + ".xml"
	with open(filename, "r") as ins:
		content = ins.read()
	return jsonify({'result': content})
	
@app.route('/ZWaveAPI/Run/network.SaveZWConfig()', methods=['GET'])
@auth.login_required
def save_openzwave_config():
	logging.info('Replace zwcfg configuration file')
	new_filename = globals.data_folder + "/zwcfg_new.xml"
	if not os.path.isfile(new_filename):
		raise Exception('zwcfg_new.xml not exist : '+str(new_filename))
	filename = globals.data_folder + "/zwcfg_" + globals.network.home_id_str + ".xml"
	globals.network_is_running = False
	globals.network.stop()
	while globals.network.state != globals.network.STATE_STOPPED:
		logging.info('%s (%s)' % (globals.network.state_str, globals.network.state,))
		time.sleep(1)
	logging.info('Replace zwcfg file: %s' % (filename,))
	FilesManager.copy_file(new_filename, filename)
	logging.info('Restart network')
	network_utils.start_network()
	return utils.format_json_result()

@app.route('/ZWaveAPI/Run/network.WriteZWConfig()', methods=['GET'])
@auth.login_required
def write_openzwave_config():
	write_config()
	return utils.format_json_result()

@app.route('/ZWaveAPI/Run/network.RemoveUnknownsDevicesZWConfig()', methods=['GET'])
@auth.login_required
def remove_unknowns_devices_openzwave_config():
	globals.network_is_running = False
	globals.network.stop()
	logging.info('ZWave network is now stopped')
	time.sleep(5)
	globals.files_manager.remove_unknowns_devices_openzwave_config(globals.network.home_id_str)
	network_utils.start_network()
	return utils.format_json_result()

@app.route('/ZWaveAPI/Run/network.GetOZBackups()', methods=['GET'])
@auth.login_required
def get_openzwave_backups():
	return jsonify(globals.files_manager.get_openzwave_backups())

@app.route('/ZWaveAPI/Run/network.RestoreBackup(<backup_name>)', methods=['GET'])
@auth.login_required
def restore_openzwave_backups(backup_name):
	logging.info('Restoring backup ' + backup_name)
	backup_folder = globals.data_folder + "/xml_backups"
	try:
		os.stat(backup_folder)
	except:
		os.mkdir(backup_folder)
	backup_file = os.path.join(backup_folder, backup_name)
	target_file = globals.data_folder + "/zwcfg_" + globals.network.home_id_str + ".xml"
	if not os.path.isfile(backup_file):
		logging.error('No config file found to backup')
		return utils.format_json_result(False, 'No config file found with name ' + backup_name, 'warning')
	else:
		tree = etree.parse(backup_file)
		globals.network_is_running = False
		globals.network.stop()
		logging.info('ZWave network is now stopped')
		time.sleep(3)
		shutil.copy2(backup_file, target_file)
		os.chmod(target_file, 0777)
		network_utils.start_network()
	return utils.format_json_result(True, backup_name + ' successfully restored')

@app.route('/ZWaveAPI/Run/network.ManualBackup()', methods=['GET'])
@auth.login_required
def manually_backup_config():
	logging.info('Manually creating a backup')
	if globals.files_manager.backup_xml_config('manual', globals.network.home_id_str):
		return utils.format_json_result(True, 'Xml config file successfully backup')
	else:
		return utils.format_json_result(False, 'See openzwave log file for details')

@app.route('/ZWaveAPI/Run/network.DeleteBackup(<backup_name>)', methods=['GET'])
@auth.login_required
def manually_delete_backup(backup_name):
	logging.info('Manually deleting a backup')
	backup_folder = globals.data_folder + "/xml_backups"
	backup_file = os.path.join(backup_folder, backup_name)
	if not os.path.isfile(backup_file):
		logging.error('No config file found to delete')
		return utils.format_json_result(False, 'No config file found with name ' + backup_name, 'warning')
	else:
		os.unlink(backup_file)
	return utils.format_json_result(True, backup_name + ' successfully deleted')

@app.route('/ZWaveAPI/Run/network.PerformSanityChecks()', methods=['GET'])
@auth.login_required
def perform_sanity_checks():
	if int(time.time()) > (globals.network_information.start_time + 120):
		if globals.network.state < globals.network.STATE_STARTED:
			logging.error("Timeouts occurred during communication with your ZWave dongle. Please check the openzwaved log file for more details.")
			try:
				network_utils.graceful_stop_network()
			finally:
				os.remove(globals.pidfile)
			try:
				server_utils.shutdown_server()
			finally:
				sys.exit()
	network_utils.sanity_checks()
	return utils.format_json_result()

@app.route('/ZWaveAPI/Run/ChangeLogLevel(<int:level>)', methods=['GET'])
@auth.login_required
def rest_change_log_level(level):
	utils.set_log_level(level)
	server_utils.set_log_level()
	return utils.format_json_result(success=True, detail=('Log level is set: %s' % (globals.log_level,)), log_level='info', code=0)

if __name__ == '__main__':
	server_utils.write_pid()
	try:
		http_server = HTTPServer(WSGIContainer(app))
		http_server.listen(globals.port_server)
		IOLoop.instance().start()
		if globals.log_level == 'Debug':
			print('REST server starting in %s mode' % (globals.log_level,))
			app.run(host='0.0.0.0', port=int(globals.port_server), debug=True, threaded=True, use_reloader=False, use_debugger=True)
		else:
			app.run(host='0.0.0.0', port=int(globals.port_server), debug=False, threaded=True, use_reloader=False, use_debugger=False)
	except Exception, ex:
		print "Fatal Error: %s" % str(ex)
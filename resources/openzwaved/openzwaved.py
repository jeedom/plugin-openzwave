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
import math
import globals
import argparse

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
	import socket
	from lxml import etree
	import signal

	from louie import dispatcher, All
except Exception as e:
	print(globals.MSG_CHECK_DEPENDENCY, 'error')
	print("Error: %s" % str(e), 'error')
	sys.exit(1)

try:
	from jeedom.jeedom import *
except ImportError:
	print "Error: importing module jeedom.jeedom"
	sys.exit(1)

if not os.path.exists('/tmp/python-openzwave-eggs'):
	os.makedirs('/tmp/python-openzwave-eggs')
os.environ['PYTHON_EGG_CACHE'] = '/tmp/python-openzwave-eggs'

# HTTP Basic Auth
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

jeedom_utils.set_log_level(globals.log_level)

logging.info('Start openzwaved')
logging.info('Log level : ' + str(globals.log_level))
logging.debug('PID file : ' + str(globals.pidfile))
logging.info('Device : ' + str(globals.device))
logging.debug('Apikey : ' + str(globals.apikey))
logging.info('Callback : ' + str(globals.callback))
logging.info('Cycle : ' + str(globals.cycle))

logging.debug('Initial disabled nodes list: ' + str(globals.disabled_nodes))

jeedom_com = jeedom_com(apikey=globals.apikey, url=globals.callback, cycle=globals.cycle)

if not jeedom_com.test():
	logging.error('Network communication issues. Please fixe your Jeedom network configuration.')
	sys.exit(1)

reload(sys)
sys.setdefaultencoding('utf8')

logging.info("Check Openzwave")
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
from utilities.NetworkExtend import *
from utilities.NodeExtend import *
from utilities.Constants import *
from utilities.FilesManager import FilesManager

# from openzwave.group import ZWaveGroup
logging.info("--> pass")

if globals.device is None or len(globals.device) == 0:
	logging.error('Dongle Key is not specified. Please check your Z-Wave (openzwave) configuration plugin page')
	sys.exit(1)

logging.info("Check if the port REST server available")
_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port_available = _sock.connect_ex(('127.0.0.1', int(globals.port_server)))
if port_available == 0:
	logging.error('The port %s is already in use. Please check your Z-Wave (openzwave) configuration plugin page' % (
	globals.port_server,), 'error')
	sys.exit(1)
logging.info("--> pass")

logging.info("Check OpenZWave Devices Database")
if not os.path.isfile(globals.config_folder + "/manufacturer_specific.xml"):
	logging.debug(globals.config_folder + "/manufacturer_specific.xml")
	logging.error('OpenZWave Devices Database is not found. Please execute Devices Configuration update, from Plugin Configuration page')
	sys.exit(1)
logging.info("--> pass")

if globals.device == 'auto':
	know_sticks = [{'idVendor': '0658', 'idProduct': '0200', 'name': 'Sigma Designs, Inc'},{'idVendor': '10c4', 'idProduct': 'ea60', 'name': 'Cygnal Integrated Products, Inc. CP210x UART Bridge'}]

	for stick in know_sticks:
		globals.device = jeedom_utils.find_tty_usb(stick['idVendor'], stick['idProduct'])
		if globals.device is not None:
			logging.info('USB Z-Wave Stick found : ' + stick['name'] + ' at ' + globals.device)
			break
	if globals.device is None:
		logging.error('No USB Z-Wave Stick detected')
		sys.exit(1)

def shutdown_server():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()

def start_network():
	# reset flags
	globals.force_refresh_nodes = []
	globals.pending_configurations.clear()
	globals.pending_associations.clear()
	globals.node_notifications.clear()
	if globals.network_information is None:
		globals.network_information = NetworkInformation(globals.maximum_number_notifications)
	else:
		globals.network_information.reset()
	logging.info('******** The ZWave network is being started ********')
	globals.network.start()

def graceful_stop_network():
	logging.info('Graceful stopping the ZWave network.')
	if globals.network is not None:
		home_id = globals.network.home_id_str
		globals.network_is_running = False
		globals.network.stop()
		# We disconnect to the louie dispatcher
		# noinspection PyBroadException
		disconnect_dispatcher()
		globals.network.destroy()
		# avoid a second pass
		globals.network = None
		logging.info('The Openzwave REST-server was stopped in a normal way')
		globals.files_manager.backup_xml_config('stop', home_id)
	else:
		logging.info('The Openzwave REST-server is already stopped')

# Define some manager options
options = ZWaveOption(globals.device, config_path=globals.config_folder, user_path=globals.data_folder, cmd_line="")
options.set_log_file("../../../log/openzwaved")
options.set_append_log_file(False)
options.set_console_output(False)
if globals.log_level == 'notice':
	options.set_save_log_level('Warning')
else:
	options.set_save_log_level(globals.log_level[0].upper() + globals.log_level[1:])

options.set_logging(True)
options.set_associate(True)
options.set_save_configuration(True)
options.set_poll_interval(globals.default_poll_interval)
options.set_interval_between_polls(False)
options.set_notify_transactions(True)  # Notifications when transaction complete is reported.
options.set_suppress_value_refresh(False)  # if true, notifications for refreshed (but unchanged) values will not be sent.
options.set_driver_max_attempts(5)
options.addOptionBool("AssumeAwake", globals.assumeAwake)
# options.addOptionInt("RetryTimeout", 6000)  # Timeout before retrying to send a message. Defaults to 40 Seconds
options.addOptionString("NetworkKey", "0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10", True)
options.set_security_strategy('SUPPORTED')  # The security strategy: SUPPORTED | ESSENTIAL | CUSTOM
# options.set_custom_secured_cc('0x62,0x4c,0x63')  # What List of Custom CC should we always encrypt if SecurityStrategy is CUSTOM
options.addOptionBool('EnforceSecureReception', False)  # if we receive a clear text message for a CC that is Secured, should we drop the message
options.addOptionBool('RefreshAllUserCodes', False)  # Some Devices have a big UserCode Table, that can mean startup times when refreshing Session Variables is very long
options.addOptionInt('ThreadTerminateTimeout', 5000)  #
options.addOptionBool('EnableSIS', True)  # Automatically become a SUC if there is no SUC on the network
options.lock()

globals.files_manager = FilesManager(globals.data_folder, globals.not_supported_nodes, logging)
globals.files_manager.check_config_files()

def save_node_value_event(node_id, timestamp, command_class, value_index, standard_type, value, instance):
	jeedom_com.add_changes('devices::' + str(node_id) + '::' + str(hex(command_class)) + str(instance) + str(value_index),{'node_id': node_id, 'instance': instance, 'CommandClass': hex(command_class), 'index': value_index,'value': value, 'type': standard_type, 'updateTime': timestamp})

def save_node_event(node_id, value):
	if value == "removed":
		jeedom_com.add_changes('controller::excluded', {"value": node_id})
	elif value == "added":
		jeedom_com.add_changes('controller::included', {"value": node_id})
	elif value in [0, 1, 5] and globals.controller_state != value:
		globals.controller_state = value
		if globals.network.state >= globals.network.STATE_AWAKED:
			jeedom_com.add_changes('controller::state', {"value": value})

def save_network_state(network_state):
	jeedom_com.add_changes('network::state', {"value": network_state})

def push_node_notification(node_id, notification_code):
	# check for notification Dead or Alive
	if notification_code in [5, 6]:
		if notification_code == 5:
			# Report when a node is presumed dead
			alert_type = 'node_dead'
		else:
			# Report when a node is revived
			alert_type = 'node_alive'
		changes = {'alert': {'type': alert_type, 'id': node_id}}
		jeedom_com.send_change_immediate(changes)

def network_started(network):
	logging.info("Openzwave network are started with homeId %0.8x." % (network.home_id,))
	globals.network_is_running = True
	globals.network_information.assign_controller_notification(ZWaveController.SIGNAL_CTRL_STARTING, "Network is started")
	save_network_state(network.state)
	if network.manager.getPollInterval() != globals.default_poll_interval:
		network.set_poll_interval(globals.default_poll_interval, False)

def network_stopped(network):
	logging.info("Openzwave network are %s" % (network.state_str,))
	globals.network_is_running = False

def network_failed(network):
	logging.error("Openzwave network can't load")
	globals.network_information.assign_controller_notification(ZWaveController.SIGNAL_CTRL_ERROR, "Network have failed")
	save_network_state(network.state)

def validate_association_groups_asynchronous():
	if not globals.network_is_running:
		return
	logging.debug("Check association")
	for node_id in list(globals.network.nodes):
		if validate_association_groups(node_id):
			# avoid stress network
			time.sleep(3)

def recovering_failed_nodes_asynchronous():
	# wait 15 seconds on first launch
	time.sleep(globals.sanity_checks_delay)
	while True:
		sanity_checks()
		# wait for next run
		time.sleep(globals.recovering_failed_nodes_timer)

def sanity_checks(force=False):
	# if controller is busy skip this run
	if globals.sanity_checks_running:
		return
	try:
		globals.sanity_checks_running = True
		if force or can_execute_network_command(0):
			logging.info("Perform network sanity test/check")
			for node_id in list(globals.network.nodes):
				my_node = globals.network.nodes[node_id]
				# first check if a ghost node wait to be removed
				if globals.ghost_node_id is not None and node_id == globals.ghost_node_id and my_node.is_failed:
					logging.info('* Try to remove a Ghost node (nodeId: %s)' % (node_id,))
					globals.network.manager.removeFailedNode(globals.network.home_id, node_id)
					time.sleep(10)
					if globals.ghost_node_id not in globals.network.nodes:
						# reset ghost node flag
						globals.ghost_node_id = None
						logging.info('=> Ghost node removed (nodeId: %s)' % (node_id,))
					continue
				if node_id in globals.not_supported_nodes:
					logging.info('=> Remove not valid nodeId: %s' % (node_id,))
					globals.network.manager.removeFailedNode(globals.network.home_id, node_id)
					time.sleep(10)
					continue
				if node_id in globals.disabled_nodes:
					continue
				if my_node.is_failed:
					if globals.ghost_node_id is not None and node_id == globals.ghost_node_id:
						continue
					logging.info('=> Try recovering, presumed Dead, nodeId: %s with a Ping' % (node_id,))
					# a ping will try to revive the node
					globals.network.manager.testNetworkNode(globals.network.home_id, node_id, 3)
					# avoid stress network
					time.sleep(5)
					if globals.network.manager.hasNodeFailed(globals.network.home_id, node_id):
						# avoid stress network
						time.sleep(4)
					if my_node.is_failed:
						# relive failed nodes
						logging.info('=> Try recovering, presumed Dead, nodeId: %s with a NIF' % (node_id,))
						if globals.network.manager.sendNodeInformation(globals.network.home_id, node_id):
							# avoid stress network
							time.sleep(4)
				elif my_node.is_listening_device and my_node.is_ready:
					# check if a ping is require
					if node_id in globals.node_notifications:
						last_notification = globals.node_notifications[node_id]
						logging.debug('=> last_notification for nodeId: %s is: %s(%s)' % (node_id, last_notification.description, last_notification.code,))
						# is in timeout or dead
						if last_notification.code in [1, 5]:
							logging.info('=> Do a test on node %s' % (node_id,))
							# a ping will try to resolve this situation with a NoOperation CC.
							globals.network.manager.testNetworkNode(globals.network.home_id, node_id, 3)
							# avoid stress network
							time.sleep(10)
				elif not my_node.is_listening_device and my_node.is_ready:
					try:
						can_wake_up = my_node.can_wake_up()
					except RuntimeError:
						can_wake_up = False
					if can_wake_up and node_id in globals.node_notifications:
						last_notification = globals.node_notifications[node_id]
						# check if controller think is awake
						if my_node.is_awake or last_notification.code == 3:
							logging.info('trying to lull the node %s' % (node_id,))
							# a ping will force the node to return sleep after the NoOperation CC. Will force node notification update
							globals.network.manager.testNetworkNode(globals.network.home_id, node_id, 1)

			logging.info("Network sanity test/check completed!")
		else:
			logging.debug("Network is loaded, skip sanity check this time")
	except Exception as error:
		logging.error('Unknown error during sanity checks: %s' % (str(error),))
	finally:
		globals.sanity_checks_running = False

def refresh_configuration_asynchronous():
	if can_execute_network_command(0):
		for node_id in list(globals.force_refresh_nodes):
			if node_id in globals.network.nodes and not globals.network.nodes[node_id].is_failed:
				logging.info('Request All Configuration Parameters for nodeId: %s' % (node_id,))
				globals.network.manager.requestAllConfigParams(globals.network.home_id, node_id)
				time.sleep(3)
	else:
		# I will try again in 2 minutes
		retry_job = threading.Timer(240.0, refresh_configuration_asynchronous)
		retry_job.start()

def refresh_user_values_asynchronous():
	logging.info("Refresh User Values of powered devices")
	if can_execute_network_command(0):
		for node_id in list(globals.network.nodes):
			my_node = globals.network.nodes[node_id]
			if my_node.is_ready and my_node.is_listening_device and not my_node.is_failed:
				logging.info('Refresh User Values for nodeId: %s' % (node_id,))
				for val in my_node.get_values():
					current_value = my_node.values[val]
					if current_value.genre == 'User':
						if current_value.type == 'Button':
							continue
						if current_value.is_write_only:
							continue
						if current_value.label in globals.user_values_to_refresh:
							current_value.refresh()
				while not can_execute_network_command(0):
					logging.debug("BackgroundWorker is waiting others tasks has be completed before proceeding")
					time.sleep(30)
	else:
		logging.debug("Network is loaded, do not execute this time")
		# I will try again in 2 minutes
		retry_job = threading.Timer(240.0, refresh_user_values_asynchronous)
		retry_job.start()

def network_awaked(network):
	logging.info(
		"Openzwave network is awake: %d nodes were found (%d are sleeping). All listening nodes are queried, but some sleeping nodes may be missing." % (
		network.nodes_count, get_sleeping_nodes_count(),))
	logging.debug("Controller is: %s" % (network.controller,))
	globals.network_information.set_as_awake()
	configuration = threading.Timer(globals.refresh_configuration_timer, refresh_configuration_asynchronous)
	configuration.start()
	logging.info("Refresh configuration parameters will starting in %d sec" % (globals.refresh_configuration_timer,))
	user_values = threading.Timer(globals.refresh_user_values_timer, refresh_user_values_asynchronous)
	user_values.start()
	logging.info("Refresh user values will starting in %d sec" % (globals.refresh_user_values_timer,))
	association = threading.Timer(globals.validate_association_groups_timer, validate_association_groups_asynchronous)
	association.start()
	logging.info("Validate association groups will starting in %d sec" % (globals.validate_association_groups_timer,))
	# threading.Thread(target=recovering_failed_nodes_asynchronous).start()
	# start listening for group changes
	dispatcher.connect(node_group_changed, ZWaveNetwork.SIGNAL_GROUP)
	save_network_state(network.state)
	if globals.ghost_node_id is not None:
		logging.info("Last step for Removing Ghost node will start in %d sec" % (globals.sanity_checks_delay,))
		sanity_checks_job = threading.Timer(globals.sanity_checks_delay, sanity_checks, [True])
		sanity_checks_job.start()

def network_ready(network):
	logging.info(
		"Openzwave network is ready with %d nodes (%d are sleeping). All nodes are queried, the network is fully functional." % (
		network.nodes_count, get_sleeping_nodes_count(),))
	write_config()
	globals.network_information.assign_controller_notification(ZWaveController.SIGNAL_CTRL_NORMAL, "Network is ready")
	save_network_state(network.state)

def button_on(network, node):
	logging.info('Controller button on pressed event')

def button_off(network, node):
	logging.info('Controller button off pressed event')

def nodes_queried(network):
	write_config()

def nodes_queried_some_dead(network):
	write_config()
	logging.info("All nodes have been queried, but some node ar mark dead")

def node_new(network, node_id):
	if node_id in globals.not_supported_nodes:
		return
	logging.info('A new node (%s), not already stored in zwcfg*.xml file, was found.' % (node_id,))
	globals.force_refresh_nodes.append(node_id)

def node_added(network, node):
	logging.info('A node has been added to OpenZWave list id:[%s] model:[%s].' % (node.node_id, node.product_name,))
	if node.node_id in globals.not_supported_nodes:
		logging.debug('remove fake nodeId: %s' % (node.node_id,))
		node_cleaner = threading.Timer(60.0, network.manager.removeFailedNode, [network.home_id, node.node_id])
		node_cleaner.start()
		return
	node.last_update = time.time()
	if network.state >= globals.network.STATE_AWAKED:
		save_node_event(node.node_id, "added")

def node_removed(network, node):
	logging.info('A node has been removed from OpenZWave list id:[%s] model:[%s].' % (node.node_id, node.product_name,))
	if node.node_id in globals.not_supported_nodes:
		return
	if network.state >= globals.network.STATE_AWAKED:
		save_node_event(node.node_id, "removed")
	# clean dict
	if node.node_id in globals.node_notifications:
		del globals.node_notifications[node.node_id]
	if node.node_id in globals.pending_associations:
		del globals.pending_associations[node.node_id]

def get_standard_value_type(value_type):
	if value_type == "Int":
		return 'int'
	elif value_type == "Decimal":
		return 'float'
	elif value_type == "Bool":
		return 'bool'
	elif value_type == "Byte":
		return 'int'
	elif value_type == "Short":
		return 'int'
	elif value_type == "Button":
		return 'bool'
	elif value_type == "Raw":
		return 'binary'
	else:
		return value_type

def change_instance(my_value):
	if my_value.instance > 1:
		return my_value.instance - 1
	return 0

def normalize_short_value(value):
	my_result = value
	# noinspection PyBroadException
	try:
		if int(value) < 0:
			my_result = 65536 + int(value)
	except:
		pass
	return my_result

def convert_fahrenheit_celsius(value):
	if value.precision is None or value.precision == 0:
		power = 1
	else:
		power = math.pow(10, value.precision)
	return int(((float(value.data_as_string) - 32) * 5.0 / 9.0) * int(power)) / power

def extract_data(value, display_raw=False, convert_fahrenheit=True):
	if value.type == "Bool":
		return value.data
	elif value.label == 'Temperature' and value.units == 'F' and convert_fahrenheit:
		return convert_fahrenheit_celsius(value)
	elif value.type == "Raw":
		my_result = binascii.b2a_hex(value.data)
		if display_raw:
			logging.info('Raw Signal: %s' % my_result)
		return my_result
	if value.type == "Decimal":
		if value.precision is None or value.precision == 0:
			power = 1
		else:
			power = math.pow(10, value.precision)
		return int(value.data * int(power)) / power
	return value.data

def can_execute_network_command(allowed_queue_count=5):
	if globals.network is None:
		return False
	if not globals.network_is_running:
		return False
	if not globals.network.controller.is_primary_controller:
		return True
	if globals.network.controller.send_queue_count > allowed_queue_count:
		return False
	if globals.network_information.controller_is_busy:
		return False
	if globals.network_information.actual_mode != ControllerMode.Idle:
		return False
	if globals.network.state < globals.network.STATE_STARTED:
		return False
	return True

def write_config():
	watchdog = 0
	while globals.network_information.config_file_save_in_progress and watchdog < 10:
		logging.debug('.')
		time.sleep(1)
		watchdog += 1
	if globals.network_information.config_file_save_in_progress:
		return
	globals.network_information.config_file_save_in_progress = True
	try:
		globals.network.write_config()
		logging.info('write configuration file')
		time.sleep(1)
	except Exception as error:
		logging.error('write_config %s' % (str(error),))
	finally:
		globals.network_information.config_file_save_in_progress = False

def essential_node_queries_complete(network, node):
	logging.info(
		'The essential queries on a node have been completed. id:[%s] model:[%s].' % (node.node_id, node.product_name,))
	my_node = network.nodes[node.node_id]
	my_node.last_update = time.time()
	# at this time is not good to save value, I skip this step

def node_queries_complete(network, node):
	logging.info('All the initialisation queries on a node have been completed. id:[%s] model:[%s].' % (
	node.node_id, node.product_name,))
	node.last_update = time.time()
	# save config
	write_config()

def save_value(node, value, last_update):
	logging.debug('A node value has been updated. nodeId:%s value:%s' % (node.node_id, value.label))
	if node.node_id in globals.network.nodes:
		my_node = globals.network.nodes[node.node_id]
		# check if am the really last update
		if my_node.last_update > last_update:
			logging.warning('Timing Error. nodeLastUpdate:%s Last_update:%s' % (str(my_node.last_update), str(last_update)))
			return
		# mark as seen flag
		my_node.last_update = last_update
		# if value.genre != 'Basic':
		value.last_update = last_update
		save_node_value_event(node.node_id, int(time.time()), value.command_class, value.index, get_standard_value_type(value.type), extract_data(value, False), change_instance(value))

def value_added(network, node, value):
	if node.node_id in globals.not_supported_nodes:
		return
	# logging.debug('value_added. %s %s' % (node.node_id, value.label,))
	# mark initial data for skip notification during interview
	value.lastData = value.data

def value_removed(network, node, value):
	if node.node_id in globals.not_supported_nodes:
		return
	# clean pending dict
	if value.value_id in globals.pending_configurations:
		del globals.pending_configurations[value.value_id]

def value_polling_enabled(network, node, value):
	# not yet handle correctly ozw lib and wrapper must updated to use this check
	# check if old polling is outside authorized range
	if value.poll_intensity > globals.maximum_poll_intensity:
		changes_value_polling(globals.maximum_poll_intensity, value)
	# check if old polling is at lower index for CC and instance
	if value.poll_intensity > 0:
		logging.debug('Poll intensity on nodeId:%s value %s command_class %s instance %s index %s' % (node.node_id, value.label, value.command_class, value.instance, value.index))
		# get all CC of node
		for val in node.get_values(class_id=value.command_class):
			# filter on same instance
			if node.values[val].instance == value.instance:
				my_value = node.values[val]
				# check is is the lower index is have polling attribute
				if my_value.index < value.index & my_value.poll_intensity == 0:
					poll_intensity = value.poll_intensity
					# reset last polling
					value.disable_poll()
					# set polling of lower index
					changes_value_polling(poll_intensity, my_value)
					logging.info('Changes poll intensity on nodeId:%s form %s to %s' % (node.node_id, value.label, my_value.label,))
					break


def prepare_value_notification(node, value):
	if value.id_on_network in globals.pending_configurations:
		pending = globals.pending_configurations[value.id_on_network]
		if pending is not None:
			# mark result
			data = value.data
			if value.type == 'Short':
				data = normalize_short_value(value.data)
			pending.data = data

	if not node.is_ready:
		# check if have the attribute
		if hasattr(value, 'lastData') and value.lastData == value.data:
			# we skip notification to avoid value refresh during the interview process
			return
	# update for next run
	value.lastData = value.data
	if value.genre == 'System':
		value.last_update = time.time()
		return
	command_class = globals.network.manager.COMMAND_CLASS_DESC[value.command_class].replace("COMMAND_CLASS_", "").replace("_", " ").lower().capitalize()
	data = extract_data(value, False, False)
	logging.info("Received %s report from node %s: %s=%s%s" % (command_class, node.node_id, value.label, data, value.units))
	try:
		save_value(node, value, time.time())
	except Exception as error:
		logging.error('An unknown error occurred while sending notification: %s. (Node %s: %s=%s)' % (str(error), node.node_id, value.label, data,))

def value_update(network, node, value):
	if node.node_id in globals.not_supported_nodes:
		return
	logging.debug('value_update. %s %s' % (node.node_id, value.label,))
	prepare_value_notification(node, value)

def value_refreshed(network, node, value):
	if node.node_id in globals.not_supported_nodes:
		return
	logging.debug('value_refreshed. %s %s' % (node.node_id, value.label,))
	prepare_value_notification(node, value)

def scene_event(network, node, scene_id):
	logging.info('Scene Activation: %s' % (scene_id,))
	standard_type = 'int'
	save_node_value_event(node.node_id, int(time.time()), COMMAND_CLASS_CENTRAL_SCENE, 0, standard_type, scene_id, 0)
	save_node_value_event(node.node_id, int(time.time()), COMMAND_CLASS_SCENE_ACTIVATION, 0, standard_type, scene_id, 0)

def controller_message_complete(network):
	logging.debug('The last message that was sent is now complete')

def controller_waiting(network, controller, state_int, state, state_full):
	logging.debug(state_full)
	# save actual state
	globals.network_information.assign_controller_notification(state, state_full)
	# notify jeedom
	save_node_event(network.controller.node_id, globals.network_information.generate_jeedom_message())

def controller_command(network, controller, node, node_id, state_int, state, state_full, error_int, error, error_full):
	logging.info('%s (%s)' % (state_full, state))
	if error_int > 0:
		logging.error('%s (%s)' % (error_full, error,))

	# save actual state
	globals.network_information.assign_controller_notification(state, state_full, error, error_full)
	# notify jeedom
	save_node_event(network.controller.node_id, globals.network_information.generate_jeedom_message())
	logging.debug('The controller is busy ? %s' % (globals.network_information.controller_is_busy,))

def node_event(network, node, value):
	logging.info('NodeId %s sends a Basic_Set command to the controller with value %s' % (node.node_id, value,))
	for val in network.nodes[node.node_id].get_values():
		my_value = network.nodes[node.node_id].values[val]
		if my_value.genre == "User" and not my_value.is_write_only:
			value_update(network, node, my_value)
	'''
	the value is actually the event data, not a zwave value object.
	This is commonly caused when a node sends a Basic_Set command to the controller.
	'''
	standard_type = 'int'
	save_node_value_event(node.node_id, int(time.time()), COMMAND_CLASS_BASIC, 0, standard_type, value, 0)

def node_group_changed(network, node, groupidx):
	logging.info('Group changed for nodeId %s index %s' % (node.node_id, groupidx,))
	validate_association_groups(node.node_id)
	# check pending for this group index
	if node.node_id in globals.pending_associations:
		pending = globals.pending_associations[node.node_id]
		if groupidx in pending:
			pending_association = pending[groupidx]
			if pending_association is not None:
				pending_association.associations = node.groups[groupidx].associations

def get_wake_up_interval(node_id):
	interval = get_value_by_label(node_id, COMMAND_CLASS_WAKE_UP, 1, 'Wake-up Interval', False)
	if interval is not None:
		return interval.data
	return None

def force_sleeping(node_id, count=1):
	if node_id in globals.network.nodes:
		my_node = globals.network.nodes[node_id]
		logging.debug('check if node %s still awake' % (node_id,))
		last_notification = None
		if node_id in globals.node_notifications:
			last_notification = globals.node_notifications[node_id]
		if my_node.is_awake or (last_notification is not None and last_notification.code == 3):
			logging.debug('trying to lull the node %s' % (node_id,))
			globals.network.manager.testNetworkNode(globals.network.home_id, node_id, count)

def node_notification(args):
	code = int(args['notificationCode'])
	node_id = int(args['nodeId'])
	if node_id in globals.not_supported_nodes:
		return
	if node_id in globals.disabled_nodes:
		return
	if node_id in globals.network.nodes:
		my_node = globals.network.nodes[node_id]
		my_node.last_update = time.time()
		if node_id in globals.not_supported_nodes and globals.network.state >= globals.network.STATE_AWAKED:
			logging.info('remove fake nodeId: %s' % (node_id,))
			globals.network.manager.removeFailedNode(globals.network.home_id, node_id)
			return
		wake_up_time = get_wake_up_interval(node_id)
		if node_id not in globals.node_notifications:
			globals.node_notifications[node_id] = NodeNotification(code, wake_up_time)
		else:
			globals.node_notifications[node_id].refresh(code, wake_up_time)
		if code == 3:
			my_value = get_value_by_label(node_id, COMMAND_CLASS_WAKE_UP, 1, 'Wake-up Interval Step', False)
			if my_value is not None:
				wake_up_interval_step = my_value.data + 2.0
			else: 
				wake_up_interval_step = 60.0
			threading.Timer(interval=wake_up_interval_step, function=force_sleeping, args=(node_id, 1)).start()
		logging.info('NodeId %s send a notification: %s' % (node_id, globals.node_notifications[node_id].description,))
		push_node_notification(node_id, code)

def connect_dispatcher():
	if globals.dispatcher_is_connect:
		return
	logging.debug('connect to the louie dispatcher')
	# We connect to the louie dispatcher
	dispatcher.connect(network_started, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
	dispatcher.connect(network_failed, ZWaveNetwork.SIGNAL_NETWORK_FAILED)
	dispatcher.connect(network_failed, ZWaveNetwork.SIGNAL_DRIVER_FAILED)
	dispatcher.connect(network_awaked, ZWaveNetwork.SIGNAL_NETWORK_AWAKED)
	dispatcher.connect(network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)
	dispatcher.connect(network_stopped, ZWaveNetwork.SIGNAL_NETWORK_STOPPED)
	# a new node has been found (not already stored in zwcfg*.xml file).
	dispatcher.connect(node_new, ZWaveNetwork.SIGNAL_NODE_NEW)
	# add node to the network, during node discovering and after a inclusion
	dispatcher.connect(node_added, ZWaveNetwork.SIGNAL_NODE_ADDED)
	# a node is fully removed from network.
	dispatcher.connect(node_removed, ZWaveNetwork.SIGNAL_NODE_REMOVED)
	# A new node value has been added to OpenZWave's list.
	# These notifications occur after a node has been discovered, and details of its command classes have been received.
	# Each command class may generate one or more values depending on the complexity of the item being represented.
	dispatcher.connect(value_added, ZWaveNetwork.SIGNAL_VALUE_ADDED)
	# A node value has been updated from the Z-Wave network and it is different from the previous value.
	dispatcher.connect(value_update, ZWaveNetwork.SIGNAL_VALUE_CHANGED)
	# A node value has been updated from the Z-Wave network.
	dispatcher.connect(value_refreshed, ZWaveNetwork.SIGNAL_VALUE_REFRESHED)
	# A node value has been removed from the Z-Wave network.
	dispatcher.connect(value_removed, ZWaveNetwork.SIGNAL_VALUE_REMOVED)
	# Polling of a node value has been successfully turned on.
	# dispatcher.connect(value_polling_enabled, ZWaveNetwork.SIGNAL_POLLING_ENABLED)
	# when a node sends a Basic_Set command to the controller.
	dispatcher.connect(node_event, ZWaveNetwork.SIGNAL_NODE_EVENT)
	# scene event
	dispatcher.connect(scene_event, ZWaveNetwork.SIGNAL_SCENE_EVENT)
	# the essential node query are completed
	dispatcher.connect(essential_node_queries_complete, ZWaveNetwork.SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE)
	# all node query are completed, the node is fully operational, is ready!
	dispatcher.connect(node_queries_complete, ZWaveNetwork.SIGNAL_NODE_QUERIES_COMPLETE)
	# is network notification same as SIGNAL_NETWORK_AWAKE, we don't need
	dispatcher.connect(nodes_queried, ZWaveNetwork.SIGNAL_AWAKE_NODES_QUERIED)
	# is network notification same as SIGNAL_NETWORK_READY, we don't need
	dispatcher.connect(nodes_queried, ZWaveNetwork.SIGNAL_ALL_NODES_QUERIED)
	dispatcher.connect(nodes_queried_some_dead, ZWaveNetwork.SIGNAL_ALL_NODES_QUERIED_SOME_DEAD)
	# a button is pressed
	dispatcher.connect(button_on, ZWaveNetwork.SIGNAL_BUTTON_ON)
	dispatcher.connect(button_off, ZWaveNetwork.SIGNAL_BUTTON_OFF)
	# Called when an error happened, or node changed (awake, sleep, death, no operation, timeout).
	dispatcher.connect(node_notification, ZWaveNetwork.SIGNAL_NOTIFICATION)
	if globals.network.state >= globals.network.STATE_AWAKED:
		dispatcher.connect(node_group_changed, ZWaveNetwork.SIGNAL_GROUP)
	# Controller is waiting for a user action
	dispatcher.connect(controller_waiting, ZWaveNetwork.SIGNAL_CONTROLLER_WAITING)
	# keep a track of actual network command in progress
	dispatcher.connect(controller_command, ZWaveNetwork.SIGNAL_CONTROLLER_COMMAND)
	# The command has completed successfully
	dispatcher.connect(controller_message_complete, ZWaveNetwork.SIGNAL_MSG_COMPLETE)
	globals.dispatcher_is_connect = True

def disconnect_dispatcher():
	logging.debug('disconnect the louie dispatcher')
	try:
		dispatcher.disconnect(network_started, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
		dispatcher.disconnect(network_failed, ZWaveNetwork.SIGNAL_NETWORK_FAILED)
		dispatcher.disconnect(network_failed, ZWaveNetwork.SIGNAL_DRIVER_FAILED)
		dispatcher.disconnect(network_awaked, ZWaveNetwork.SIGNAL_NETWORK_AWAKED)
		dispatcher.disconnect(network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)
		dispatcher.disconnect(network_stopped, ZWaveNetwork.SIGNAL_NETWORK_STOPPED)
		dispatcher.disconnect(node_new, ZWaveNetwork.SIGNAL_NODE_NEW)
		dispatcher.disconnect(node_added, ZWaveNetwork.SIGNAL_NODE_ADDED)
		dispatcher.disconnect(node_removed, ZWaveNetwork.SIGNAL_NODE_REMOVED)
		dispatcher.disconnect(value_added, ZWaveNetwork.SIGNAL_VALUE_ADDED)
		dispatcher.disconnect(value_update, ZWaveNetwork.SIGNAL_VALUE_CHANGED)
		dispatcher.disconnect(value_refreshed, ZWaveNetwork.SIGNAL_VALUE_REFRESHED)
		dispatcher.disconnect(value_removed, ZWaveNetwork.SIGNAL_VALUE_REMOVED)
		# dispatcher.disconnect(value_polling_enabled, ZWaveNetwork.SIGNAL_POLLING_ENABLED)
		dispatcher.disconnect(node_event, ZWaveNetwork.SIGNAL_NODE_EVENT)
		dispatcher.disconnect(scene_event, ZWaveNetwork.SIGNAL_SCENE_EVENT)
		dispatcher.disconnect(essential_node_queries_complete, ZWaveNetwork.SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE)
		dispatcher.disconnect(node_queries_complete, ZWaveNetwork.SIGNAL_NODE_QUERIES_COMPLETE)
		dispatcher.disconnect(nodes_queried, ZWaveNetwork.SIGNAL_AWAKE_NODES_QUERIED)
		dispatcher.disconnect(nodes_queried, ZWaveNetwork.SIGNAL_ALL_NODES_QUERIED)
		dispatcher.disconnect(nodes_queried_some_dead, ZWaveNetwork.SIGNAL_ALL_NODES_QUERIED_SOME_DEAD)
		dispatcher.disconnect(button_on, ZWaveNetwork.SIGNAL_BUTTON_ON)
		dispatcher.disconnect(button_off, ZWaveNetwork.SIGNAL_BUTTON_OFF)
		dispatcher.disconnect(node_notification, ZWaveNetwork.SIGNAL_NOTIFICATION)
		if globals.network.state >= globals.network.STATE_AWAKED:
			dispatcher.disconnect(node_group_changed, ZWaveNetwork.SIGNAL_GROUP)
		dispatcher.disconnect(controller_waiting, ZWaveNetwork.SIGNAL_CONTROLLER_WAITING)
		dispatcher.disconnect(controller_command, ZWaveNetwork.SIGNAL_CONTROLLER_COMMAND)
		dispatcher.disconnect(controller_message_complete, ZWaveNetwork.SIGNAL_MSG_COMPLETE)
	except Exception:
		pass
	globals.dispatcher_is_connect = False

app = Flask(__name__, static_url_path='/static')
# Create a network object
globals.network = ZWaveNetwork(options, autostart=False)
connect_dispatcher()
start_network()
logging.info('OpenZwave Library Version %s' % (globals.network.manager.getOzwLibraryVersionNumber(),))
logging.info('Python-OpenZwave Wrapper Version %s' % (globals.network.manager.getPythonLibraryVersionNumber(),))
# We wait for the network.
logging.info('Waiting for network to become ready')

def get_value_by_label(node_id, command_class, instance, label, trace=True):
	if node_id in globals.network.nodes:
		my_node = globals.network.nodes[node_id]
		for value_id in my_node.get_values(class_id=command_class):
			if my_node.values[value_id].instance == instance and my_node.values[value_id].label == label:
				return my_node.values[value_id]
	if trace:
		logging.debug("get_value_by_label Value not found for node_id:%s, cc:%s, instance:%s, label:%s" % (
		node_id, command_class, instance, label,))
	return None

def get_value_by_index(node_id, command_class, instance, index_id, trace=True):
	if node_id in globals.network.nodes:
		my_node = globals.network.nodes[node_id]
		for value_id in my_node.get_values(class_id=command_class):
			if my_node.values[value_id].instance == instance and my_node.values[value_id].index == index_id:
				return my_node.values[value_id]
	if trace:
		logging.debug("get_value_by_index Value not found for node_id:%s, cc:%s, instance:%s, index:%s" % (
		node_id, command_class, instance, index_id,))
	return None

def get_value_by_id(node_id, value_id):
	if node_id in globals.network.nodes:
		my_node = globals.network.nodes[node_id]
		if value_id in my_node.values:
			return my_node.values[value_id]
	logging.debug("get_value_by_id Value not found for node_id:%s, value_id:%s" % (node_id, value_id,))
	return None

def mark_pending_change(my_value, data, wake_up_time=0):
	if my_value is not None and not my_value.is_write_only:
		globals.pending_configurations[my_value.id_on_network] = PendingConfiguration(data, wake_up_time)

def concatenate_list(list_values, separator=';'):
	try:
		if list_values is None:
			return ""
		else:
			if isinstance(list_values, set):
				return separator.join(str(s) for s in sorted(list_values))
			return list_values
	except Exception as error:
		logging.error(str(error))
	return ""

def convert_query_stage_to_int(stage):
	if stage == "None":
		return 0
	elif stage == "ProtocolInfo":
		return 1
	elif stage == "Probe":
		return 2
	elif stage == "WakeUp":
		return 3
	elif stage == "ManufacturerSpecific1":
		return 4
	elif stage == "NodeInfo":
		return 5
	elif stage == "NodePlusInfo":
		return 5
	elif stage == "SecurityReport":
		return 6
	elif stage == "ManufacturerSpecific2":
		return 7
	elif stage == "Versions":
		return 8
	elif stage == "Instances":
		return 9
	elif stage == "Static":
		return 10
	elif stage == "CacheLoad":
		return 11
	elif stage == "Associations":
		return 12
	elif stage == "Neighbors":
		return 13
	elif stage == "Session":
		return 14
	elif stage == "Dynamic":
		return 15
	elif stage == "Configuration":
		return 16
	elif stage == "Complete":
		return 17
	return 0

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
		if is_none_or_empty(node_name):
			node_name = my_node.product_name
		if is_none_or_empty(node_name):
			node_name = 'Unknown'
		json_result['data']['name'] = {'value': node_name}
		json_result['data']['isPrimaryController'] = {'value': globals.network.controller.node_id == node_id}
		neighbour_is_enabled = my_node.generic != 1 # not a remote control
		if my_node.generic == 8 and not my_node.is_listening_device:
			neighbour_is_enabled = len(my_node.neighbors) > 0
		json_result['data']['neighbours'] = {'value': list(my_node.neighbors), 'enabled': neighbour_is_enabled}
		json_result['data']['isDead'] = {'value': my_node.is_failed}
		json_result['data']['type'] = {'basic': my_node.basic, 'generic': my_node.generic, 'specific': my_node.specific}
		json_result['data']['state'] = {'value': convert_query_stage_to_int(my_node.query_stage)}
		json_result['data']['isListening'] = {'value': my_node.is_listening_device}
		json_result['data']['isRouting'] = {'value': my_node.is_routing_device}
	else:
		logging.warning('This network does not contain any node with the id %s' % (node_id,))
	return json_result

def validate_association_groups(node_id):
	fake_found = False
	if globals.network is not None and globals.network.state >= globals.network.STATE_AWAKED:
		if node_id in globals.network.nodes:
			my_node = globals.network.nodes[node_id]
			query_stage_index = convert_query_stage_to_int(my_node.query_stage)
			if query_stage_index >= 12:
				logging.debug("validate_association_groups for nodeId: %s" % (node_id,))
				for group_index in list(my_node.groups):
					group = my_node.groups[group_index]
					for target_node_id in list(group.associations):
						if target_node_id in globals.network.nodes and target_node_id not in globals.not_supported_nodes:
							continue
						logging.debug("Remove association for nodeId: %s index %s with not exist target: %s" % (
						node_id, group_index, target_node_id,))
						globals.network.manager.removeAssociation(globals.network.home_id, node_id, group_index, target_node_id)
						fake_found = True
	return fake_found

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
	if is_none_or_empty(node_name):
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
	json_result['data']['wakeup_interval'] = {'value': get_wake_up_interval(node_id), 'next_wakeup': next_wake_up}
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
	query_stage_index = convert_query_stage_to_int(my_node.query_stage)
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
	is_secured = get_value_by_label(node_id, COMMAND_CLASS_SECURITY, 1, 'Secured', False)
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
		json_result['command_classes'][command_class] = {'name': my_node.get_command_class_as_string(command_class),'hex': '0x' + convert_user_code_to_hex(command_class)}
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
			standard_type = get_standard_value_type(my_value.type)
		else:
			standard_type = 'int'
		if my_value.is_write_only:
			value2 = None
		else:
			if my_value.type == 'Short':
				value2 = normalize_short_value(my_value.data)
			else:
				value2 = extract_data(my_value)
		instance2 = change_instance(my_value)
		if my_value.index:
			index2 = my_value.index
		else:
			index2 = 0
		pending_state = None
		expected_data = None
		data_items = concatenate_list(my_value.data_items)
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


def serialize_node_notification(node_id):
	json_result = {}
	if node_id in globals.not_supported_nodes:
		return json_result
	my_node = globals.network.nodes[node_id]
	if node_id in globals.node_notifications:
		notification = globals.node_notifications[node_id]
		return {"receiveTime": notification.receive_time,"description": notification.description,"isFailed": my_node.is_failed}
	else:
		return {"receiveTime": None,"description": None,"isFailed": my_node.is_failed}

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

def get_network_mode():
	if globals.network_information.controller_is_busy:
		if globals.network_information.actual_mode == ControllerMode.AddDevice:
			return NetworkInformation.AddDevice
		elif globals.network_information.actual_mode == ControllerMode.RemoveDevice:
			return NetworkInformation.RemoveDevice
	return NetworkInformation.Idle

def serialize_controller_to_json():
	json_result = {'data': {}}
	json_result['data']['roles'] = {'isPrimaryController': globals.network.controller.is_primary_controller, 'isStaticUpdateController': globals.network.controller.is_static_update_controller, 'isBridgeController': globals.network.controller.is_bridge_controller}
	json_result['data']['nodeId'] = {'value': globals.network.controller.node_id}
	json_result['data']['mode'] = {'value': get_network_mode()}
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

def convert_user_code_to_hex(value, length=2):
	value1 = int(value)
	my_result = hex(value1)[length:]
	if len(my_result) == 1:
		my_result = '0' * (length - 1) + my_result
	return my_result

def set_value(node_id, value_id, data):
	check_node_exist(node_id)
	logging.debug("set a value for nodeId:%s valueId:%s data:%s" % (node_id, value_id, data,))
	my_node = globals.network.nodes[node_id]
	if not my_node.is_ready:
		return format_json_result(False, 'The node must be Ready', 'debug')
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
				return format_json_result()
			return format_json_result(False, result_message, 'warning')
	return format_json_result(False, 'valueId not exist', 'warning')

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

def is_motor(node_id):
	return globals.network.nodes[node_id].specific in [SPECIFIC_TYPE_MOTOR_MULTI_POSITION, SPECIFIC_TYPE_CLASS_A_MOTOR_CONTROL, SPECIFIC_TYPE_CLASS_B_MOTOR_CONTROL, SPECIFIC_TYPE_CLASS_C_MOTOR_CONTROL]


def get_sleeping_nodes_count():
	sleeping_nodes_count = 0
	for idNode in list(globals.network.nodes):
		if not globals.network.nodes[idNode].is_awake:
			sleeping_nodes_count += 1
	return sleeping_nodes_count

def convert_level_to_color(level):
	if level > 99:
		return 255
	return level * 255 / 99

def convert_color_to_level(color):
	if color > 255:
		color = 255
	if color < 0:
		color = 0
	return color * 99 / 255

def is_none_or_empty(value):
	if value is None:
		return True
	if value:
		return False
	else:
		return True

def format_json_result(success=True, detail=None, log_level=None, code=0):
	if log_level is not None and not is_none_or_empty(detail):
		if log_level == 'debug':
			logging.debug(detail)
		elif log_level == 'warning':
			logging.warning(detail)
		elif log_level == 'error':
			logging.error(detail)
	if detail is not None:
		return jsonify({'result': success, 'data': detail, 'code': code})
	return jsonify({'result': success})

def refresh_switch_binary(node_id, value_id, target_value):
	if node_id in globals.network.nodes:
		my_value = globals.network.nodes[node_id].values[value_id]
		if my_value is not None:
			if my_value.data != target_value:
				logging.debug("Force refresh switch binary")
				my_value.refresh()

def check_node_exist(_node_id,enable=False):
	if _node_id not in globals.network.nodes:
		raise Exception('Unknow node id '+str(_node_id))
	if enable and _node_id not in globals.disabled_nodes:
		raise Exception('Disable node id '+str(_node_id))
	return

def send_command_zwave(_node_id, _cc_id, _instance_id, _index, _value):
	logging.info("Send command to "+str(_node_id)+" on "+str(_cc_id)+" instance "+str(_instance_id)+" index "+str(_index)+" value "+str(_value))
	check_node_exist(_node_id)
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
				prepare_refresh(_node_id, val, _value, is_motor(_node_id))
			if int(_cc_id, 16) == COMMAND_CLASS_THERMOSTAT_SETPOINT:
				logging.debug("COMMAND_CLASS_THERMOSTAT_SETPOINT")
				save_node_value_event(_node_id, int(time.time()), COMMAND_CLASS_THERMOSTAT_SETPOINT, _index, get_standard_value_type(globals.network.nodes[_node_id].values[val].type), _value, _instance_id + 10)
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
	check_node_exist(_node_id)
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
	my_value = get_value_by_index(_node_id, COMMAND_CLASS_CONFIGURATION, 1, _index_id)
	result = globals.network.nodes[_node_id].set_config_param(_index_id, _value, _size)
	if my_value is not None and my_value.type != 'List':
		mark_pending_change(my_value, _value)
	return result

'''
default routes
'''

@app.errorhandler(Exception)
def all_exception_handler(error):
	return format_json_result(False, str(error))

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
	check_node_exist(node_id)
	logging.debug("refresh_assoc for nodeId: %s" % (node_id,))
	for val in globals.network.nodes[node_id].get_values(class_id=COMMAND_CLASS_ASSOCIATION):
		globals.network.nodes[node_id].values[val].refresh()
	return format_json_result()
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[0].commandClasses[133].data', methods=['GET'])
@auth.login_required
def get_assoc(node_id):
	check_node_exist(node_id)
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
	check_node_exist(node_id)
	logging.info("remove_assoc to nodeId: %s in group %s with nodeId: %s" % (node_id, group_index, target_node_id,))
	my_node = globals.network.nodes[node_id]
	if my_node.node_id not in globals.pending_associations:
		globals.pending_associations[my_node.node_id] = dict()
	globals.pending_associations[my_node.node_id][group_index] = PendingAssociation(pending_added=None, pending_removed=target_node_id, timeout=0)
	globals.network.manager.removeAssociation(globals.network.home_id, node_id, group_index, target_node_id)
	return format_json_result()
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[0].commandClasses[0x85].Add(<int:group_index>,<int:target_node_id>)', methods=['GET'])
@auth.login_required
def add_assoc(node_id, group_index, target_node_id):
	if globals.network_information.controller_is_busy:
		raise Exception('Controller is bussy')
	check_node_exist(node_id)
	logging.info("add_assoc to nodeId: %s in group %s with nodeId: %s" % (node_id, group_index, target_node_id,))
	my_node = globals.network.nodes[node_id]
	if not (target_node_id in my_node.groups[group_index].associations):
		if my_node.node_id not in globals.pending_associations:
			globals.pending_associations[my_node.node_id] = dict()
	globals.pending_associations[my_node.node_id][group_index] = PendingAssociation(pending_added=target_node_id, pending_removed=None, timeout=0)
	globals.network.manager.addAssociation(globals.network.home_id, node_id, group_index, target_node_id)
	return format_json_result()

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].Associations[<int:group_index>].Remove(<int:target_node_id>,<int:target_node_instance>)', methods=['GET'])
@auth.login_required
def remove_association(node_id, group_index, target_node_id, target_node_instance):
	if globals.network_information.controller_is_busy:
		raise Exception('Controller is bussy')
	check_node_exist(node_id)
	logging.info("remove_association to nodeId: %s in group %s with nodeId: %s instance %s" % (node_id, group_index, target_node_id, target_node_instance,))
	my_node = globals.network.nodes[node_id]
	if my_node.node_id not in globals.pending_associations:
		globals.pending_associations[my_node.node_id] = dict()
	globals.pending_associations[my_node.node_id][group_index] = PendingAssociation(pending_added=None, pending_removed=target_node_id, timeout=0)
	globals.network.manager.removeAssociation(globals.network.home_id, node_id, group_index, target_node_id, target_node_instance)
	return format_json_result()
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].Associations[<int:group_index>].Add(<int:target_node_id>,<int:target_node_instance>)', methods=['GET'])
@auth.login_required
def add_association(node_id, group_index, target_node_id, target_node_instance):
	if globals.network_information.controller_is_busy:
		raise Exception('Controller is bussy')
	check_node_exist(node_id)
	logging.info("add_association to nodeId: %s in group %s with nodeId: %s instance %s" % (
	node_id, group_index, target_node_id, target_node_instance,))
	my_node = globals.network.nodes[node_id]
	if not (target_node_id in my_node.groups[group_index].associations):
		if my_node.node_id not in globals.pending_associations:
			globals.pending_associations[my_node.node_id] = dict()
	globals.pending_associations[my_node.node_id][group_index] = PendingAssociation(pending_added=target_node_id, pending_removed=None, timeout=0)
	globals.network.manager.addAssociation(globals.network.home_id, node_id, group_index, target_node_id, target_node_instance)
	return format_json_result()
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].SetPolling(<int:value_id>,<frequency>)', methods=['GET'])
@auth.login_required
def set_polling2(node_id, value_id, frequency):
	check_node_exist(node_id)
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
			return format_json_result()
	return format_json_result(False, 'valueId: %s not found' % (value_id,), 'warning')
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].SetPolling(<int:frequency>)', methods=['GET'])
@auth.login_required
def set_polling_value(node_id, instance_id, cc_id, index, frequency):
	check_node_exist(node_id)
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
	return format_json_result()

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].SetPolling(<int:frequency>)', methods=['GET'])
@auth.login_required
def set_polling_instance(node_id, instance_id, cc_id, frequency):
	check_node_exist(node_id)
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
	return format_json_result()
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].SetWakeup(<wake_up_time>)', methods=['GET'])
@auth.login_required
def set_wake_up(node_id, wake_up_time):
	check_node_exist(node_id)
	logging.info("set wakeup interval for nodeId %s at: %s" % (node_id, wake_up_time,))
	for val in globals.network.nodes[node_id].get_values(class_id=COMMAND_CLASS_WAKE_UP):
		my_value = globals.network.nodes[node_id].values[val]
		if my_value.label == "Wake-up Interval":
			return format_json_result(set_value(node_id, my_value.value_id, int(wake_up_time)))
	return format_json_result(False, 'Wake-up Interval not found', 'warning')
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].Refresh()', methods=['GET'])
@auth.login_required
def request_all_config_params(node_id):
	check_node_exist(node_id)
	logging.info("Request the values of all known configurable parameters from nodeId %s" % (node_id,))
	for val in globals.network.nodes[node_id].get_values(class_id=COMMAND_CLASS_CONFIGURATION):
		configuration_item = globals.network.nodes[node_id].values[val]
		if configuration_item.id_on_network in globals.pending_configurations:
			del globals.pending_configurations[configuration_item.id_on_network]
	globals.network.manager.requestAllConfigParams(globals.network.home_id, node_id)
	return format_json_result()
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].Get(<int:index_id>)', methods=['GET'])
@auth.login_required
def refresh_config(node_id, index_id):
	check_node_exist(node_id)
	logging.debug("refresh_config for nodeId:%s index_id:%s" % (node_id, index_id,))
	for val in globals.network.nodes[node_id].get_values(class_id=COMMAND_CLASS_CONFIGURATION):
		if globals.network.nodes[node_id].values[val].index == index_id:
			globals.network.nodes[node_id].values[val].refresh()
	return format_json_result()
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].SetDeviceName(<string:location>,<string:name>,<int:is_enable>)', methods=['GET'])
@auth.login_required
def set_device_name(node_id, location, name, is_enable):
	check_node_exist(node_id)
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
	return format_json_result()

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].data', methods=['GET'])
@auth.login_required
def get_config(node_id):
	check_node_exist(node_id)
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
	check_node_exist(source_id)
	check_node_exist(target_id)
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
					target_value = get_value_by_index(target_id, COMMAND_CLASS_CONFIGURATION, 1,configuration_value.index)
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
		return format_json_result(False,'The two nodes must be with same: manufacturer_id, product_type and product_id','warning')
	return jsonify({'result': my_result, 'copied_configuration_items': items})

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[0x70].data[<int:index_id2>].Set(<int:index_id>,<string:value>,<int:size>)', methods=['GET'])
@auth.login_required
def set_config5(node_id, instance_id, index_id2, index_id, value, size):
	return format_json_result(set_config(node_id, index_id, value, size))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[0x70].data[<int:index_id2>].Set(<int:index_id>,<float:value>,<int:size>)', methods=['GET'])
@auth.login_required
def set_config6(node_id, instance_id, index_id2, index_id, value, size):
	return format_json_result(set_config(node_id, index_id, value, size))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[0x70].data[<int:index_id2>].Set(<int:index_id>,<int:value>,<int:size>)', methods=['GET'])
@auth.login_required
def set_config4(node_id, instance_id, index_id2, index_id, value, size):
	return format_json_result(set_config(node_id, index_id, value, size))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].Set(<int:index_id>,<string:value>,<int:size>)', methods=['GET'])
@auth.login_required
def set_config2(node_id, index_id, value, size):
	return format_json_result(set_config(node_id, index_id, value, size))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].Set(<int:index_id>,<float:value>,<int:size>)', methods=['GET'])
@auth.login_required
def set_config3(node_id, index_id, value, size):
	return format_json_result(set_config(node_id, index_id, value, size))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].Set(<int:index_id>,<int:value>,<int:size>)', methods=['GET'])
@auth.login_required
def set_config1(node_id, index_id, value, size):
	return format_json_result(set_config(node_id, index_id, value, size))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses', methods=['GET'])
@auth.login_required
def get_command_classes(node_id):
	my_result = {}
	logging.debug("get_command_classes for nodeId:%s" % (node_id,))
	check_node_exist(node_id)
	for val in globals.network.nodes[node_id].get_values():
		my_result[globals.network.nodes[node_id].values[val].command_class] = {}
	return jsonify(my_result)

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].RequestNodeDynamic()', methods=['GET'])
@auth.login_required
def request_node_dynamic(node_id):
	check_node_exist(node_id)
	globals.network.manager.requestNodeDynamic(globals.network.home_id, node_id)
	globals.network.nodes[node_id].last_update = time.time()
	logging.info("Fetch the dynamic command class data for the node %s" % (node_id,))
	return format_json_result()

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].Get()', methods=['GET'])
@auth.login_required
def get_value(node_id, instance_id, cc_id):
	check_node_exist(node_id)
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
	return format_json_result()

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].val', methods=['GET'])
@auth.login_required
def get_value6(node_id, instance_id, index, cc_id):
	check_node_exist(node_id)
	for val in globals.network.nodes[node_id].get_values(class_id=int(cc_id, 16)):
		if globals.network.nodes[node_id].values[val].instance - 1 == instance_id and globals.network.nodes[node_id].values[
			val].index == index:
			if globals.network.nodes[node_id].values[val].units == 'F':
				return str(convert_fahrenheit_celsius(globals.network.nodes[node_id].values[val]))
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
	check_node_exist(node_id)
	for val in globals.network.nodes[node_id].get_values(class_id=cc_id):
		if globals.network.nodes[node_id].values[val].instance - 1 == instance_id and globals.network.nodes[node_id].values[
			val].index == index:
			globals.network.nodes[node_id].values[val].refresh()
			return format_json_result()
	return format_json_result(False, 'This device does not contain the specified value', 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[0x63].data[<int:index>].code', methods=['GET'])
@auth.login_required
def get_user_code(node_id, instance_id, index):
	check_node_exist(node_id)
	logging.debug("getValueRaw nodeId:%s instance:%s commandClasses:%s index:%s" % (
	node_id, instance_id, hex(COMMAND_CLASS_USER_CODE), index))
	my_result = {}
	my_node = globals.network.nodes[node_id]
	for val in my_node.get_values(class_id=COMMAND_CLASS_USER_CODE):
		my_value = my_node.values[val]
		if my_value.instance - 1 == instance_id and my_value.index == index:
			user_code = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			timestamp = int(1)
			raw_data = extract_data(my_value)
			if raw_data != '00000000000000000000':
				try:
					timestamp = int(my_value.last_update)
					chunks, chunk_size = len(raw_data), len(raw_data) / 10
					user_code = [int(raw_data[i:i + chunk_size], 16) for i in range(0, chunks, chunk_size)]
				except TypeError:
					timestamp = int(1)
			my_result = {'invalidateTime': int(time.time() - datetime.timedelta(seconds=30).total_seconds()), 'type': get_standard_value_type(my_value.type),'value': user_code,'updateTime': timestamp}
			break
	return jsonify(my_result)

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[0x63].data', methods=['GET'])
@auth.login_required
def get_user_codes(node_id, instance_id):
	check_node_exist(node_id)
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
			raw_data = extract_data(my_value)
			if raw_data == '00000000000000000000':
				result_value[my_value.index] = None
			else:
				result_value[my_value.index] = {}
	return jsonify(result_value)

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].UserCode.SetRaw(<int:slot_id>,[<string:value>],1)', methods=['GET'])
@auth.login_required
def set_user_code(node_id, slot_id, value):
	check_node_exist(node_id)
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
	check_node_exist(node_id)
	logging.info("set_user_code2 nodeId:%s slot:%s user code:%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (node_id, slot_id, value1, value2, value3, value4, value5, value6, value7, value8, value9, value10,))
	result_value = {}
	for val in globals.network.nodes[node_id].get_values(class_id=COMMAND_CLASS_USER_CODE):
		if globals.network.nodes[node_id].values[val].index == slot_id:
			result_value['data'] = {}
			value = convert_user_code_to_hex(value1) + convert_user_code_to_hex(value2) + convert_user_code_to_hex(value3) + convert_user_code_to_hex(value4) + convert_user_code_to_hex(value5) + convert_user_code_to_hex(value6) + convert_user_code_to_hex(value7) + convert_user_code_to_hex(value8) + convert_user_code_to_hex(value9) + convert_user_code_to_hex(value10)
			original_value = value
			value = binascii.a2b_hex(value)
			globals.network.nodes[node_id].values[val].data = value
			result_value['data'][val] = {'device': node_id, 'slot': slot_id, 'val': original_value}
			return jsonify(result_value)
	return jsonify(result_value)

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].Set(<float:value>)', methods=['GET'])
@auth.login_required
def set_value8(node_id, instance_id, cc_id, index, value):
	return format_json_result(True, send_command_zwave(node_id, cc_id, instance_id, index, value))
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].Set(<string:value>)', methods=['GET'])
@auth.login_required
def set_value6(node_id, instance_id, cc_id, value):
	return format_json_result(True, send_command_zwave(node_id, cc_id, instance_id, None, value))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].Set(<int:value>)', methods=['GET'])
@auth.login_required
def set_value7(node_id, instance_id, cc_id, index, value):
	return format_json_result(True, send_command_zwave(node_id, cc_id, instance_id, index, value))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].Set(<string:value>)', methods=['GET'])
@auth.login_required
def set_value9(node_id, instance_id, cc_id, index, value):
	return format_json_result(True, send_command_zwave(node_id, cc_id, instance_id, index, value))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].GetColor()', methods=['GET'])
@auth.login_required
def get_color(node_id):
	check_node_exist(node_id)
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
			red_level = convert_level_to_color(my_value.data)
		elif my_value.instance == 4:
			green_level = convert_level_to_color(my_value.data)
		elif my_value.instance == 5:
			blue_level = convert_level_to_color(my_value.data)
		elif my_value.instance == 6:
			white_level = convert_level_to_color(my_value.data)
	my_result['data'] = {'red': red_level, 'green': green_level, 'blue': blue_level, 'white': white_level}
	return jsonify(my_result)

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].SetColor(<int:red_level>,<int:green_level>,<int:blue_level>,<int:white_level>)', methods=['GET'])
@auth.login_required
def set_color(node_id, red_level, green_level, blue_level, white_level):
	check_node_exist(node_id)
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
			my_value.data = convert_color_to_level(red_level)
		elif my_value.instance == 4:
			green_value = val
			my_value.data = convert_color_to_level(green_level)
		elif my_value.instance == 5:
			blue_value = val
			my_value.data = convert_color_to_level(blue_level)
		elif my_value.instance == 6:
			my_value.data = convert_color_to_level(white_level)
	if red_value is not None and green_value is not None and blue_value is not None:
		prepare_refresh(node_id, intensity_value, None)
		my_result = True
	return format_json_result(my_result)

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].PressButton()', methods=['GET'])
@auth.login_required
def press_button(node_id, instance_id, cc_id, index):
	check_node_exist(node_id)
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
				value_level = get_value_by_label(node_id, COMMAND_CLASS_SWITCH_MULTILEVEL,
                                                 globals.network.nodes[node_id].values[val].instance, 'Level')
				if value_level:
					prepare_refresh(node_id, value_level.value_id, value, is_motor(node_id))
			return format_json_result()
	return format_json_result(False, 'button not found', 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].ReleaseButton()', methods=['GET'])
@auth.login_required
def release_button(node_id, instance_id, cc_id, index):
	check_node_exist(node_id)
	for val in globals.network.nodes[node_id].get_values(class_id=int(cc_id, 16), genre='All', type='All', readonly='All', writeonly='All'):
		if globals.network.nodes[node_id].values[val].instance - 1 == instance_id and globals.network.nodes[node_id].values[
			val].index == index:
			globals.network.manager.releaseButton(globals.network.nodes[node_id].values[val].value_id)
			# stop refresh if running in background
			if cc_id == hex(COMMAND_CLASS_SWITCH_MULTILEVEL):
				value_level = get_value_by_label(node_id, COMMAND_CLASS_SWITCH_MULTILEVEL,
                                                 globals.network.nodes[node_id].values[val].instance, 'Level')
				if value_level:
					stop_refresh(node_id, value_level.value_id)

			return format_json_result()
	return format_json_result(False, 'button not found', 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[0].commandClasses[0xF0].SwitchAll(<int:state>)', methods=['GET'])
@auth.login_required
def switch_all(state):
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
	return format_json_result()

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].RequestNodeNeighbourUpdate()', methods=['GET'])
@auth.login_required
def request_node_neighbour_update(node_id):
	if not can_execute_network_command():
		raise Exception('Controller is bussy')
	check_node_exist(node_id,True)
	logging.info("request_node_neighbour_update for node %s" % (node_id,))
	return format_json_result(globals.network.manager.requestNodeNeighborUpdate(globals.network.home_id, node_id), 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].RemoveFailedNode()', methods=['GET'])
@auth.login_required
def remove_failed_node(node_id):
	check_node_exist(node_id)
	if not can_execute_network_command(0):
		raise Exception('Controller is bussy')
	logging.info("Remove a failed node %s" % (node_id,))
	return format_json_result(globals.network.manager.removeFailedNode(globals.network.home_id, node_id))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].HealNode()', methods=['GET'])
@auth.login_required
def heal_node(node_id, perform_return_routes_initialization=False):
	if not can_execute_network_command():
		raise Exception('Controller is bussy')
	check_node_exist(node_id,True)
	logging.info("Heal network node (%s) by requesting the node rediscover their neighbors" % (node_id,))
	globals.network.manager.healNetworkNode(globals.network.home_id, node_id, perform_return_routes_initialization)
	return format_json_result()

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].AssignReturnRoute()', methods=['GET'])
@auth.login_required
def assign_return_route(node_id):
	if not can_execute_network_command():
		raise Exception('Controller is bussy')
	check_node_exist(node_id)
	logging.info("Ask Node (%s) to update its Return Route to the Controller" % (node_id,))
	return format_json_result(globals.network.manager.assignReturnRoute(globals.network.home_id, node_id))
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>]', methods=['GET'])
def get_serialized_device(node_id):
	check_node_exist(node_id)
	return jsonify(serialize_node_to_json(node_id))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].ReplaceFailedNode()', methods=['GET'])
@auth.login_required
def replace_failed_node(node_id):
	if not can_execute_network_command():
		raise Exception('Controller is bussy')
	check_node_exist(node_id,True)
	logging.info("replace_failed_node node %s" % (node_id,))
	return format_json_result(globals.network.manager.replaceFailedNode(globals.network.home_id, node_id))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].SendNodeInformation()', methods=['GET'])
@auth.login_required
def send_node_information(node_id):
	if not can_execute_network_command():
		raise Exception('Controller is bussy')
	check_node_exist(node_id,True)
	logging.info("send_node_information node %s" % (node_id,))
	return format_json_result(globals.network.manager.sendNodeInformation(globals.network.home_id, node_id))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].HasNodeFailed()', methods=['GET'])
@auth.login_required
def has_node_failed(node_id):
	if not can_execute_network_command():
		raise Exception('Controller is bussy')
	check_node_exist(node_id,True)
	logging.info("has_node_failed node %s" % (node_id,))
	return format_json_result(globals.network.manager.hasNodeFailed(globals.network.home_id, node_id))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].RefreshNodeInfo()', methods=['GET'])
@auth.login_required
def refresh_node_info(node_id):
	if not can_execute_network_command():
		raise Exception('Controller is bussy')
	check_node_exist(node_id,True)
	logging.info("refresh_node_info node %s" % (node_id,))
	return format_json_result(globals.network.manager.refreshNodeInfo(globals.network.home_id, node_id))
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].RefreshAllValues()', methods=['GET'])
@auth.login_required
def refresh_all_values(node_id):
	check_node_exist(node_id,True)
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
	return format_json_result(True, message)

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].TestNode()', methods=['GET'])
@auth.login_required
def test_node(node_id=0, count=3):
	if not can_execute_network_command():
		raise Exception('Controller is bussy')
	check_node_exist(node_id,True)
	globals.network.manager.testNetworkNode(globals.network.home_id, node_id, count)
	return format_json_result()
		
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].GetNodeStatistics()', methods=['GET'])
@auth.login_required
def get_node_statistics(node_id):
	check_node_exist(node_id,True)
	query_stage_description = globals.network.manager.getNodeQueryStage(globals.network.home_id, node_id)
	query_stage_code = globals.network.manager.getNodeQueryStageCode(query_stage_description)
	return jsonify({'statistics': globals.network.manager.getNodeStatistics(globals.network.home_id, node_id), 'queryStageCode': query_stage_code, 'queryStageDescription': query_stage_description})

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].RemoveDeviceZWConfig(<int:identical>)', methods=['GET'])
@auth.login_required
def remove_device_openzwave_config(node_id, identical):
	check_node_exist(node_id)
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
	start_network()
	return format_json_result()
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].GhostKiller()', methods=['GET'])
@auth.login_required
def ghost_killer(node_id):
	if not can_execute_network_command(0):
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
	return format_json_result(found, message)
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].GetPendingChanges()', methods=['GET'])
@auth.login_required
def get_pending_changes(node_id):
	check_node_exist(node_id)
	pending_changes = check_pending_changes(node_id)
	if pending_changes == 0:
		return format_json_result()
	return format_json_result(False, str(pending_changes))
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].GetHealth()', methods=['GET'])
@auth.login_required
def get_node_health(node_id):
	check_node_exist(node_id)
	return jsonify(serialize_node_to_json(node_id))
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].GetLastNotification()', methods=['GET'])
@auth.login_required
def get_node_last_notification(node_id):
	check_node_exist(node_id)
	return jsonify(serialize_node_notification(node_id))
	
"""
controllers routes
"""
@app.route('/ZWaveAPI/Run/controller.AddNodeToNetwork(<int:state>,<int:do_security>)', methods=['GET'])
@auth.login_required
def start_node_inclusion(state, do_security):
	if globals.network_information.controller_is_busy:
		raise Exception('Controller is bussy')
	if state == 1:
		if not can_execute_network_command(0):
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
		return format_json_result(execution_result)
	elif state == 0:
		logging.info("Start the Inclusion (Cancel)")
		globals.network.manager.cancelControllerCommand(globals.network.home_id)
		return format_json_result()

@app.route('/ZWaveAPI/Run/controller.RemoveNodeFromNetwork(<int:state>)', methods=['GET'])
@auth.login_required
def start_node_exclusion(state):
	if globals.network_information.controller_is_busy:
		raise Exception('Controller is bussy')
	if state == 1:
		if not can_execute_network_command(0):
			raise Exception('Controller is bussy')
		logging.info("Remove a Device from the Z-Wave Network (Started)")
		execution_result = globals.network.manager.removeNode(globals.network.home_id)
		if execution_result:
			globals.network_information.actual_mode = ControllerMode.RemoveDevice
		return format_json_result(execution_result)
	elif state == 0:
		logging.info("Remove a Device from the Z-Wave Network (Cancel)")
		globals.network.manager.cancelControllerCommand(globals.network.home_id)
		return format_json_result()

@app.route('/ZWaveAPI/Run/controller.CancelCommand()', methods=['GET'])
@auth.login_required
def cancel_command():
	logging.info("Cancels any in-progress command running on a controller.")
	execution_result = globals.network.manager.cancelControllerCommand(globals.network.home_id)
	if execution_result:
		globals.network_information.controller_is_busy = False
	return format_json_result(execution_result)

@app.route('/ZWaveAPI/Run/controller.RequestNetworkUpdate(<node_id>)', methods=['GET'])
@auth.login_required
def request_network_update(node_id):
	if not can_execute_network_command(0):
		raise Exception('Controller is bussy')
	check_node_exist(node_id)
	logging.info("Update the controller (%s) with network information from the SUC/SIS" % (node_id,))
	execution_result = globals.network.manager.requestNetworkUpdate(globals.network.home_id, node_id)
	return format_json_result(execution_result)

@app.route('/ZWaveAPI/Run/controller.ReplicationSend(<node_id>)', methods=['GET'])
@auth.login_required
def replication_send(node_id):
	if not can_execute_network_command(0):
		raise Exception('Controller is bussy')
	check_node_exist(node_id)
	logging.info('Send information from primary to secondary %s' % (node_id,))
	return format_json_result(globals.network.manager.replicationSend(globals.network.home_id, node_id))
	
@app.route('/ZWaveAPI/Run/controller.HealNetwork()', methods=['GET'])
@auth.login_required
def heal_network(perform_return_routes_initialization=False):
	if not can_execute_network_command(0):
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
	return format_json_result()

@app.route('/ZWaveAPI/Run/controller.SerialAPISoftReset()', methods=['GET'])
@auth.login_required
def soft_reset():
	logging.info("Resets a controller without erasing its network configuration settings")
	globals.network.controller.soft_reset()
	return format_json_result()

@app.route('/ZWaveAPI/Run/controller.TestNetwork()', methods=['GET'])
@auth.login_required
def test_network(count=3):
	if not can_execute_network_command():
		raise Exception('Controller is bussy')
	logging.info("Sends a series of messages to a network node for testing network reliability")
	for node_id in list(globals.network.nodes):
		if node_id in globals.not_supported_nodes:
			logging.debug("skip not supported (nodeId: %s)" % (node_id,))
			continue
		if node_id in globals.disabled_nodes:
			continue
		globals.network.manager.testNetworkNode(globals.network.home_id, node_id, count)
	return format_json_result()

@app.route('/ZWaveAPI/Run/controller.CreateNewPrimary()', methods=['GET'])
@auth.login_required
def create_new_primary():
	if not can_execute_network_command(0):
		raise Exception('Controller is bussy')
	logging.info("Add a new controller to the Z-Wave network")
	return format_json_result(globals.network.manager.createNewPrimary(globals.network.home_id))

@app.route('/ZWaveAPI/Run/controller.TransferPrimaryRole()', methods=['GET'])
@auth.login_required
def transfer_primary_role():
	if not can_execute_network_command(0):
		raise Exception('Controller is bussy')
	logging.info("Transfer Primary Role")
	return format_json_result(globals.network.manager.transferPrimaryRole(globals.network.home_id))

@app.route('/ZWaveAPI/Run/controller.ReceiveConfiguration()', methods=['GET'])
@auth.login_required
def receive_configuration():
	if not can_execute_network_command(0):
		raise Exception('Controller is bussy')
	logging.info("Receive Configuration")
	return format_json_result(globals.network.manager.receiveConfiguration(globals.network.home_id))

@app.route('/ZWaveAPI/Run/controller.HardReset()', methods=['GET'])
@auth.login_required
def hard_reset():
	logging.info("Resets a controller and erases its network configuration settings")
	globals.network.controller.hard_reset()
	logging.info('The controller becomes a primary controller ready to add devices to a new network')
	time.sleep(3)
	start_network()
	return format_json_result()

"""
network routes
"""
@app.route('/ZWaveAPI/Run/network.Start()', methods=['GET'])
@auth.login_required
def network_start():
	logging.info('******** The ZWave network is being started ********')
	start_network()
	return format_json_result()
	

@app.route('/ZWaveAPI/Run/network.Stop()', methods=['GET'])
@auth.login_required
def stop_network():
	graceful_stop_network()
	return format_json_result()

@app.route('/ZWaveAPI/Run/network.GetStatus()', methods=['GET'])
@auth.login_required
def get_network_status():
	if globals.network is not None and globals.network.state >= globals.network.STATE_STARTED and globals.network_is_running:
		json_result = {'nodesCount': globals.network.nodes_count, 'sleepingNodesCount': get_sleeping_nodes_count(),
                       'scenesCount': globals.network.scenes_count, 'pollInterval': globals.network.manager.getPollInterval(),
                       'isReady': globals.network.is_ready, 'stateDescription': globals.network.state_str, 'state': globals.network.state,
                       'controllerCapabilities': concatenate_list(globals.network.controller.capabilities),
                       'controllerNodeCapabilities': concatenate_list(globals.network.controller.node.capabilities),
					   'outgoingSendQueue': globals.network.controller.send_queue_count,
					   'controllerStatistics': globals.network.controller.stats, 'devicePath': globals.network.controller.device,
					   'OpenZwaveLibraryVersion': globals.network.manager.getOzwLibraryVersionNumber(),
					   'PythonOpenZwaveLibraryVersion': globals.network.manager.getPythonLibraryVersionNumber(),
					   'neighbors': concatenate_list(globals.network.controller.node.neighbors),
					   'notifications': list(globals.network_information.last_controller_notifications),
					   'isBusy': globals.network_information.controller_is_busy, 'startTime': globals.network_information.start_time,
					   'isPrimaryController': globals.network.controller.is_primary_controller,
					   'isStaticUpdateController': globals.network.controller.is_static_update_controller,
					   'isBridgeController': globals.network.controller.is_bridge_controller,
					   'awakedDelay': globals.network_information.controller_awake_delay, 'mode': get_network_mode()
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
		if is_none_or_empty(node_name):
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
	start_network()
	return format_json_result()

@app.route('/ZWaveAPI/Run/network.WriteZWConfig()', methods=['GET'])
@auth.login_required
def write_openzwave_config():
	write_config()
	return format_json_result()

@app.route('/ZWaveAPI/Run/network.RemoveUnknownsDevicesZWConfig()', methods=['GET'])
@auth.login_required
def remove_unknowns_devices_openzwave_config():
	globals.network_is_running = False
	globals.network.stop()
	logging.info('ZWave network is now stopped')
	time.sleep(5)
	globals.files_manager.remove_unknowns_devices_openzwave_config(globals.network.home_id_str)
	start_network()
	return format_json_result()

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
		return format_json_result(False, 'No config file found with name ' + backup_name, 'warning')
	else:
		tree = etree.parse(backup_file)
		globals.network_is_running = False
		globals.network.stop()
		logging.info('ZWave network is now stopped')
		time.sleep(3)
		shutil.copy2(backup_file, target_file)
		os.chmod(target_file, 0777)
		start_network()
	return format_json_result(True, backup_name + ' successfully restored')

@app.route('/ZWaveAPI/Run/network.ManualBackup()', methods=['GET'])
@auth.login_required
def manually_backup_config():
	logging.info('Manually creating a backup')
	if globals.files_manager.backup_xml_config('manual', globals.network.home_id_str):
		return format_json_result(True, 'Xml config file successfully backup')
	else:
		return format_json_result(False, 'See openzwave log file for details')

@app.route('/ZWaveAPI/Run/network.DeleteBackup(<backup_name>)', methods=['GET'])
@auth.login_required
def manually_delete_backup(backup_name):
	logging.info('Manually deleting a backup')
	backup_folder = globals.data_folder + "/xml_backups"
	backup_file = os.path.join(backup_folder, backup_name)
	if not os.path.isfile(backup_file):
		logging.error('No config file found to delete')
		return format_json_result(False, 'No config file found with name ' + backup_name, 'warning')
	else:
		os.unlink(backup_file)
	return format_json_result(True, backup_name + ' successfully deleted')

@app.route('/ZWaveAPI/Run/network.PerformSanityChecks()', methods=['GET'])
@auth.login_required
def perform_sanity_checks():
	if int(time.time()) > (globals.network_information.start_time + 120):
		if globals.network.state < globals.network.STATE_STARTED:
			logging.error("Timeouts occurred during communication with your ZWave dongle. Please check the openzwaved log file for more details.")
			try:
				graceful_stop_network()
			finally:
				os.remove(globals.pidfile)
			try:
				shutdown_server()
			finally:
				sys.exit()
	sanity_checks()
	return format_json_result()

@app.route('/ZWaveAPI/Run/ChangeLogLevel(<int:level>)', methods=['GET'])
@auth.login_required
def rest_change_log_level(level):
	if level == 40:
		globals.log_level = 'error'
	elif level == 20:
		globals.log_level = 'debug'
	elif level == 10:
		globals.log_level = 'info'
	else:
		globals.log_level = 'none'
	jeedom_utils.set_log_level(globals.log_level)
	return format_json_result(success=True, detail=('Log level is set: %s' % (globals.log_level,)), log_level='info', code=0)

if __name__ == '__main__':
	jeedom_utils.write_pid(str(globals.pidfile))
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
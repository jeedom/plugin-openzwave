import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import logging
import globals,utils,dispatcher_utils,node_utils,serialization,server_utils
import threading
from openzwave.network import ZWaveNetwork,ZWaveController
from utilities.NetworkExtend import *
from utilities.Constants import *

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
	return utils.format_json_result()

def graceful_stop_network():
	logging.info('Graceful stopping the ZWave network.')
	if globals.network is not None:
		home_id = globals.network.home_id_str
		globals.network_is_running = False
		globals.network.stop()
		# We disconnect to the louie dispatcher
		dispatcher_utils.disconnect_dispatcher()
		globals.network.destroy()
		# avoid a second pass
		globals.network = None
		logging.info('The Openzwave REST-server was stopped in a normal way')
		globals.files_manager.backup_xml_config('stop', home_id)
	else:
		logging.info('The Openzwave REST-server is already stopped')
	return utils.format_json_result()

def create_network():
	globals.network = ZWaveNetwork(globals.options, autostart=False)

def network_ready(network):
	logging.info(
		"Openzwave network is ready with %d nodes (%d are sleeping). All nodes are queried, the network is fully functional." % (
		network.nodes_count, utils.get_sleeping_nodes_count(),))
	utils.write_config()
	globals.network_information.assign_controller_notification(ZWaveController.SIGNAL_CTRL_NORMAL, "Network is ready")
	save_network_state(network.state)

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

def save_network_state(network_state):
	globals.jeedom_com.add_changes('network::state', {"value": network_state})

def network_failed(network):
	logging.error("Openzwave network can't load")
	globals.network_information.assign_controller_notification(ZWaveController.SIGNAL_CTRL_ERROR, "Network have failed")
	save_network_state(network.state)

def network_awaked(network):
	logging.info(
		"Openzwave network is awake: %d nodes were found (%d are sleeping). All listening nodes are queried, but some sleeping nodes may be missing." % (
		network.nodes_count, utils.get_sleeping_nodes_count(),))
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
	dispatcher_utils.add_dispatcher_listen(node_utils.node_group_changed, ZWaveNetwork.SIGNAL_GROUP)
	save_network_state(network.state)
	if globals.ghost_node_id is not None:
		logging.info("Last step for Removing Ghost node will start in %d sec" % (globals.sanity_checks_delay,))
		sanity_checks_job = threading.Timer(globals.sanity_checks_delay, sanity_checks, [True])
		sanity_checks_job.start()

def get_network_mode():
	if globals.network_information.controller_is_busy:
		if globals.network_information.actual_mode == ControllerMode.AddDevice:
			return NetworkInformation.AddDevice
		elif globals.network_information.actual_mode == ControllerMode.RemoveDevice:
			return NetworkInformation.RemoveDevice
	return NetworkInformation.Idle

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

def validate_association_groups_asynchronous():
	if not globals.network_is_running:
		return
	logging.debug("Check association")
	for node_id in list(globals.network.nodes):
		if node_utils.validate_association_groups(node_id):
			# avoid stress network
			time.sleep(3)

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

def manual_backup():
	logging.info('Manually creating a backup')
	if globals.files_manager.backup_xml_config('manual', globals.network.home_id_str):
		return utils.format_json_result(data='Xml config file successfully backup')
	else:
		return utils.format_json_result(sucess='error',data='See openzwave log file for details')

def perform_sanity_checks():
	if int(time.time()) > (globals.network_information.start_time + 120):
		if globals.network.state < globals.network.STATE_STARTED:
			logging.error("Timeouts occurred during communication with your ZWave dongle. Please check the openzwaved log file for more details.")
			try:
				graceful_stop_network()
			finally:
				os.remove(globals.pidfile)
			try:
				server_utils.shutdown_server()
			finally:
				sys.exit()
			sanity_checks()
	return utils.format_json_result()

def get_status():
	json_result = {}
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
					   'awakedDelay': globals.network_information.controller_awake_delay, 'mode': get_network_mode()
					   }
	return utils.format_json_result(data=json_result)

def get_health():
	network_health = {'updateTime': int(time.time())}
	nodes_data = {}
	if globals.network is not None and globals.network.state >= globals.network.STATE_STARTED and globals.network_is_running:
		for node_id in list(globals.network.nodes):
			nodes_data[node_id] = serialization.serialize_node_to_json(node_id)
	network_health['devices'] = nodes_data
	return utils.format_json_result(data=network_health)

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
	return utils.format_json_result(data=nodes_list)

def get_neighbours():
	neighbours = {'updateTime': int(time.time())}
	nodes_data = {}
	if globals.network is not None and globals.network.state >= globals.network.STATE_STARTED and globals.network_is_running:
		for node_id in list(globals.network.nodes):
			if node_id not in globals.disabled_nodes:
				nodes_data[node_id] = serialization.serialize_neighbour_to_json(node_id)
	neighbours['devices'] = nodes_data
	return utils.format_json_result(data=neighbours)

def get_oz_backups():
	return utils.format_json_result(data=globals.files_manager.get_openzwave_backups())

def get_oz_config():
	utils.write_config()
	filename = globals.data_folder + "/zwcfg_" + globals.network.home_id_str + ".xml"
	with open(filename, "r") as ins:
		content = ins.read()
	return utils.format_json_result(data=content)

def get_oz_logs():
	std_in, std_out = os.popen2("tail -n 1000 " + globals.data_folder + "/openzwave.log")
	std_in.close()
	lines = std_out.readlines()
	std_out.close()
	return utils.format_json_result(data=lines)
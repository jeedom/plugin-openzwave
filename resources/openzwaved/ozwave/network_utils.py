import sys
reload(sys)
sys.setdefaultencoding('utf8')
import logging
import globals,utils,dispatcher_utils,serialization
import threading
from openzwave.network import ZWaveNetwork,ZWaveController
from utilities.NetworkExtend import *

def start_network():
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
		dispatcher_utils.disconnect_dispatcher()
		globals.network.destroy()
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
	save_network_state(network.state)

def network_started(network):
	logging.info("Openzwave network are started with homeId %0.8x." % (network.home_id,))
	globals.network_is_running = True
	save_network_state(network.state)

def network_stopped(network):
	logging.info("Openzwave network are %s" % (network.state_str,))
	globals.network_is_running = False

def save_network_state(network_state):
	globals.jeedom_com.add_changes('network::state', {"value": network_state})

def network_failed(network):
	logging.error("Openzwave network can't load")
	save_network_state(network.state)

def network_awaked(network):
	logging.info(
		"Openzwave network is awake: %d nodes were found (%d are sleeping). All listening nodes are queried, but some sleeping nodes may be missing." % (
		network.nodes_count, utils.get_sleeping_nodes_count(),))
	logging.debug("Controller is: %s" % (network.controller,))
	globals.network_information.set_as_awake()
	save_network_state(network.state)
	if globals.ghost_node_id is not None:
		logging.info("Last step for Removing Ghost node will start in %d sec" % (globals.ghost_removal_delay,))
		ghost_removal_job = threading.Timer(globals.ghost_removal_delay, ghost_removal)
		ghost_removal_job.start()

def ghost_removal():
	logging.info("Perform ghost_removal")
	for node_id in list(globals.network.nodes):
		if globals.ghost_node_id is not None and node_id == globals.ghost_node_id and globals.network.nodes[node_id].is_failed:
			logging.info('* Try to remove a Ghost node (nodeId: %s)' % (node_id,))
			globals.network.manager.removeFailedNode(globals.network.home_id, node_id)
			time.sleep(10)
			if globals.ghost_node_id not in globals.network.nodes:
				globals.ghost_node_id = None
				logging.info('=> Ghost node removed (nodeId: %s)' % (node_id,))

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

def manual_backup():
	logging.info('Manually creating a backup')
	if globals.files_manager.backup_xml_config('manual', globals.network.home_id_str):
		return utils.format_json_result(data='Xml config file successfully backup')
	else:
		return utils.format_json_result(success='error',data='See openzwave log file for details')

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
		for value_id in my_node.get_values(genre='User'):
			if my_node.values[value_id].instance in instances:
				continue
			instances.append(my_node.values[value_id].instance)
		json_node['multi_instance'] = {'support': globals.COMMAND_CLASS_MULTI_CHANNEL in my_node.command_classes,'instances': len(instances)}
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
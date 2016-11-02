import logging
import globals,utils,dispatcher_utils,node_utils
import threading
from threading import Event, Thread

from openzwave.network import ZWaveNetwork
from utilities.NetworkExtend import *
from utilities.NodeExtend import *
from utilities.Constants import *
from utilities.FilesManager import FilesManager

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
		dispatcher_utils.disconnect_dispatcher()
		globals.network.destroy()
		# avoid a second pass
		globals.network = None
		logging.info('The Openzwave REST-server was stopped in a normal way')
		globals.files_manager.backup_xml_config('stop', home_id)
	else:
		logging.info('The Openzwave REST-server is already stopped')

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
	# threading.Thread(target=recovering_failed_nodes_asynchronous).start()
	# start listening for group changes
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
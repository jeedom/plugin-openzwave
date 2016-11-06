import logging
import time
import globals,node_utils,serialization
import network_utils,node_utils,value_utils,scene_utils,button_utils,commands

def controller_message_complete(network):
	logging.debug('The last message that was sent is now complete')

def controller_waiting(network, controller, state_int, state, state_full):
	logging.debug(state_full)
	# save actual state
	globals.network_information.assign_controller_notification(state, state_full)
	# notify jeedom
	node_utils.save_node_event(network.controller.node_id, globals.network_information.generate_jeedom_message())

def controller_command(network, controller, node, node_id, state_int, state, state_full, error_int, error, error_full):
	logging.info('%s (%s)' % (state_full, state))
	if error_int > 0:
		logging.error('%s (%s)' % (error_full, error,))

	# save actual state
	globals.network_information.assign_controller_notification(state, state_full, error, error_full)
	# notify jeedom
	node_utils.save_node_event(network.controller.node_id, globals.network_information.generate_jeedom_message())
	logging.debug('The controller is busy ? %s' % (globals.network_information.controller_is_busy,))

def get_controller_status():
	controller_status = {}
	if globals.network is not None and globals.network.state >= globals.network.STATE_STARTED and globals.network_is_running:
		if globals.network.controller:
			controller_status = serialization.serialize_controller_to_json()
	return utils.format_json_result(data=controller_status)

def hard_reset():
	globals.network.controller.hard_reset()
	logging.info('The controller becomes a primary controller ready to add devices to a new network')
	time.sleep(3)
	network_utils.start_network()
	
def hard_reset():
	globals.network.controller.hard_reset()
	logging.info('The controller becomes a primary controller ready to add devices to a new network')
	time.sleep(3)
	network_utils.start_network()
	return utils.format_json_result()
	
def receive_configuration():
	if not network_utils.can_execute_network_command(0):
		raise Exception('Controller is busy')
	logging.info("Receive Configuration")
	return utils.format_json_result(data=globals.network.manager.receiveConfiguration(globals.network.home_id))

def transfer_primary_role():
	if not network_utils.can_execute_network_command(0):
		raise Exception('Controller is bussy')
	logging.info("Transfer Primary Role")
	return utils.format_json_result(data=globals.network.manager.transferPrimaryRole(globals.network.home_id))
	
def create_new_primary():
	if not network_utils.can_execute_network_command(0):
		raise Exception('Controller is busy')
	logging.info("Add a new controller to the Z-Wave network")
	return utils.format_json_result(data=globals.network.manager.createNewPrimary(globals.network.home_id))

def test_network():
	if not network_utils.can_execute_network_command():
		raise Exception('Controller is bussy')
	logging.info("Sends a series of messages to a network node for testing network reliability")
	for node_id in list(globals.network.nodes):
		if node_id in globals.not_supported_nodes:
			logging.debug("skip not supported (nodeId: %s)" % (node_id,))
			continue
		if node_id in globals.disabled_nodes:
			continue
		globals.network.manager.testNetworkNode(globals.network.home_id, node_id, 3)
	return utils.format_json_result()
	
def serial_api_soft_reset():
	globals.network.controller.soft_reset()
	return utils.format_json_result()

def heal_network():
	if not network_utils.can_execute_network_command(0):
		raise Exception('Controller is busy')
	logging.info("Heal network by requesting node's rediscover their neighbors")
	for node_id in list(globals.network.nodes):
		if node_id in globals.not_supported_nodes:
			logging.debug("skip not supported (nodeId: "+str(node_id)+")")
			continue
		if globals.network.nodes[node_id].is_failed:
			logging.debug("skip presume dead (nodeId: "+str(node_id)+")")
			continue
		if globals.network.nodes[node_id].query_stage != "Complete":
			logging.debug("skip query stage not complete (nodeId:"+str(node_id)+")")
			continue
		if globals.network.nodes[node_id].generic == 1:
			logging.debug("skip Remote controller (nodeId: "+str(node_id)+") (they don't have neighbors)")
			continue
		if node_id in globals.disabled_nodes:
			continue
		globals.network.manager.healNetworkNode(globals.network.home_id, node_id, False)
	return utils.format_json_result()

def cancel_command():
	if globals.network.manager.cancelControllerCommand(globals.network.home_id):
		globals.network_information.controller_is_busy = False
	return utils.format_json_result()
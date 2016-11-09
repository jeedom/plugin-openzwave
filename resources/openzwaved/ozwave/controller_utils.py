import logging
import time
import globals,network_utils,utils
	
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
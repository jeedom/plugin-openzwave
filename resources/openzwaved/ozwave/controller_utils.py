import logging
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
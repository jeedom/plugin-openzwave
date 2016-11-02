import logging
import globals,node_utils

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
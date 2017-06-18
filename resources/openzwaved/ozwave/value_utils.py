import logging
import binascii
import math
import time
import globals,utils,node_utils
from utilities.NodeExtend import *

def value_added(network, node, value):
	if node.node_id in globals.not_supported_nodes:
		return
	value.lastData = value.data

def value_removed(network, node, value):
	if node.node_id in globals.not_supported_nodes:
		return
	if value == None:
		return
	if value.value_id in globals.pending_configurations:
		del globals.pending_configurations[value.value_id]

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

def save_value(node, value, last_update):
	logging.debug('A node value has been updated. nodeId:%s value:%s' % (node.node_id, value.label))
	if node.node_id in globals.network.nodes:
		if globals.network.nodes[node.node_id].last_update > last_update:
			logging.warning('Timing Error. nodeLastUpdate:%s Last_update:%s' % (str(globals.network.nodes[node.node_id].last_update), str(last_update)))
			return
		globals.network.nodes[node.node_id].last_update = last_update
		value.last_update = last_update
		node_utils.save_node_value_event(node.node_id, value.command_class, value.index, extract_data(value, False),value.instance)

def prepare_value_notification(node, value):
	if value.id_on_network in globals.pending_configurations:
		pending = globals.pending_configurations[value.id_on_network]
		if pending is not None:
			data = value.data
			if value.type == 'Short':
				data = utils.normalize_short_value(value.data)
			pending.data = data
	if not node.is_ready and value.command_class not in [globals.COMMAND_CLASS_CENTRAL_SCENE or value.command_class, globals.COMMAND_CLASS_SCENE_ACTIVATION]:
		if hasattr(value, 'lastData') and value.lastData == value.data:
			# we skip notification to avoid value refresh during the interview process
			return
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

def extract_data(value, display_raw=False, convert_fahrenheit=True):
	if value.type == "Bool":
		return value.data
	elif value.label == 'Temperature' and value.units == 'F' and convert_fahrenheit:
		return utils.convert_fahrenheit_celsius(value)
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

def get_value_by_label(node_id, command_class, instance, label):
	if node_id in globals.network.nodes:
		my_node = globals.network.nodes[node_id]
		for value_id in my_node.get_values(class_id=command_class):
			if my_node.values[value_id].instance == instance and my_node.values[value_id].label == label:
				return my_node.values[value_id]
	return None

def get_value_by_index(node_id, command_class, instance, index_id):
	if node_id in globals.network.nodes:
		my_node = globals.network.nodes[node_id]
		for value_id in my_node.get_values(class_id=command_class):
			if my_node.values[value_id].instance == instance and my_node.values[value_id].index == index_id:
				return my_node.values[value_id]
	return None
	
def mark_pending_change(my_value, data, wake_up_time=0):
	if my_value is not None and not my_value.is_write_only:
		globals.pending_configurations[my_value.id_on_network] = PendingConfiguration(data, wake_up_time)

def changes_value_polling(intensity, value):
	if intensity == 0: 
		if value.poll_intensity > 0:
			value.disable_poll()
	elif value.genre == "User" and not value.is_write_only: 
		if intensity > globals.maximum_poll_intensity:
			intensity = globals.maximum_poll_intensity
		value.enable_poll(intensity)

def set_config(_node_id, _index_id, _value, _size):
	utils.can_execute_command(0)
	utils.check_node_exist(_node_id)
	if _size > 4:
		_size = 4
	if _size not in [0, 1, 2, 4]:
		_size = 1
	logging.info('set_config for nodeId : %s index : %s, value : %s, size : %s' % (_node_id, _index_id, _value, _size))
	wake_up_time = node_utils.get_wake_up_interval(_node_id)
	if wake_up_time is None :
		wake_up_time = 0 
	wake_up_time += 10
	for value_id in globals.network.nodes[_node_id].get_values(class_id=globals.COMMAND_CLASS_CONFIGURATION, genre='All', type='All', readonly=False, writeonly='All'):
		if globals.network.nodes[_node_id].values[value_id].index == _index_id:
			value = _value.replace("@", "/")
			my_value = globals.network.nodes[_node_id].values[value_id]
			if my_value.type == 'Button':
				if value.lower() == 'true':
					result = globals.network.manager.pressButton(my_value.value_id)
				else:
					result = globals.network.manager.releaseButton(my_value.value_id)
			elif my_value.type == 'List' and _size == 0:
				# list item must be a string, the size must be set to 0
				result = globals.network.manager.setValue(value_id, value)
				mark_pending_change(my_value, value,wake_up_time)
			elif my_value.type == 'Bool':
				value = globals.network.nodes[_node_id].values[value_id].check_data(value)
				result = globals.network.manager.setValue(value_id, value)
				mark_pending_change(my_value, value,wake_up_time)
			else:
				# recommend parameters size is set to 0, for list item value handling
				if _size == 0:
					_size = 1
				# set a parameter list item with value or not configured device
				result = globals.network.nodes[_node_id].set_config_param(_index_id, int(value), _size)
				# don't mark list item if set with value
				if my_value is not None and my_value.type != 'List':
					mark_pending_change(my_value, value,wake_up_time)
			logging.debug('set_configuration result: %s' % (result,))
			return

	if _value.isdigit() and globals.network.nodes[_node_id].set_config_param(_index_id, int(_value), _size):
		logging.debug('set_configuration device without defined parameters')
	else:
		raise Exception('Configuration index : '+str(_index_id)+' not found')

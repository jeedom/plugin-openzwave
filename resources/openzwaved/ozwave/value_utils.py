import logging
import binascii
import math
import time
import globals,utils,node_utils
from utilities.NodeExtend import *
from ozwave.utilities.Constants import *
import node_utils,commands

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
		node_utils.save_node_value_event(node.node_id, int(time.time()), value.command_class, value.index, utils.get_standard_value_type(value.type), extract_data(value, False), utils.change_instance(value))

def prepare_value_notification(node, value):
	if value.id_on_network in globals.pending_configurations:
		pending = globals.pending_configurations[value.id_on_network]
		if pending is not None:
			# mark result
			data = value.data
			if value.type == 'Short':
				data = utils.normalize_short_value(value.data)
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

def get_value_by_label(node_id, command_class, instance, label, trace=True):
	if node_id in globals.network.nodes:
		my_node = globals.network.nodes[node_id]
		for value_id in my_node.get_values(class_id=command_class):
			if my_node.values[value_id].instance == instance and my_node.values[value_id].label == label:
				return my_node.values[value_id]
	return None

def get_value_by_index(node_id, command_class, instance, index_id, trace=True):
	if node_id in globals.network.nodes:
		my_node = globals.network.nodes[node_id]
		for value_id in my_node.get_values(class_id=command_class):
			if my_node.values[value_id].instance == instance and my_node.values[value_id].index == index_id:
				return my_node.values[value_id]
	return None

def get_value_by_id(node_id, value_id):
	if node_id in globals.network.nodes:
		my_node = globals.network.nodes[node_id]
		if value_id in my_node.values:
			return my_node.values[value_id]
	logging.debug("get_value_by_id Value not found for node_id:%s, value_id:%s" % (node_id, value_id,))
	return None
	
def prepare_refresh(node_id, value_id, target_value=None, motor=False):
	if globals.suppress_refresh:
		return
	# logging.debug("prepare_refresh for nodeId:%s valueId:%s data:%s" % (node_id, value_id, target_value,))
	stop_refresh(node_id, value_id)
	starting_value = globals.network.nodes[node_id].values[value_id].data
	utils.create_worker(node_id, value_id, target_value, starting_value, 0, motor)
	globals.network.nodes[node_id].values[value_id].start_refresh_time = int(time.time())
	
def stop_refresh(node_id, value_id):
	# check if for a existing worker
	worker = globals.refresh_workers.get(value_id)
	if worker is not None:
		# logging.debug("Stop the timer")
		# Stop the timer, and cancel the execution of the timer action. This will only work if the timer is still in its waiting stage.
		worker.cancel()
		# remove worker
		del globals.refresh_workers[value_id]
	# reset start time if refresh is running to avoid start again
	globals.network.nodes[node_id].values[value_id].start_refresh_time = 0
	
def mark_pending_change(my_value, data, wake_up_time=0):
	if my_value is not None and not my_value.is_write_only:
		globals.pending_configurations[my_value.id_on_network] = PendingConfiguration(data, wake_up_time)

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
	return utils.format_json_result(False, 'valueId not exist', 'warning')


def changes_value_polling(intensity, value):
	if intensity == 0:  # disable the value polling for any value
		if value.poll_intensity > 0:
			value.disable_poll()
	elif value.genre == "User" and not value.is_write_only:  # we activate the value polling only on user genre value and is not a writeOnly
		if intensity > globals.maximum_poll_intensity:
			intensity = globals.maximum_poll_intensity
		value.enable_poll(intensity)

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

def refresh_switch_binary(node_id, value_id, target_value):
	if node_id in globals.network.nodes:
		my_value = globals.network.nodes[node_id].values[value_id]
		if my_value is not None:
			if my_value.data != target_value:
				logging.debug("Force refresh switch binary")
				my_value.refresh()

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

def set_config2(_node_id, _index_id, _value, _size):
	if globals.network_information.controller_is_busy:
		raise Exception('Controller is bussy')
	utils.check_node_exist(_node_id)
	if _size == 0:
		_size = 2
	if _size > 4:
		_size = 4
	logging.info('Set_config 2 for nodeId : '+str(_node_id)+' index : '+str(_index_id)+', value : '+str(_value)+', size : '+str(_size))	
	for value_id in globals.network.nodes[_node_id].get_values(class_id=COMMAND_CLASS_CONFIGURATION, genre='All', type='All', readonly=False, writeonly='All'):
		if globals.network.nodes[_node_id].values[value_id].index == _index_id:
			value = _value.replace("@", "/")
			my_value = globals.network.nodes[_node_id].values[value_id]
			if my_value.type == 'Button':
				if value.lower() == 'true':
					globals.network.manager.pressButton(my_value.value_id)
				else:
					globals.network.manager.releaseButton(my_value.value_id)
			elif my_value.type == 'List':
				globals.network.manager.setValue(value_id, value)
				mark_pending_change(my_value, value)
			elif my_value.type == 'Bool':
				value = commands.convert_to_value_type(my_value.type,value)
				globals.network.manager.setValue(value_id, value)
				mark_pending_change(my_value, value)
			else:
				value = commands.convert_to_value_type(my_value.type,value)
				globals.network.nodes[_node_id].set_config_param(_index_id, value, _size)
				if my_value is not None:
					mark_pending_change(my_value, value)
			return
	raise Exception('Configuration index : '+str(_index_id)+' not found')
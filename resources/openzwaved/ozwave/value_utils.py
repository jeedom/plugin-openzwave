import logging
import math
import time
import globals,utils,node_utils

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
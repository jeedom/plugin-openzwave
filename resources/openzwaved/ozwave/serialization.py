import logging
import globals,utils,node_utils,value_utils,network_utils
from utilities.Constants import *

def serialize_neighbour_to_json(node_id):
	json_result = {}
	if node_id in globals.network.nodes:
		my_node = globals.network.nodes[node_id]
		json_result['data'] = {}
		json_result['data']['product_name'] = {'value': my_node.product_name}
		json_result['data']['location'] = {'value': my_node.location}
		node_name = my_node.name
		if globals.network.controller.node_id == node_id:
			node_name = my_node.product_name
		if utils.is_none_or_empty(node_name):
			node_name = my_node.product_name
		if utils.is_none_or_empty(node_name):
			node_name = 'Unknown'
		json_result['data']['name'] = {'value': node_name}
		json_result['data']['isPrimaryController'] = {'value': globals.network.controller.node_id == node_id}
		neighbour_is_enabled = my_node.generic != 1 # not a remote control
		if my_node.generic == 8 and not my_node.is_listening_device:
			neighbour_is_enabled = len(my_node.neighbors) > 0
		json_result['data']['neighbours'] = {'value': list(my_node.neighbors), 'enabled': neighbour_is_enabled}
		json_result['data']['isDead'] = {'value': my_node.is_failed}
		json_result['data']['type'] = {'basic': my_node.basic, 'generic': my_node.generic, 'specific': my_node.specific}
		json_result['data']['state'] = {'value': utils.convert_query_stage_to_int(my_node.query_stage)}
		json_result['data']['isListening'] = {'value': my_node.is_listening_device}
		json_result['data']['isRouting'] = {'value': my_node.is_routing_device}
	else:
		logging.warning('This network does not contain any node with the id %s' % (node_id,))
	return json_result

def serialize_node_to_json(node_id):
	json_result = {}
	if node_id not in globals.network.nodes or node_id in globals.not_supported_nodes:
		return json_result
	my_node = globals.network.nodes[node_id]
	try:
		timestamp = int(my_node.last_update)
	except TypeError:
		timestamp = int(1)
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
	json_result['data'] = {}
	node_name = my_node.name
	if globals.network.controller.node_id == node_id:
		node_name = my_node.product_name
	if utils.is_none_or_empty(node_name):
		node_name = 'Unknown'
	json_result['data']['description'] = {'name': node_name, 'location': my_node.location,'product_name': my_node.product_name}
	json_result['data']['manufacturerId'] = {'value': manufacturer_id, 'hex': my_node.manufacturer_id}
	json_result['data']['vendorString'] = {'value': my_node.manufacturer_name}
	json_result['data']['manufacturerProductId'] = {'value': product_id, 'hex': my_node.product_id}
	json_result['data']['product_name'] = {'value': my_node.product_name}
	json_result['data']['location'] = {'value': my_node.location}
	json_result['data']['name'] = {'value': my_node.name}
	json_result['data']['version'] = {'value': my_node.version}
	json_result['data']['manufacturerProductType'] = {'value': product_type, 'hex': my_node.product_type}
	json_result['data']['neighbours'] = {'value': list(my_node.neighbors)}
	json_result['data']['isVirtual'] = {'value': ''}
	if globals.network.controller.node_id == node_id and my_node.basic == 1:
		json_result['data']['basicType'] = {'value': 2}
	else:
		json_result['data']['basicType'] = {'value': my_node.basic}
	json_result['data']['genericType'] = {'value': my_node.generic}
	json_result['data']['specificType'] = {'value': my_node.specific}
	json_result['data']['type'] = {'value': my_node.type}
	json_result['data']['state'] = {'value': str(my_node.query_stage)}
	json_result['data']['isAwake'] = {'value': my_node.is_awake, "updateTime": timestamp}
	json_result['data']['isReady'] = {'value': my_node.is_ready, "updateTime": timestamp}
	json_result['data']['isEnable'] = {'value': int(node_id) not in globals.disabled_nodes}
	json_result['data']['isInfoReceived'] = {'value': my_node.is_info_received}
	try:
		can_wake_up = my_node.can_wake_up()
	except RuntimeError:
		can_wake_up = False
	json_result['data']['can_wake_up'] = {'value': can_wake_up}
	json_result['data']['battery_level'] = {'value': my_node.get_battery_level()}
	json_result['last_notification'] = {}
	next_wake_up = None
	if node_id in globals.node_notifications:
		notification = globals.node_notifications[node_id]
		next_wake_up = notification.next_wake_up
		json_result['last_notification'] = {"receiveTime": notification.receive_time,"description": notification.description,"help": notification.help}
	json_result['data']['wakeup_interval'] = {'value': node_utils.get_wake_up_interval(node_id), 'next_wakeup': next_wake_up}
	json_result['data']['isFailed'] = {'value': my_node.is_failed}
	json_result['data']['isListening'] = {'value': my_node.is_listening_device}
	json_result['data']['isRouting'] = {'value': my_node.is_routing_device}
	json_result['data']['isSecurity'] = {'value': my_node.is_security_device}
	json_result['data']['isBeaming'] = {'value': my_node.is_beaming_device}
	json_result['data']['isFrequentListening'] = {'value': my_node.is_frequent_listening_device}
	json_result['data']['security'] = {'value': my_node.security}
	json_result['data']['lastReceived'] = {'updateTime': timestamp}
	json_result['data']['maxBaudRate'] = {'value': my_node.max_baud_rate}
	json_result['data']['is_enable'] = {'value': int(node_id) not in globals.disabled_nodes}
	json_result['data']['isZwavePlus'] = {'value': my_node.is_zwave_plus}
	statistics = globals.network.manager.getNodeStatistics(globals.network.home_id, node_id)
	send_total = statistics['sentCnt'] + statistics['sentFailed']
	percent_delivered = 0
	if send_total > 0:
		percent_delivered = (statistics['sentCnt'] * 100) / send_total
	average_request_rtt = statistics['averageRequestRTT']
	json_result['data']['statistics'] = {'total': send_total, 'delivered': percent_delivered,'deliveryTime': average_request_rtt}
	have_group = False
	query_stage_index = utils.convert_query_stage_to_int(my_node.query_stage)
	if my_node.groups and query_stage_index >= 12 and my_node.generic != 2:
		check_for_group = len(my_node.groups) > 0
		if check_for_group :
			have_group = node_utils.check_primary_controller(my_node)
	else:
		check_for_group = False
	json_result['data']['is_groups_ok'] = {'value': have_group, 'enabled': check_for_group}
	is_neighbours_ok = query_stage_index > 13
	if my_node.generic == 1:
		is_neighbours_ok = False
	if my_node.generic == 8 and not my_node.is_listening_device:
		is_neighbours_ok = False
	json_result['data']['is_neighbours_ok'] = {'value': len(my_node.neighbors) > 0,'neighbors': len(my_node.neighbors), 'enabled': is_neighbours_ok}
	json_result['data']['is_manufacturer_specific_ok'] = {'value': my_node.manufacturer_id != 0 and my_node.product_id != 0 and my_node.product_type != 0,'enabled': query_stage_index >= 7} 
	is_secured = value_utils.get_value_by_label(node_id, COMMAND_CLASS_SECURITY, 1, 'Secured', False)
	json_result['data']['isSecured'] = {'value': is_secured is not None and is_secured.data, 'enabled' : is_secured is not None}
	pending_changes = 0
	json_result['instances'] = {"updateTime": timestamp}
	json_result['groups'] = {"updateTime": timestamp}
	for groupIndex in list(my_node.groups):
		group = my_node.groups[groupIndex]
		pending_state = 1
		if my_node.node_id in globals.pending_associations:
			pending_associations = globals.pending_associations[my_node.node_id]
			if groupIndex in pending_associations:
				pending_association = pending_associations[groupIndex]
				if pending_association.state is not None:
					pending_state = pending_association.state
					if pending_state is not None and pending_state > 1:
						pending_changes += 1
		json_result['groups'][groupIndex] = {"label": group.label, "maximumAssociations": group.max_associations,"associations": list(group.associations_instances),"pending": pending_state}
	json_result['associations'] = serialize_associations(node_id)
	if node_id in globals.node_notifications:
		notification = globals.node_notifications[node_id]
		json_result['last_notification'] = {"receiveTime": notification.receive_time,"code": notification.code,"description": notification.description,"help": notification.help,"next_wakeup": notification.next_wake_up}
	else:
		json_result['last_notification'] = {}
	json_result['command_classes'] = {}
	for command_class in my_node.command_classes:
		json_result['command_classes'][command_class] = {'name': my_node.get_command_class_as_string(command_class),'hex': '0x' + utils.convert_user_code_to_hex(command_class)}
	instances = []
	for val in my_node.get_values():
		my_value = my_node.values[val]
		if my_value.command_class is None or (my_value.instance > 1 and my_value.command_class in [COMMAND_CLASS_ZWAVEPLUS_INFO,COMMAND_CLASS_VERSION]):
			continue
		try:
			label = my_value.label
		except Exception, exception:
			label = exception.message
			logging.error('Value label contains unsupported text: %s' % (str(exception),))
		try:
			value_help = my_value.help
		except Exception, exception:
			value_help = exception.message
			logging.error('Value help contains unsupported text: %s' % (str(exception),))
		if label == 'Temperature' and my_value.units == 'F':
			value_units = 'C'
		else:
			value_units = my_value.units
		if my_value.genre != 'Basic':
			standard_type = utils.get_standard_value_type(my_value.type)
		else:
			standard_type = 'int'
		if my_value.is_write_only:
			value2 = None
		else:
			if my_value.type == 'Short':
				value2 = utils.normalize_short_value(my_value.data)
			else:
				value2 = value_utils.extract_data(my_value)
		instance2 = utils.change_instance(my_value)
		if my_value.index:
			index2 = my_value.index
		else:
			index2 = 0
		pending_state = None
		expected_data = None
		data_items = utils.concatenate_list(my_value.data_items)
		if my_value.id_on_network in globals.pending_configurations:
			pending = globals.pending_configurations[my_value.id_on_network]
			if pending is not None:
				pending_state = pending.state
				expected_data = pending.expected_data
				if pending_state is not None and pending_state > 1:
					pending_changes += 1
		try:
			timestamp = int(my_value.last_update)
		except TypeError:
			timestamp = int(1)
		if my_value.genre == 'User' and not my_value.instance in instances:
			instances.append(my_node.values[val].instance)
		if instance2 not in json_result['instances']:
			json_result['instances'][instance2] = {"updateTime": timestamp}
			json_result['instances'][instance2]['commandClasses'] = {"updateTime": timestamp}
			json_result['instances'][instance2]['commandClasses']['data'] = {"updateTime": timestamp}
			serialize_command_class_info(instance2, json_result, my_node, my_value, timestamp)
			serialize_command_class_data(data_items, expected_data, index2, instance2, json_result, label, my_value, pending_state, standard_type, timestamp, value2, value_help, value_units)
		elif my_value.command_class not in json_result['instances'][instance2]['commandClasses']:
			json_result['instances'][instance2]['commandClasses'][my_value.command_class] = {"updateTime": timestamp}
			serialize_command_class_info(instance2, json_result, my_node, my_value, timestamp)
			serialize_command_class_data(data_items, expected_data, index2, instance2, json_result, label, my_value,pending_state, standard_type, timestamp, value2, value_help, value_units)
		elif index2 not in json_result['instances'][instance2]['commandClasses'][my_value.command_class]['data']:
			serialize_command_class_data(data_items, expected_data, index2, instance2, json_result, label, my_value,pending_state, standard_type, timestamp, value2, value_help, value_units)
	json_result['data']['pending_changes'] = {'count': pending_changes}
	json_result['multi_instance'] = {'support': COMMAND_CLASS_MULTI_CHANNEL in my_node.command_classes,'instances': len(instances)}
	return json_result

def serialize_command_class_data(data_items, expected_data, index2, instance2, json_result, label, my_value,pending_state, standard_type, timestamp, value2, value_help, value_units):
	json_result['instances'][instance2]['commandClasses'][my_value.command_class]['data'][index2] = {"val": value2,
																									 "name": label,
																									 "help": value_help,
																									 "type": standard_type,
																									 "typeZW": my_value.type,
																									 "units": value_units,
																									 "data_items": data_items,
																									 "read_only": my_value.is_read_only,
																									 "write_only": my_value.is_write_only,
																									 "updateTime": timestamp,
																									 "genre": my_value.genre,
																									 "value_id": my_value.value_id,
																									 "poll_intensity": my_value.poll_intensity,
																									 "pendingState": pending_state,
																									 "expected_data": expected_data}


def serialize_command_class_info(instance2, json_result, my_node, my_value, timestamp):
	json_result['instances'][instance2]['commandClasses'][my_value.command_class] = {"name": my_node.get_command_class_as_string(my_value.command_class)}
	json_result['instances'][instance2]['commandClasses'][my_value.command_class]['data'] = {"updateTime": timestamp}

def serialize_controller_to_json():
	json_result = {'data': {}}
	json_result['data']['roles'] = {'isPrimaryController': globals.network.controller.is_primary_controller, 'isStaticUpdateController': globals.network.controller.is_static_update_controller, 'isBridgeController': globals.network.controller.is_bridge_controller}
	json_result['data']['nodeId'] = {'value': globals.network.controller.node_id}
	json_result['data']['mode'] = {'value': network_utils.get_network_mode()}
	json_result['data']['softwareVersion'] = {'ozw_library': globals.network.controller.ozw_library_version, 'python_library': globals.network.controller.python_library_version}
	json_result['data']['notification'] = globals.network_information.last_controller_notifications[0]
	json_result['data']['isBusy'] = {"value": globals.network_information.controller_is_busy}
	json_result['data']['networkstate'] = {"value": globals.network.state}
	return json_result

def serialize_associations(node_id):
	json_result = {}
	for other_node_id in list(globals.network.nodes):
		other_node = globals.network.nodes[other_node_id]
		if other_node.groups:
			for group in list(other_node.groups):
				if node_id in other_node.groups[group].associations:
					value = {'index': other_node.groups[group].index, 'label': other_node.groups[group].label}
					try:
						json_result[other_node_id].append(value)
					except KeyError:
						json_result[other_node_id] = [value]
	return json_result

def serialize_node_notification(node_id):
	json_result = {}
	if node_id in globals.not_supported_nodes:
		return json_result
	my_node = globals.network.nodes[node_id]
	if node_id in globals.node_notifications:
		notification = globals.node_notifications[node_id]
		return {"receiveTime": notification.receive_time,"description": notification.description,"isFailed": my_node.is_failed}
	else:
		return {"receiveTime": None,"description": None,"isFailed": my_node.is_failed}
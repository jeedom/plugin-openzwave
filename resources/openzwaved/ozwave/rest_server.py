#!flask/bin/python
import os
import sys
import datetime
import shutil
import binascii
import threading
import logging
import time
from lxml import etree
import globals,utils,network_utils,node_utils,dispatcher_utils
import server_utils,manager_utils,value_utils,commands,serialization
from utilities.Constants import *
from utilities.NodeExtend import *
from utilities.NetworkExtend import *
try:
	from flask import Flask, jsonify, abort, request, make_response, redirect, url_for
	from flask_httpauth import HTTPBasicAuth
except Exception as e:
	print(globals.MSG_CHECK_DEPENDENCY, 'error')
	print("Error: %s" % str(e), 'error')
	sys.exit(1)

auth = HTTPBasicAuth()
globals.app = app = Flask(__name__, static_url_path='/static')

'''
default routes
'''

@app.before_first_request
def _run_on_start():
	pass

@app.route('/', methods=['GET'])
def default_index():
	with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'index.html')), 'rb') as f:
		content = f.read()
	return content


@app.errorhandler(400)
def not_found400(error):
	logging.error('%s %s' % (error, request.url))
	return utils.format_json_result(success='error', data='Bad request')

@app.errorhandler(404)
def not_found404(error):
	logging.error('%s %s' % (error, request.url))
	return utils.format_json_result(success='error', data='Not found')

@app.teardown_appcontext
def close_network(error):
	if error is not None:
		logging.error('%s %s' % (error, 'teardown'))

@app.errorhandler(Exception)
def unhandled_exception(exception):
	return utils.format_json_result(success='error', data=str(exception))

@auth.verify_password
def verify_password(username, password):
	return password == globals.apikey

'''
devices routes
'''

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[0].commandClasses[133].Get()', methods=['GET'])
@auth.login_required
def refresh_assoc(node_id):
	utils.check_node_exist(node_id)
	logging.debug("refresh_assoc for nodeId: %s" % (node_id,))
	for val in globals.network.nodes[node_id].get_values(class_id=COMMAND_CLASS_ASSOCIATION):
		globals.network.nodes[node_id].values[val].refresh()
	return utils.format_json_result()
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[0].commandClasses[133].data', methods=['GET'])
@auth.login_required
def get_assoc(node_id):
	utils.check_node_exist(node_id)
	logging.debug("get_assoc for nodeId: %s" % (node_id,))
	config = {}
	if globals.network.nodes[node_id].groups:
		config['supported'] = {'value': True}
		for group in list(globals.network.nodes[node_id].groups):
			config[globals.network.nodes[node_id].groups[group].index] = {}
			config[globals.network.nodes[node_id].groups[group].index]['nodes'] = {'value': list(globals.network.nodes[node_id].groups[group].associations), 'updateTime': int(time.time()), 'invalidateTime': 0}
	return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[0].commandClasses[0x85].Remove(<int:group_index>,<int:target_node_id>)', methods=['GET'])
@auth.login_required
def remove_assoc(node_id, group_index, target_node_id):
	if globals.network_information.controller_is_busy:
		raise Exception('Controller is bussy')
	utils.check_node_exist(node_id)
	logging.info("remove_assoc to nodeId: %s in group %s with nodeId: %s" % (node_id, group_index, target_node_id,))
	my_node = globals.network.nodes[node_id]
	if my_node.node_id not in globals.pending_associations:
		globals.pending_associations[my_node.node_id] = dict()
	globals.pending_associations[my_node.node_id][group_index] = PendingAssociation(pending_added=None, pending_removed=target_node_id, timeout=0)
	globals.network.manager.removeAssociation(globals.network.home_id, node_id, group_index, target_node_id)
	return utils.format_json_result()
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[0].commandClasses[0x85].Add(<int:group_index>,<int:target_node_id>)', methods=['GET'])
@auth.login_required
def add_assoc(node_id, group_index, target_node_id):
	if globals.network_information.controller_is_busy:
		raise Exception('Controller is bussy')
	utils.check_node_exist(node_id)
	logging.info("add_assoc to nodeId: %s in group %s with nodeId: %s" % (node_id, group_index, target_node_id,))
	my_node = globals.network.nodes[node_id]
	if not (target_node_id in my_node.groups[group_index].associations):
		if my_node.node_id not in globals.pending_associations:
			globals.pending_associations[my_node.node_id] = dict()
	globals.pending_associations[my_node.node_id][group_index] = PendingAssociation(pending_added=target_node_id, pending_removed=None, timeout=0)
	globals.network.manager.addAssociation(globals.network.home_id, node_id, group_index, target_node_id)
	return utils.format_json_result()

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].Associations[<int:group_index>].Remove(<int:target_node_id>,<int:target_node_instance>)', methods=['GET'])
@auth.login_required
def remove_association(node_id, group_index, target_node_id, target_node_instance):
	if globals.network_information.controller_is_busy:
		raise Exception('Controller is bussy')
	utils.check_node_exist(node_id)
	logging.info("remove_association to nodeId: %s in group %s with nodeId: %s instance %s" % (node_id, group_index, target_node_id, target_node_instance,))
	my_node = globals.network.nodes[node_id]
	if my_node.node_id not in globals.pending_associations:
		globals.pending_associations[my_node.node_id] = dict()
	globals.pending_associations[my_node.node_id][group_index] = PendingAssociation(pending_added=None, pending_removed=target_node_id, timeout=0)
	globals.network.manager.removeAssociation(globals.network.home_id, node_id, group_index, target_node_id, target_node_instance)
	return utils.format_json_result()
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].Associations[<int:group_index>].Add(<int:target_node_id>,<int:target_node_instance>)', methods=['GET'])
@auth.login_required
def add_association(node_id, group_index, target_node_id, target_node_instance):
	if globals.network_information.controller_is_busy:
		raise Exception('Controller is bussy')
	utils.check_node_exist(node_id)
	logging.info("add_association to nodeId: %s in group %s with nodeId: %s instance %s" % (
	node_id, group_index, target_node_id, target_node_instance,))
	my_node = globals.network.nodes[node_id]
	if not (target_node_id in my_node.groups[group_index].associations):
		if my_node.node_id not in globals.pending_associations:
			globals.pending_associations[my_node.node_id] = dict()
	globals.pending_associations[my_node.node_id][group_index] = PendingAssociation(pending_added=target_node_id, pending_removed=None, timeout=0)
	globals.network.manager.addAssociation(globals.network.home_id, node_id, group_index, target_node_id, target_node_instance)
	return utils.format_json_result()
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].SetPolling(<int:value_id>,<frequency>)', methods=['GET'])
@auth.login_required
def set_polling2(node_id, value_id, frequency):
	utils.check_node_exist(node_id)
	logging.info("set_polling for nodeId: %s ValueId %s at: %s" % (node_id, value_id, frequency,))
	my_node = globals.network.nodes[node_id]
	for val in my_node.get_values():
		my_value = my_node.values[val]
		if my_value.value_id == value_id:
			changes_value_polling(frequency, my_value)
			for value_id in my_node.get_values(class_id=my_value.command_class):
				if my_node.values[value_id].instance == my_value.instance and my_node.values[
					value_id].index != my_value.index_id:
					changes_value_polling(0, value_id)
			return utils.format_json_result()
	return utils.format_json_result(False, 'valueId: %s not found' % (value_id,), 'warning')
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].SetPolling(<int:frequency>)', methods=['GET'])
@auth.login_required
def set_polling_value(node_id, instance_id, cc_id, index, frequency):
	utils.check_node_exist(node_id)
	logging.info("set_polling_value for nodeId: %s instance: %s cc:%s index:%s at: %s" % (node_id, instance_id, cc_id, index, frequency,))
	for val in globals.network.nodes[node_id].get_values(class_id=int(cc_id, 16)):
		if globals.network.nodes[node_id].values[val].instance - 1 == instance_id:
			my_value = globals.network.nodes[node_id].values[val]
			if frequency == 0 & my_value.poll_intensity > 0:
				my_value.disable_poll()
			else:
				if globals.network.nodes[node_id].values[val].index == index:
					changes_value_polling(frequency, my_value)
				else:
					if my_value.poll_intensity > 0:
						my_value.disable_poll()
	utils.write_config()
	return utils.format_json_result()

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].SetPolling(<int:frequency>)', methods=['GET'])
@auth.login_required
def set_polling_instance(node_id, instance_id, cc_id, frequency):
	utils.check_node_exist(node_id)
	logging.info("set_polling_instance for nodeId: %s instance: %s cc:%s at: %s" % (node_id, instance_id, cc_id, frequency,))
	polling_apply = False
	for val in globals.network.nodes[node_id].get_values(class_id=int(cc_id, 16)):
		if globals.network.nodes[node_id].values[val].instance - 1 == instance_id:
			my_value = globals.network.nodes[node_id].values[val]
			if frequency == 0 & my_value.poll_intensity > 0:
				my_value.disable_poll()
			else:
				if not polling_apply:
					polling_apply = True
					changes_value_polling(frequency, my_value)
				else:
					if my_value.poll_intensity > 0:
						my_value.disable_poll()
	utils.write_config()
	return utils.format_json_result()
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].SetWakeup(<wake_up_time>)', methods=['GET'])
@auth.login_required
def set_wake_up(node_id, wake_up_time):
	utils.check_node_exist(node_id)
	logging.info("set wakeup interval for nodeId %s at: %s" % (node_id, wake_up_time,))
	for val in globals.network.nodes[node_id].get_values(class_id=COMMAND_CLASS_WAKE_UP):
		my_value = globals.network.nodes[node_id].values[val]
		if my_value.label == "Wake-up Interval":
			return utils.format_json_result(set_value(node_id, my_value.value_id, int(wake_up_time)))
	return utils.format_json_result(False, 'Wake-up Interval not found', 'warning')
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].Refresh()', methods=['GET'])
@auth.login_required
def request_all_config_params(node_id):
	utils.check_node_exist(node_id)
	logging.info("Request the values of all known configurable parameters from nodeId %s" % (node_id,))
	for val in globals.network.nodes[node_id].get_values(class_id=COMMAND_CLASS_CONFIGURATION):
		configuration_item = globals.network.nodes[node_id].values[val]
		if configuration_item.id_on_network in globals.pending_configurations:
			del globals.pending_configurations[configuration_item.id_on_network]
	globals.network.manager.requestAllConfigParams(globals.network.home_id, node_id)
	return utils.format_json_result()
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].Get(<int:index_id>)', methods=['GET'])
@auth.login_required
def refresh_config(node_id, index_id):
	utils.check_node_exist(node_id)
	logging.debug("refresh_config for nodeId:%s index_id:%s" % (node_id, index_id,))
	for val in globals.network.nodes[node_id].get_values(class_id=COMMAND_CLASS_CONFIGURATION):
		if globals.network.nodes[node_id].values[val].index == index_id:
			globals.network.nodes[node_id].values[val].refresh()
	return utils.format_json_result()
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].SetDeviceName(<string:location>,<string:name>,<int:is_enable>)', methods=['GET'])
@auth.login_required
def set_device_name(node_id, location, name, is_enable):
	utils.check_node_exist(node_id)
	logging.info("set_device_name node_id:%s new name ; '%s'. Is enable: %s" % (node_id, name, is_enable,))
	if node_id in globals.disabled_nodes and is_enable:
		globals.disabled_nodes.remove(node_id)
	elif node_id not in globals.disabled_nodes and not is_enable:
		globals.disabled_nodes.append(node_id)
	name = name.encode('utf8')
	name = name.replace('+', ' ')
	globals.network.nodes[node_id].set_field('name', name)
	location = location.encode('utf8')
	location = location.replace('+', ' ')
	globals.network.nodes[node_id].set_field('location', location)
	return utils.format_json_result()

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].data', methods=['GET'])
@auth.login_required
def get_config(node_id):
	utils.check_node_exist(node_id)
	logging.debug("get_config for nodeId:%s" % (node_id,))
	config = {}
	for val in globals.network.nodes[node_id].values:
		list_values = []
		my_value = globals.network.nodes[node_id].values[val]
		if my_value.command_class == COMMAND_CLASS_CONFIGURATION:
			config[globals.network.nodes[node_id].values[val].index] = {}
			if my_value.type == "List" and not my_value.is_read_only:
				result_data = globals.network.manager.getValueListSelectionNum(my_value.value_id)
				values = my_value.data_items
				for index_item, value_item in enumerate(values):
					list_values.append(value_item)
					if value_item == my_value.data_as_string:
						result_data = index_item
			elif my_value.type == "Bool" and not my_value.data:
				result_data = 0
			elif my_value.type == "Bool" and my_value.data:
				result_data = 1
			else:
				result_data = my_value.data
			config[my_value.index]['val'] = {'value2': my_value.data, 'value': result_data,'value3': my_value.label, 'value4': sorted(list_values),'updateTime': int(time.time()), 'invalidateTime': 0}
	return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:source_id>].CopyConfigurations(<int:target_id>)', methods=['GET'])
@auth.login_required
def copy_configuration(source_id, target_id):
	if globals.network_information.controller_is_busy:
		raise Exception('Controller is bussy')
	logging.info("copy_configuration from source_id:%s to target_id:%s" % (source_id, target_id,))
	items = 0
	utils.check_node_exist(source_id)
	utils.check_node_exist(target_id)
	source = globals.network.nodes[source_id]
	target = globals.network.nodes[target_id]
	if source.manufacturer_id == target.manufacturer_id and source.product_type == target.product_type and source.product_id == target.product_id:
		for val in source.get_values():
			configuration_value = source.values[val]
			if configuration_value.genre == 'Config':
				if configuration_value.type == 'Button':
					continue
				if configuration_value.is_write_only:
					continue
				try:
					target_value = value_utils.get_value_by_index(target_id, COMMAND_CLASS_CONFIGURATION, 1,configuration_value.index)
					if target_value is not None:
						if configuration_value.type == 'List':
							globals.network.manager.setValue(target_value.value_id, configuration_value.data)
							accepted = True
						else:
							accepted = target.set_config_param(configuration_value.index,configuration_value.data)
						if accepted:
							items += 1
							value_utils.mark_pending_change(target_value, configuration_value.data)
				except Exception as error:
					logging.error('Copy configuration %s (index:%s): %s' % (
					configuration_value.label, configuration_value.index, str(error),))
		my_result = items != 0
	else:
		return utils.format_json_result(False,'The two nodes must be with same: manufacturer_id, product_type and product_id','warning')
	return jsonify({'result': my_result, 'copied_configuration_items': items})



@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses', methods=['GET'])
@auth.login_required
def get_command_classes(node_id):
	my_result = {}
	logging.debug("get_command_classes for nodeId:%s" % (node_id,))
	utils.check_node_exist(node_id)
	for val in globals.network.nodes[node_id].get_values():
		my_result[globals.network.nodes[node_id].values[val].command_class] = {}
	return jsonify(my_result)



@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].Get()', methods=['GET'])
@auth.login_required
def get_value(node_id, instance_id, cc_id):
	utils.check_node_exist(node_id)
	try:
		globals.network.nodes[node_id].last_update
	except NameError:
		globals.network.nodes[node_id].last_update = time.time()
	now = datetime.datetime.now()
	if isinstance(globals.network.nodes[node_id].last_update, float):
		last_update = datetime.datetime.fromtimestamp(globals.network.nodes[node_id].last_update)
	else:
		last_update = datetime.datetime.now()
		globals.network.nodes[node_id].last_update = time.time()
	last_delta = last_update + datetime.timedelta(seconds=30)
	if now > last_delta and globals.network.nodes[node_id].is_listening_device and globals.network.nodes[node_id].is_ready:
		globals.network.manager.requestNodeDynamic(globals.network.home_id, globals.network.nodes[node_id].node_id)
		globals.network.nodes[node_id].last_update = time.time()
		logging.debug("Fetch the dynamic command class data for the node %s" % (node_id,))
	return utils.format_json_result()

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].val', methods=['GET'])
@auth.login_required
def get_value6(node_id, instance_id, index, cc_id):
	utils.check_node_exist(node_id)
	for val in globals.network.nodes[node_id].get_values(class_id=int(cc_id, 16)):
		if globals.network.nodes[node_id].values[val].instance - 1 == instance_id and globals.network.nodes[node_id].values[
			val].index == index:
			if globals.network.nodes[node_id].values[val].units == 'F':
				return str(utils.convert_fahrenheit_celsius(globals.network.nodes[node_id].values[val]))
			else:
				return str(globals.network.nodes[node_id].values[val].data)
	return jsonify({})

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].ForceRefresh()', methods=['GET'])
@auth.login_required
def force_refresh_one_value(node_id, instance_id, index, cc_id):
	return refresh_one_value(node_id, instance_id, index, int(cc_id, 16))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<int:cc_id>].data[<int:index>].Refresh()', methods=['GET'])
@auth.login_required
def refresh_one_value(node_id, instance_id, index, cc_id):
	utils.check_node_exist(node_id)
	for val in globals.network.nodes[node_id].get_values(class_id=cc_id):
		if globals.network.nodes[node_id].values[val].instance - 1 == instance_id and globals.network.nodes[node_id].values[val].index == index:
			globals.network.nodes[node_id].values[val].refresh()
			return utils.format_json_result()
	return utils.format_json_result(False, 'This device does not contain the specified value', 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[0x63].data[<int:index>].code', methods=['GET'])
@auth.login_required
def get_user_code(node_id, instance_id, index):
	utils.check_node_exist(node_id)
	logging.debug("getValueRaw nodeId:%s instance:%s commandClasses:%s index:%s" % (
	node_id, instance_id, hex(COMMAND_CLASS_USER_CODE), index))
	my_result = {}
	my_node = globals.network.nodes[node_id]
	for val in my_node.get_values(class_id=COMMAND_CLASS_USER_CODE):
		my_value = my_node.values[val]
		if my_value.instance - 1 == instance_id and my_value.index == index:
			user_code = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			timestamp = int(1)
			raw_data = value_utils.extract_data(my_value)
			if raw_data != '00000000000000000000':
				try:
					timestamp = int(my_value.last_update)
					chunks, chunk_size = len(raw_data), len(raw_data) / 10
					user_code = [int(raw_data[i:i + chunk_size], 16) for i in range(0, chunks, chunk_size)]
				except TypeError:
					timestamp = int(1)
			my_result = {'invalidateTime': int(time.time() - datetime.timedelta(seconds=30).total_seconds()), 'type': utils.get_standard_value_type(my_value.type),'value': user_code,'updateTime': timestamp}
			break
	return jsonify(my_result)

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[0x63].data', methods=['GET'])
@auth.login_required
def get_user_codes(node_id, instance_id):
	utils.check_node_exist(node_id)
	logging.debug("getValueAllRaw nodeId:%s instance:%s commandClasses:%s" % (node_id, instance_id, hex(COMMAND_CLASS_USER_CODE),))
	result_value = {}
	my_node = globals.network.nodes[node_id]
	for val in my_node.get_values(class_id=COMMAND_CLASS_USER_CODE):
		my_value = my_node.values[val]
		if my_value.instance - 1 == instance_id:
			if my_value.index == 0:
				continue
			if my_value.index > 10:
				continue
			raw_data = value_utils.extract_data(my_value)
			if raw_data == '00000000000000000000':
				result_value[my_value.index] = None
			else:
				result_value[my_value.index] = {}
	return jsonify(result_value)

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].UserCode.SetRaw(<int:slot_id>,[<string:value>],1)', methods=['GET'])
@auth.login_required
def set_user_code(node_id, slot_id, value):
	utils.check_node_exist(node_id)
	logging.info("set_user_code nodeId:%s slot:%s user code:%s" % (node_id, slot_id, value,))
	result_value = {}
	for val in globals.network.nodes[node_id].get_values(class_id=COMMAND_CLASS_USER_CODE):
		if globals.network.nodes[node_id].values[val].index == slot_id:
			result_value['data'] = {}
			original_value = value
			value = binascii.a2b_hex(value)
			globals.network.nodes[node_id].values[val].data = value
			result_value['data'][val] = {'device': node_id, 'slot': slot_id, 'val': original_value}
			return jsonify(result_value)
	return jsonify(result_value)

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[0].commandClasses[0x63].SetRaw(<int:slot_id>,[<value1>,<value2>,<value3>,<value4>,<value5>,<value6>,<value7>,<value8>,<value9>,<value10>],1)', methods=['GET'])
@auth.login_required
def set_user_code2(node_id, slot_id, value1, value2, value3, value4, value5, value6, value7, value8, value9, value10):
	utils.check_node_exist(node_id)
	logging.info("set_user_code2 nodeId:%s slot:%s user code:%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (node_id, slot_id, value1, value2, value3, value4, value5, value6, value7, value8, value9, value10,))
	result_value = {}
	for val in globals.network.nodes[node_id].get_values(class_id=COMMAND_CLASS_USER_CODE):
		if globals.network.nodes[node_id].values[val].index == slot_id:
			result_value['data'] = {}
			value = utils.convert_user_code_to_hex(value1) + utils.convert_user_code_to_hex(value2) + utils.convert_user_code_to_hex(value3) + utils.convert_user_code_to_hex(value4) + utils.convert_user_code_to_hex(value5) + utils.convert_user_code_to_hex(value6) + utils.convert_user_code_to_hex(value7) + utils.convert_user_code_to_hex(value8) + utils.convert_user_code_to_hex(value9) + utils.convert_user_code_to_hex(value10)
			original_value = value
			value = binascii.a2b_hex(value)
			globals.network.nodes[node_id].values[val].data = value
			result_value['data'][val] = {'device': node_id, 'slot': slot_id, 'val': original_value}
			return jsonify(result_value)
	return jsonify(result_value)

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].GetColor()', methods=['GET'])
@auth.login_required
def get_color(node_id):
	utils.check_node_exist(node_id)
	logging.debug("get_color nodeId:%s" % (node_id,))
	my_result = {}
	red_level = 0
	green_level = 0
	blue_level = 0
	white_level = 0
	for val in globals.network.nodes[node_id].get_values(class_id=COMMAND_CLASS_SWITCH_MULTILEVEL, genre='User', type='Byte', readonly='All', writeonly=False):
		my_value = globals.network.nodes[node_id].values[val]
		if my_value.label != 'Level':
			continue
		if my_value.instance < 2:
			continue
		if my_value.instance == 3:
			red_level = utils.convert_level_to_color(my_value.data)
		elif my_value.instance == 4:
			green_level = utils.convert_level_to_color(my_value.data)
		elif my_value.instance == 5:
			blue_level = utils.convert_level_to_color(my_value.data)
		elif my_value.instance == 6:
			white_level = utils.convert_level_to_color(my_value.data)
	my_result['data'] = {'red': red_level, 'green': green_level, 'blue': blue_level, 'white': white_level}
	return jsonify(my_result)

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].SetColor(<int:red_level>,<int:green_level>,<int:blue_level>,<int:white_level>)', methods=['GET'])
@auth.login_required
def set_color(node_id, red_level, green_level, blue_level, white_level):
	utils.check_node_exist(node_id)
	logging.info("set_color nodeId:%s red:%s green:%s blue:%s white:%s" % (node_id, red_level, green_level, blue_level, white_level,))
	my_result = False
	intensity_value = None
	red_value = None
	green_value = None
	blue_value = None
	for val in globals.network.nodes[node_id].get_values(class_id=COMMAND_CLASS_SWITCH_MULTILEVEL, genre='User', type='Byte', readonly='All', writeonly=False):
		my_value = globals.network.nodes[node_id].values[val]
		if my_value.label != 'Level':
			continue
		if my_value.instance == 2:
			continue
		if my_value.instance == 1:
			intensity_value = val
		elif my_value.instance == 3:
			red_value = val
			my_value.data = utils.convert_color_to_level(red_level)
		elif my_value.instance == 4:
			green_value = val
			my_value.data = utils.convert_color_to_level(green_level)
		elif my_value.instance == 5:
			blue_value = val
			my_value.data = utils.convert_color_to_level(blue_level)
		elif my_value.instance == 6:
			my_value.data = utils.convert_color_to_level(white_level)
	if red_value is not None and green_value is not None and blue_value is not None:
		value_utils.prepare_refresh(node_id, intensity_value, None)
		my_result = True
	return utils.format_json_result(my_result)

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].PressButton()', methods=['GET'])
@auth.login_required
def press_button(node_id, instance_id, cc_id, index):
	utils.check_node_exist(node_id)
	logging.info("press_button nodeId:%s, instance:%s, cc:%s, index:%s" % (node_id, instance_id, cc_id, index,))
	for val in globals.network.nodes[node_id].get_values(class_id=int(cc_id, 16), genre='All', type='All', readonly='All', writeonly='All'):
		if globals.network.nodes[node_id].values[val].instance - 1 == instance_id and globals.network.nodes[node_id].values[
			val].index == index:
			globals.network.manager.pressButton(globals.network.nodes[node_id].values[val].value_id)
			if cc_id == hex(COMMAND_CLASS_SWITCH_MULTILEVEL) and globals.network.nodes[node_id].values[val].label in ['Bright', 'Dim', 'Open', 'Close']:
				value = 1
				if globals.network.nodes[node_id].values[val].label in ['Bright', 'Open']:
					value = 99
				elif globals.network.nodes[node_id].values[val].label in ['Close']:
					value = 0
				value_level = value_utils.get_value_by_label(node_id, COMMAND_CLASS_SWITCH_MULTILEVEL,
												 globals.network.nodes[node_id].values[val].instance, 'Level')
				if value_level:
					value_utils.prepare_refresh(node_id, value_level.value_id, value, utils.is_motor(node_id))
			return utils.format_json_result()
	return utils.format_json_result(False, 'button not found', 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].ReleaseButton()', methods=['GET'])
@auth.login_required
def release_button(node_id, instance_id, cc_id, index):
	utils.check_node_exist(node_id)
	for val in globals.network.nodes[node_id].get_values(class_id=int(cc_id, 16), genre='All', type='All', readonly='All', writeonly='All'):
		if globals.network.nodes[node_id].values[val].instance - 1 == instance_id and globals.network.nodes[node_id].values[
			val].index == index:
			globals.network.manager.releaseButton(globals.network.nodes[node_id].values[val].value_id)
			if cc_id == hex(COMMAND_CLASS_SWITCH_MULTILEVEL):
				value_level = value_utils.get_value_by_label(node_id, COMMAND_CLASS_SWITCH_MULTILEVEL,
												 globals.network.nodes[node_id].values[val].instance, 'Level')
				if value_level:
					value_utils.stop_refresh(node_id, value_level.value_id)

			return utils.format_json_result()
	return utils.format_json_result(False, 'button not found', 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[0].commandClasses[0xF0].SwitchAll(<int:state>)', methods=['GET'])
@auth.login_required
def switch_all(node_id, state):
	if state == 0:
		logging.info("SwitchAll Off")
		globals.network.switch_all(False)
	else:
		logging.info("SwitchAll On")
		globals.network.switch_all(True)
	for node_id in globals.network.nodes:
		my_node = globals.network.nodes[node_id]
		if my_node.is_failed:
			continue
		value_ids = my_node.get_switches_all()
		if value_ids is not None and len(value_ids) > 0:
			for value_id in value_ids:
				if my_node.values[value_id].data == "Disabled":
					continue
				elif my_node.values[value_id].data == "On and Off Enabled":
					pass
				if my_node.values[value_id].data == "Off Enabled" and state != 0:
					continue
				if my_node.values[value_id].data == "On Enabled" and state == 0:
					continue
				for switch in my_node.get_switches():
					my_node.values[switch].refresh()
				for dimmer in my_node.get_dimmers():
					my_node.values[dimmer].refresh()
	return utils.format_json_result()

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].RemoveDeviceZWConfig(<int:identical>)', methods=['GET'])
@auth.login_required
def remove_device_openzwave_config(node_id, identical):
	utils.check_node_exist(node_id)
	my_node = globals.network.nodes[node_id]
	manufacturer_id = my_node.manufacturer_id
	product_id = my_node.product_id
	product_type = my_node.product_type
	list_to_remove = [node_id]
	if identical != 0:
		for child_id in list(globals.network.nodes):
			node = globals.network.nodes[child_id]
			if child_id != node_id and node.manufacturer_id == manufacturer_id and node.product_id == product_id and node.product_type == product_type:
				list_to_remove.append(child_id)
	globals.network_is_running = False
	globals.network.stop()
	logging.info('ZWave network is now stopped')
	time.sleep(5)
	filename = globals.data_folder + "/zwcfg_" + globals.network.home_id_str + ".xml"
	tree = etree.parse(filename)
	for child_id in list_to_remove:
		logging.info("Remove xml element for node %s" % (child_id,))
		node = tree.find("{http://code.google.com/p/open-zwave/}Node[@id='" + str(child_id) + "']")
		tree.getroot().remove(node)
	working_file = open(filename, "w")
	working_file.write('<?xml version="1.0" encoding="utf-8" ?>\n')
	working_file.writelines(etree.tostring(tree, pretty_print=True))
	working_file.close()
	network_utils.start_network()
	return utils.format_json_result()

@app.route('/ZWaveAPI/Run/devices[<int:node_id>]', methods=['GET'])
def get_serialized_device(node_id):
	utils.check_node_exist(node_id)
	return jsonify(serialization.serialize_node_to_json(node_id))
	
"""
controllers routes
"""


@app.route('/ZWaveAPI/Run/controller.RequestNetworkUpdate(<node_id>)', methods=['GET'])
@auth.login_required
def request_network_update(node_id):
	if not network_utils.can_execute_network_command(0):
		raise Exception('Controller is bussy')
	utils.check_node_exist(node_id)
	logging.info("Update the controller (%s) with network information from the SUC/SIS" % (node_id,))
	execution_result = globals.network.manager.requestNetworkUpdate(globals.network.home_id, node_id)
	return utils.format_json_result(execution_result)

@app.route('/ZWaveAPI/Run/controller.ReplicationSend(<node_id>)', methods=['GET'])
@auth.login_required
def replication_send(node_id):
	if not network_utils.can_execute_network_command(0):
		raise Exception('Controller is bussy')
	utils.check_node_exist(node_id)
	logging.info('Send information from primary to secondary %s' % (node_id,))
	return utils.format_json_result(globals.network.manager.replicationSend(globals.network.home_id, node_id))

"""
network routes
"""

@app.route('/ZWaveAPI/Run/network.DeleteBackup(<backup_name>)', methods=['GET'])
@auth.login_required
def manually_delete_backup(backup_name):
	logging.info('Manually deleting a backup')
	backup_folder = globals.data_folder + "/xml_backups"
	backup_file = os.path.join(backup_folder, backup_name)
	if not os.path.isfile(backup_file):
		logging.error('No config file found to delete')
		return utils.format_json_result(False, 'No config file found with name ' + backup_name, 'warning')
	else:
		os.unlink(backup_file)
	return utils.format_json_result(True, backup_name + ' successfully deleted')

@app.route('/ZWaveAPI/Run/ChangeLogLevel(<int:level>)', methods=['GET'])
@auth.login_required
def rest_change_log_level(level):
	utils.set_log_level(level)
	server_utils.set_log_level()
	return utils.format_json_result(data=('Log level is set: %s' % (globals.log_level,)), log_level='info', code=0)

'''
new routes
'''

@app.route('/controller/info(<info>)', methods=['GET'])
@auth.login_required
def controller_info(info):
	logging.info("Controller info "+str(info))
	return utils.format_json_result()


@app.route('/controller/action(<action>)', methods=['GET'])
@auth.login_required
def controller_action(action):
	logging.info("Controller action "+str(action))
	if action == 'hardReset':
		globals.network.controller.hard_reset()
		logging.info('The controller becomes a primary controller ready to add devices to a new network')
		time.sleep(3)
		network_utils.start_network()
	elif action == 'receiveConfiguration':
		if not network_utils.can_execute_network_command(0):
			raise Exception('Controller is bussy')
		logging.info("Receive Configuration")
		return utils.format_json_result(data=globals.network.manager.receiveConfiguration(globals.network.home_id))
	elif action == 'transferPrimaryRole':
		if not network_utils.can_execute_network_command(0):
			raise Exception('Controller is bussy')
		logging.info("Transfer Primary Role")
		return utils.format_json_result(data=globals.network.manager.transferPrimaryRole(globals.network.home_id))
	elif action == 'createNewPrimary':
		if not network_utils.can_execute_network_command(0):
			raise Exception('Controller is bussy')
		logging.info("Add a new controller to the Z-Wave network")
		return utils.format_json_result(data=globals.network.manager.createNewPrimary(globals.network.home_id))
	elif action == 'testNetwork':
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
	elif action == 'serialAPISoftReset':
		globals.network.controller.soft_reset()
	elif action == 'healNetwork':
		if not network_utils.can_execute_network_command(0):
			raise Exception('Controller is bussy')
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
	elif action == 'cancelCommand':
		if globals.network.manager.cancelControllerCommand(globals.network.home_id):
			globals.network_information.controller_is_busy = False
		return utils.format_json_result()
	return utils.format_json_result()

@app.route('/controller/addNodeToNetwork(<int:state>,<int:do_security>)', methods=['GET'])
@auth.login_required
def start_node_inclusion(state, do_security):
	if globals.network_information.controller_is_busy:
		raise Exception('Controller is bussy')
	if state == 1:
		if not network_utils.can_execute_network_command(0):
			raise Exception('Controller is bussy')
		if do_security == 1:
			do_security = True
			logging.info(
				"Start the Inclusion Process to add a Node to the Network with Security CC if the node is supports it")
		else:
			do_security = False
			logging.info("Start the Inclusion Process to add a Node to the Network")
		execution_result = globals.network.manager.addNode(globals.network.home_id, do_security)
		if execution_result:
			globals.network_information.actual_mode = ControllerMode.AddDevice
		return utils.format_json_result(data=execution_result)
	elif state == 0:
		logging.info("Start the Inclusion (Cancel)")
		globals.network.manager.cancelControllerCommand(globals.network.home_id)
		return utils.format_json_result()

@app.route('/controller/removeNodeFromNetwork(<int:state>)', methods=['GET'])
@auth.login_required
def start_node_exclusion(state):
	if globals.network_information.controller_is_busy:
		raise Exception('Controller is bussy')
	if state == 1:
		if not network_utils.can_execute_network_command(0):
			raise Exception('Controller is bussy')
		logging.info("Remove a Device from the Z-Wave Network (Started)")
		execution_result = globals.network.manager.removeNode(globals.network.home_id)
		if execution_result:
			globals.network_information.actual_mode = ControllerMode.RemoveDevice
		return utils.format_json_result(data=execution_result)
	elif state == 0:
		logging.info("Remove a Device from the Z-Wave Network (Cancel)")
		globals.network.manager.cancelControllerCommand(globals.network.home_id)
		return utils.format_json_result()	

@app.route('/network/action(<action>)', methods=['GET'])
@auth.login_required
def network_action(action):
	if action in globals.NETWORK_REST_MAPPING:
		return globals.NETWORK_REST_MAPPING[action]()
	else:
		return utils.format_json_result()

@app.route('/network/info(<info>)', methods=['GET'])
@auth.login_required
def network_info(info):
	if info in globals.NETWORK_REST_MAPPING:
		return globals.NETWORK_REST_MAPPING[info]()
	else:
		return utils.format_json_result()

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[0x70].data[<int:index_id2>].Set(<int:index_id>,<string:value>,<int:size>)', methods=['GET'])
@auth.login_required
def set_config5(node_id, instance_id, index_id2, index_id, value, size):
	return utils.format_json_result(data=value_utils.set_config(node_id, index_id, value, size))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[0x70].data[<int:index_id2>].Set(<int:index_id>,<float:value>,<int:size>)', methods=['GET'])
@auth.login_required
def set_config6(node_id, instance_id, index_id2, index_id, value, size):
	return utils.format_json_result(data=value_utils.set_config(node_id, index_id, value, size))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[0x70].data[<int:index_id2>].Set(<int:index_id>,<int:value>,<int:size>)', methods=['GET'])
@auth.login_required
def set_config4(node_id, instance_id, index_id2, index_id, value, size):
	return utils.format_json_result(data=value_utils.set_config(node_id, index_id, value, size))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].Set(<int:index_id>,<string:value>,<int:size>)', methods=['GET'])
@auth.login_required
def set_config2(node_id, index_id, value, size):
	return utils.format_json_result(data=value_utils.set_config(node_id, index_id, value, size))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].Set(<int:index_id>,<float:value>,<int:size>)', methods=['GET'])
@auth.login_required
def set_config3(node_id, index_id, value, size):
	return utils.format_json_result(data=value_utils.set_config(node_id, index_id, value, size))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].commandClasses[0x70].Set(<int:index_id>,<int:value>,<int:size>)', methods=['GET'])
@auth.login_required
def set_config1(node_id, index_id, value, size):
	return utils.format_json_result(data=value_utils.set_config(node_id, index_id, value, size))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].Set(<float:value>)', methods=['GET'])
@auth.login_required
def set_value8(node_id, instance_id, cc_id, index, value):
	return utils.format_json_result(data=commands.send_command_zwave(node_id, cc_id, instance_id, index, value))
	
@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].Set(<string:value>)', methods=['GET'])
@auth.login_required
def set_value6(node_id, instance_id, cc_id, value):
	return utils.format_json_result(data=commands.send_command_zwave(node_id, cc_id, instance_id, None, value))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].Set(<int:value>)', methods=['GET'])
@auth.login_required
def set_value7(node_id, instance_id, cc_id, index, value):
	return utils.format_json_result(data=commands.send_command_zwave(node_id, cc_id, instance_id, index, value))

@app.route('/ZWaveAPI/Run/devices[<int:node_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].Set(<string:value>)', methods=['GET'])
@auth.login_required
def set_value9(node_id, instance_id, cc_id, index, value):
	return utils.format_json_result(data=commands.send_command_zwave(node_id, cc_id, instance_id, index, value))


@app.route('/node/info(<int:node_id>,<info>)', methods=['GET'])
@auth.login_required
def node_info(node_id,info):
	utils.check_node_exist(node_id)
	logging.info("node info "+str(info))
	if info in globals.NODE_REST_MAPPING:
		return globals.NODE_REST_MAPPING[info](node_id)
	else:
		return utils.format_json_result()

@app.route('/node/action(<int:node_id>,<action>)', methods=['GET'])
@auth.login_required
def node_action(node_id,action):
	utils.check_node_exist(node_id)
	utils.check_network_can_execute()
	logging.info("node action "+str(action))
	if action in globals.NODE_REST_MAPPING:
		return globals.NODE_REST_MAPPING[action](node_id)
	else:
		return utils.format_json_result()
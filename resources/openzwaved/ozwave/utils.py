import logging
import time
import math
import globals
from utilities.Constants import *
from flask import Flask, jsonify

def get_standard_value_type(value_type):
	if value_type in globals.CONVERSION:
		value_type = globals.CONVERSION[value_type]
	return value_type

def set_log_level(level):
	globals.log_level = 'none'
	if level in globals.CONVERSION:
		globals.log_level = globals.CONVERSION[level]

def convert_query_stage_to_int(stage):
	if stage in globals.CONVERSION:
		return globals.CONVERSION[stage]
	return 0

def convert_level_to_color(level):
	if level > 99:
		return 255
	return level * 255 / 99

def convert_color_to_level(color):
	if color > 255:
		return 99
	elif color < 0:
		return 0
	return color * 99 / 255

def is_none_or_empty(value):
	if value is None:
		return True
	elif value:
		return False
	else:
		return True

def change_instance(my_value):
	if my_value.instance > 1:
		return my_value.instance - 1
	return 0

def normalize_short_value(value):
	my_result = value
	try:
		if int(value) < 0:
			my_result = 65536 + int(value)
	except:
		pass
	return my_result

def convert_fahrenheit_celsius(value):
	if value.precision is None or value.precision == 0:
		power = 1
	else:
		power = math.pow(10, value.precision)
	return int(((float(value.data_as_string) - 32) * 5.0 / 9.0) * int(power)) / power

def is_motor(node_id):
	return globals.network.nodes[node_id].specific in [SPECIFIC_TYPE_MOTOR_MULTI_POSITION, SPECIFIC_TYPE_CLASS_A_MOTOR_CONTROL, SPECIFIC_TYPE_CLASS_B_MOTOR_CONTROL, SPECIFIC_TYPE_CLASS_C_MOTOR_CONTROL]

def get_sleeping_nodes_count():
	sleeping_nodes_count = 0
	for idNode in list(globals.network.nodes):
		if not globals.network.nodes[idNode].is_awake:
			sleeping_nodes_count += 1
	return sleeping_nodes_count

def format_json_result(success=True, detail=None, log_level=None, code=0):
	if log_level is not None and not is_none_or_empty(detail):
		if log_level == 'debug':
			logging.debug(detail)
		elif log_level == 'warning':
			logging.warning(detail)
		elif log_level == 'error':
			logging.error(detail)
	if detail is not None:
		return jsonify({'result': success, 'data': detail, 'code': code})
	return jsonify({'result': success})

def check_node_exist(_node_id,enable=False):
	if _node_id not in globals.network.nodes:
		raise Exception('Unknow node id '+str(_node_id))
	if enable and _node_id not in globals.disabled_nodes:
		raise Exception('Disabled node id '+str(_node_id))
	return

def convert_user_code_to_hex(value, length=2):
	value1 = int(value)
	my_result = hex(value1)[length:]
	if len(my_result) == 1:
		my_result = '0' * (length - 1) + my_result
	return my_result

def concatenate_list(list_values, separator=';'):
	try:
		if list_values is None:
			return ""
		else:
			if isinstance(list_values, set):
				return separator.join(str(s) for s in sorted(list_values))
			return list_values
	except Exception as error:
		logging.error(str(error))
	return ""

def write_config():
	watchdog = 0
	while globals.network_information.config_file_save_in_progress and watchdog < 10:
		logging.debug('.')
		time.sleep(1)
		watchdog += 1
	if globals.network_information.config_file_save_in_progress:
		return
	globals.network_information.config_file_save_in_progress = True
	try:
		globals.network.write_config()
		logging.info('write configuration file')
		time.sleep(1)
	except Exception as error:
		logging.error('write_config %s' % (str(error),))
	finally:
		globals.network_information.config_file_save_in_progress = False
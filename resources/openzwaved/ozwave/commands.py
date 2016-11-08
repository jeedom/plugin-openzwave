import logging
import time
import globals,utils
import threading
from ozwave.utilities.Constants import *
import node_utils,value_utils

def send_command_zwave(_node_id, _cc_id, _instance_id, _index, _value):
	logging.info("Send command to node "+str(_node_id)+" on class "+str(_cc_id)+" instance "+str(_instance_id)+" index "+str(_index)+" value "+str(_value))
	utils.check_node_exist(_node_id)
	if _cc_id == COMMAND_CLASS_NO_OPERATION:
		return node_utils.test_node(_node_id, 1)
	if _cc_id == COMMAND_CLASS_WAKE_UP:
		arr = _value.split(",")
		wake_up_time = int(arr[0])
		for val in globals.network.nodes[_node_id].get_values(class_id=COMMAND_CLASS_WAKE_UP): 
			if globals.network.nodes[_node_id].values[val].label == "Wake-up Interval":
				globals.network.nodes[_node_id].values[val].data = int(wake_up_time)
		return
	if _cc_id == COMMAND_CLASS_ASSOCIATION:
		arr = _value.split(",")
		group = int(arr[0])
		target_node = int(arr[1])
		try:
			return node_utils.assoc_action(_node_id, group, target_node,0,'add')
		except ValueError:
			raise Exception('Node is not Ready for associations')
	for val in globals.network.nodes[_node_id].get_values(class_id=_cc_id, genre='All', type='All', readonly=False, writeonly='All'):
		if globals.network.nodes[_node_id].values[val].instance - 1 == _instance_id and (_index is None or globals.network.nodes[_node_id].values[val].index == _index):
			value = globals.network.nodes[_node_id].values[val].check_data(_value)
			if _cc_id == COMMAND_CLASS_SWITCH_MULTILEVEL and value > 99:
				logging.debug("Switch light ON to dim level that was last known")
				value = 255
			globals.network.nodes[_node_id].values[val].data = value
			if globals.network.nodes[_node_id].values[val].genre == 'System':
				value_utils.mark_pending_change(globals.network.nodes[_node_id].values[val], value)
			if _cc_id == COMMAND_CLASS_SWITCH_MULTILEVEL and value <= 99:
				value_utils.prepare_refresh(_node_id, val, value, utils.is_motor(_node_id))
			if _cc_id == COMMAND_CLASS_THERMOSTAT_SETPOINT:
				logging.debug("COMMAND_CLASS_THERMOSTAT_SETPOINT")
				node_utils.save_node_value_event(_node_id,  COMMAND_CLASS_THERMOSTAT_SETPOINT, _index, value, _instance_id + 10)
			if _cc_id == COMMAND_CLASS_SWITCH_BINARY:
				worker = threading.Timer(interval=0.5, function=value_utils.refresh_switch_binary, args=(_node_id, val, value))
				worker.start()
			return True
	raise Exception('Value not found')
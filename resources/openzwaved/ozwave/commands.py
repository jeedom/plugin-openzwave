import logging
import globals,utils
import threading
from ozwave.utilities.Constants import *

def send_command_zwave(_node_id, _cc_id, _instance_id, _index, _value):
	logging.info("Send command to "+str(_node_id)+" on "+str(_cc_id)+" instance "+str(_instance_id)+" index "+str(_index)+" value "+str(_value))
	utils.check_node_exist(_node_id)
	if _cc_id == hex(COMMAND_CLASS_NO_OPERATION):
		return test_node(_node_id, 1)
	if _cc_id == str(COMMAND_CLASS_WAKE_UP):
		arr = _value.split(",")
		wake_up_time = int(arr[0])
		return set_wake_up(_node_id, wake_up_time)
	if _cc_id == '0x85':
		arr = _value.split(",")
		group = int(arr[0])
		target_node = int(arr[1])
		try:
			return add_assoc(_node_id, group, target_node)
		except ValueError:
			raise Exception('Node is not Ready for associations')
	for val in globals.network.nodes[_node_id].get_values(class_id=int(_cc_id, 16), genre='All', type='All', readonly='All', writeonly='All'):
		if globals.network.nodes[_node_id].values[val].instance - 1 == _instance_id and (_index is None or globals.network.nodes[_node_id].values[val].index == _index):
			if _cc_id == hex(COMMAND_CLASS_SWITCH_MULTILEVEL) and _value > 99:
				logging.debug("Switch light ON to dim level that was last known")
				_value = 255
			globals.network.nodes[_node_id].values[val].data = _value
			if globals.network.nodes[_node_id].values[val].genre == 'System':
				if globals.network.nodes[_node_id].values[val].type == 'Bool':
					if _value == 0:
						_value = False
					else:
						_value = True
				mark_pending_change(globals.network.nodes[_node_id].values[val], _value)
			if _cc_id == hex(COMMAND_CLASS_SWITCH_MULTILEVEL) and _value <= 99:
				prepare_refresh(_node_id, val, _value, utils.is_motor(_node_id))
			if int(_cc_id, 16) == COMMAND_CLASS_THERMOSTAT_SETPOINT:
				logging.debug("COMMAND_CLASS_THERMOSTAT_SETPOINT")
				node_utils.save_node_value_event(_node_id, int(time.time()), COMMAND_CLASS_THERMOSTAT_SETPOINT, _index, utils.get_standard_value_type(globals.network.nodes[_node_id].values[val].type), _value, _instance_id + 10)
			if _cc_id == hex(COMMAND_CLASS_SWITCH_BINARY):
				if _value == 0:
					_value = False
				else:
					_value = True
				worker = threading.Timer(interval=0.5, function=refresh_switch_binary, args=(_node_id, val, _value))
				worker.start()
			return True
	raise Exception('Value not found')
import logging
import globals,utils,node_utils,value_utils, network_utils
import thread
import time

def send_command_zwave(_node_id, _cc_id, _instance_id, _index, _value):
	logging.info("Send command to node "+str(_node_id)+" on class "+str(_cc_id)+" instance "+str(_instance_id)+" index "+str(_index)+" value "+str(_value))
	utils.check_node_exist(_node_id)
	if len(_value) == 0:
		raise Exception('No value passed')
	if _cc_id == globals.COMMAND_CLASS_NO_OPERATION:
		return node_utils.test_node(_node_id, 1)
	if _cc_id == globals.COMMAND_CLASS_ASSOCIATION :
		return
	if _cc_id in [globals.COMMAND_CLASS_SWITCH_MULTILEVEL]:
		_value = round(float(_value)) 
	for value_id in globals.network.nodes[_node_id].get_values(class_id=_cc_id, genre='All', type='All', readonly=False, writeonly='All'):
		if globals.network.nodes[_node_id].values[value_id].instance == _instance_id and (_index is None or globals.network.nodes[_node_id].values[value_id].index == _index):
			value = globals.network.nodes[_node_id].values[value_id].check_data(_value)
			globals.network.nodes[_node_id].values[value_id].data = value
			if globals.network.nodes[_node_id].values[value_id].genre == 'System':
				value_utils.mark_pending_change(globals.network.nodes[_node_id].values[value_id], value)
			thread.start_new_thread( refresh_value, (_node_id,_instance_id,_cc_id,_index, _value))
			return True
	raise Exception('Value not found')
	
def refresh_value(node_id,instance_id,cc_id,index,value):
	try:
		if node_id not in globals.network.nodes or node_id in globals.not_supported_nodes:
			return
		my_node = globals.network.nodes[node_id]
		product_id = str(int(my_node.product_id, 16))
		product_type = str(int(my_node.product_type, 16))
		manufacturer_id = str(int(my_node.manufacturer_id, 16))
		globalId = manufacturer_id+'|'+product_type+'|'+product_id
		logging.debug("Searching refresh for : " + globalId)
		if globalId in globals.REFRESH_MAPPING:
			globalCommand = str(cc_id)+'|'+str(instance_id)+'|'+str(index)
			logging.debug("Found refresh for : " + globalId + " searching for " + globalCommand)
			if globalCommand in globals.REFRESH_MAPPING[globalId]:
				for value_id in globals.network.nodes[node_id].get_values(class_id=cc_id):
					if globals.network.nodes[node_id].values[value_id].instance == instance_id and globals.network.nodes[node_id].values[value_id].index == index:
						logging.debug("Refresh node "+str(node_id)+" on class "+str(cc_id)+" instance "+str(instance_id)+" index "+str(index)+ " " +str(globals.REFRESH_MAPPING[globalId][globalCommand]['number']) + " times in "+str(globals.REFRESH_MAPPING[globalId][globalCommand]['sleep']) + " seconds")
						if 'onlyset' in globals.REFRESH_MAPPING[globalId][globalCommand]:
							commandTorefresh = globals.REFRESH_MAPPING[globalId][globalCommand]['onlyset']
							commandTorefreshArray = commandTorefresh.split('|')
							logging.debug("Setting back value for "+str(node_id)+" on class "+str(commandTorefreshArray[0])+" instance "+str(commandTorefreshArray[1])+" index "+str(commandTorefreshArray[2])+ " with value " + str(value))
							node_utils.save_node_value_event(node_id,commandTorefreshArray[0], commandTorefreshArray[2], value, commandTorefreshArray[1])
							continue
						for i in range(0,globals.REFRESH_MAPPING[globalId][globalCommand]['number']):
							time.sleep(globals.REFRESH_MAPPING[globalId][globalCommand]['sleep'])
							logging.debug("Performing refresh for node : "+str(node_id))
							globals.network.nodes[node_id].values[value_id].refresh()
							if 'other' in globals.REFRESH_MAPPING[globalId][globalCommand]:
								other = globals.REFRESH_MAPPING[globalId][globalCommand]['other']
								list = other.split('|')
								for value_id in globals.network.nodes[node_id].get_values(class_id=int(list[0])):
									if globals.network.nodes[node_id].values[value_id].instance == int(list[1]) and globals.network.nodes[node_id].values[value_id].index == int(list[2]):
										logging.debug("Refresh node "+str(node_id)+" on class "+str(list[0])+" instance "+str(list[1])+" index "+str(list[2]))
										globals.network.nodes[node_id].values[value_id].refresh()
		return
	except Exception as e:
		logging.debug("Ignoring refresh for node : " + str(node_id))
		logging.debug(str(e))
		pass

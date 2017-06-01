#!flask/bin/python
import sys
import binascii
import logging
import os
import shutil
from lxml import etree
import globals,utils,network_utils,node_utils
import value_utils,commands
from utilities.NetworkExtend import *
try:
	from tornado.web import RequestHandler,Application,HTTPError
except Exception as e:
	print(globals.MSG_CHECK_DEPENDENCY, 'error')
	print("Error: %s" % str(e), 'error')
	sys.exit(1)

class ControllerHandler(RequestHandler):
	def get(self):
		try:
			utils.check_apikey(self.get_argument('apikey',''))
			type = self.get_argument('type','')
			node_id = int(self.get_argument('node_id','0'))
			info = self.get_argument('info','')
			action = self.get_argument('action','')
			do_security = int(self.get_argument('security','0'))
			if type == 'replicationSend':
				utils.can_execute_command(0)
				utils.check_node_exist(node_id)
				logging.info('Send information from primary to secondary %s' % (node_id,))
				self.write(utils.format_json_result(data=globals.network.manager.replicationSend(globals.network.home_id, node_id)))
			elif type == 'info':
				logging.info("Controller info "+str(info))
				self.write(utils.format_json_result())
			elif type == 'action':
				logging.info("Controller action "+str(action))
				if action in globals.CONTROLLER_REST_MAPPING:
					self.write(globals.CONTROLLER_REST_MAPPING[action]())
				else:
					self.write(utils.format_json_result())
			elif type == 'addNode':
				utils.can_execute_command(0)
				if do_security == 1:
					do_security = True
					logging.info("Start the Inclusion Process to add a Node to the Network with Security CC if the node is supports it")
				else:
					do_security = False
					logging.info("Start the Inclusion Process to add a Node to the Network")
				execution_result = globals.network.manager.addNode(globals.network.home_id, do_security)
				if execution_result:
					globals.network_information.actual_mode = ControllerMode.AddDevice
				self.write(utils.format_json_result(data=execution_result))
			elif type == 'removeNode':
				utils.can_execute_command(0)
				logging.info("Remove a Device from the Z-Wave Network (Started)")
				execution_result = globals.network.manager.removeNode(globals.network.home_id)
				if execution_result:
					globals.network_information.actual_mode = ControllerMode.RemoveDevice
				self.write(utils.format_json_result(data=execution_result))
			else:
				self.write(utils.format_json_result())
		except Exception,e:
			self.write(utils.format_json_result(success="error",data=str(e)))

class NetworkHandler(RequestHandler):
	def get(self):
		try:
			utils.check_apikey(self.get_argument('apikey',''))
			type = self.get_argument('type','')
			action = self.get_argument('action','')
			info = self.get_argument('info','')
			if type == 'action':
				if action in globals.NETWORK_REST_MAPPING:
					self.write(globals.NETWORK_REST_MAPPING[action]())
				else:
					self.write(utils.format_json_result())
			elif type == 'info':
				if info in globals.NETWORK_REST_MAPPING:
					self.write(globals.NETWORK_REST_MAPPING[info]())
				else:
					self.write(utils.format_json_result())
			else:
				self.write(utils.format_json_result())
		except Exception,e:
			self.write(utils.format_json_result(success="error",data=str(e)))

class NodeHandler(RequestHandler):
	def get(self):
		try:
			utils.check_apikey(self.get_argument('apikey',''))
			type = self.get_argument('type','')
			node_id = int(self.get_argument('node_id','0'))
			target_id = int(self.get_argument('target_id','0'))
			cc_id = int(self.get_argument('cc_id','0'))
			instance_id = int(self.get_argument('instance_id','0'))
			index = int(self.get_argument('index','0'))
			identical = int(self.get_argument('identical','0'))
			frequency = int(self.get_argument('frequency','0'))
			action = self.get_argument('action','')
			info = self.get_argument('info','')
			buttonaction = self.get_argument('buttonaction','')
			utils.check_node_exist(node_id)
			if type == 'action':
				utils.can_execute_command()
				logging.info("node action "+str(action))
				if action in globals.NODE_REST_MAPPING:
					self.write(globals.NODE_REST_MAPPING[action](node_id))
				else:
					self.write(utils.format_json_result())
			elif type == 'info':
				logging.info("node info "+str(info))
				if info in globals.NODE_REST_MAPPING:
					self.write(globals.NODE_REST_MAPPING[info](node_id))
				else:
					self.write(utils.format_json_result())
			elif type == 'refreshClass':
				logging.info('Request values refresh for '+str(node_id)+' on class '+str(cc_id))
				for value_id in globals.network.nodes[node_id].get_values(class_id=cc_id):
					if globals.network.nodes[node_id].values[value_id].id_on_network in globals.pending_configurations:
						del globals.pending_configurations[globals.network.nodes[node_id].values[value_id].id_on_network]
				globals.network.manager.requestAllConfigParams(globals.network.home_id, node_id)
				self.write(utils.format_json_result())
			elif type == 'removeDeviceZWConfig':
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
				self.write(utils.format_json_result())
			elif type == 'copyConfigurations':
				utils.can_execute_command(0)
				logging.info("copy_configuration from source_id:%s to target_id:%s" % (node_id, target_id,))
				items = 0
				utils.check_node_exist(target_id)
				source = globals.network.nodes[node_id]
				target = globals.network.nodes[target_id]
				if source.manufacturer_id != target.manufacturer_id or source.product_type != target.product_type or source.product_id != target.product_id:
					raise Exception('The two nodes must be with same: manufacturer_id, product_type and product_id')
				for value_id in source.get_values():
					configuration_value = source.values[value_id]
					if configuration_value.genre == 'Config':
						if configuration_value.type == 'Button':
							continue
						if configuration_value.is_write_only:
							continue
						target_value = value_utils.get_value_by_index(target_id, globals.COMMAND_CLASS_CONFIGURATION, 1,configuration_value.index)
						if target_value is not None:
							if configuration_value.type == 'List':
								globals.network.manager.setValue(target_value.value_id, configuration_value.data)
								accepted = True
							else:
								accepted = target.set_config_param(configuration_value.index,configuration_value.data)
							if accepted:
								items += 1
								value_utils.mark_pending_change(target_value, configuration_value.data)
				my_result = items != 0
				self.write(utils.format_json_result())
			elif type == 'refreshData':
				for value_id in globals.network.nodes[node_id].get_values(class_id=cc_id):
					if globals.network.nodes[node_id].values[value_id].instance == instance_id and globals.network.nodes[node_id].values[value_id].index == index:
						globals.network.nodes[node_id].values[value_id].refresh()
						self.write(utils.format_json_result())
						return
				raise Exception('This device does not contain the specified value')
			elif type == 'data':
				logging.debug("get_config for nodeId:%s" % (node_id,))
				config = {}
				for value_id in globals.network.nodes[node_id].values:
					list_values = []
					my_value = globals.network.nodes[node_id].values[value_id]
					if my_value.command_class == cc_id:
						config[globals.network.nodes[node_id].values[value_id].index] = {}
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
				self.write(utils.format_json_result(data=config))
			elif type == 'setPolling':
				logging.info('set_polling_value for nodeId: '+str(node_id)+' instance: '+str(instance_id)+' cc : '+str(cc_id)+' index : '+str(index)+' at: '+str(frequency))
				for value_id in globals.network.nodes[node_id].get_values(class_id=cc_id):
					if globals.network.nodes[node_id].values[value_id].instance == instance_id:
						my_value = globals.network.nodes[node_id].values[value_id]
						if frequency == 0 & my_value.poll_intensity > 0:
							my_value.disable_poll()
						else:
							if globals.network.nodes[node_id].values[value_id].index == index:
								value_utils.changes_value_polling(frequency, my_value)
							elif my_value.poll_intensity > 0:
									my_value.disable_poll()
				utils.write_config()
				self.write(utils.format_json_result())
			elif type == 'buttonaction':
				logging.info('Button nodeId : '+str(node_id)+' instance: '+str(instance_id)+' cc : '+str(cc_id)+' index : '+str(index)+' : ' +str(action))
				for value_id in globals.network.nodes[node_id].get_values(class_id=cc_id, genre='All', type='All', readonly=False, writeonly='All'):
					if globals.network.nodes[node_id].values[value_id].instance == instance_id and globals.network.nodes[node_id].values[value_id].index == index:
						if action == 'press':
							globals.network.manager.pressButton(globals.network.nodes[node_id].values[value_id].value_id)
						elif action == 'release':
							globals.network.manager.releaseButton(globals.network.nodes[node_id].values[value_id].value_id)
						self.write(utils.format_json_result())
				self.write(utils.format_json_result(success='error', data='Button not found'))
			elif type == 'setRaw':
				slot_id = int(self.get_argument('slot_id','0'))
				value0 = self.get_argument('value0','')
				logging.info("set_user_code2 nodeId:%s slot:%s user code:%s" % (node_id, slot_id, value0,))
				result_value = {}
				for value_id in globals.network.nodes[node_id].get_values(class_id=globals.COMMAND_CLASS_USER_CODE):
					if globals.network.nodes[node_id].values[value_id].index == slot_id:
						result_value['data'] = {}
						original_value = value0
						globals.network.nodes[node_id].values[value_id].data = binascii.a2b_hex(value0)
						result_value['data'][value_id] = {'device': node_id, 'slot': slot_id, 'val': original_value}
						self.write(utils.format_json_result(result_value))
				self.write(utils.format_json_result())
			elif type == 'setconfig':
				size = int(self.get_argument('size','0'))
				value = self.get_argument('value','')
				self.write(utils.format_json_result(data=value_utils.set_config(node_id, index, value, size)))
			elif type == 'setvalue':
				value = self.get_argument('value','')
				self.write(utils.format_json_result(data=commands.send_command_zwave(node_id, cc_id, instance_id, index, value)))
			elif type == 'switchall':
				state = int(self.get_argument('state','0'))
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
				self.write(utils.format_json_result())
			elif type == 'setDeviceName':
				location = self.get_argument('location','')
				name = self.get_argument('name','')
				is_enable = int(self.get_argument('is_enable','0'))
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
				self.write(utils.format_json_result())
			elif type == 'association':
				group = int(self.get_argument('group','0'))
				self.write(node_utils.add_assoc(node_id, group, target_id,instance_id,action))
			else:
				self.write(utils.format_json_result())
		except Exception,e:
			logging.error('RequestHandler ' + e.message)
			self.write(utils.format_json_result(success="error",data=str(e)))

class BackupHandler(RequestHandler):
	def get(self):
		try:
			utils.check_apikey(self.get_argument('apikey',''))
			type = self.get_argument('type','')
			if type == 'do':
				logging.info('Manually creating a backup')
				if globals.files_manager.backup_xml_config('manual', globals.network.home_id_str):
					self.write(utils.format_json_result())
				else:
					raise Exception ('See openzwave log file for details')
			elif type == 'list':
				self.write(utils.format_json_result(data=globals.files_manager.get_openzwave_backups()))
			elif type == 'restore':
				backup = self.get_argument('backup','')
				logging.info('Restoring backup ' + backup)
				backup_folder = globals.data_folder + "/xml_backups"
				try:
					os.stat(backup_folder)
				except:
					os.mkdir(backup_folder)
				backup_file = os.path.join(backup_folder, backup)
				target_file = globals.data_folder + "/zwcfg_" + globals.network.home_id_str + ".xml"
				if not os.path.isfile(backup_file):
					raise Exception ('No config file found with name ' + str(backup))
				else:
					tree = etree.parse(backup_file)
					globals.network_is_running = False
					globals.network.stop()
					logging.info('ZWave network is now stopped')
					time.sleep(3)
					shutil.copy2(backup_file, target_file)
					os.chmod(target_file, 0777)
					network_utils.start_network()
				self.write(utils.format_json_result())
			elif type == 'delete':
				backup = self.get_argument('backup','')
				logging.info('Manually deleting a backup')
				backup_file = os.path.join(globals.data_folder + '/xml_backups', backup)
				if not os.path.isfile(backup_file):
					raise Exception ('No config file found with name ' + str(backup))
				else:
					os.unlink(backup_file)
				self.write(utils.format_json_result())
		except Exception,e:
			self.write(utils.format_json_result(success="error",data=str(e)))

globals.app = Application([
		(r"/controller", ControllerHandler),
		(r"/network", NetworkHandler),
		(r"/node", NodeHandler),
		(r"/backup", BackupHandler)
    ])
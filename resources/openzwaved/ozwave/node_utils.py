import logging
import threading
import globals,utils,value_utils,serialization,network_utils
import time
from lxml import etree
from utilities.NodeExtend import *

def save_node_value_event(node_id, command_class, value_index, value, instance):
	globals.jeedom_com.add_changes('devices::' + str(node_id)+'::'+  str(command_class) + str(instance) + str(value_index),{'node_id': node_id, 'instance': instance, 'CommandClass': command_class, 'index': value_index,'value': value})

def save_node_event(node_id, value):
	if value == "removed":
		globals.jeedom_com.add_changes('controller::excluded', {"value": node_id})
	elif value == "added":
		globals.jeedom_com.add_changes('controller::included', {"value": node_id})
	elif value in [0, 1, 5] and globals.controller_state != value:
		globals.controller_state = value
		if globals.network.state >= globals.network.STATE_AWAKED:
			globals.jeedom_com.add_changes('controller::state', {"value": value})

def node_added(network, node):
	logging.info('A node has been added to OpenZWave list id:[%s] model:[%s].' % (node.node_id, node.product_name,))
	if node.node_id in globals.not_supported_nodes:
		logging.debug('remove fake nodeId: %s' % (node.node_id,))
		node_cleaner = threading.Timer(60.0, network.manager.removeFailedNode, [network.home_id, node.node_id])
		node_cleaner.start()
		return
	node.last_update = time.time()
	if network.state >= globals.network.STATE_AWAKED:
		utils.write_config()
		save_node_event(node.node_id, "added")

def node_removed(network, node):
	logging.info('A node has been removed from OpenZWave list id:[%s] model:[%s].' % (node.node_id, node.product_name,))
	if node.node_id in globals.not_supported_nodes:
		return
	if network.state >= globals.network.STATE_AWAKED:
		utils.write_config()
		save_node_event(node.node_id, "removed")
	if node.node_id in globals.node_notifications:
		del globals.node_notifications[node.node_id]
	if node.node_id in globals.pending_associations:
		del globals.pending_associations[node.node_id]

def node_queries_complete(network, node):
	logging.info('All the initialisation queries on a node have been completed. id:[%s] model:[%s].' % (node.node_id, node.product_name,))
	node.last_update = time.time()

def node_group_changed(network, node, groupidx):
	logging.info('Group changed for nodeId %s index %s' % (node.node_id, groupidx,))
	validate_association_groups(node.node_id)
	if node.node_id in globals.pending_associations:
		pending = globals.pending_associations[node.node_id]
		if groupidx in pending:
			pending_association = pending[groupidx]
			if pending_association is not None:
				pending_association.associations = node.groups[groupidx].associations

def node_event(network, node, value):
	logging.info('NodeId %s sends a Basic_Set command to the controller with value %s' % (node.node_id, value,))
	for value_id in network.nodes[node.node_id].get_values():
		my_value = network.nodes[node.node_id].values[value_id]
		if my_value.genre == "User" and not my_value.is_write_only:
			value_utils.value_update(network, node, my_value)
	save_node_value_event(node.node_id, globals.COMMAND_CLASS_BASIC, 0, value, 1)

def get_wake_up_interval(node_id):
	interval = value_utils.get_value_by_label(node_id, globals.COMMAND_CLASS_WAKE_UP, 1, 'Wake-up Interval')
	if interval is not None:
		return interval.data
	return None

def validate_association_groups(node_id):
	fake_found = False
	if globals.network is not None and globals.network.state >= globals.network.STATE_AWAKED:
		if node_id in globals.network.nodes:
			my_node = globals.network.nodes[node_id]
			query_stage_index = utils.convert_query_stage_to_int(my_node.query_stage)
			if query_stage_index >= 12:
				logging.debug("validate_association_groups for nodeId: %s" % (node_id,))
				for group_index in list(my_node.groups):
					group = my_node.groups[group_index]
					for target_node_id in list(group.associations):
						if target_node_id in globals.network.nodes and target_node_id not in globals.not_supported_nodes:
							continue
						logging.debug("Remove association for nodeId: %s index %s with not exist target: %s" % (
						node_id, group_index, target_node_id,))
						globals.network.manager.removeAssociation(globals.network.home_id, node_id, group_index, target_node_id)
						fake_found = True
	return fake_found

def check_primary_controller(my_node):
	for groupIndex in list(my_node.groups):
		group = my_node.groups[groupIndex]
		if len(group.associations_instances) > 0:
			for associations_instance in group.associations_instances:
				for node_instance in associations_instance:
					if globals.network.controller.node_id == node_instance:
						return True
					break
	return False
	
def get_all_info(node_id):
	return utils.format_json_result(data=serialization.serialize_node_to_json(node_id))

def get_statistics(node_id):
	utils.check_node_exist(node_id,True)
	query_stage_description = globals.network.manager.getNodeQueryStage(globals.network.home_id, node_id)
	query_stage_code = globals.network.manager.getNodeQueryStageCode(query_stage_description)
	return utils.format_json_result(data={'statistics': globals.network.manager.getNodeStatistics(globals.network.home_id, node_id), 'queryStageCode': query_stage_code, 'queryStageDescription': query_stage_description})
	
def get_pending_changes(node_id):
	utils.check_node_exist(node_id,True)
	query_stage_description = globals.network.manager.getNodeQueryStage(globals.network.home_id, node_id)
	query_stage_code = globals.network.manager.getNodeQueryStageCode(query_stage_description)
	return utils.format_json_result(data={'statistics': globals.network.manager.getNodeStatistics(globals.network.home_id, node_id), 'queryStageCode': query_stage_code, 'queryStageDescription': query_stage_description})

def get_health(node_id):
	return utils.format_json_result(data=serialization.serialize_node_to_json(node_id))

def request_neighbour_update(node_id):
	utils.check_node_exist(node_id,True)
	logging.info("request_node_neighbour_update for node %s" % (node_id,))
	return utils.format_json_result(data=globals.network.manager.requestNodeNeighborUpdate(globals.network.home_id, node_id))
	
def remove_failed(node_id):
	logging.info("Remove a failed node %s" % (node_id,))
	return utils.format_json_result(data=globals.network.manager.removeFailedNode(globals.network.home_id, node_id))

def heal(node_id,perform_return_routes_initialization=False):
	utils.check_node_exist(node_id,True)
	logging.info("Heal network node (%s) by requesting the node rediscover their neighbors" % (node_id,))
	globals.network.manager.healNetworkNode(globals.network.home_id, node_id, perform_return_routes_initialization)
	return utils.format_json_result()
	
def replace_failed(node_id):
	utils.check_node_exist(node_id,True)
	logging.info("replace_failed_node node %s" % (node_id,))
	return utils.format_json_result(data=globals.network.manager.replaceFailedNode(globals.network.home_id, node_id))
	
def send_information(node_id):
	utils.check_node_exist(node_id,True)
	logging.info("send_node_information node %s" % (node_id,))
	return utils.format_json_result(data=globals.network.manager.sendNodeInformation(globals.network.home_id, node_id))

def has_failed(node_id):
	utils.check_node_exist(node_id,True)
	logging.info("has_node_failed node %s" % (node_id,))
	return utils.format_json_result(data=globals.network.manager.hasNodeFailed(globals.network.home_id, node_id))
	
def test(node_id):
	utils.check_node_exist(node_id,True)
	globals.network.manager.testNetworkNode(globals.network.home_id, node_id, 3)
	return utils.format_json_result()

def refresh_all_values(node_id):
	utils.check_node_exist(node_id,True)
	current_node = globals.network.nodes[node_id]
	counter = 0
	logging.info("refresh_all_values node %s" % (node_id,))
	for value_id in current_node.get_values():
		current_value = current_node.values[value_id]
		if current_value.type == 'Button':
			continue
		if current_value.is_write_only:
			continue
		current_value.refresh()
		counter += 1
	message = 'Refreshed values count: %s' % (counter,)
	return utils.format_json_result(data=message)
	
def ghost_killer(node_id):
	logging.info('Remove cc 0x84 (wake_up) for a ghost device: %s' % (node_id,))
	filename = globals.data_folder + "/zwcfg_" + globals.network.home_id_str + ".xml"
	globals.network_is_running = False
	globals.network.stop()
	logging.info('ZWave network is now stopped')
	time.sleep(5)
	found = False
	message = None
	tree = etree.parse(filename)
	namespace = tree.getroot().tag[1:].split("}")[0]
	node = tree.find("{%s}Node[@id='%s']" % (namespace, node_id,))
	if node is None:
		message = 'node not found'
	else:
		command_classes = node.find(".//{%s}CommandClasses" % namespace)
		if command_classes is None:
			message = 'commandClasses not found'
		else:
			for command_Class in command_classes.findall(".//{%s}CommandClass" % namespace):
				if int(command_Class.get("id")[:7]) == globals.COMMAND_CLASS_WAKE_UP:
					command_classes.remove(command_Class)
					found = True
					break
			if found:
				config_file = open(filename, "w")
				config_file.write('<?xml version="1.0" encoding="utf-8" ?>\n')
				config_file.writelines(etree.tostring(tree, pretty_print=True))
				config_file.close()
			else:
				message = 'commandClass wake_up not found'
		globals.ghost_node_id = node_id
	network_utils.start_network()
	return utils.format_json_result(found, message)

def refresh_dynamic(node_id):
	globals.network.manager.requestNodeDynamic(globals.network.home_id, node_id)
	globals.network.nodes[node_id].last_update = time.time()
	logging.info("Fetch the dynamic command class data for the node %s" % (node_id,))
	return utils.format_json_result()

def refresh_info(node_id):
	utils.check_node_exist(node_id,True)
	logging.info("refresh_node_info node %s" % (node_id,))
	return utils.format_json_result(data=globals.network.manager.refreshNodeInfo(globals.network.home_id, node_id))

def assign_return_route(node_id):
	logging.info("Ask Node (%s) to update its Return Route to the Controller" % (node_id,))
	return utils.format_json_result(data=globals.network.manager.assignReturnRoute(globals.network.home_id, node_id))

def add_assoc(node_id, group, target_id,instance,action):
	utils.can_execute_command(0)
	utils.check_node_exist(node_id)
	if action == 'add':
		utils.check_node_exist(target_id)
	logging.info(action + ' assoc to nodeId: ' + str(node_id) + ' in group ' + str(group) + ' with nodeId: ' + str(
		node_id) + ' on instance ' + str(instance))
	if node_id not in globals.pending_associations:
		globals.pending_associations[node_id] = dict()
	if action == 'remove':
		globals.pending_associations[node_id][group] = PendingAssociation(pending_added=None, pending_removed=target_id,timeout=0)
		if instance < 1:
			globals.network.manager.removeAssociation(globals.network.home_id, node_id, group, target_id)
		else:
			globals.network.manager.removeAssociation(globals.network.home_id, node_id, group, target_id, instance)
	if action == 'add':
		globals.pending_associations[node_id][group] = PendingAssociation(pending_added=target_id, pending_removed=None,timeout=0)
		if instance < 1:
			globals.network.manager.addAssociation(globals.network.home_id, node_id, group, target_id)
		else:
			globals.network.manager.addAssociation(globals.network.home_id, node_id, group, target_id, instance)
	return utils.format_json_result()

def test_node(node_id, count=3):
	utils.can_execute_command()
	utils.check_node_exist(node_id,True)
	globals.network.manager.testNetworkNode(globals.network.home_id, node_id, count)
	return utils.format_json_result()

def node_notification(args):
	code = int(args['notificationCode'])
	node_id = int(args['nodeId'])
	if node_id in globals.not_supported_nodes:
		return
	if node_id in globals.disabled_nodes:
		return
	if node_id in globals.network.nodes:
		my_node = globals.network.nodes[node_id]
		# mark as updated
		my_node.last_update = time.time()
		# try auto remove unsupported nodes
		if node_id in globals.not_supported_nodes and globals.network.state >= globals.network.STATE_AWAKED:
			logging.info('remove fake nodeId: %s' % (node_id,))
			globals.network.manager.removeFailedNode(globals.network.home_id, node_id)
			return
		wake_up_time = get_wake_up_interval(node_id)
		if node_id not in globals.node_notifications:
			globals.node_notifications[node_id] = NodeNotification(code, wake_up_time)
		else:
			globals.node_notifications[node_id].refresh(code, wake_up_time)
		if code == 3:
			my_value = value_utils.get_value_by_label(node_id, globals.COMMAND_CLASS_WAKE_UP, 1, 'Wake-up Interval Step')
			if my_value is not None:
				wake_up_interval_step = my_value.data + 2.0
			else:
				wake_up_interval_step = 60.0
		logging.info('NodeId %s send a notification: %s' % (node_id, globals.node_notifications[node_id].description,))
		push_node_notification(node_id, code)

def push_node_notification(node_id, notification_code):
	if notification_code in [5, 6]:
		if notification_code == 5:
			alert_type = 'node_dead'
		else:
			alert_type = 'node_alive'
		changes = {'alert': {'type': alert_type, 'id': node_id}}
		globals.jeedom_com.send_change_immediate(changes)

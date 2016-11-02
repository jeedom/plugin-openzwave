import logging
import time
import threading
from threading import Event, Thread
import globals,utils,value_utils
from utilities.NodeExtend import *
from utilities.Constants import *

def save_node_value_event(node_id, timestamp, command_class, value_index, standard_type, value, instance):
	globals.jeedom_com.add_changes('devices::' + str(node_id) + '::' + str(hex(command_class)) + str(instance) + str(value_index),{'node_id': node_id, 'instance': instance, 'CommandClass': hex(command_class), 'index': value_index,'value': value, 'type': standard_type, 'updateTime': timestamp})

def save_node_event(node_id, value):
	if value == "removed":
		globals.jeedom_com.add_changes('controller::excluded', {"value": node_id})
	elif value == "added":
		globals.jeedom_com.add_changes('controller::included', {"value": node_id})
	elif value in [0, 1, 5] and globals.controller_state != value:
		globals.controller_state = value
		if globals.network.state >= globals.network.STATE_AWAKED:
			globals.jeedom_com.add_changes('controller::state', {"value": value})

def push_node_notification(node_id, notification_code):
	# check for notification Dead or Alive
	if notification_code in [5, 6]:
		if notification_code == 5:
			# Report when a node is presumed dead
			alert_type = 'node_dead'
		else:
			# Report when a node is revived
			alert_type = 'node_alive'
		changes = {'alert': {'type': alert_type, 'id': node_id}}
		globals.jeedom_com.send_change_immediate(changes)

def recovering_failed_nodes_asynchronous():
	# wait 15 seconds on first launch
	time.sleep(globals.sanity_checks_delay)
	while True:
		sanity_checks()
		# wait for next run
		time.sleep(globals.recovering_failed_nodes_timer)

def nodes_queried(network):
	utils.write_config()

def nodes_queried_some_dead(network):
	utils.write_config()
	logging.info("All nodes have been queried, but some node ar mark dead")

def node_new(network, node_id):
	if node_id in globals.not_supported_nodes:
		return
	logging.info('A new node (%s), not already stored in zwcfg*.xml file, was found.' % (node_id,))
	globals.force_refresh_nodes.append(node_id)

def node_added(network, node):
	logging.info('A node has been added to OpenZWave list id:[%s] model:[%s].' % (node.node_id, node.product_name,))
	if node.node_id in globals.not_supported_nodes:
		logging.debug('remove fake nodeId: %s' % (node.node_id,))
		node_cleaner = threading.Timer(60.0, network.manager.removeFailedNode, [network.home_id, node.node_id])
		node_cleaner.start()
		return
	node.last_update = time.time()
	if network.state >= globals.network.STATE_AWAKED:
		save_node_event(node.node_id, "added")

def node_removed(network, node):
	logging.info('A node has been removed from OpenZWave list id:[%s] model:[%s].' % (node.node_id, node.product_name,))
	if node.node_id in globals.not_supported_nodes:
		return
	if network.state >= globals.network.STATE_AWAKED:
		save_node_event(node.node_id, "removed")
	# clean dict
	if node.node_id in globals.node_notifications:
		del globals.node_notifications[node.node_id]
	if node.node_id in globals.pending_associations:
		del globals.pending_associations[node.node_id]

def essential_node_queries_complete(network, node):
	logging.info(
		'The essential queries on a node have been completed. id:[%s] model:[%s].' % (node.node_id, node.product_name,))
	my_node = network.nodes[node.node_id]
	my_node.last_update = time.time()
	# at this time is not good to save value, I skip this step

def node_queries_complete(network, node):
	logging.info('All the initialisation queries on a node have been completed. id:[%s] model:[%s].' % (
	node.node_id, node.product_name,))
	node.last_update = time.time()
	# save config
	utils.write_config()

def node_group_changed(network, node, groupidx):
	logging.info('Group changed for nodeId %s index %s' % (node.node_id, groupidx,))
	validate_association_groups(node.node_id)
	# check pending for this group index
	if node.node_id in globals.pending_associations:
		pending = globals.pending_associations[node.node_id]
		if groupidx in pending:
			pending_association = pending[groupidx]
			if pending_association is not None:
				pending_association.associations = node.groups[groupidx].associations

def node_notification(arguments):
	code = int(arguments['notificationCode'])
	node_id = int(arguments['nodeId'])
	if node_id in globals.not_supported_nodes:
		return
	if node_id in globals.disabled_nodes:
		return
	if node_id in globals.network.nodes:
		my_node = globals.network.nodes[node_id]
		my_node.last_update = time.time()
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
			my_value = values_utils.get_value_by_label(node_id, COMMAND_CLASS_WAKE_UP, 1, 'Wake-up Interval Step', False)
			if my_value is not None:
				wake_up_interval_step = my_value.data + 2.0
			else: 
				wake_up_interval_step = 60.0
			threading.Timer(interval=wake_up_interval_step, function=force_sleeping, args=(node_id, 1)).start()
		logging.info('NodeId %s send a notification: %s' % (node_id, globals.node_notifications[node_id].description,))
		push_node_notification(node_id, code)

def node_event(network, node, value):
	logging.info('NodeId %s sends a Basic_Set command to the controller with value %s' % (node.node_id, value,))
	for val in network.nodes[node.node_id].get_values():
		my_value = network.nodes[node.node_id].values[val]
		if my_value.genre == "User" and not my_value.is_write_only:
			value_update(network, node, my_value)
	'''
	the value is actually the event data, not a zwave value object.
	This is commonly caused when a node sends a Basic_Set command to the controller.
	'''
	standard_type = 'int'
	save_node_value_event(node.node_id, int(time.time()), COMMAND_CLASS_BASIC, 0, standard_type, value, 0)

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

def get_wake_up_interval(node_id):
	interval = value_utils.get_value_by_label(node_id, COMMAND_CLASS_WAKE_UP, 1, 'Wake-up Interval', False)
	if interval is not None:
		return interval.data
	return None

def force_sleeping(node_id, count=1):
	if node_id in globals.network.nodes:
		my_node = globals.network.nodes[node_id]
		logging.debug('check if node %s still awake' % (node_id,))
		last_notification = None
		if node_id in globals.node_notifications:
			last_notification = globals.node_notifications[node_id]
		if my_node.is_awake or (last_notification is not None and last_notification.code == 3):
			logging.debug('trying to lull the node %s' % (node_id,))
			globals.network.manager.testNetworkNode(globals.network.home_id, node_id, count)

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
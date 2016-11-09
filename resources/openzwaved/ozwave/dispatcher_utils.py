import logging
import sys
import globals
import network_utils,node_utils,value_utils,scene_utils,controller_utils
try:
	from louie import dispatcher
except Exception as e:
	print(globals.MSG_CHECK_DEPENDENCY, 'error')
	print("Error: %s" % str(e), 'error')
	sys.exit(1)

def connect_dispatcher():
	if globals.dispatcher_is_connect:
		return
	logging.debug('connect to the louie dispatcher')
	add_dispatcher_listen(network_utils.network_started, globals.network.SIGNAL_NETWORK_STARTED)
	add_dispatcher_listen(network_utils.network_failed, globals.network.SIGNAL_NETWORK_FAILED)
	add_dispatcher_listen(network_utils.network_failed, globals.network.SIGNAL_DRIVER_FAILED)
	add_dispatcher_listen(network_utils.network_awaked, globals.network.SIGNAL_NETWORK_AWAKED)
	add_dispatcher_listen(network_utils.network_ready, globals.network.SIGNAL_NETWORK_READY)
	add_dispatcher_listen(network_utils.network_stopped, globals.network.SIGNAL_NETWORK_STOPPED)
	add_dispatcher_listen(node_utils.node_new, globals.network.SIGNAL_NODE_NEW)
	add_dispatcher_listen(node_utils.node_added, globals.network.SIGNAL_NODE_ADDED)
	add_dispatcher_listen(node_utils.node_removed, globals.network.SIGNAL_NODE_REMOVED)
	add_dispatcher_listen(value_utils.value_added, globals.network.SIGNAL_VALUE_ADDED)
	add_dispatcher_listen(value_utils.value_update, globals.network.SIGNAL_VALUE_CHANGED)
	add_dispatcher_listen(value_utils.value_refreshed, globals.network.SIGNAL_VALUE_REFRESHED)
	add_dispatcher_listen(value_utils.value_removed, globals.network.SIGNAL_VALUE_REMOVED)
	# dispatcher.connect(value_utils.value_polling_enabled, globals.network.SIGNAL_POLLING_ENABLED)
	add_dispatcher_listen(node_utils.node_event, globals.network.SIGNAL_NODE_EVENT)
	add_dispatcher_listen(scene_utils.scene_event, globals.network.SIGNAL_SCENE_EVENT)
	add_dispatcher_listen(node_utils.essential_node_queries_complete, globals.network.SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE)
	add_dispatcher_listen(node_utils.node_queries_complete, globals.network.SIGNAL_NODE_QUERIES_COMPLETE)
	add_dispatcher_listen(node_utils.nodes_queried, globals.network.SIGNAL_AWAKE_NODES_QUERIED)
	add_dispatcher_listen(node_utils.nodes_queried, globals.network.SIGNAL_ALL_NODES_QUERIED)
	add_dispatcher_listen(node_utils.nodes_queried_some_dead, globals.network.SIGNAL_ALL_NODES_QUERIED_SOME_DEAD)
	#add_dispatcher_listen(node_utils.node_notification, globals.network.SIGNAL_NOTIFICATION)
	if globals.network.state >= globals.network.STATE_AWAKED:
		add_dispatcher_listen(node_utils.node_group_changed, globals.network.SIGNAL_GROUP)
	globals.dispatcher_is_connect = True

def disconnect_dispatcher():
	logging.debug('disconnect the louie dispatcher')
	try:
		remove_dispatcher_listen(network_utils.network_started, globals.network.SIGNAL_NETWORK_STARTED)
		remove_dispatcher_listen(network_utils.network_failed, globals.network.SIGNAL_NETWORK_FAILED)
		remove_dispatcher_listen(network_utils.network_failed, globals.network.SIGNAL_DRIVER_FAILED)
		remove_dispatcher_listen(network_utils.network_awaked, globals.network.SIGNAL_NETWORK_AWAKED)
		remove_dispatcher_listen(network_utils.network_ready, globals.network.SIGNAL_NETWORK_READY)
		remove_dispatcher_listen(network_utils.network_stopped, globals.network.SIGNAL_NETWORK_STOPPED)
		remove_dispatcher_listen(node_utils.node_new, globals.network.SIGNAL_NODE_NEW)
		remove_dispatcher_listen(node_utils.node_added, globals.network.SIGNAL_NODE_ADDED)
		remove_dispatcher_listen(node_utils.node_removed, globals.network.SIGNAL_NODE_REMOVED)
		remove_dispatcher_listen(value_utils.value_added, globals.network.SIGNAL_VALUE_ADDED)
		remove_dispatcher_listen(value_utils.value_update, globals.network.SIGNAL_VALUE_CHANGED)
		remove_dispatcher_listen(value_utils.value_refreshed, globals.network.SIGNAL_VALUE_REFRESHED)
		remove_dispatcher_listen(value_utils.value_removed, globals.network.SIGNAL_VALUE_REMOVED)
		#remove_dispatcher_listen(value_utils.value_polling_enabled, globals.network.SIGNAL_POLLING_ENABLED)
		remove_dispatcher_listen(node_utils.node_event, globals.network.SIGNAL_NODE_EVENT)
		remove_dispatcher_listen(scene_utils.scene_event, globals.network.SIGNAL_SCENE_EVENT)
		remove_dispatcher_listen(node_utils.essential_node_queries_complete, globals.network.SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE)
		remove_dispatcher_listen(node_utils.node_queries_complete, globals.network.SIGNAL_NODE_QUERIES_COMPLETE)
		remove_dispatcher_listen(node_utils.nodes_queried, globals.network.SIGNAL_AWAKE_NODES_QUERIED)
		remove_dispatcher_listen(node_utils.nodes_queried, globals.network.SIGNAL_ALL_NODES_QUERIED)
		remove_dispatcher_listen(node_utils.nodes_queried_some_dead, globals.network.SIGNAL_ALL_NODES_QUERIED_SOME_DEAD)
		#remove_dispatcher_listent(node_utils.node_notification, globals.network.SIGNAL_NOTIFICATION)
		if globals.network.state >= globals.network.STATE_AWAKED:
			remove_dispatcher_listen(node_utils.node_group_changed, globals.network.SIGNAL_GROUP)
	except Exception:
		pass
	globals.dispatcher_is_connect = False

def add_dispatcher_listen(func,notif):
	dispatcher.connect(func, notif)

def remove_dispatcher_listen(func,notif):
	dispatcher.disconnect(func, notif)
import logging
import node_utils,globals

def scene_event(network, node, scene_id):
	logging.info('Scene Activation: %s' % (scene_id,))
	node_utils.save_node_value_event(node.node_id,  globals.COMMAND_CLASS_SCENE_ACTIVATION, 0, scene_id, 1)

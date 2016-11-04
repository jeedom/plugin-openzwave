import utils,network_utils,controller_utils,node_utils
#Various mappings
CONVERSION = {'Int': 'int',\
	'Decimal': 'float',\
	'Bool':'bool',\
	'Byte':'int',\
	'Short':'int',\
	'Button':'bool',\
	'Raw':'binary',\
	40 : 'error',\
	20 : 'debug',\
	10 : 'info',\
	'None': 0,\
	'ProtocolInfo': 1,\
	'Probe': 2,\
	'WakeUp': 3,\
	'ManufacturerSpecific1': 4,\
	'NodeInfo': 5,\
	'NodePlusInfo': 5,\
	'SecurityReport': 6,\
	'ManufacturerSpecific2': 7,\
	'Versions': 8,\
	'Instances': 9,\
	'Static': 10,\
	'CacheLoad': 11,\
	'Associations': 12,\
	'Neighbors': 13,\
	'Session': 14,\
	'Dynamic': 15,\
	'Configuration': 16,\
	'Complete': 17,\
	}

NETWORK_REST_MAPPING = {'start' : network_utils.start_network,\
	'stop' : network_utils.graceful_stop_network, \
	'writeZWConfig' : utils.write_config,\
	'manualBackup' : network_utils.manual_backup,\
	'performSanityChecks' : network_utils.perform_sanity_checks,\
	'getStatus': network_utils.get_status,\
	'getHealth' : network_utils.get_health,\
	'getNodesList' : network_utils.get_nodes_list,\
	'getControllerStatus' : controller_utils.get_controller_status,\
	'getOZLogs' : network_utils.get_oz_logs,\
	'getZWConfig' : network_utils.get_oz_config,\
	'getOZBackups' : network_utils.get_oz_backups,\
	'getNeighbours' : network_utils.get_neighbours,\
	}

NODE_REST_MAPPING = {'all' : node_utils.get_all_info,\
	'getNodeStatistics' : node_utils.get_statistics, \
	'getPendingChanges' : node_utils.get_pending_changes,\
	'getLastNotification' : node_utils.get_last_notification,\
	'getHealth' : node_utils.get_health,\
	'requestNodeNeighbourUpdate': node_utils.request_neighbour_update,\
	'removeFailedNode': node_utils.remove_failed,\
	'healNode': node_utils.heal,\
	'replaceFailedNode': node_utils.replace_failed,\
	'sendNodeInformation': node_utils.send_information,\
	'hasNodeFailed': node_utils.has_failed,\
	'testNode': node_utils.test,\
	'refreshAllValues': node_utils.refresh_all_values,\
	'ghostKiller': node_utils.ghost_killer,\
	'requestNodeDynamic': node_utils.refresh_dynamic,\
	'refreshNodeInfo': node_utils.refresh_info,\
	'assignReturnRoute': node_utils.assign_return_route,\
	}

#Various message
MSG_CHECK_DEPENDENCY = 'The dependency of openzwave plugin are not installed. Please check the plugin openzwave configuration page for instructions'

#Init Daemon
device = "auto"
# noinspection PyRedeclaration
log_level = "error"
port_server = 8083
config_folder = None
data_folder = None
pidfile = '/tmp/openzwaved.pid'
apikey = ''
callback = ''
assumeAwake = False
suppress_refresh = False
disabled_nodes = []
cycle = 0.3

# default_poll_interval = 1800000  # 30 minutes
default_poll_interval = 300000  # 5 minutes
maximum_poll_intensity = 1
controller_state = -1
# maximum time (in seconds) allowed for a background refresh
refresh_timeout = 120
# background refresh interval step in seconds
refresh_interval = 3
# post topology loaded delay tasks
refresh_configuration_timer = 360.0
refresh_user_values_timer = 120.0
validate_association_groups_timer = 45.0
recovering_failed_nodes_timer = 900.0  # 15 minutes
# perform sanitary jobs
recovering_failed_nodes_jobs_timer = 900.0  # 15 minutes
maximum_number_notifications = 25
sanity_checks_delay = 15.0
not_supported_nodes = [0, 255]
user_values_to_refresh = ["Level", "Sensor", "Switch", "Power", "Temperature", "Alarm Type", "Alarm Type", "Power Management"]
network = None
network_information = None
force_refresh_nodes = []
changes_async = {'device': {}}
ghost_node_id = None
sanity_checks_running = False
pending_configurations = {}
pending_associations = {}
node_notifications = {}
dispatcher_is_connect = False
network_is_running = False
files_manager = None

#Daemon Globals
know_sticks = [{'idVendor': '0658', 'idProduct': '0200', 'name': 'Sigma Designs, Inc'},{'idVendor': '10c4', 'idProduct': 'ea60', 'name': 'Cygnal Integrated Products, Inc. CP210x UART Bridge'}]
jeedom_com = ''
options = ''
app = ''
refresh_workers = {}

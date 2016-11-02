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

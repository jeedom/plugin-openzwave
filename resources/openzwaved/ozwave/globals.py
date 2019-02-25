import utils,network_utils,controller_utils,node_utils
#Various mappings
REFRESH_MAPPING = {'2|3|32784': {'67|1|1' : {'onlyset' : '67|11|1','sleep' :1 , 'number' :1 , 'com' : 'lc13 vanne setvalue setpoint sans attendre reveil' }},\
					'2|5|3': {'67|1|1' : {'onlyset' : '67|11|1','sleep' :1 , 'number' :1 , 'com' : 'lc13 vanne setvalue setpoint sans attendre reveil' }},\
					'2|5|4': {'67|1|1' : {'onlyset' : '67|11|1','sleep' :1 , 'number' :1 , 'com' : 'lc13 vanne setvalue setpoint sans attendre reveil' }},\
					'2|5|373': {'67|1|1' : {'onlyset' : '67|11|1','sleep' :1 , 'number' :1 , 'com' : 'devolo vanne setvalue setpoint sans attendre reveil' }},\
					'2|100|1': {'67|1|1' : {'onlyset' : '67|11|1','sleep' :1 , 'number' :1 , 'com' : 'lc13 vanne setvalue setpoint sans attendre reveil' }},\
					'2|277|40976': {'67|1|1' : {'onlyset' : '67|11|1','sleep' :1 , 'number' :1 , 'com' : 'lc13 vanne setvalue setpoint sans attendre reveil' }},\
					'2|32773|1': {'67|1|1' : {'onlyset' : '67|11|1','sleep' :1 , 'number' :1 , 'com' : 'lc13 vanne setvalue setpoint sans attendre reveil' }},\
					'2|32773|32769': {'67|1|1' : {'onlyset' : '67|11|1','sleep' :1 , 'number' :1 , 'com' : 'lc13 vanne setvalue setpoint sans attendre reveil' }},\
					'271|2304|4096': {'51|1|0' : {'sleep' :5 , 'number' :3 , 'other' : '38|1|0'},'38|1|0' : {'sleep' :5 , 'number' :3 , 'other' : '51|1|0'}},\
					'271|4865|4096': {'64|1|0' : {'sleep' :5 , 'number' :1},'67|1|1' : {'sleep' :5 , 'number' :1}},\
					'526|19522|12596': {'38|1|0' : {'sleep' :2 , 'number' :3}},\
					'271|6145|4096': {'37|1|0' : {'sleep' :1 , 'number' :1}},\
					'271|769|4097': {'38|1|0' : {'sleep' :5 , 'number' :4},'38|1|1' : {'sleep' :5 , 'number' :4, 'other':'38|1|0'},'38|1|2' : {'sleep' :5 , 'number' :4, 'other':'38|1|0'}},\
					'271|771|4096': {'38|1|0' : {'sleep' :5 , 'number' :4},'38|1|1' : {'sleep' :5 , 'number' :4, 'other':'38|1|0'},'38|1|2' : {'sleep' :5 , 'number' :4, 'other':'38|1|0'}},\
					'271|7425|4096': {'38|1|0' : {'sleep' :5 , 'number' :4},'38|1|1' : {'sleep' :5 , 'number' :4, 'other':'38|1|0'},'38|1|2' : {'sleep' :5 , 'number' :4, 'other':'38|1|0'}},\
					}


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
	'getStatus': network_utils.get_status,\
	'getHealth' : network_utils.get_health,\
	'getNodesList' : network_utils.get_nodes_list,\
	'getZWConfig' : network_utils.get_oz_config,\
	'getOZBackups' : network_utils.get_oz_backups,\
	'getNeighbours' : network_utils.get_neighbours,\
	}

NODE_REST_MAPPING = {'all' : node_utils.get_all_info,\
	'getNodeStatistics' : node_utils.get_statistics, \
	'getPendingChanges' : node_utils.get_pending_changes,\
	'getHealth' : node_utils.get_health,\
	'requestNodeNeighbourUpdate': node_utils.request_neighbour_update,\
	'removeFailedNode': node_utils.remove_failed,\
	'healNode': node_utils.heal,\
	'replaceFailedNode': node_utils.replace_failed,\
	'sendNodeInformation': node_utils.send_information,\
	'hasNodeFailed': node_utils.has_failed,\
	'testNode': node_utils.test,\
	'refreshAllValues': node_utils.refresh_all_values,\
	'removeGhostNode': node_utils.ghost_killer,\
	'requestNodeDynamic': node_utils.refresh_dynamic,\
	'refreshNodeInfo': node_utils.refresh_info,\
	'assignReturnRoute': node_utils.assign_return_route,\
	}

CONTROLLER_REST_MAPPING = {'hardReset' : controller_utils.hard_reset,\
	'receiveConfiguration' : controller_utils.receive_configuration, \
	'transferPrimaryRole' : controller_utils.transfer_primary_role,\
	'createNewPrimary' : controller_utils.create_new_primary,\
	'testNetwork' : controller_utils.test_network,\
	'serialAPISoftReset': controller_utils.serial_api_soft_reset,\
	'healNetwork': controller_utils.heal_network,\
	'cancelCommand': controller_utils.cancel_command,\
	'writeZWConfig' : utils.write_config,\
	'removeUnknownsDevices' : controller_utils.remove_unknowns_devices_openzwave_config,\
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
disabled_nodes = []
cycle = 0.3
socket_host = '127.0.0.1'

# default_poll_interval = 1800000  # 30 minutes
default_poll_interval = 300000  # 5 minutes
maximum_poll_intensity = 1
controller_state = -1
maximum_number_notifications = 25
ghost_removal_delay = 15.0
not_supported_nodes = [0, 255]
network = None
network_information = None
ghost_node_id = None
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

#some constants
COMMAND_CLASS_ALARM = 113 # 0x71
# COMMAND_CLASS_ANTITHEFT = 93 # 0x5D
# COMMAND_CLASS_APPLICATION_CAPABILITY = 87 # 0x57
COMMAND_CLASS_APPLICATION_STATUS = 34 # 0x22
COMMAND_CLASS_ASSOCIATION = 133 # 0x85
COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION = 155 # 0x9B
# COMMAND_CLASS_ASSOCIATION_GRP_INFO = 89 # 0x59
COMMAND_CLASS_BATTERY = 128 # 0x80
COMMAND_CLASS_CENTRAL_SCENE = 91 # 0x5B
COMMAND_CLASS_CLOCK = 129 # 0x81
COMMAND_CLASS_CONFIGURATION = 112 # 0x70
COMMAND_CLASS_CONTROLLER_REPLICATION = 33 # 0x21
COMMAND_CLASS_CRC_16_ENCAP = 86 # 0x56
COMMAND_CLASS_DEVICE_RESET_LOCALLY = 90 # 0x5A
COMMAND_CLASS_FIRMWARE_UPDATE_MD = 122 #0x7A
COMMAND_CLASS_GEOGRAPHIC_LOCATION = 150 # 0x8C
COMMAND_CLASS_GROUPING_NAME = 123 # 0x7B [DEPRECATED]
COMMAND_CLASS_HAIL = 130 # 0x82 [DEPRECATED]
COMMAND_CLASS_INDICATOR = 135 # 0x87
# COMMAND_CLASS_IP_ASSOCIATION = 92 # 0x5C
COMMAND_CLASS_IP_CONFIGURATION = 154 # 0x9A
COMMAND_CLASS_LANGUAGE = 137 # 0x89
# COMMAND_CLASS_MAILBOX = 105 # 0x69
COMMAND_CLASS_MANUFACTURER_PROPRIETARY = 145 # 0x91
COMMAND_CLASS_MANUFACTURER_SPECIFIC= 114 # 0x72
COMMAND_CLASS_MARK= 239 # 0xEF
COMMAND_CLASS_MULTI_CHANNEL= 96 # 0x60 COMMAND_CLASS_MULTI_INSTANCE
COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION= 142 # 0x8E COMMAND_CLASS_MULTI_INSTANCE_ASSOCIATION
COMMAND_CLASS_MULTI_COMMAND = 143 # 0x8F COMMAND_CLASS_MULTI_CMD
COMMAND_CLASS_NETWORK_MANAGEMENT_BASIC = 0 # 0x4D
COMMAND_CLASS_NETWORK_MANAGEMENT_INCLUSION = 52 # 0x34 COMMAND_CLASS_ZIP_ADV_CLIENT
COMMAND_CLASS_NETWORK_MANAGEMENT_PRIMARY = 0 # 0x54
COMMAND_CLASS_NETWORK_MANAGEMENT_PROXY = 0 # 0x52
COMMAND_CLASS_NO_OPERATION = 0 # 0 # 0x00
COMMAND_CLASS_NODE_NAMING = 119 # 0x77
COMMAND_CLASS_NON_INTEROPERABLE = 240 # 0xF0
# COMMAND_CLASS_NOTIFICATION = 113 # 0x71
COMMAND_CLASS_PROPRIETARY = 136 # 0x88 [DEPRECATED]
COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE = 124 # 0x7C
COMMAND_CLASS_REMOTE_ASSOCIATION = 125 # 0x7D
# COMMAND_CLASS_SCHEDULE = 83 # 0x53
COMMAND_CLASS_SCREEN_ATTRIBUTES = 147 # 0x93
COMMAND_CLASS_SCREEN_MD = 146 # 0x92
COMMAND_CLASS_SECURITY = 152 # 0x98
COMMAND_CLASS_SECURITY_SCHEME0_MARK = 0 # 0xF100
# COMMAND_CLASS_SUPERVISION = 108 # 0x6C
COMMAND_CLASS_TIME = 138 # 0x8A
COMMAND_CLASS_TIME_PARAMETERS = 139 # 0x8B
COMMAND_CLASS_TRANSPORT_SERVICE = 0 # 0x55
COMMAND_CLASS_USER_CODE = 99 # 0x63
COMMAND_CLASS_VERSION = 134 # 0x86
COMMAND_CLASS_WAKE_UP = 132 # 0x84
COMMAND_CLASS_ZIP = 35 # 0x23 COMMAND_CLASS_ZIP_SERVICES
# COMMAND_CLASS_ZIP_NAMING = 104 # 0x68
# COMMAND_CLASS_ZIP_ND = 88 # 0x58
# COMMAND_CLASS_ZIP_6LOWPAN = 79 # 0x4F
# COMMAND_CLASS_ZIP_GATEWAY= 95 # 0x5F
# COMMAND_CLASS_ZIP_PORTAL= 97 # 0x61
COMMAND_CLASS_ZWAVEPLUS_INFO = 94 # 0x5E COMMAND_CLASS_ZWAVE_PLUS_INFO

# Device related Command Class identifiers
COMMAND_CLASS_SENSOR_ALARM = 156 # 0x9C [DEPRECATED]
COMMAND_CLASS_SILENCE_ALARM = 157 # 0x9D
COMMAND_CLASS_SWITCH_ALL = 39 # 0x27
COMMAND_CLASS_BARRIER_OPERATOR = 102 # 0x66
COMMAND_CLASS_BASIC = 32 # 0x20
# COMMAND_CLASS_BASIC_TARIFF_INFO = 54 # 0x36
COMMAND_CLASS_BASIC_WINDOW_COVERING = 80 # 0x50
COMMAND_CLASS_SENSOR_BINARY = 48 # 0x30 [DEPRECATED]
COMMAND_CLASS_SWITCH_BINARY = 37 # 0x25
COMMAND_CLASS_SWITCH_TOGGLE_BINARY = 40 # 0x28 [DEPRECATED]
COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE = 70 # 0x46 [DEPRECATED]
COMMAND_CLASS_SWITCH_COLOR = 51 # 0x33 COMMAND_CLASS_COLOR
# COMMAND_CLASS_DCP_CONFIG = 58 # 0x3A
# COMMAND_CLASS_DCP_MONITOR = 59 # 0x3B
COMMAND_CLASS_DOOR_LOCK = 98 # 0x62
COMMAND_CLASS_DOOR_LOCK_LOGGING = 76 # 0x4C
COMMAND_CLASS_ENERGY_PRODUCTION = 144 # 0x90
# COMMAND_CLASS_ENTRY_CONTROL = 111 # 0x6F
# COMMAND_CLASS_HRV_STATUS = 55 # 0x37
# COMMAND_CLASS_HRV_CONTROL = 57 # 0x39
# COMMAND_CLASS_HUMIDITY_CONTROL_MODE = 109 # 0x6D
# COMMAND_CLASS_HUMIDITY_CONTROL_OPERATING_STATE = 110 # 0x6E
# COMMAND_CLASS_HUMIDITY_CONTROL_SETPOINT = 100 # 0x64
# COMMAND_CLASS_IRRIGATION = 107 # 0x6B
COMMAND_CLASS_LOCK = 118 # 0x76
COMMAND_CLASS_METER = 50 #0x32
COMMAND_CLASS_METER_TBL_CONFIG = 60 #0x3C
COMMAND_CLASS_METER_TBL_MONITOR = 61 #0x3D
COMMAND_CLASS_METER_TBL_PUSH = 62 #0x3E
COMMAND_CLASS_MTP_WINDOW_COVERING = 81 #0x51
COMMAND_CLASS_SENSOR_MULTILEVEL = 49 #0x31
COMMAND_CLASS_SWITCH_MULTILEVEL = 38 #0x26
COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL = 41 #0x29 [DEPRECATED]
COMMAND_CLASS_POWERLEVEL = 115 #0x73 COMMAND_CLASS_POWER_LEVEL
# COMMAND_CLASS_PREPAYMENT = 63 #0x3F
# COMMAND_CLASS_PREPAYMENT_ENCAPSULATION = 65 #0x41
COMMAND_CLASS_PROTECTION = 117 #0x75
COMMAND_CLASS_METER_PULSE  = 53 #0x35 [DEPRECATED]
# COMMAND_CLASS_RATE_TBL_CONFIG = 74 #0x48
# COMMAND_CLASS_RATE_TBL_MONITOR = 75 #0x49
COMMAND_CLASS_SCENE_ACTIVATION = 43 #0x2B
COMMAND_CLASS_SCENE_ACTUATOR_CONF = 44 #0x2C
COMMAND_CLASS_SCENE_CONTROLLER_CONF = 45 #0x2D
COMMAND_CLASS_SCHEDULE_ENTRY_LOCK = 78 #0x4E [DEPRECATED]
COMMAND_CLASS_SENSOR_CONFIGURATION  = 158 #0x9E
COMMAND_CLASS_SIMPLE_AV_CONTROL = 148 #0x94
# COMMAND_CLASS_TARIFF_TBL_CONFIG = 74 #0x4A
# COMMAND_CLASS_TARIFF_TBL_MONITOR = 75 #0x4B
COMMAND_CLASS_THERMOSTAT_FAN_MODE = 68 #0x44
COMMAND_CLASS_THERMOSTAT_FAN_STATE = 69 #0x45
COMMAND_CLASS_THERMOSTAT_MODE  = 64 #0x40
COMMAND_CLASS_THERMOSTAT_OPERATING_STATE = 66 #0x42
COMMAND_CLASS_THERMOSTAT_SETBACK = 71 #0x47
COMMAND_CLASS_THERMOSTAT_SETPOINT = 67 #0x43 COMMAND_CLASS_THERMOSTAT_SET_POINT
# COMMAND_CLASS_WINDOW_COVERING = 106 #0x6A

# not present in Sigma SDK
# COMMAND_CLASS_ZIP_SERVER                = 36  # 0x24
# COMMAND_CLASS_CHIMNEY_FAN               = 42  # 0x2A
# COMMAND_CLASS_ZIP_CLIENT                = 46  # 0x2E
# COMMAND_CLASS_ZIP_ADV_SERVICES          = 47  # 0x2F
# COMMAND_CLASS_THERMOSTAT_HEATING        = 56  # 0x38
# COMMAND_CLASS_COMPOSITE                 = 141  # 0x8D
# COMMAND_CLASS_AV_CONTENT_DIRECTORY_MD   = 149  # 0x95
# COMMAND_CLASS_AV_RENDERER_STATUS        = 150  # 0x96
# COMMAND_CLASS_AV_CONTENT_SEARCH_MD      = 151  # 0x97
# COMMAND_CLASS_AV_TAGGING_MD             = 153  # 0x99

SPECIFIC_TYPE_MOTOR_MULTI_POSITION = 3
SPECIFIC_TYPE_CLASS_A_MOTOR_CONTROL = 5
SPECIFIC_TYPE_CLASS_B_MOTOR_CONTROL = 6
SPECIFIC_TYPE_CLASS_C_MOTOR_CONTROL = 7

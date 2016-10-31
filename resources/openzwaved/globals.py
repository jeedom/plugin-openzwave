import os

#Various message
MSG_CHECK_DEPENDENCY = 'The dependency of openzwave plugin are not installed. Please check the plugin openzwave configuration page for instructions'

#Init Daemon
_device = "auto"
# noinspection PyRedeclaration
_log_level = "error"
_port_server = 8083
_config_folder = None
_data_folder = None
_pidfile = '/tmp/openzwaved.pid'
_apikey = ''
_callback = ''
_assumeAwake = False
_suppress_refresh = False
_disabled_nodes = []
_cycle = 0.3

# default_poll_interval = 1800000  # 30 minutes
_default_poll_interval = 300000  # 5 minutes
_maximum_poll_intensity = 1
_controller_state = -1
# maximum time (in seconds) allowed for a background refresh
_refresh_timeout = 120
# background refresh interval step in seconds
_refresh_interval = 3
# post topology loaded delay tasks
_refresh_configuration_timer = 360.0
_refresh_user_values_timer = 120.0
_validate_association_groups_timer = 45.0
_recovering_failed_nodes_timer = 900.0  # 15 minutes
# perform sanitary jobs
_recovering_failed_nodes_jobs_timer = 900.0  # 15 minutes
_maximum_number_notifications = 25
_sanity_checks_delay = 15.0
_not_supported_nodes = [0, 255]
_user_values_to_refresh = ["Level", "Sensor", "Switch", "Power", "Temperature", "Alarm Type", "Alarm Type", "Power Management"]
_network = None
_network_information = None
_force_refresh_nodes = []
_changes_async = {'device': {}}
_ghost_node_id = None
_sanity_checks_running = False
_pending_configurations = {}
_pending_associations = {}
_node_notifications = {}
_dispatcher_is_connect = False
_network_is_running = False

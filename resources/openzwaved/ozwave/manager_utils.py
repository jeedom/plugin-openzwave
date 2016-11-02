import logging

import globals

from openzwave.option import ZWaveOption
from utilities.NetworkExtend import *
from utilities.NodeExtend import *
from utilities.Constants import *
from utilities.FilesManager import FilesManager

def init_manager():
	#Define some manager options
	globals.options = ZWaveOption(globals.device, config_path=globals.config_folder, user_path=globals.data_folder, cmd_line="")
	globals.options.set_log_file("../../../log/openzwaved")
	globals.options.set_append_log_file(False)
	globals.options.set_console_output(False)
	if globals.log_level == 'notice':
		globals.options.set_save_log_level('Warning')
	else:
		globals.options.set_save_log_level(globals.log_level[0].upper() + globals.log_level[1:])

	globals.options.set_logging(True)
	globals.options.set_associate(True)
	globals.options.set_save_configuration(True)
	globals.options.set_poll_interval(globals.default_poll_interval)
	globals.options.set_interval_between_polls(False)
	globals.options.set_notify_transactions(True)  # Notifications when transaction complete is reported.
	globals.options.set_suppress_value_refresh(False)  # if true, notifications for refreshed (but unchanged) values will not be sent.
	globals.options.set_driver_max_attempts(5)
	globals.options.addOptionBool("AssumeAwake", globals.assumeAwake)
	# options.addOptionInt("RetryTimeout", 6000)  # Timeout before retrying to send a message. Defaults to 40 Seconds
	globals.options.addOptionString("NetworkKey", "0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10", True)
	globals.options.set_security_strategy('SUPPORTED')  # The security strategy: SUPPORTED | ESSENTIAL | CUSTOM
	# options.set_custom_secured_cc('0x62,0x4c,0x63')  # What List of Custom CC should we always encrypt if SecurityStrategy is CUSTOM
	globals.options.addOptionBool('EnforceSecureReception', False)  # if we receive a clear text message for a CC that is Secured, should we drop the message
	globals.options.addOptionBool('RefreshAllUserCodes', False)  # Some Devices have a big UserCode Table, that can mean startup times when refreshing Session Variables is very long
	globals.options.addOptionInt('ThreadTerminateTimeout', 5000)  #
	globals.options.addOptionBool('EnableSIS', True)  # Automatically become a SUC if there is no SUC on the network
	globals.options.lock()

	globals.files_manager = FilesManager(globals.data_folder, globals.not_supported_nodes, logging)
	globals.files_manager.check_config_files()
import logging
import globals
from openzwave.option import ZWaveOption
from utilities.FilesManager import FilesManager

def init_manager():
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
	globals.options.set_notify_transactions(True)
	globals.options.set_suppress_value_refresh(False)
	globals.options.set_driver_max_attempts(5)
	globals.options.addOptionBool("AssumeAwake", globals.assumeAwake)
	globals.options.addOptionString("NetworkKey", "0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10", True)
	globals.options.set_security_strategy('SUPPORTED')
	globals.options.addOptionBool('EnforceSecureReception', False)
	globals.options.addOptionBool('RefreshAllUserCodes', False)
	globals.options.addOptionInt('ThreadTerminateTimeout', 5000)
	globals.options.addOptionBool('EnableSIS', True)
	globals.options.lock()
	globals.files_manager = FilesManager(globals.data_folder, globals.not_supported_nodes, logging)
	globals.files_manager.check_config_files()
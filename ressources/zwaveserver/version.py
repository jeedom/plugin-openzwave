import sys, os
import time

import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
from openzwave.group import ZWaveGroup
options = ZWaveOption(None)
options.set_append_log_file(False)
options.set_console_output(False)
options.set_logging(False)
options.set_associate(False)                       
options.set_save_configuration(False)               
options.set_interval_between_polls(False)         
options.set_notify_transactions(True) # Notifications when transaction complete is reported.           
options.set_suppress_value_refresh(False) # if true, notifications for refreshed (but unchanged) values will not be sent.        
options.set_driver_max_attempts(5) 
options.addOptionBool("AssumeAwake", False)        
#options.addOptionInt("RetryTimeout", 6000) # Timeout before retrying to send a message. Defaults to 40 Seconds
options.addOptionString("NetworkKey","0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10",True)
options.set_security_strategy('CUSTOM') # The security strategy : SUPPORTED | ESSENTIAL | CUSTOM
options.set_custom_secured_cc('0x62,0x4c,0x63') # What List of Custom CC should we always encrypt if SecurityStrategy is CUSTOM
options.addOptionBool('EnforceSecureReception', False) # if we recieve a clear text message for a CC that is Secured, should we drop the message
options.lock()
network = ZWaveNetwork(options, autostart=False)
print network.manager.getOzwLibraryVersionNumber()
print '|'
print network.manager.getPythonLibraryVersionNumber() 
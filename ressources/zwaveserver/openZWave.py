#!flask/bin/python
'''
Copyright (c) 2014 
author : Thomas Martinez tmartinez69009@gmail.com
author : Jean-Francois Auger jeanfrancois.auger@gmail.com
SOFTWARE NOTICE AND LICENSE This file is part of Plugin openzwave for jeedom project
Plugin openzwave for jeedom is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
Plugin openzwave for jeedom is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with Plugin openzwave for jeedom. If not, see http://www.gnu.org/licenses.
''' 
import sys, os
import time

log = 'Debug'

def add_log_entry(message, level="info"):
    if log == 'Error' and  level != 'error' :
        return
    if log == 'Info' and  level != 'debug' :
        return
    print('%s | %s | %s' % (time.strftime('%d-%m-%Y %H:%M:%S',time.localtime()), level, message.encode('utf8'),)) 

add_log_entry("Check flask dependances")
try:
    from flask import Flask, jsonify, abort, request, make_response, redirect, url_for
    add_log_entry("--> pass")
except Exception as e:
    add_log_entry("The dependances of openzwave plugin are not installed. Please, check the plugin openzwave configuration page for instructions",'error')
    add_log_entry("Error : %s" % str(e),'error')
    sys.exit(1)

add_log_entry("Check other dependances")
try:
    import logging
    import os.path
    import shutil
    import platform
    import datetime
    import binascii
    import threading
    from threading import Event, Thread
    import socket
    from lxml import etree
    import signal
    import requests
    from louie import dispatcher, All
    add_log_entry("--> pass")
except Exception as e:
    add_log_entry("The dependances of openzwave plugin are not installed. Please, check the plugin openzwave configuration page for instructions",'error')
    add_log_entry("Error : %s" % str(e),'error')
    sys.exit(1)

if not os.path.exists('/tmp/python-openzwave-eggs'):
    os.makedirs('/tmp/python-openzwave-eggs')
    
os.environ['PYTHON_EGG_CACHE'] = '/tmp/python-openzwave-eggs'

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger('openzwave')

reload(sys)  
sys.setdefaultencoding('utf8')

add_log_entry("Check Openzwave")
import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
from openzwave.group import ZWaveGroup
add_log_entry("--> pass")

    
device="auto"
log="None"
#default_poll_interval = 1800000 # 30 minutes
default_poll_interval = 300000 # 5 minutes
maximum_poll_intensity = 1
controller_state = -1

# maximum time (in secondes) allowed for a background refresh
refresh_timeout = 120
# background refresh interval step in secondes
refresh_interval = 3
#post topology loaded delais tasks
refresh_configuration_timer = 360.0    
refresh_user_values_timer = 120.0
validate_association_groups_timmer = 45.0   
recovering_failed_nodes_timer = 900.0 # 15min 
#perform sanitary jobs
recovering_failed_nodes_jobs_timer = 900.0 #15 minutes

network = None
networkInformations = None

COMMAND_CLASS_NO_OPERATION              = 0 # 0x00
COMMAND_CLASS_BASIC                     = 32 # 0x20 
COMMAND_CLASS_CONTROLLER_REPLICATION    = 33 # 0x21
COMMAND_CLASS_APPLICATION_STATUS        = 34 # 0x22
#COMMAND_CLASS_ZIP_SERVICES              = 35 # 0x23
#COMMAND_CLASS_ZIP_SERVER                = 36 # 0x24
COMMAND_CLASS_SWITCH_BINARY             = 37 # 0x25
COMMAND_CLASS_SWITCH_MULTILEVEL         = 38 # 0x26
COMMAND_CLASS_SWITCH_ALL                = 39 # 0x27
COMMAND_CLASS_SWITCH_TOGGLE_BINARY      = 40 # 0x28
COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL  = 41 # 0x29
#COMMAND_CLASS_CHIMNEY_FAN               = 42 # 0x2A
COMMAND_CLASS_SCENE_ACTIVATION          = 43 # 0x2B
#COMMAND_CLASS_SCENE_ACTUATOR_CONF       = 44 # 0x2C
#COMMAND_CLASS_SCENE_CONTROLLER_CONF     = 45 # 0x2D
#COMMAND_CLASS_ZIP_CLIENT                = 46 # 0x2E
#COMMAND_CLASS_ZIP_ADV_SERVICES          = 47 # 0x2F
COMMAND_CLASS_SENSOR_BINARY             = 48 # 0x30
COMMAND_CLASS_SENSOR_MULTILEVEL         = 49 # 0x31
COMMAND_CLASS_METER                     = 50 # 0x32    
COMMAND_CLASS_COLOR                     = 51 # 0x33
#COMMAND_CLASS_ZIP_ADV_CLIENT            = 52 # 0x34
COMMAND_CLASS_METER_PULSE               = 53 # 0x35
#COMMAND_CLASS_THERMOSTAT_HEATING        = 56 # 0x38
#COMMAND_CLASS_METER_TBL_CONFIG          = 60 # 0x3C
#COMMAND_CLASS_METER_TBL_MONITOR         = 61 # 0x3D
#COMMAND_CLASS_METER_TBL_PUSH            = 62 # 0x3E
COMMAND_CLASS_THERMOSTAT_MODE           = 64 # 0x40
COMMAND_CLASS_THERMOSTAT_OPERATING_STATE = 66 # 0x42
COMMAND_CLASS_THERMOSTAT_SETPOINT       = 67 # 0x43
COMMAND_CLASS_THERMOSTAT_FAN_MODE       = 68 # 0x44
COMMAND_CLASS_THERMOSTAT_FAN_STATE      = 69 # 0x45
COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE  = 70 # 0x46
#COMMAND_CLASS_THERMOSTAT_SETBACK        = 71 # 0x47
COMMAND_CLASS_DOOR_LOCK_LOGGING         = 76 # 0x4C
#COMMAND_CLASS_SCHEDULE_ENTRY_LOCK       = 78 # 0x4E
COMMAND_CLASS_BASIC_WINDOW_COVERING     = 80 # 0x50
#COMMAND_CLASS_MTP_WINDOW_COVERING       = 81 # 0x51
COMMAND_CLASS_CRC_16_ENCAP              = 86 # 0x56
COMMAND_CLASS_DEVICE_RESET_LOCALLY      = 90 # 0x5A
COMMAND_CLASS_CENTAL_SCENE              = 91 # 0x5B
COMMAND_CLASS_ZWAVE_PLUS_INFO           = 94 # 0x5E
COMMAND_CLASS_MULTI_INSTANCE            = 96 # 0x60
COMMAND_CLASS_DOOR_LOCK                 = 98 # 0x62
COMMAND_CLASS_USER_CODE                 = 99 # 0x63
#COMMAND_CLASS_BARRIER_OPERATOR          = 102 # 0x66
COMMAND_CLASS_CONFIGURATION             = 112 # 0x70
COMMAND_CLASS_ALARM                     = 113 # 0x71
COMMAND_CLASS_MANUFACTURER_SPECIFIC     = 114 # 0x72    
COMMAND_CLASS_POWERLEVEL                = 115 # 0x73
COMMAND_CLASS_PROTECTION                = 117 # 0x75
COMMAND_CLASS_LOCK                      = 118 # 0x76
COMMAND_CLASS_NODE_NAMING               = 119 # 0x77
#COMMAND_CLASS_FIRMWARE_UPDATE_MD        = 122 # 0x7A
#COMMAND_CLASS_GROUPING_NAME             = 123 # 0x7B
#COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE =124 # 0x7C
#COMMAND_CLASS_REMOTE_ASSOCIATION        = 125 # 0x7D
COMMAND_CLASS_BATTERY                   = 128 #0x80
COMMAND_CLASS_CLOCK                     = 129 #0x81
COMMAND_CLASS_HAIL                      = 130 #0x82
COMMAND_CLASS_WAKE_UP                   = 132 #0x84
COMMAND_CLASS_ASSOCIATION               = 133 #0x85
COMMAND_CLASS_VERSION                   = 134 #0x86
COMMAND_CLASS_INDICATOR                 = 135 #0x87
COMMAND_CLASS_PROPRIETARY               = 136 #0x88
COMMAND_CLASS_LANGUAGE                  = 137 #0x89
#COMMAND_CLASS_TIME                      = 138 #0x8A
COMMAND_CLASS_TIME_PARAMETERS           = 139 # 0x8B
#COMMAND_CLASS_GEOGRAPHIC_LOCATION       = 150 #0x8C
#COMMAND_CLASS_COMPOSITE                 = 141 # 0x8D
COMMAND_CLASS_MULTI_INSTANCE_ASSOCIATION = 142 #0x8E
COMMAND_CLASS_MULTI_CMD                 = 143 # 0x8F
COMMAND_CLASS_ENERGY_PRODUCTION         = 144 # 0x90
#COMMAND_CLASS_MANUFACTURER_PROPRIETARY  = 145 # 0x91
#COMMAND_CLASS_SCREEN_MD                 = 146 #0x92
#COMMAND_CLASS_SCREEN_ATTRIBUTES         = 147 # 0x93
#COMMAND_CLASS_SIMPLE_AV_CONTROL         = 148 # 0x94
#COMMAND_CLASS_AV_CONTENT_DIRECTORY_MD   = 149 # 0x95
#COMMAND_CLASS_AV_RENDERER_STATUS        = 150 # 0x96
#COMMAND_CLASS_AV_CONTENT_SEARCH_MD      = 151 # 0x97
COMMAND_CLASS_SECURITY                  = 152 # 0x98
#COMMAND_CLASS_AV_TAGGING_MD             = 153 # 0x99
#COMMAND_CLASS_IP_CONFIGURATION          = 154 # 0x9A
COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION = 155 # 0x9B
COMMAND_CLASS_SENSOR_ALARM              = 156 # 0x9C
#COMMAND_CLASS_SILENCE_ALARM             = 157 # 0x9D
#COMMAND_CLASS_SENSOR_CONFIGURATION      = 158 #0x9E
#COMMAND_CLASS_MARK                      = 239 # 0xEF
#COMMAND_CLASS_NON_INTEROPERABLE         = 240 # 0xF0

add_log_entry("validate startup arguments") 
for arg in sys.argv:
    if arg.startswith("--device="):
        temp,device = arg.split("=")        
    elif arg.startswith("--port="):
        temp,port_server = arg.split("=")
    elif arg.startswith("--log="):
        temp,log = arg.split("=")
    elif arg.startswith("--config_folder="):
        temp,config_folder = arg.split("=")
    elif arg.startswith("--data_folder="):
        temp,data_folder = arg.split("=")
    elif arg.startswith("--pidfile"):
        temp,pidfile = arg.split("=")
    elif arg.startswith("--callback="):
        temp,callback = arg.split("=")
    elif arg.startswith("--apikey="):
        temp,apikey = arg.split("=")
    elif arg.startswith("--serverId="):
        temp,serverId = arg.split("=")
    elif arg.startswith("--help"):
        print("help : ")
        print("  --device=/dev/yourdevice ")
        print("  --log=Info|Debug")
add_log_entry("--> pass")  

def find_tty_usb(idVendor, idProduct):
    '''find_tty_usb('0658', '0200') -> '/dev/ttyUSB021' for Sigma Designs, Inc.'''    
    # Note: if searching for a lot of pairs, it would be much faster to search
    # for the enitre lot at once instead of going over all the usb devices
    # each time.
    debug_print('check for idVendor:%s idProduct: %s' %(idVendor, idProduct,))
    for dnbase in os.listdir('/sys/bus/usb/devices'):
        dn = str.join('/sys/bus/usb/devices', dnbase)
        #debug_print(dn)
        if not os.path.exists(str.join(dn, 'idVendor')):
            continue
        idv = open(str.join(dn, 'idVendor')).read().strip()
        #debug_print(idv)
        if idv != idVendor:
            continue
        idp = open(str.join(dn, 'idProduct')).read().strip()
        #debug_print(idp)
        if idp != idProduct:
            continue
        for subdir in os.listdir(dn):
            if subdir.startswith(dnbase+':'):
                for subsubdir in os.listdir(str.join(dn, subdir)):
                    if subsubdir.startswith('ttyUSB'):
                        return str.join('/dev', subsubdir)
    return None
    
def debug_print(message):
    add_log_entry(message, 'debug')

add_log_entry("check if port is available")     
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1',int(port_server)))
if result == 0:
    add_log_entry('The port %s is already in use. Please check your openzwave configuration plugin page' % (port_server,), 'error')
    sys.exit(1) 
add_log_entry("--> pass")   

#device = 'auto'
if device == 'auto':
    know_sticks = [{'idVendor':'0658', 'idProduct':'0200', 'name':'Sigma Designs, Inc'},
                   {'idVendor':'10c4', 'idProduct':'ea60', 'name':'Cygnal Integrated Products, Inc. CP210x UART Bridge'}]
    
    for stick in know_sticks:
        device = find_tty_usb(stick['idVendor'], stick['idProduct'])
        if device != None:
            add_log_entry('USB Z-Wave Stick found :%s' %(stick['name'],))
            break
    if device == None:        
        add_log_entry('No USB Z-Wave Stick detected', 'error')
        sys.exit(1)

Idle= 0
AddDevice = 1
RemoveDevice = 5

not_supported_nodes = [0,255]

user_values_to_refresh = ["Level","Sensor","Switch", "Power", "Temperature", "Alarm Type" ,"Alarm Type", "Power Management"]

class ControllerMode:
    class Idle: pass
    class AddDevice: pass
    class RemoveDevice: pass

  
class NetworkInformations(object):
    '''
    STATE_NORMAL = 'Normal'
    STATE_STARTING = 'Starting'
    STATE_CANCEL = 'Cancel'
    STATE_ERROR = 'Error'
    STATE_WAITING = 'Waiting'
    STATE_SLEEPING = 'Sleeping'
    STATE_INPROGRESS = 'InProgress'
    STATE_COMPLETED = 'Completed'
    STATE_FAILED = 'Failed'
    STATE_NODEOK = 'NodeOK'
    STATE_NODEFAILED = 'NodeFailed'
    '''
    def __init__(self):
        self.reset()
    
    @property
    def actualMode(self):        
        return self._actualMode
    
    @actualMode.setter
    def actualMode(self, value):        
        self._actualMode = value
        
    @property
    def startTime(self):        
        return self._startTime
    
    @startTime.setter
    def startTime(self, value):        
        self._startTime = value
        
    @property
    def configFileSaveInProgress(self):        
        return self._configFileSaveInProgress
    
    @configFileSaveInProgress.setter
    def configFileSaveInProgress(self, value):        
        self._configFileSaveInProgress = value
        
    @property
    def controllerIsBusy(self):        
        return self._controllerIsBusy
    
    @controllerIsBusy.setter
    def controllerIsBusy(self, value):        
        self._controllerIsBusy = value
        
    @property
    def controllerState(self):        
        return self._controllerState
    
    @property
    def lastControllerNotification(self):        
        return self._lastControllerNotification
    
    @property
    def error(self):        
        return self._error
    
    @property
    def error_description(self):        
        return self._error_description
    
    def awaked(self):
        self._awakeTime = int(time.time())
        self.assignControllerNotification(ZWaveController.SIGNAL_CTRL_NORMAL, "Network is awaked")
        
    @property
    def controllerAwakedDelay(self):   
        if self._awakeTime is not None:
            return self._awakeTime - self._startTime   
        return None
    
    def assignControllerNotification(self, state, details, error=None, error_description=None):
        self._controllerState = state
        self._lastControllerNotification['state'] = state
        self._lastControllerNotification['details'] = details
        if error == 'None':
            self._lastControllerNotification['error'] = None
            self._lastControllerNotification['error_description'] = None
        else:
            self._lastControllerNotification['error'] = error
            self._lastControllerNotification['error_description'] = error_description
        self._lastControllerNotification['timestamp'] = int(time.time())
        self._error = error
        self._error_description = error_description
        
        if state == ZWaveController.STATE_WAITING:
            self.controllerIsBusy = True
        elif state == ZWaveController.STATE_INPROGRESS:
            self.controllerIsBusy = True
        elif state == ZWaveController.STATE_STARTING:
            self.controllerIsBusy = True 
        else:
            self.controllerIsBusy = False
            #reset flag
            self.actualMode = ControllerMode.Idle
            
    def computeJeeDomMessage(self):
        if self.actualMode == ControllerMode.AddDevice:
            return AddDevice         
        elif self.actualMode == ControllerMode.RemoveDevice:
            return RemoveDevice
        else:
            return Idle

    def reset(self):
        self._actualMode = ControllerMode.Idle
        self._startTime=int(time.time())
        self._awakeTime = None
        self._configFileSaveInProgress = False
        self._controllerIsBusy = False;
        self._controllerState = ZWaveController.STATE_STARTING
        self._lastControllerNotification = {"state": self._controllerState, "details": '', "error": None, "error_description": None, "timestamp" :int(time.time())}         
        self._error = None
        self._error_description = None

class PendingConfiguration(object):
    
    def __init__(self, expectedData, timeOut):
        self._startTime=int(time.time())
        self._expectedData = expectedData
        self._timeOut = timeOut;    
        self._data = None 
        
    @property
    def data(self):        
        return self._data
    
    @data.setter
    def data(self, value):        
        self._data = value
        
    @property
    def state(self):  
        if (self._data == None):
            # is pending
            return 3
        if (self._data != self._expectedData)  :
            # the node reject changes and set a default
            return 2
        # the parameter have be set succesfully
        return 1

            
class NodeNotification(object):
    
    def __init__(self, code, wakeup_time=None):
        self._code = code 
        self._description = code 
        self._help = code 
        self._wakeup_time = wakeup_time 
        self._next_wakeup = None       
        self.refresh(code, wakeup_time)
        
    def refresh(self, code, wakeup_time):
        # reset time stamp
        self._receive_time=int(time.time())
        if code == 0:
            self._description = "Completed"
            self._help = "Completed messages"
        elif code == 1:
            self._description = "Timeout"
            self._help = "Messages that timeout will send a Notification with this code"
        elif code == 2:
            self._description = "NoOperation"
            self._help = "Report on NoOperation message sent completion"
        elif code == 3:
            self._description = "Awake."
            self._help = "Report when a sleeping node wakes"
            self._next_wakeup = None #clear and wait sleep to calcul next expected wakeup
        elif code == 4:
            self._description = "Sleep."
            self._help = "Report when a node goes to sleep"
            #if they go to sleep, calcul the next expected wakeup time
            if wakeup_time != None and wakeup_time > 0:
                self._next_wakeup = self._receive_time + wakeup_time
        elif code == 5:
            self._description = "Dead."
            self._help = "Report when a node is presumed dead"
        elif code == 6:
            self._description = "Alive."
            self._help = "Report when a node is revived"
        else:
            self._description = "Unknown state"
            self._help = ""
            
    @property
    def code(self):        
        return self._code
    
    @property
    def receive_time(self):        
        return self._receive_time
    
    @property
    def description(self):        
        return self._description
    
    @property
    def help(self):        
        return self._help
    
    @property
    def next_wakeup(self):        
        return self._next_wakeup
        

def start_network():
    global networkInformations
    # reset flags
    force_refresh_nodes = []
    if networkInformations is None:
        networkInformations = NetworkInformations()
    else:
        networkInformations.reset()
    add_log_entry('******** The ZWave network is being started ********')
    network.start()
    
def cleanup_confing_file(fileName):
    global data_folder
    add_log_entry('validate configuration file: %s' %(fileName,)) 
    if os.path.isfile(fileName) :
        try:            
            tree = etree.parse(fileName)
            nodes = tree.findall(".//{http://code.google.com/p/open-zwave/}Product")
            for node in nodes:
                if node.get("id")[:7] in not_supported_nodes :
                    tree.getroot().remove(node.getparent().getparent())
                elif node.get("name")[:7]=="Unknown" :
                    tree.getroot().remove(node.getparent().getparent())
            FILE = open(fileName,"w")
            FILE.write('<?xml version="1.0" encoding="utf-8" ?>\n')
            FILE.writelines(etree.tostring(tree, pretty_print=True))
            FILE.close()          
        except Exception as e:
            add_log_entry(str(e), 'error')
            add_log_entry('Trying to find the most recent valid xml in backups')
            backupFolder = data_folder+"/xml_backups"
            try:
                os.stat(backupFolder)
            except:
                os.mkdir(backupFolder)
            pattern = "_zwcfg_"
            alist_filter = ['xml'] 
            path=os.path.join(backupFolder,"")
            actualBackups = os.listdir(backupFolder)
            actualBackups.sort(reverse=True)
            foundValidBackup=0
            for candidateBackup in actualBackups:
                if candidateBackup[-3:] in alist_filter and pattern in candidateBackup:
                    try:            
                        tree = etree.parse(os.path.join(backupFolder,candidateBackup))
                        finalFilename=candidateBackup[candidateBackup.find('zwcfg'):]
                        shutil.copy2(os.path.join(backupFolder,candidateBackup), os.path.join(data_folder,finalFilename))
                        os.chmod(finalFilename, 0777)
                        add_log_entry('Found one valid backup. Using it')
                        foundValidBackup=1
                        break
                    except Exception as e:
                        add_log_entry(str(e), 'error')
                        continue
            if foundValidBackup==0:
                add_log_entry('No valid backup found. Regenerating')
                     
def check_config_files():
    global data_folder
    root = data_folder
    pattern = "zwcfg_"
    alist_filter = ['xml'] 
    path=os.path.join(root,"")
    actualConfs = os.listdir(root)
    for file in actualConfs:
        if file[-3:] in alist_filter and pattern in file:
            cleanup_confing_file(os.path.join(root,file))

def backup_xml_config(mode,homeId):
    global data_folder
    #backup xml config file
    add_log_entry('Backuping xml config file with mode : %s' % (mode))
    #prepare all variables
    dateTimestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
    xmlToBackup = data_folder+"/zwcfg_" + homeId +".xml"
    if not os.path.isfile(xmlToBackup) :
        add_log_entry('No config file found to backup', "error")
        return format_json_result(False,'No config file found to backup')
    backupFolder = data_folder+"/xml_backups"
    backupName = dateTimestamp+"_"+mode+"_zwcfg_"+homeId+".xml"
    #check if folder exist (more efficient way)
    try:
        os.stat(backupFolder)
    except:
        os.mkdir(backupFolder)
    #check if we need to clean the folder
    actualBackups = os.listdir(backupFolder)
    actualBackups.sort()
    for backup in actualBackups:
        if 'manual' in backup:
            actualBackups.remove(backup)
    if len(actualBackups) > 12 :
        add_log_entry('More than 12 autobackups found. Cleaning the folder')
        for fileToDelete in actualBackups[:-11]:
            os.unlink(os.path.join(backupFolder,fileToDelete))
    #make the backup
    try:
        finalPath = os.path.join(backupFolder,backupName)
        tree = etree.parse(xmlToBackup)
        shutil.copy2(xmlToBackup, finalPath)
    except Exception as error:
        add_log_entry('Backuping xml failed %s' % (str(error),), "error")
        return format_json_result(False,'Backuping xml failed')
    add_log_entry('Xml config file succesfully backuped')
    return format_json_result(True,'Xml config file succesfully backuped')
                
def graceful_stop_network():
    add_log_entry('Graceful stopping the ZWave network.')   
    global network
    homeId=network.home_id_str
    if network is not None:
        network.stop()
        #We disconnect to the louie dispatcher
        try:
            dispatcher.disconnect(network_started, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
            dispatcher.disconnect(network_failed, ZWaveNetwork.SIGNAL_NETWORK_FAILED)
            dispatcher.disconnect(network_failed, ZWaveNetwork.SIGNAL_DRIVER_FAILED)
            dispatcher.disconnect(network_awaked, ZWaveNetwork.SIGNAL_NETWORK_AWAKED)
            dispatcher.disconnect(network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)
            dispatcher.disconnect(node_new, ZWaveNetwork.SIGNAL_NODE_NEW)
            dispatcher.disconnect(node_added, ZWaveNetwork.SIGNAL_NODE_ADDED)
            dispatcher.disconnect(node_removed, ZWaveNetwork.SIGNAL_NODE_REMOVED)
            dispatcher.disconnect(value_added, ZWaveNetwork.SIGNAL_VALUE_ADDED)
            dispatcher.disconnect(value_update, ZWaveNetwork.SIGNAL_VALUE_CHANGED)
            dispatcher.disconnect(value_refreshed, ZWaveNetwork.SIGNAL_VALUE_REFRESHED)
            dispatcher.disconnect(node_event, ZWaveNetwork.SIGNAL_NODE_EVENT)
            dispatcher.disconnect(scene_event, ZWaveNetwork.SIGNAL_SCENE_EVENT)
            dispatcher.disconnect(essential_node_queries_complete, ZWaveNetwork.SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE)
            dispatcher.disconnect(node_queries_complete, ZWaveNetwork.SIGNAL_NODE_QUERIES_COMPLETE)
            dispatcher.disconnect(nodes_queried, ZWaveNetwork.SIGNAL_AWAKE_NODES_QUERIED)
            dispatcher.disconnect(nodes_queried, ZWaveNetwork.SIGNAL_ALL_NODES_QUERIED)
            dispatcher.disconnect(nodes_queried_some_dead, ZWaveNetwork.SIGNAL_ALL_NODES_QUERIED_SOME_DEAD)
            dispatcher.disconnect(button_on, ZWaveNetwork.SIGNAL_BUTTON_ON)
            dispatcher.disconnect(button_off, ZWaveNetwork.SIGNAL_BUTTON_OFF)
            dispatcher.disconnect(node_notification, ZWaveNetwork.SIGNAL_NOTIFICATION) 
            dispatcher.disconnect(node_group_changed, ZWaveNetwork.SIGNAL_GROUP)
            dispatcher.disconnect(controller_waiting, ZWaveNetwork.SIGNAL_CONTROLLER_WAITING)
            dispatcher.disconnect(controller_command, ZWaveNetwork.SIGNAL_CONTROLLER_COMMAND)
            dispatcher.disconnect(controller_message_complete, ZWaveNetwork.SIGNAL_MSG_COMPLETE)
        except Exception:
            pass
        network.destroy()
        #avoid a second pass
        network = None
    add_log_entry('The Openzwave REST-server was stopped in a normal way')
    backup_xml_config('stop',homeId)

#Define some manager options
options = ZWaveOption(device, config_path=config_folder, user_path=data_folder, cmd_line="")
options.set_log_file("openzwave.log")
options.set_append_log_file(False)
options.set_console_output(False)
options.set_save_log_level(log)
options.set_logging(True)
options.set_associate(True)                       
options.set_save_configuration(True)              
options.set_poll_interval(default_poll_interval)    
options.set_interval_between_polls(False)         
options.set_notify_transactions(True) # Notifications when transaction complete is reported.           
options.set_suppress_value_refresh(False) # if true, notifications for refreshed (but unchanged) values will not be sent.        
options.set_driver_max_attempts(5) 
options.addOptionBool("AssumeAwake", True)        
#options.addOptionInt("RetryTimeout", 6000) # Timeout before retrying to send a message. Defaults to 40 Seconds
options.addOptionString("NetworkKey","0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10",True)
options.set_security_strategy('CUSTOM') # The security strategy : SUPPORTED | ESSENTIAL | CUSTOM
options.set_custom_secured_cc('0x62,0x4c,0x63') # What List of Custom CC should we always encrypt if SecurityStrategy is CUSTOM
options.addOptionBool('EnforceSecureReception', False) # if we recieve a clear text message for a CC that is Secured, should we drop the message
options.lock()

force_refresh_nodes = []    

check_config_files()

changes_async = {}
changes_async['device']={}
cycle = 0.5

def send_changes_async():
    global changes_async
    global serverId
    try:
        start_time = datetime.datetime.now()
        changes = changes_async
        changes_async = {}
        if changes.has_key('device') or changes.has_key('controller') :
            changes['serverId'] = serverId
            debug_print('Send data async to jeedom %s => %s' % (callback+'?apikey='+apikey,str(changes),))
            try:
                r = requests.post(callback+'?apikey='+apikey, json=changes,timeout=(0.5,120),verify=False)
                if r.status_code != requests.codes.ok :
                    add_log_entry('Error on send request to jeedom, return code %s' % (str(r.status_code),), "error")
            except Exception as error:
                add_log_entry('Error on send request to jeedom %s' % (str(error),), "error")
        dt = datetime.datetime.now() - start_time
        ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
        timer_duration = cycle - ms
        if(timer_duration < 0.1):
            timer_duration = 0.1
        resend_changes = threading.Timer(timer_duration, send_changes_async)
        resend_changes.start() 
    except Exception as error:
        add_log_entry('Critical error on  send_changes_async %s' % (str(error),), "error")
        resend_changes = threading.Timer(cycle, send_changes_async)
        resend_changes.start() 

send_changes_async()

def save_node_value_event(node_id, timestamp, command_class, index, typeStandard, value, instance):
    global changes_async
    if not changes_async.has_key('device') :
        changes_async['device']={}
    if not changes_async['device'].has_key(node_id) :
        changes_async['device'][node_id]={}
    changes_async['device'][node_id][str(hex(command_class))+str(instance)+str(index)] = {'node_id':node_id,'instance':instance, 'CommandClass':hex(command_class), 'index':index,'value':value,'type':typeStandard,'updateTime' : timestamp}

def save_node_event(node_id, timestamp, value):
    global controller_state
    global changes_async
    if value=="removed":
        if not changes_async.has_key('controller') :
            changes_async['controller']={}
        changes_async['controller']['excluded'] = {"value":node_id}
    elif value=="added":
        if not changes_async.has_key('controller') :
            changes_async['controller']={}
        changes_async['controller']['included'] = {"value":node_id}
    elif value in [0,1,5] and controller_state != value :
        if not changes_async.has_key('controller') :
            changes_async['controller']={}
        controller_state = value
        changes_async['controller']['state'] = {"value":value}
    return

def network_started(network):
    add_log_entry("Openzwave network are started with homeId %0.8x." % (network.home_id,))    
    networkInformations.assignControllerNotification(ZWaveController.SIGNAL_CTRL_STARTING, "Network is started")
    if network.manager.getPollInterval() != default_poll_interval:
        network.set_poll_interval(default_poll_interval, False)

def network_failed(network):
    add_log_entry("Openzwave network can't load", "error")
    networkInformations.assignControllerNotification(ZWaveController.SIGNAL_CTRL_ERROR, "Network have failed")

def validate_association_groups_asynchronous():
    debug_print("Check association")
    for node_id in list(network.nodes):
        if validate_association_groups(node_id):
            #avoid stress network
            time.sleep(3)

def recovering_failed_nodes_asynchronous():
    debug_print("Start recovering_failed_nodes background thread")
    #wait 15 seconds on first launch
    time.sleep(15.0)    
    while True: 
        #if controler is busy skip this run
        if can_execute_network_command(0):      
            debug_print("Perform network sanity check")  
            for node_id in list(network.nodes):
                myNode = network.nodes[node_id]
                if node_id in not_supported_nodes :   
                    debug_print('Remove fake nodeId: %s' % (node_id)) 
                    network.manager.removeFailedNode(network.home_id, node_id)
                    continue
                if myNode.is_failed:
                    debug_print('Try recovering nodeId: %s' % (node_id)) 
                    if network.manager.hasNodeFailed(network.home_id, node_id):
                        #avoid stress network
                        time.sleep(3)
                if myNode.is_listening_device and myNode.is_awake:
                    #check if a ping is require 
                    if hasattr(myNode, 'last_notification') :
                        #is in timeout or dead
                        if myNode.last_notification.code == 1 or myNode.last_notification.code == 5:
                            debug_print('Do a test on node %s' % (node_id,)) 
                            # a ping will try to resolve this situation with a NoOperation CC. 
                            network.manager.testNetworkNode(network.home_id, node_id, 1) 
                            #avoid stress network
                            time.sleep(3)  
        else:
            debug_print("Network is loaded, skip sanity check this time")
        # wait for next run    
        time.sleep(recovering_failed_nodes_timer)
    
def refresh_configuration_asynchronous():
    if can_execute_network_command(0):
        for node_id in list(force_refresh_nodes):
            if node_id in network.nodes and not network.nodes[node_id].is_failed :
                debug_print('Request All Configuration Parameters for nodeId: %s' % (node_id,)) 
                network._manager.requestAllConfigParams(network.home_id, node_id)
                time.sleep(3)
    else:
        #I will try again in 2 minutes
        retry_job = threading.Timer(240.0, refresh_configuration_asynchronous)
        retry_job.start()        
    
def refresh_user_values_asynchronous():
    debug_print("Refresh User Values of powered devices")
    if can_execute_network_command(0):
        for node_id in list(network.nodes):
            myNode = network.nodes[node_id]
            if myNode.is_ready and myNode.is_listening_device and not myNode.is_failed:
                debug_print('Refresh User Values for nodeId: %s' % (node_id,))
                for val in myNode.get_values():
                    currentValue = myNode.values[val]
                    if currentValue.genre == 'User':
                        if currentValue.type == 'Button':
                            continue
                        if currentValue.is_write_only:
                            continue   
                        if currentValue.label in user_values_to_refresh :
                            currentValue.refresh()
                while not can_execute_network_command(0):
                    debug_print("Network Waiting execution of all messages in the waiting")
                    time.sleep(10) 
    else:
        debug_print("Network is loaded, do not execute this time")
        #I will try again in 2 minutes
        retry_job = threading.Timer(240.0, refresh_user_values_asynchronous)
        retry_job.start()           
            
def network_awaked(network):
    add_log_entry("Openzwave network is awake : %d nodes were found (%d are sleeping). All listening nodes are queried, but some sleeping nodes may be missing." % (network.nodes_count, get_sleeping_nodes_count(),))
    add_log_entry("Controller is : %s" % (network.controller,))
    networkInformations.awaked()
    configuration = threading.Timer(refresh_configuration_timer, refresh_configuration_asynchronous)
    configuration.start() 
    debug_print("refresh_configuration starting in %d sec" %(refresh_configuration_timer,))    
    user_values = threading.Timer(refresh_user_values_timer, refresh_user_values_asynchronous)
    user_values.start() 
    debug_print("refresh_user_values starting in %d sec" %(refresh_user_values_timer,))    
    association = threading.Timer(validate_association_groups_timmer, validate_association_groups_asynchronous)
    association.start()
    debug_print("validate_association_groups starting in %d sec" %(validate_association_groups_timmer,)) 
    threading.Thread(target=recovering_failed_nodes_asynchronous).start()
    #start listening for group changes
    dispatcher.connect(node_group_changed, ZWaveNetwork.SIGNAL_GROUP)    
        
def network_ready(network):
    add_log_entry("Openzwave network is ready with %d nodes (%d are sleeping). All nodes are queried, the network is fully functional." % (network.nodes_count, get_sleeping_nodes_count(),))   
    write_config()
    networkInformations.assignControllerNotification(ZWaveController.SIGNAL_CTRL_NORMAL, "Network is ready")

def button_on(network, node):
    add_log_entry('Controller button on pressed event') 
    
def button_off(network, node):
    add_log_entry('Controller button off pressed event') 

def nodes_queried(network):    
    write_config() 
    
def nodes_queried_some_dead(network):
    write_config()  
    add_log_entry("All nodes have been queried, but some node ar mark dead") 

def node_new(network, node_id):
    if node_id in not_supported_nodes:
        return
    add_log_entry('A new node (%s), not already stored in zwcfg*.xml file, was found.' % (node_id,))
    force_refresh_nodes.append(node_id)    
    
def node_added(network, node):    
    add_log_entry('A node has been added to OpenZWave list id:[%s] model:[%s].' % (node.node_id, node.product_name,))
    if node.node_id in not_supported_nodes:
        debug_print('remove fake nodeId: %s' % (node.node_id)) 
        node_cleaner = threading.Timer(60.0, network.manager.removeFailedNode, [network.home_id, node.node_id])
        node_cleaner.start()        
        return
    node.last_update=time.time()   
    if network.state >= 7: #STATE_AWAKED
        save_node_event(node.node_id, int(time.time()), "added") 
            
def node_removed(network, node):
    add_log_entry('A node has been removed from OpenZWave list id:[%s] model:[%s].' % (node.node_id, node.product_name,))
    if node.node_id in not_supported_nodes:
        return
    if network.state >= 7: #STATE_AWAKED
        save_node_event(node.node_id, int(time.time()), "removed")
    
def get_standard_value_type(valueType):
    if valueType == "Int" :
        return 'int'
    elif valueType == "Decimal" :
        return 'float'
    elif valueType == "Bool" :
        return 'bool'
    elif valueType == "Byte" :
        return 'int'
    elif valueType == "Short" :
        return 'int'
    elif valueType == "Button" :
        return 'bool'
    elif valueType == "Raw" :
        return 'binary'
    else :
        return valueType

def change_instance(myValue):
    if myValue.instance > 1:
        return myValue.instance - 1
    return 0

def normalize_short_value(value):
    result=value
    try:
        if int(value)<0:
            result = 65536 + int(value)
    except:
        pass
    return result
   
def extract_data(value, displayRaw = False):
    if value.type == "Bool":
        return value.data    
    elif value.label == 'Temperature' and value.units == 'F':
        return int(((float(value.data_as_string) - 32) * 5.0 / 9.0) * 100) / 100.0
    elif value.type == "Raw":
        result = binascii.b2a_hex(value.data)
        if displayRaw :
            add_log_entry('Raw Signal : %s' % result)
        return result
    if value.type == "Decimal":
        precision = value.precision
        if precision == None:
            precision = 0
        return round(value.data, precision)
    return value.data

def can_execute_network_command(allowed_queue_count=5):
    global network
    if network is None:
        return False
    if not network.controller.is_primary_controller:
        return True
    if network.controller.send_queue_count > allowed_queue_count:
        return False
    if networkInformations.controllerIsBusy:
        return False
    if networkInformations.actualMode != ControllerMode.Idle:
        return False
    if network.state < network.STATE_STARTED:
        return False
    return True

def write_config():  
    watchDog = 0  
    while(networkInformations.configFileSaveInProgress and watchDog <10):
        if log == 'Debug':
            add_log_entry('.')
        time.sleep(1)
        watchDog +=1
    if networkInformations.configFileSaveInProgress:
        return        
    networkInformations.configFileSaveInProgress = True
    try:
        network.write_config()
        add_log_entry('write configuration file')
        time.sleep(1)
    except Exception as error:
        add_log_entry('write_config %s' % (str(error),), "error")
    finally:
        networkInformations.configFileSaveInProgress = False

def essential_node_queries_complete(network, node):   
    debug_print('The essential queries on a node have been completed. id:[%s] model:[%s].' % (node.node_id, node.product_name,))   
    timestamp = int(time.time())
    myNode = network.nodes[node.node_id]
    myNode.last_update=time.time()   
    #at this time is not good to save value, I skip this step                                    

def node_queries_complete(network, node):
    add_log_entry('All the initialisation queries on a node have been completed. id:[%s] model:[%s].' % (node.node_id, node.product_name,))        
    node.last_update=time.time()  
    #save config 
    write_config()       
    
def save_value(node, value, last_update):
    #debug_print('A node value has been updated. nodeId:%s value:%s' % (node.node_id, value.label))
    if node.node_id in network.nodes :
        myNode = network.nodes[node.node_id]    
        #check if am the realy last update
        if myNode.last_update>last_update:
            return
        #mark as seen flag
        myNode.last_update=last_update
        #if value.genre != 'Basic':
        value.last_update=last_update         
        save_node_value_event(node.node_id, int(time.time()), value.command_class, value.index, get_standard_value_type(value.type), extract_data(value, False), change_instance(value))    

def value_added(network, node, value):  
    if node.node_id in not_supported_nodes:
        return
    #debug_print('value_added. %s %s' % (node.node_id, value.label,)) 
    #mark initial data for skip notification durring interview
    value.lastData = value.data 
    #check if old polling is outside autorised range
    if value.poll_intensity > maximum_poll_intensity:
        changes_value_polling(maximum_poll_intensity, value)

def prepare_value_notification(node, value):
    if hasattr(value, 'pendingConfiguration' ):
        if(value.pendingConfiguration != None):
            #mark result
            data = value.data
            if value.type =='Short':
                data = normalize_short_value(value.data)
            value.pendingConfiguration.data = data
            
    if not node.is_ready :
        #check if have the attribute
        if hasattr(value, 'lastData') and value.lastData == value.data :
            #we skip notification to avoid value refresh durring the interview process
            return
    #update for next run    
    value.lastData = value.data    
    if value.genre == 'System' or value.genre == 'Config':
        value.last_update = time.time()
        return
    
    debug_print('send value notification %s %s %s' % (node.node_id, value.label, value.data_as_string))  
    thread = None
    try:
        save_value(node, value, time.time());
    except Exception as error:
        add_log_entry('value_update %s' % (str(error), ), "error")
        if (thread != None):
            thread.stop()

def value_update(network, node, value): 
    if node.node_id in not_supported_nodes:
        return
    #debug_print('value_update. %s %s' % (node.node_id, value.label,))
    prepare_value_notification(node, value)
                
def value_refreshed(network, node, value): 
    if node.node_id in not_supported_nodes:
        return
    #debug_print('value_refreshed. %s %s' % (node.node_id, value.label,))  
    value_update(network, node, value)
        
def scene_event(network, node, scene_id):
    add_log_entry('Scene Activation : %s' % (scene_id,))        
    timestamp = int(time.time())
    typestd = 'int'        
    save_node_value_event(node.node_id, int(time.time()), COMMAND_CLASS_CENTAL_SCENE, 0, typestd, scene_id, 0)  
    save_node_value_event(node.node_id, int(time.time()), COMMAND_CLASS_SCENE_ACTIVATION, 0, typestd, scene_id, 0)  
    
def controller_message_complete(network):
    debug_print('The last message that was sent is now complete')

def controller_waiting (network, controller, state_int, state, state_full):
    debug_print(state_full)
    #save actual state
    networkInformations.assignControllerNotification(state, state_full)    
    #notify jeedom
    save_node_event(network.controller.node_id, int(time.time()), networkInformations.computeJeeDomMessage()) 
    
def controller_command(network, controller, node, node_id, state_int, state, state_full, error_int, error, error_full):
    debug_print('%s (%s)' % (state_full, state))
    if error_int > 0:
        add_log_entry('%s (%s)' % (error_full, error,), "error")
    
    #save actual state
    networkInformations.assignControllerNotification(state, state_full, error, error_full)    
    #notify jeedom
    save_node_event(network.controller.node_id, int(time.time()), networkInformations.computeJeeDomMessage()) 
    debug_print('Controller is busy: %s' % (networkInformations.controllerIsBusy,))

def node_event(network, node, value):
    debug_print('NodeId %s sends a Basic_Set command to the controller with value %s' % (node.node_id, value,)) 
    for val in network.nodes[node.node_id].get_values():
        myValue = network.nodes[node.node_id].values[val]
        if myValue.genre == "User" and myValue.is_write_only == False :
            value_update(network, node, myValue)
    '''
    the value is actualy the event data, not a zwave value object.
    This is commonly caused when a node sends a Basic_Set command to the controller.
    '''  

def node_group_changed(network, node):
    debug_print('Group changed for nodeId %s' % (node.node_id,)) 
    #TODO: reset group changed for pending associations
    validate_association_groups(node.node_id)

def get_wakeup_interval(device_id) :
    interval = get_value_by_label(device_id, COMMAND_CLASS_WAKE_UP, 1, 'Wake-up Interval', False)
    if interval != None:
        return interval.data
    return None

def force_sleeping(device_id, count=1):
    if device_id in network.nodes :
        myNode = network.nodes[device_id]
        debug_print('check if node %s still awake' % (device_id,)) 
        # check if still awake
        if myNode.is_awake:
            debug_print('trying to lull the node %s' % (device_id,)) 
            # a ping will force the node to return sleep after the NoOperation CC. 
            network.manager.testNetworkNode(network.home_id, device_id, count)          

def node_notification(args):
    code = int(args['notificationCode'])
    device_id = int(args['nodeId'])    
    if device_id in not_supported_nodes:
        return
    if device_id in network.nodes :
        myNode = network.nodes[device_id]
        #mark as updated
        myNode.last_update=time.time()
        #try auto remove unsupported nodes
        if device_id in not_supported_nodes and network.state >= 7:   # STATE_AWAKED
            debug_print('remove fake nodeId: %s' % (device_id))
            network.manager.removeFailedNode(network.home_id, device_id)
            return
        
        wakeup_time = get_wakeup_interval(device_id)
        if not hasattr(myNode, 'last_notification') :                         
            myNode.last_notification = NodeNotification(code, wakeup_time) 
        else:
            #I refresh notification, the wakeup_time can be modified from last time, we need to calculate the next expected wakeup time 
            myNode.last_notification.refresh(code, wakeup_time)  
        if code == 3: 
            #get the device Wake-up Interval Step
            my_value =  get_value_by_label(device_id, COMMAND_CLASS_WAKE_UP, 1, 'Wake-up Interval Step', False)
            if my_value is not None:
                #add 2 seconds at device Wake-up Interval Step
                wakeup_interval_step = my_value.data + 2.0   
            else:
                # assume a default Wake-up Interval Step     
                wakeup_interval_step = 60.0
            #perform a ping to avoid device still awake after the Wake-up Interval Step        
            threading.Timer(interval=wakeup_interval_step, function=force_sleeping, args=(device_id, 1)).start()    
        debug_print('NodeId %s send a notification: %s' % (device_id, myNode.last_notification.description,))                
    
#app = Flask(__name__, static_url_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'static')))
app = Flask(__name__, static_url_path = '/static')

#Create a network object
network = ZWaveNetwork(options, autostart=False)

#We connect to the louie dispatcher
dispatcher.connect(network_started, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
dispatcher.connect(network_failed, ZWaveNetwork.SIGNAL_NETWORK_FAILED)
dispatcher.connect(network_failed, ZWaveNetwork.SIGNAL_DRIVER_FAILED)
dispatcher.connect(network_awaked, ZWaveNetwork.SIGNAL_NETWORK_AWAKED)
dispatcher.connect(network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)

start_network()

#a new node has been found (not already stored in zwcfg*.xml file).
dispatcher.connect(node_new, ZWaveNetwork.SIGNAL_NODE_NEW)
#add node to the network, durring node discovering and after a inclusion 
dispatcher.connect(node_added, ZWaveNetwork.SIGNAL_NODE_ADDED)
# a node is fully removed from network.
dispatcher.connect(node_removed, ZWaveNetwork.SIGNAL_NODE_REMOVED)
# value is add, changed or is refreshed.

# A new node value has been added to OpenZWave's list. 
# These notifications occur after a node has been discovered, and details of its command classes have been received. 
# Each command class may generate one or more values depending on the complexity of the item being represented.
dispatcher.connect(value_added, ZWaveNetwork.SIGNAL_VALUE_ADDED)
# A node value has been updated from the Z-Wave network and it is different from the previous value.
dispatcher.connect(value_update, ZWaveNetwork.SIGNAL_VALUE_CHANGED)
# A node value has been updated from the Z-Wave network.
dispatcher.connect(value_refreshed, ZWaveNetwork.SIGNAL_VALUE_REFRESHED)
# when a node sends a Basic_Set command to the controller.
dispatcher.connect(node_event, ZWaveNetwork.SIGNAL_NODE_EVENT)
# scene event
dispatcher.connect(scene_event, ZWaveNetwork.SIGNAL_SCENE_EVENT)
# the essential node query are completed
dispatcher.connect(essential_node_queries_complete, ZWaveNetwork.SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE)
# all node querys are completed, the node is fully operational, is ready!
dispatcher.connect(node_queries_complete, ZWaveNetwork.SIGNAL_NODE_QUERIES_COMPLETE)
# is network notification same as SIGNAL_NETWORK_AWAKED, we don't need
dispatcher.connect(nodes_queried, ZWaveNetwork.SIGNAL_AWAKE_NODES_QUERIED)
# is network notification same as SIGNAL_NETWORK_READY, we don't need
dispatcher.connect(nodes_queried, ZWaveNetwork.SIGNAL_ALL_NODES_QUERIED)

dispatcher.connect(nodes_queried_some_dead, ZWaveNetwork.SIGNAL_ALL_NODES_QUERIED_SOME_DEAD)
# a button is pressed
dispatcher.connect(button_on, ZWaveNetwork.SIGNAL_BUTTON_ON)
dispatcher.connect(button_off, ZWaveNetwork.SIGNAL_BUTTON_OFF)

# Called when an error happened, or node changed (awake, sleep, death, no operation, timeout).
dispatcher.connect(node_notification, ZWaveNetwork.SIGNAL_NOTIFICATION)

# Controller is waiting for a user action
dispatcher.connect(controller_waiting, ZWaveNetwork.SIGNAL_CONTROLLER_WAITING)
# keep a track of actual network command in progress
dispatcher.connect(controller_command, ZWaveNetwork.SIGNAL_CONTROLLER_COMMAND)
# The command has completed successfully
dispatcher.connect(controller_message_complete, ZWaveNetwork.SIGNAL_MSG_COMPLETE)

add_log_entry('OpenZwave Library Version %s' %(network.manager.getOzwLibraryVersionNumber(),)) 
add_log_entry('Python-OpenZwave Wrapper Version %s' %(network.manager.getPythonLibraryVersionNumber(),)) 

#We wait for the network.
add_log_entry('Waiting for network to become ready')

def get_value_by_label(device_id, command_class, instance, label, trace=True):
    if device_id in network.nodes :
        myDevice = network.nodes[device_id]
        for value_id in myDevice.get_values(class_id=command_class) :
            if myDevice.values[value_id].instance==instance and myDevice.values[value_id].label==label:
                return myDevice.values[value_id]     
    if trace :
        debug_print("get_value_by_label Value not found for device_id:%s, cc:%s, instance:%s, label:%s" % (device_id, command_class, instance, label,))            
    return None

def get_value_by_index(device_id, command_class, instance, index_id, trace=True):
    if device_id in network.nodes :
        myDevice = network.nodes[device_id]
        for value_id in myDevice.get_values(class_id=command_class) :
            if myDevice.values[value_id].instance==instance and myDevice.values[value_id].index==index_id:
                return myDevice.values[value_id]     
    if trace :
        debug_print("get_value_by_index Value not found for device_id:%s, cc:%s, instance:%s, index:%s" % (device_id, command_class, instance, index_id,))            
    return None

def get_value_by_id(device_id, value_id):
    if device_id in network.nodes :
        myDevice = network.nodes[device_id]
        if (value_id in myDevice.values) :
            return myDevice.values[value_id]                 
    debug_print("get_value_by_id Value not found for device_id:%s, value_id:%s" % (device_id, value_id,)) 
    return None

def mark_pending_change(myValue, data, wakeupTime = 0):
    if(myValue != None):
        myValue.pendingConfiguration = PendingConfiguration(data, wakeupTime)
        
def build_network_busy_message():
    return format_json_result(False, 'Controller is too busy', networkInformations.computeJeeDomMessage())

def concatenate_list(listValues, separator=';'):
    try:
        if listValues is None:
            return ""
        else:
            if isinstance(listValues, set):
                return separator.join(str(s) for s in listValues)
            return listValues

    except Exception as error:
        add_log_entry(str(error), "error")
    return ""

def convert_query_stage_to_int(stage):    
    if stage == "None":
        return 0
    elif stage == "ProtocolInfo":
        return 1
    elif stage == "Probe":
        return 2
    elif stage == "WakeUp":
        return 3
    elif stage == "ManufacturerSpecific1":
        return 4
    elif stage == "NodeInfo":
        return 5
    elif stage == "SecurityReport":
        return 6
    elif stage == "ManufacturerSpecific2":
        return 7
    elif stage == "Versions":
        return 8
    elif stage == "Instances":
        return 9
    elif stage == "Static":
        return 10
    elif stage == "Probe1":
        return 11
    elif stage == "Associations":
        return 12
    elif stage == "Neighbors":
        return 13
    elif stage == "Session":
        return 14
    elif stage == "Dynamic":
        return 15
    elif stage == "Configuration":
        return 16
    elif stage == "Complete":
        return 17
    return 0 
        
def serialize_neighbour_to_json(device_id):    
    tmpNode = {}    
    if device_id in network.nodes :
        myNode = network.nodes[device_id]        
        try:
            timestamp = int(myNode.last_update)
        except TypeError:
            timestamp = int(1)
            
        tmpNode['data']= {}
        tmpNode['data']['product_name'] = {'value' : myNode.product_name}
        tmpNode['data']['location'] = {'value' : myNode.location}
        node_name = myNode.name
        if network.controller.node_id == device_id :
            node_name = myNode.product_name
        if network.controller.node_id == device_id :
            node_name = myNode.product_name
        if is_none_or_empty(node_name) :
            node_name = 'Unknown'                
        tmpNode['data']['name'] = {'value' : node_name}
        tmpNode['data']['neighbours'] = {'value' : list(myNode.neighbors), 'enabled': myNode.generic != 1}
        tmpNode['data']['isVirtual'] = {'value' : ''}
        if network.controller.node_id == device_id and myNode.basic==1:
            tmpNode['data']['basicType'] = {'value' : 2}
        else:
            tmpNode['data']['basicType'] = {'value' : myNode.basic}            
        tmpNode['data']['genericType'] = {'value' : myNode.generic}
        tmpNode['data']['specificType'] = {'value' : myNode.specific}
        tmpNode['data']['type'] = {'value' : myNode.type}
        tmpNode['data']['state'] = {'value' : convert_query_stage_to_int(myNode.query_stage)}
        tmpNode['data']['isListening'] = {'value' : myNode.is_listening_device}
        tmpNode['data']['isRouting'] = {'value' : myNode.is_routing_device}
        
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return tmpNode

def validate_association_groups(device_id):
    fake_found = False
    if network != None and network.state >= 7:
        
        if device_id in network.nodes :
            myNode = network.nodes[device_id]            
            query_stage_index = convert_query_stage_to_int(myNode.query_stage)
            if query_stage_index >= 12:
                debug_print("validate_association_groups for nodeId: %s" % (device_id,))
                for group_index in list(myNode.groups):
                    group = myNode.groups[group_index]
                    for target_node_id in list(group.associations):
                        if target_node_id in network.nodes and not target_node_id in not_supported_nodes:
                            continue
                        debug_print("Remove association for nodeId: %s index %s with not exsit target: %s" % (device_id, group_index, target_node_id,))
                        network.manager.removeAssociation(network.home_id, device_id, group_index, target_node_id) 
                        fake_found = True
    return fake_found
     
def serialize_node_to_json(device_id):    
    tmpNode = {}    
    if device_id in not_supported_nodes:
        return tmpNode
    if device_id in network.nodes :
        myNode = network.nodes[device_id]        
        try:
            timestamp = int(myNode.last_update)
        except TypeError:
            timestamp = int(1)
        try :
            manufacturer_id=int(myNode.manufacturer_id,16)
        except ValueError:
            manufacturer_id = None
        try :
            product_id=int(myNode.product_id,16)
        except ValueError:
            product_id = None
        try :
            product_type=int(myNode.product_type,16)
        except ValueError:
            product_type = None
                    
        tmpNode['data']= {}
        tmpNode['data']['manufacturerId'] = {'value' : manufacturer_id, 'hex': '0x' + myNode.manufacturer_id}
        tmpNode['data']['vendorString'] = {'value' : myNode.manufacturer_name}
        tmpNode['data']['manufacturerProductId'] = {'value' : product_id, 'hex': '0x' + myNode.product_id}
        tmpNode['data']['product_name'] = {'value' : myNode.product_name}
        tmpNode['data']['location'] = {'value' : myNode.location}
        tmpNode['data']['name'] = {'value' : myNode.name}
        tmpNode['data']['version'] = {'value' : myNode.version}    
        tmpNode['data']['manufacturerProductType'] = {'value' : product_type, 'hex': '0x' + myNode.product_type}
        tmpNode['data']['neighbours'] = {'value' : list(myNode.neighbors)}
        tmpNode['data']['isVirtual'] = {'value' : ''}
        if network.controller.node_id == device_id and myNode.basic==1:
            tmpNode['data']['basicType'] = {'value' : 2}
        else:
            tmpNode['data']['basicType'] = {'value' : myNode.basic}            
        tmpNode['data']['genericType'] = {'value' : myNode.generic}
        tmpNode['data']['specificType'] = {'value' : myNode.specific}        
        tmpNode['data']['type'] = {'value' : myNode.type}            
        tmpNode['data']['state'] = {'value' : str(myNode.query_stage)}
        tmpNode['data']['isAwake'] = {'value' : myNode.is_awake,"updateTime":timestamp}
        tmpNode['data']['isReady'] = {'value' : myNode.is_ready,"updateTime":timestamp}   
        tmpNode['data']['isInfoReceived'] = {'value' : myNode.is_info_received}  
             
        tmpNode['data']['can_wake_up'] = {'value' : myNode.can_wake_up()}        
        tmpNode['data']['battery_level'] = {'value' : myNode.get_battery_level()} 
        tmpNode['data']['isFailed'] = {'value' : myNode.is_failed}
        tmpNode['data']['isListening'] = {'value' : myNode.is_listening_device}
        tmpNode['data']['isRouting'] = {'value' : myNode.is_routing_device}
        tmpNode['data']['isSecurity'] = {'value' : myNode.is_security_device}
        tmpNode['data']['isBeaming'] = {'value' : myNode.is_beaming_device}
        tmpNode['data']['isFrequentListening'] = {'value' : myNode.is_frequent_listening_device}
        tmpNode['data']['security'] = {'value' : myNode.security}        
        tmpNode['data']['lastReceived'] = {'updateTime' : timestamp}
        tmpNode['data']['maxBaudRate'] = {'value' : myNode.max_baud_rate} 
        
        tmpNode['instances'] = {"updateTime":timestamp}    
        tmpNode['groups'] = {"updateTime":timestamp}            
        for groupIndex in list(myNode.groups):
            group = myNode.groups[groupIndex]
            tmpNode['groups'][groupIndex] = {"label":group.label, "maximumAssociations": group.max_associations, "associations": concatenate_list(group.associations)}        
        if hasattr(myNode, 'last_notification') : 
            notification = myNode.last_notification
            tmpNode['last_notification'] = {"receiveTime":notification.receive_time,
                                            "code":notification.code,
                                            "description":notification.description,
                                            "help":notification.help,
                                            "next_wakeup": notification.next_wakeup}
        else:
            tmpNode['last_notification'] = {}
            
        tmpNode['command_classes'] = {}    
        for command_class in myNode.command_classes:
            tmpNode['command_classes'][command_class] = {'name': myNode.get_command_class_as_string(command_class),'hex': '0x' +convert_user_code_to_hex(command_class)}
            
        for val in myNode.get_values() : 
            myValue = myNode.values[val]
            if myValue.genre != 'Basic':
                typeStandard = get_standard_value_type(myValue.type)
            else:
                typeStandard = 'int'            
            if myValue.type == 'Short':
                value2 = normalize_short_value(myValue.data)
            else:
                value2 = extract_data(myValue)
            if myValue.label == 'Temperature' and myValue.units == 'F':
                value_units = 'C'
            else:
                value_units = myValue.units
            instance2 = change_instance(myValue)            
            if myValue.index :
                index2 = myValue.index
            else :
                index2 = 0            
            pendingState = None    
            data_items = concatenate_list(myValue.data_items)
            if hasattr(myValue, 'pendingConfiguration' ):
                if(myValue.pendingConfiguration != None) :
                    pendingState = myValue.pendingConfiguration.state 
            try:
                timestamp = int(myValue.last_update)
            except TypeError:
                timestamp = int(1)
            
            if myValue.command_class == None:
                continue    
            if instance2 not in tmpNode['instances']:
                tmpNode['instances'][instance2] = {"updateTime":timestamp}
                tmpNode['instances'][instance2]['commandClasses'] = {"updateTime":timestamp}
                tmpNode['instances'][instance2]['commandClasses']['data'] = {"updateTime":timestamp}
                tmpNode['instances'][instance2]['commandClasses'][myValue.command_class] = {"name": myNode.get_command_class_as_string(myValue.command_class)}                
                tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data'] = {"updateTime":timestamp}  
                if myNode.is_ready==False:
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['interviewDone']={}
                if myValue.command_class in [128] :
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['supported']={"value":True,"type":"bool","updateTime":timestamp}
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['last']={"value":value2,"type":"int","updateTime":timestamp}
                if myValue.command_class in [COMMAND_CLASS_WAKE_UP] :
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['interval']={"value":value2,"type":"int","updateTime":timestamp}
                tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data'][index2] = {"val": value2, "name": myValue.label, "help": myValue.help,"type":typeStandard,"typeZW":myValue.type,"units":value_units,"data_items":data_items,"read_only":myValue.is_read_only,"write_only":myValue.is_write_only,"updateTime":timestamp, "genre":myValue.genre, "value_id": myValue.value_id, "poll_intensity":myValue.poll_intensity, "pendingState":pendingState}
                
            elif myValue.command_class not in tmpNode['instances'][instance2]['commandClasses']:
                tmpNode['instances'][instance2]['commandClasses'][myValue.command_class] = {"updateTime":timestamp}
                tmpNode['instances'][instance2]['commandClasses'][myValue.command_class] = {"name": myNode.get_command_class_as_string(myValue.command_class)}
                tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data'] = {"updateTime":timestamp}
                if myNode.is_ready==False:
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['interviewDone']={}
                if myValue.command_class in [128] :
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['supported']={"value":True,"type":"bool","updateTime":timestamp}
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['last']={"value":value2,"type":"int","updateTime":timestamp}
                if myValue.command_class in [COMMAND_CLASS_WAKE_UP] :
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['interval']={"value":value2,"type":"int","updateTime":timestamp}
                tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data'][index2] ={"val": value2, "name": myValue.label, "help": myValue.help,"type":typeStandard,"typeZW":myValue.type,"units":value_units,"data_items":data_items,"read_only":myValue.is_read_only,"write_only":myValue.is_write_only,"updateTime":timestamp, "genre":myValue.genre, "value_id": myValue.value_id, "poll_intensity":myValue.poll_intensity, "pendingState":pendingState}
                
            elif index2 not in tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data'] :
                if myValue.command_class in [128] :
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['supported']={"value":True,"type":"bool","updateTime":timestamp}
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['last']={"value":value2,"type":"int","updateTime":timestamp}
                if myValue.command_class in [COMMAND_CLASS_WAKE_UP] :
                    tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data']['interval']={"value":value2,"type":"int","updateTime":timestamp}
                tmpNode['instances'][instance2]['commandClasses'][myValue.command_class]['data'][index2] ={"val": value2, "name": myValue.label, "help": myValue.help,"type":typeStandard,"typeZW":myValue.type,"units":value_units,"data_items":data_items,"read_only":myValue.is_read_only,"write_only":myValue.is_write_only,"updateTime":timestamp, "genre":myValue.genre, "value_id": myValue.value_id, "poll_intensity":myValue.poll_intensity, "pendingState":pendingState}
                
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return tmpNode

def serialize_node_health(device_id):    
    tmpNode = {}    
    if device_id in not_supported_nodes:
        return tmpNode
    if device_id in network.nodes :        
        myNode = network.nodes[device_id]          
        if myNode.basic == 2: #STATIC_CONTROLLER   = 0x02
            return tmpNode
        try:
            timestamp = int(myNode.last_update)
        except TypeError:
            timestamp = int(1)
        
        query_stage_index = convert_query_stage_to_int(myNode.query_stage)
        tmpNode['data']= {}       
        node_name = myNode.name
        if network.controller.node_id == device_id :
            node_name = myNode.product_name            
        if is_none_or_empty(node_name) :
            node_name = 'Unknown'
        tmpNode['data']['description'] = {'name' : node_name, 'location':myNode.location ,'product_name': myNode.product_name} 
        tmpNode['data']['type'] = {'basic' : myNode.basic,'generic': myNode.generic}
        tmpNode['data']['state'] = {'value' : myNode.query_stage, 'index' : query_stage_index}
        tmpNode['data']['isAwake'] = {'value' : myNode.is_awake}
        tmpNode['data']['isReady'] = {'value' : myNode.is_ready}              
        try:            
            can_wake_up = myNode.can_wake_up()  
        except RuntimeError:
            can_wake_up = False               
        tmpNode['data']['can_wake_up'] = {'value' : can_wake_up}  
        battery_level_data = None
        battery_level_last_update = None
        try:            
            battery_level = get_value_by_index(device_id, COMMAND_CLASS_BATTERY, 1, 0, False)
            if battery_level is not None:
                battery_level_data = battery_level.data
                battery_level_last_update = battery_level.last_update            
        except RuntimeError:
            pass
        tmpNode['data']['battery_level'] = {'value': battery_level_data, 'updateTime': battery_level_last_update}        
        next_wakeup = None
        if hasattr(myNode, 'last_notification') : 
            notification = myNode.last_notification
            next_wakeup = notification.next_wakeup
            tmpNode['last_notification'] = {"receiveTime":notification.receive_time,
                                            "description":notification.description,
                                            "help":notification.help
                                            }
        else:
            tmpNode['last_notification'] = {}             
        tmpNode['data']['wakeup_interval'] = {'value': get_wakeup_interval(device_id), 'next_wakeup': next_wakeup}        
        tmpNode['data']['isFailed'] = {'value' : myNode.is_failed}
        tmpNode['data']['isListening'] = {'value' : myNode.is_listening_device}
        tmpNode['data']['isRouting'] = {'value' : myNode.is_routing_device}
        tmpNode['data']['isBeaming'] = {'value' : myNode.is_beaming_device}
        tmpNode['data']['isFrequentListening'] = {'value' : myNode.is_frequent_listening_device}
        tmpNode['data']['lastReceived'] = {'updateTime' : timestamp}
        tmpNode['data']['maxBaudRate'] = {'value' : myNode.max_baud_rate}
                        
        statistics = network.manager.getNodeStatistics(network.home_id, device_id)        
        sentOk = statistics['sentCnt']    
        sentFailed = statistics['sentFailed']
        send_total = sentOk + sentFailed            
        if send_total > 0 :             
            percent_delivered = (sentOk* 100) / send_total             
        else:
            percent_delivered = 0            
        averageRequestRTT = statistics['averageRequestRTT']
        tmpNode['data']['statistics'] = {'total': send_total, 'delivered': percent_delivered, 'deliveryTime': averageRequestRTT}
        
        check_for_group = True        
        have_group = False
        if myNode.groups and query_stage_index >= 12 and myNode.generic != 2:    
            check_for_group = len(myNode.groups) > 0 
            for groupIndex in list(myNode.groups) :
                if len(myNode.groups[groupIndex].associations) > 0:
                    have_group = True
                    break            
        else:
            check_for_group = False
        tmpNode['data']['is_groups_ok'] = {'value' : have_group, 'enabled': check_for_group}
        tmpNode['data']['is_neighbours_ok'] = {'value' : len(myNode.neighbors) > 0, 'neighbors': len(myNode.neighbors), 'enabled': myNode.generic != 1 and query_stage_index >13 } 
        tmpNode['data']['is_manufacturer_specific_ok'] = {'value' : not is_none_or_empty(myNode.manufacturer_id) and not is_none_or_empty(myNode.product_id)  and not is_none_or_empty(myNode.product_type), 'enabled': query_stage_index >=7 } #ManufacturerSpecific2
        
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return tmpNode

def get_network_mode():
    '''
    if the controller is flag as busy I set the coresponding networkInformations.controllerState, 
    if not yet busy, I ignore the actual ControllerMode and assume is idle
    '''
    if networkInformations.controllerIsBusy  :
        if networkInformations.actualMode == ControllerMode.AddDevice:
            return AddDevice
        elif networkInformations.actualMode == ControllerMode.RemoveDevice:
            return RemoveDevice
        else:
            return Idle
    else:
        return Idle
        
def serialize_controller_to_json():    
    result={}     
    result['data'] = {}         
   
    result['data']['roles'] = {'isPrimaryController': network.controller.is_primary_controller,
                               'isStaticUpdateController': network.controller.is_static_update_controller,
                               'isBridgeController': network.controller.is_bridge_controller
                               }                      
    result['data']['nodeId'] = {'value':network.controller.node_id}     
    result['data']['mode'] = {'value': get_network_mode()}   
    result['data']['softwareVersion'] = {'ozw_library': network.controller.ozw_library_version, 'python_library':  network.controller.python_library_version}            
    result['data']['notification'] = networkInformations.lastControllerNotification
    result['data']['isBusy'] = {"value" : networkInformations.controllerIsBusy} 
    result['data']['networkstate'] = {"value" : network.state} 
    return result

def changes_value_polling(intensity, value):
    if intensity == 0: #disable the value polling for any value
        value.disable_poll()
    elif value.genre == "User" and not value.is_write_only: #we activate the value polling only on user genre value and is not a writeOnly
        if intensity > maximum_poll_intensity:
            intensity = maximum_poll_intensity
        value.enable_poll(intensity)
    write_config() 

def convert_user_code_to_hex(value, lenght=2):
    value1 = int(value)
    result = hex(value1)[lenght:]
    if len(result)==1:
        result = '0' *(lenght-1) + result
    return result

def set_value(device_id, valueId, data):    
    debug_print("set a value for nodeId:%s valueId:%s data:%s" % (device_id, valueId, data,))
    #check for a valid device_id    
    if device_id in network.nodes :
        currentNode = network.nodes[device_id]
        if not currentNode.is_ready:
            return format_json_result(False, 'The node must be Ready') 
        for value in currentNode.get_values():
            if value == valueId:
                zwaveValue = currentNode.values[value]
                lastValue = zwaveValue.data
                #cast data in desired type
                data = zwaveValue.check_data(data=data)        
                if data is None:
                    return jsonify({'result' : False, 'reason' : 'cant convert in desired dataType'})
                result = network.manager.setValue(zwaveValue.value_id, data)
                if result == 0:
                    resultMessage = 'fails'
                elif result == 1:
                    resultMessage = 'succeed'
                elif result == 2:
                    resultMessage = 'fails (valueId not exist)'
                else:
                    resultMessage = 'fails (unknown error)'
                if result == 1 :
                    return format_json_result()                    
                return format_json_result(False, resultMessage)
        return format_json_result(False, 'valueId not exist' )
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')

refresh_workers = {}

def create_worker(device_id, value_id, target_value, starting_value, counter):
    #create a new refresh worker
    worker = threading.Timer(interval=refresh_interval, function=refresh_background, args=(device_id, value_id, target_value, starting_value, counter))
    # save worker
    refresh_workers[value_id] = worker
    #start refresh timer
    worker.start() 

def prepare_refresh(device_id, value_id, target_value=None):   
    #debug_print("prepare_refresh for nodeId:%s valueId:%s data:%s" % (device_id, value_id, target_value,))     
    stop_refresh(device_id, value_id)
    starting_value = network.nodes[device_id].values[value_id].data 
    create_worker(device_id, value_id, target_value, starting_value, 0)
    network.nodes[device_id].values[value_id].start_refresh_time = int(time.time()) 

def refresh_background(device_id, value_id, target_value, starting_value, counter):
    do_refresh = True
    actual_value = network.nodes[device_id].values[value_id].data 
    if target_value is not None:
        if isinstance(target_value, basestring):
            #clor CC test
            do_refresh = actual_value != target_value
            #debug_print("delta %s : %s" % (actual_value, target_value,))
        else:
            #check if target is reported         
            delta = abs(actual_value - target_value)
            #debug_print("delta for nodeId:%s valueId:%s is: %s" % (device_id, value_id, delta,))
            if delta < 2 :
                #if delta is too small don't refresh
                do_refresh = False
                #debug_print("delta is too small don't refresh")
    if do_refresh : 
        #debug_print("check for changes, actual : %s , starting : %s (retry %s)" % (actual_value, starting_value, counter,))
        #check if won't changes   
        if starting_value == actual_value:
            counter+=1
            if counter >3:
                do_refresh = False
        else:
            counter = 0                
    if do_refresh :
        #debug_print("refresh")
        network.nodes[device_id].values[value_id].refresh()   
        #check if someone stop this refresh or we reach the timeout
        timeout = int(time.time()) - network.nodes[device_id].values[value_id].start_refresh_time 
        if (timeout < refresh_timeout):
            # I will start again a refresh timer
            create_worker(device_id, value_id, target_value, starting_value, counter)
    else:
        #remove worker the consigne is set
        del refresh_workers[value_id]

def stop_refresh(device_id, value_id):    
    #check if for a existing worker
    worker = refresh_workers.get(value_id)
    if worker is not None:
        #debug_print("Stop the timer")
        #Stop the timer, and cancel the execution of the timer action. This will only work if the timer is still in its waiting stage.
        worker.cancel()
        #remove worker
        del refresh_workers[value_id]
    #reset start time if refresh is running to avoid start again
    network.nodes[device_id].values[value_id].start_refresh_time = 0
    
def get_sleeping_nodes_count():
    sleeping_nodes_count = 0
    for idNode in list(network.nodes):
        if not network.nodes[idNode].is_awake:
            sleeping_nodes_count += 1
    return sleeping_nodes_count  

def convert_level_to_color(level):
    if level > 99:
        return 255
    return level*255/99

def convert_color_to_level(color):
    if color > 255:
        color = 255
    if color < 0:
        color = 0
    return color*99/255

def is_none_or_empty(value):
    if value is None:
        return True
    if value:
        return False
    else:
        return True
    
def format_json_result(success=True, detail=None, log_Level=None, code=0):
    if (log_Level != None and not is_none_or_empty(detail)):
        add_log_entry(detail, log_Level)
    if detail != None :
        return jsonify({'result': success, 'data': detail,'code': code}) 
    return jsonify({'result': success}) 

'''
default routes
'''
            
@app.before_first_request
def _run_on_start():    
    global con

@app.route('/',methods = ['GET'])
def index() :
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'index.html')), 'rb') as f:
        content = f.read()
    return content

@app.errorhandler(400)
def not_found400(error):
    add_log_entry('%s %s' % (error, request.url), "error")
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)
 
@app.errorhandler(404)
def not_found404(error):
    add_log_entry('%s %s' % (error, request.url), "error") 
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.teardown_appcontext
def close_network(error):
    return error

'''
devices routes
'''

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[0].commandClasses[133].Get()',methods = ['GET'])
def refresh_assoc(device_id) :
    debug_print("refresh_assoc for nodeId: %s" % (device_id,))
    config = {}
    if device_id in network.nodes :
        for val in network.nodes[device_id].get_values(class_id=COMMAND_CLASS_ASSOCIATION):
            network.nodes[device_id].values[val].refresh()
        return format_json_result()
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[0].commandClasses[133].data',methods = ['GET'])
def get_assoc(device_id) :
    debug_print("get_assoc for nodeId: %s" % (device_id,))
    timestamp = int(time.time())
    config = {}
    if device_id in network.nodes :
        if network.nodes[device_id].groups :
            config['supported']={'value':True}
            for group in list(network.nodes[device_id].groups) :
                config[network.nodes[device_id].groups[group].index]={}
                config[network.nodes[device_id].groups[group].index]['nodes']={'value':list(network.nodes[device_id].groups[group].associations),'updateTime':int(timestamp), 'invalidateTime':0}
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[0].commandClasses[0x85].Remove(<int:value>,<int:value2>)',methods = ['GET'])
def remove_assoc(device_id,value,value2) :    
    if networkInformations.controllerIsBusy:
        return format_json_result(False, 'Controller is busy') 
    groupIndex=value
    targetNodeId=value2    
    debug_print("remove_assoc to nodeId: %s in group %s with nodeId: %s" % (device_id, groupIndex, targetNodeId,))
    if device_id in network.nodes : 
        network.manager.removeAssociation(network.home_id, device_id, groupIndex, targetNodeId)
        return format_json_result()
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[0].commandClasses[0x85].Add(<int:value>,<int:value2>)',methods = ['GET'])
def add_assoc(device_id, value, value2) :  
    if networkInformations.controllerIsBusy:
        return format_json_result(False, 'Controller is busy')   
    config = {}
    groupIndex=value
    targetNodeId=value2
    debug_print("add_assoc to nodeId: %s in group %s with nodeId: %s" % (device_id, groupIndex, targetNodeId,))
    if device_id in network.nodes :
        network.manager.addAssociation(network.home_id, device_id, groupIndex, targetNodeId)
        return format_json_result()
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].GetPolling()',methods = ['GET'])
def get_polling(device_id) :
    polling = 0
    if device_id in network.nodes :
        for val in network.nodes[device_id].get_values() :
            if network.nodes[device_id].values[val].poll_intensity > polling :
                polling = network.nodes[device_id].values[val].poll_intensity
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return str(polling)
        
@app.route('/ZWaveAPI/Run/devices[<int:device_id>].ResetPolling()',methods = ['GET'])
def reset_polling(device_id) :
    debug_print("reset_polling for nodeId: %s" % (device_id,))    
    if device_id in network.nodes :
        for val in network.nodes[device_id].get_values():
            myValue = network.nodes[device_id].values[val]        
            changes_value_polling(0, myValue)    
        return format_json_result()  
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning') 

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].SetPolling(<int:value_id>,<int:frequence>)',methods = ['GET'])
def set_polling2(device_id, value_id, frequence) :
    debug_print("set_polling for nodeId: %s ValueId %s at: %s" % (device_id, value_id, frequence,))   
    if device_id in network.nodes :
        for val in network.nodes[device_id].get_values() :
            myValue = network.nodes[device_id].values[val] 
            if(myValue.value_id==value_id):
                changes_value_polling(frequence, myValue)
                return format_json_result()
        return format_json_result(False, 'valueId not found') 
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].SetPolling(<int:frequence>)',methods = ['GET'])
def set_polling_value(device_id, instance_id, cc_id, index, frequence) :
    debug_print("set_polling_value for nodeId: %s instance: %s cc:%s index:%s at: %s" % (device_id, instance_id, cc_id, index, frequence,))
    if device_id in network.nodes : 
        for val in network.nodes[device_id].get_values(class_id=int(cc_id,16)) :
            if network.nodes[device_id].values[val].instance - 1 == instance_id and network.nodes[device_id].values[val].index == index:
                myValue = network.nodes[device_id].values[val]
                if frequence == 0:
                    #disable the value polling for any value
                    myValue.disable_poll()
                else :                    
                    changes_value_polling(frequence, myValue)
        write_config()  
        return format_json_result()      
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning') 

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[0].commandClasses[132].data.interval.value',methods = ['GET'])
def get_wakeup(device_id) :
    if device_id in network.nodes : 
        return str(get_wakeup_interval(device_id))
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')        
    return str('')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].SetWakeup(<int:time>)',methods = ['GET'])       
def set_wakeup(device_id, time) :    
    debug_print("set wakeup interval for nodeId %s at: %s" % (device_id, time,))
    if device_id in network.nodes :
        for val in network.nodes[device_id].get_values(class_id=COMMAND_CLASS_WAKE_UP) :
            myValue = network.nodes[device_id].values[val]
            #we need to find the right valueId
            if myValue.label == "Wake-up Interval":
                result = set_value(device_id, myValue.value_id, int(time))  
                return format_json_result(result) 
        return format_json_result(False,'Wake-up Interval not found')
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')  

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].SetChangeVerified(<int:index>,<int:verified>)',methods = ['GET'])       
def set_change_verified(device_id, instance_id, cc_id, index, verified) :
    '''
    Sets a flag indicating whether value changes noted upon a refresh should be verified
    '''       
    debug_print("set_change_verified nodeId:%s instance:%s commandClasses:%s index:%s verified:%s" % (device_id, instance_id, cc_id, index, verified,))
    if device_id in network.nodes : 
        for val in network.nodes[device_id].get_values(class_id=int(cc_id,16)) :
            myValue = network.nodes[device_id].values[val]
            if myValue.instance - 1 == instance_id and myValue.index == index:
                network._manager.setChangeVerified(myValue.value_id, bool(verified))    
                return format_json_result()
        return format_json_result(False,'value not found')
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[0x70].Refresh()',methods = ['GET'])
def request_all_config_params(device_id) :    
    '''
    Request the values of all known configurable parameters from a device
    '''       
    debug_print("Request the values of all known configurable parameters from nodeId %s" % (device_id,))
    result = False
    if device_id in network.nodes : 
        network._manager.requestAllConfigParams(network.home_id, device_id)   
        return format_json_result()
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[0x70].Get(<int:index_id>)',methods = ['GET'])
def refresh_config(device_id, index_id) :
    debug_print("refresh_config for nodeId:%s index_id:%s" % (device_id, index_id,))
    if device_id in network.nodes : 
        for val in network.nodes[device_id].get_values(class_id=COMMAND_CLASS_CONFIGURATION) :
            if network.nodes[device_id].values[val].index == index_id :
                network.nodes[device_id].values[val].refresh()  
        return format_json_result()  
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].SetDeviceName(<string:location>,<string:name>)',methods = ['GET'])
def set_device_name(device_id, location, name) :    
    if networkInformations.controllerIsBusy:
        return format_json_result(False,'Controller is busy')    
    debug_print("setName for device_id:%s New Name ; '%s'" % (device_id, name,))
    result = False
    if device_id in network.nodes :   
        name = name.encode('utf8')
        name = name.replace('+',' ')      
        network.nodes[device_id].set_field('name',name)
        location = location.encode('utf8')
        location = location.replace('+',' ')
        network.nodes[device_id].set_field('location',location)
        return format_json_result()
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[0x70].data',methods = ['GET'])
def get_config(device_id) :
    debug_print("get_config for nodeId:%s" % (device_id,))
    timestamp = int(time.time())
    config = {}
    if device_id in network.nodes : 
        for val in network.nodes[device_id].values :
            list_values=[]
            if network.nodes[device_id].values[val].command_class == COMMAND_CLASS_CONFIGURATION :
                config[network.nodes[device_id].values[val].index]={}
                if network.nodes[device_id].values[val].type == "List" :
                    value10 = network._manager.getValueListSelectionNum(network.nodes[device_id].values[val].value_id)
                    values = network.nodes[device_id].values[val].data_items
                    for index, valeur in enumerate(values):
                        list_values.append(valeur)
                        if valeur == network.nodes[device_id].values[val].data_as_string :
                            value10 = index
                elif network.nodes[device_id].values[val].type == "Bool" and network.nodes[device_id].values[val].data== False:
                    value10 = 0
                elif network.nodes[device_id].values[val].type == "Bool" and network.nodes[device_id].values[val].data== True:
                    value10 = 1
                else :
                    value10 = network.nodes[device_id].values[val].data
                config[network.nodes[device_id].values[val].index]['val']={'value2':network.nodes[device_id].values[val].data,'value':value10,'value3':network.nodes[device_id].values[val].label,'value4':list_values,'updateTime':int(timestamp), 'invalidateTime':0}
                config[network.nodes[device_id].values[val].index]['size']={'value':len(str(value10))}
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:source_id>].CopyConfigurations(<int:target_id>)',methods = ['GET'])
def copy_configuration(source_id, target_id):
    if networkInformations.controllerIsBusy:
        return format_json_result(False,'Controller is busy')
    debug_print("copy_configuration from source_id:%s to target_id:%s'" % (source_id, target_id,))
    result = False
    items = 0
    if(source_id in network.nodes) : 
        if(target_id in network.nodes) : 
            source = network.nodes[source_id]
            target = network.nodes[target_id]            
            if source.manufacturer_id == target.manufacturer_id and source.product_type == target.product_type and source.product_id == target.product_id :
                for val in source.get_values() :
                    configurationValue = source.values[val]
                    if configurationValue.genre == 'Config':
                        if configurationValue.type == 'Button':
                            continue
                        if configurationValue.is_write_only:
                            continue                
                        try:
                            target_value = get_value_by_index(target_id, COMMAND_CLASS_CONFIGURATION, 1, configurationValue.index)
                            if target_value != None:
                                if configurationValue.type == 'List':
                                    network._manager.setValue(target_value.value_id, configurationValue.data)
                                    accepted = True
                                else:
                                    accepted = target.set_config_param(configurationValue.index, configurationValue.data)
                                if accepted :
                                    items +=1
                                    mark_pending_change(target_value, configurationValue.data)                                    
                        except Exception as error:
                            add_log_entry('Copy configuration %s (index:%s) :%s' % (configurationValue.label, configurationValue.index, str(error), ), "error")
                result = items != 0       
            else:
                return format_json_result(False, 'The two nodes must be with same: manufacturer_id, product_type and product_id', 'warning')
        else:
            return format_json_result(False, 'This network does not contain any node with the id %s' % (target_id,), 'warning')
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (source_id,), 'warning')            
    return jsonify({'result' : result, 'copied_configuration_items': items})

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].SetConfigurationItem(<int:index_id>,<string:item>)',methods = ['GET'])
def set_configuration_item(device_id, value_id, item) :    
    if networkInformations.controllerIsBusy:
        return format_json_result(False,'Controller is busy') 
    debug_print("set_configuration_item for device_id:%s change valueId:%s to '%s'" % (device_id, value_id, item,))
    if device_id in network.nodes : 
        result = False
        result = network._manager.setValue(device_id, value_id, item)
        if (result):
           mark_pending_change(get_value_by_id(device_id, value_id), item) 
        return format_json_result(result)   
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[0x70].Set(<int:index_id>,<int:value>,<int:size>)',methods = ['GET'])
def set_config(device_id,index_id,value,size) :
    if networkInformations.controllerIsBusy:
        return format_json_result(False,'Controller is busy')
    debug_print("set_config for nodeId:%s index:%s, value:%s, size:%s" % (device_id, index_id, value, size,))
    if size==0 :
        size=2
    try :
        if device_id in network.nodes :
            network.nodes[device_id].set_config_param(index_id, value, size)
            myValue = get_value_by_index(device_id, COMMAND_CLASS_CONFIGURATION, 1, index_id)
            mark_pending_change(myValue, value) 
            return format_json_result()
        else:
            return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')
    except Exception,e:
        return format_json_result(False, str(e), 'error')         
    return jsonify(config)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[0x70].Set(<int:index_id>,<string:value>,<int:size>)',methods = ['GET'])
def set_config2(device_id,index_id,value,size) :
    if networkInformations.controllerIsBusy:
        return format_json_result(False,'Controller is busy')
    debug_print("set_config2 for device_id:%s change index:%s to '%s' size:(%s)" % (device_id,index_id,value,size,))    
    try :
        if device_id in network.nodes :
            for value_id in network.nodes[device_id].get_values(class_id=COMMAND_CLASS_CONFIGURATION, genre='All', type='All', readonly='All', writeonly='All') :
                if network.nodes[device_id].values[value_id].index==index_id:
                    value=value.replace("@","/")
                    myValue = network.nodes[device_id].values[value_id]
                    if myValue.type == 'Button':
                        if value.lower() == 'true':
                            network._manager.pressButton(myValue.value_id)
                        else:
                            network._manager.releaseButton(myValue.value_id)                                 
                    elif  myValue.type == 'List':
                        network._manager.setValue(value_id, value)                    
                        mark_pending_change(myValue, value) 
                    elif myValue.type == 'Bool':
                        if value.lower() == 'true':
                            value = True
                        else: 
                            value = False
                        network._manager.setValue(value_id, value)                    
                        mark_pending_change(myValue, value)
                    return format_json_result()   
            return format_json_result( False, 'configuration parameter not found') 
        else:
            return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')
    except Exception,e:
        return format_json_result(False, str(e), 'error')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses[0x70].Set(<int:index_id>,<float:value>,<int:size>)',methods = ['GET'])
def set_config3(device_id,index_id,value,size) :
    if networkInformations.controllerIsBusy:
        return format_json_result(False,'Controller is busy') 
    debug_print("set_config3 for nodeId:%s index:%s, value:%s, size:%s" % (device_id, index_id, value, size,))
    if size==0 :
        size=2
    value=int(value)
    try :
        if device_id in network.nodes :
            network.nodes[device_id].set_config_param(index_id, value, size)
            mark_pending_change(get_value_by_index(device_id, COMMAND_CLASS_CONFIGURATION, 1, index_id), value) 
            return format_json_result()
        else:
            return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')
    except Exception,e:
        return format_json_result(False, str(e), 'error')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[0x70].data[<int:index_id2>].Set(<int:index_id>,<int:value>,<int:size>)',methods = ['GET'])
def set_config4(device_id,instance_id,index_id2,index_id,value,size) :
    if networkInformations.controllerIsBusy:
        return format_json_result( False, 'Controller is busy')    
    debug_print("set_config4 for nodeId:%s instance_id:%s, index:%s, value:%s, size:%s" % (device_id, instance_id, index_id, value, size,))
    if size==0 :
        size=2
    value=int(value)
    try :
        if device_id in network.nodes :
            myValue = get_value_by_index(device_id, COMMAND_CLASS_CONFIGURATION, 1, index_id)
            network.nodes[device_id].set_config_param(index_id, value, size)
            if myValue != None and myValue.type != 'List':
                mark_pending_change(myValue, value) 
            return format_json_result()
        else:
            return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')
    except Exception,e:
        return format_json_result(False, str(e), 'error')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[0x70].data[<int:index_id2>].Set(<int:index_id>,<string:value>,<int:size>)',methods = ['GET'])
def set_config5(device_id,instance_id,index_id2,index_id,value,size) :
    if networkInformations.controllerIsBusy:
        return format_json_result( False, 'Controller is busy') 
    debug_print("set_config5 for nodeId:%s instance_id:%s, index:%s, value:%s, size:%s" % (device_id, instance_id, index_id, value, size,))
    if size==0 :
        size=2
    value=int(value)
    try :
        if device_id in network.nodes :
            network.nodes[device_id].set_config_param(index_id, value, size)
            mark_pending_change(get_value_by_index(device_id, COMMAND_CLASS_CONFIGURATION, 1, index_id), value)  
            return format_json_result()
        else:
            return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')
    except Exception,e:
        return format_json_result(False, str(e), 'error')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[0x70].data[<int:index_id2>].Set(<int:index_id>,<float:value>,<int:size>)',methods = ['GET'])
def set_config6(device_id,instance_id,index_id2,index_id,value,size) :
    if networkInformations.controllerIsBusy:
        return format_json_result(False,'Controller is busy') 
    debug_print("set_config6 for nodeId:%s instance_id:%s, index:%s, value:%s, size:%s" % (device_id, instance_id, index_id, value, size,))
    if size==0 :
        size=2
    value=int(value)    
    try :
        if device_id in network.nodes : 
            network.nodes[device_id].set_config_param(index_id, value, size)
            mark_pending_change(get_value_by_index(device_id, COMMAND_CLASS_CONFIGURATION, 1, index_id), value)   
            return format_json_result()
        else:
            return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')
    except Exception,e:
        return format_json_result(False, str(e), 'error')
            
@app.route('/ZWaveAPI/Run/devices[<int:device_id>].commandClasses',methods = ['GET'])
def get_command_classes(device_id) :
    result = {}
    debug_print("get_command_classes for nodeId:%s" % (device_id,))
    if device_id in network.nodes : 
        for val in network.nodes[device_id].get_values():
            result[network.nodes[device_id].values[val].command_class] = {}
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(result)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].RequestNodeDynamic()',methods = ['GET'])
def request_node_dynamic(device_id) :
    if device_id in network.nodes :  
        #Fetch only the dynamic command class data for a node from the Z-Wave network
        network._manager.requestNodeDynamic(network.home_id, device_id)
        #mark as updated to avoid a second pass
        network.nodes[device_id].last_update=time.time()
        debug_print("Fetch the dynamic command class data for the node %s" % (device_id,))
        return format_json_result()
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')
    
@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].Get()',methods = ['GET'])
def get_value(device_id, instance_id,cc_id) :
    
    if device_id in network.nodes :        
        try:
            network.nodes[device_id].last_update
        except NameError:
            network.nodes[device_id].last_update=time.time()
     
        now = datetime.datetime.now()
        if isinstance(network.nodes[device_id].last_update, float) :
            last_update = datetime.datetime.fromtimestamp(network.nodes[device_id].last_update)
        else:
            last_update = datetime.datetime.now()
            network.nodes[device_id].last_update=time.time()
        last_delta = last_update + datetime.timedelta(seconds=30)
        #check last update is out of delta time, if the node is not a sleeping device and isReady
        if now > last_delta and network.nodes[device_id].is_listening_device and network.nodes[device_id].is_ready:
            #Fetch only the dynamic command class data for a node from the Z-Wave network
            network._manager.requestNodeDynamic(network.home_id,network.nodes[device_id].node_id)
            #mark as updated to avoid a second pass
            network.nodes[device_id].last_update=time.time()
            debug_print("Fetch the dynamic command class data for the node %s" % (device_id,))
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')
    return format_json_result()

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].val',methods = ['GET'])
def get_value6(device_id, instance_id, index,cc_id) :
    Value = {}
    if device_id in network.nodes :
        for val in network.nodes[device_id].get_values(class_id=int(cc_id,16)) :
            if network.nodes[device_id].values[val].instance - 1 == instance_id and network.nodes[device_id].values[val].index == index:
                if network.nodes[device_id].values[val].units=="F" :
                    return str((float(network.nodes[device_id].values[val].data) - 32) * 5.0/9.0)[0:5]
                else :
                    return str(network.nodes[device_id].values[val].data)
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value) 
        
@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[0x63].data[<int:index>].code',methods = ['GET'])
def get_user_code(device_id, instance_id, index) :
    debug_print("getValueRaw nodeId:%s instance:%s commandClasses:%s index:%s" % (device_id, instance_id, hex(COMMAND_CLASS_USER_CODE), index))
    Value = {}
    if device_id in network.nodes :        
        myDevice = network.nodes[device_id]
        for val in myDevice.get_values(class_id=COMMAND_CLASS_USER_CODE) :  
            myValue = myDevice.values[val]                                  
            if myValue.instance -1 == instance_id and myValue.index == index:                            
                userCode = [0,0,0,0,0,0,0,0,0,0] 
                timestamp = int(1)
                rawData = extract_data(myValue) 
                #debug_print("found a value: %s with data: (%s)" % (myValue.label, rawData,))                  
                if rawData != '00000000000000000000' :        
                    try:
                        timestamp = int(myValue.last_update)
                        chunks, chunk_size = len(rawData), len(rawData)/10
                        userCode = [ int(rawData[i:i+chunk_size], 16)  for i in range(0, chunks, chunk_size) ] 
                       
                    except TypeError:
                        timestamp = int(1)                 
                Value = {'invalidateTime': int(time.time() - datetime.timedelta(seconds=30).total_seconds()),
                         'type': get_standard_value_type(myValue.type),
                         'value':userCode,
                         'updateTime':timestamp
                         }                            
                break
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[0x63].data',methods = ['GET'])
def get_user_codes(device_id, instance_id) :    
    debug_print("getValueAllRaw nodeId:%s instance:%s commandClasses:%s" % (device_id, instance_id, hex(COMMAND_CLASS_USER_CODE),))
    Value = {}
    if device_id in network.nodes :        
        myDevice = network.nodes[device_id]
        for val in myDevice.get_values(class_id=COMMAND_CLASS_USER_CODE) :  

            myValue = myDevice.values[val]
            if myValue.instance -1 == instance_id : 
                if myValue.index == 0 :
                    continue
                if myValue.index > 10 :
                    continue
                rawData = extract_data(myValue)     
                #debug_print("found a value: %s with data: (%s)" % (myValue.label, rawData,))                
                if rawData == '00000000000000000000' :
                    Value[myValue.index] = None
                else:
                    Value[myValue.index] = {}
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning') 
    return jsonify(Value)  

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].UserCode.SetRaw(<int:slot_id>,[<string:value>],1)',methods = ['GET'])
def set_user_code(device_id, slot_id, value) :
    debug_print("set_user_code nodeId:%s slot:%s usercode:%s" % (device_id, slot_id, value,))
    Value2 = {}
    for val in network.nodes[device_id].get_values(class_id=COMMAND_CLASS_USER_CODE) :
        if network.nodes[device_id].values[val].index == slot_id:
            Value2['data'] = {}
            valueorig = value
            value=binascii.a2b_hex(value)            
            network.nodes[device_id].values[val].data=value
            Value2['data'][val] = {'device':device_id,'slot':slot_id,'val': valueorig}
            return jsonify(Value2) 
    return jsonify(Value2)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[0].commandClasses[0x63].SetRaw(<int:slot_id>,[<value1>,<value2>,<value3>,<value4>,<value5>,<value6>,<value7>,<value8>,<value9>,<value10>],1)',methods = ['GET'])
def set_user_code2(device_id, slot_id, value1, value2, value3, value4, value5, value6, value7, value8, value9, value10) :    
    debug_print("set_user_code2 nodeId:%s slot:%s usercode:%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (device_id, slot_id, value1,value2,value3,value4,value5,value6,value7,value8,value9,value10,))
    Value2 = {}
    if device_id in network.nodes : 
        for val in network.nodes[device_id].get_values(class_id=COMMAND_CLASS_USER_CODE) :
            if network.nodes[device_id].values[val].index == slot_id:
                Value2['data'] = {}            
                value = convert_user_code_to_hex(value1)+convert_user_code_to_hex(value2)+convert_user_code_to_hex(value3)+convert_user_code_to_hex(value4)+convert_user_code_to_hex(value5)+convert_user_code_to_hex(value6)+convert_user_code_to_hex(value7)+convert_user_code_to_hex(value8)+convert_user_code_to_hex(value9)+convert_user_code_to_hex(value10)
                valueorig = value
                value=binascii.a2b_hex(value)            
                network.nodes[device_id].values[val].data=value
                Value2['data'][val] = {'device':device_id,'slot':slot_id,'val': valueorig}
                return jsonify(Value2) 
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(Value2)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].Set(<int:value>)',methods = ['GET'])
def set_value7(device_id,instance_id, cc_id, index, value) :
    debug_print("set_value7 nodeId:%s instance:%s commandClasses:%s index:%s data:%s" % (device_id, instance_id, cc_id, index, value,))
    if device_id in network.nodes :
        for val in network.nodes[device_id].get_values(class_id=int(cc_id, 16), genre='All', type='All', readonly='All', writeonly='All') :
            if network.nodes[device_id].values[val].instance - 1 == instance_id and network.nodes[device_id].values[val].index == index :
                network.nodes[device_id].values[val].data=value
                if network.nodes[device_id].values[val].genre=='System':
                    if network.nodes[device_id].values[val].type=='Bool':
                        if value == 0:
                            value =False
                        else:
                            value = True                        
                    mark_pending_change(network.nodes[device_id].values[val], value) 
                if cc_id == hex(COMMAND_CLASS_SWITCH_MULTILEVEL):
                    #dimmer don't report the final value until the value changes is completed
                    prepare_refresh(device_id, val, value)
                return format_json_result()
        return format_json_result(False, 'value not found')
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].Set(<float:value>)',methods = ['GET'])
def set_value8(device_id,instance_id, cc_id, index, value) :
    debug_print("set_value8 nodeId:%s instance:%s commandClasses:%s index:%s data:%s" % (device_id, instance_id, cc_id, index, value,))
    if device_id in network.nodes :
        for val in network.nodes[device_id].get_values(class_id=int(cc_id, 16), genre='All', type='All', readonly='All', writeonly='All') :
            if network.nodes[device_id].values[val].instance - 1 == instance_id and network.nodes[device_id].values[val].index == index :
                network.nodes[device_id].values[val].data=value
                if network.nodes[device_id].values[val].genre=='System':
                    mark_pending_change(network.nodes[device_id].values[val], value)  
                if cc_id == hex(COMMAND_CLASS_SWITCH_MULTILEVEL):
                    #dimmer don't report the final value until the value changes is completed
                    prepare_refresh(device_id, val, value)
                return format_json_result()
        return format_json_result(False, 'value not found')
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].Set(<string:value>)',methods = ['GET'])
def set_value9(device_id,instance_id, cc_id, index, value) :
    debug_print("set_value9 nodeId:%s instance:%s commandClasses:%s index:%s data:%s" % (device_id, instance_id, cc_id, index, value,))
    if device_id in network.nodes :
        for val in network.nodes[device_id].get_values(class_id=int(cc_id, 16), genre='All', type='All', readonly='All', writeonly='All') :
            if network.nodes[device_id].values[val].instance - 1 == instance_id and network.nodes[device_id].values[val].index == index :
                last_value = network.nodes[device_id].values[val].data
                network.nodes[device_id].values[val].data=value
                if network.nodes[device_id].values[val].genre=='System':
                    mark_pending_change(network.nodes[device_id].values[val], value) 
                if cc_id == hex(COMMAND_CLASS_SWITCH_MULTILEVEL):
                    #dimmer don't report the final value until the value changes is completed
                    prepare_refresh(device_id, val, value)
                if cc_id == hex(COMMAND_CLASS_COLOR):                       
                    if len(last_value) == 9 and len(value) > 9:
                        value = value[:9]     
                    prepare_refresh(device_id, val, value.upper())
                return format_json_result() 
        return format_json_result(False, 'value not found')
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].Set(<string:value>)',methods = ['GET'])
def set_value6(device_id, instance_id, cc_id, value) :
    debug_print("set_value6 nodeId:%s instance:%s commandClasses:%s  data:%s" % (device_id, instance_id, cc_id,  value,))
    if cc_id == str(COMMAND_CLASS_WAKE_UP) :
        #is a wakeup interval update  
        arr=value.split(",")
        time=int(arr[0])      
        return set_wakeup(device_id, time) 
    if device_id in network.nodes :       
        if cc_id == '0x85' :
            # is a add association
            arr=value.split(",")
            group=int(arr[0])
            nodeTarget=int(arr[1])
            try:
                return format_json_result(add_assoc(device_id, group, nodeTarget))
            except ValueError:
                debug_print('Node not Ready for associations')
                return format_json_result(False,'Node not Ready for associations')
        for val in network.nodes[device_id].get_values(class_id=int(cc_id,16), genre='All', type='All', readonly='All', writeonly='All') :
            if network.nodes[device_id].values[val].instance - 1 == instance_id:
                network.nodes[device_id].values[val].data=value
                return format_json_result()
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')
    return format_json_result(False,'value not found')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].GetColor()',methods = ['GET'])
def get_color(device_id) :
    debug_print("get_color nodeId:%s" % (device_id,))
    result = {}
    if device_id in network.nodes :
        red_level = 0  
        green_level = 0 
        blue_level = 0 
        white_level = 0
        
        for val in network.nodes[device_id].get_values(class_id=COMMAND_CLASS_SWITCH_MULTILEVEL, genre='User', type='Byte', readonly='All', writeonly=False) :
            my_value = network.nodes[device_id].values[val]
            if my_value.label != 'Level':
                continue
            if my_value.instance < 2 :
                continue            
            
            if my_value.instance == 3 :                
                red_level = convert_level_to_color(my_value.data)
            elif my_value.instance == 4 :
                green_level = convert_level_to_color(my_value.data)
            elif my_value.instance == 5 :
                blue_level = convert_level_to_color(my_value.data)
            elif my_value.instance == 6 :
                white_level = convert_level_to_color(my_value.data) 
        result['data'] = {'red': red_level, 'green': green_level, 'blue': blue_level, 'white': white_level}
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify(result)

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].SetColor(<int:red_level>,<int:green_level>,<int:blue_level>,<int:white_level>)',methods = ['GET'])
def set_color(device_id,  red_level, green_level, blue_level, white_level) :
    debug_print("set_color nodeId:%s red:%s green:%s blue:%s white:%s" % (device_id, red_level,  green_level, blue_level, white_level,))
    result = False
    if device_id in network.nodes :
        intensity_Value = None
        red_Value = None
        green_Value = None
        blue_Value = None
        white_Value = None
        for val in network.nodes[device_id].get_values(class_id=COMMAND_CLASS_SWITCH_MULTILEVEL, genre='User', type='Byte', readonly='All', writeonly=False) :
            my_value = network.nodes[device_id].values[val]
            if my_value.label != 'Level':
                continue
            if my_value.instance == 2 :
                continue
            if my_value.instance == 1 :
                intensity_Value = val
            elif my_value.instance == 3 :
                red_Value = val
                my_value.data = convert_color_to_level(red_level)
            elif my_value.instance == 4 :
                green_Value = val
                my_value.data = convert_color_to_level(green_level)
            elif my_value.instance == 5 :
                blue_Value = val
                my_value.data = convert_color_to_level(blue_level)
            elif my_value.instance == 6 :
                white_Value = val
                my_value.data = convert_color_to_level(white_level)
        if red_Value != None and green_Value != None and blue_Value != None  :
            prepare_refresh(device_id, intensity_Value, None)
            result = True
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')
    return format_json_result(result) 

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].PressButton()',methods = ['GET'])
def press_button(device_id, instance_id, cc_id, index) :
    """
    Start an activity in a device
    """
    debug_print("press_button nodeId:%s, instance:%s, cc:%s, index:%s" % (device_id,  instance_id, cc_id, index,))
    if device_id in network.nodes :
        for val in network.nodes[device_id].get_values(class_id=int(cc_id, 16), genre='All', type='All', readonly='All', writeonly='All') :
            if network.nodes[device_id].values[val].instance - 1 == instance_id and network.nodes[device_id].values[val].index == index :
                network._manager.pressButton(network.nodes[device_id].values[val].value_id)
                #special case for dimmer and store
                if cc_id == hex(COMMAND_CLASS_SWITCH_MULTILEVEL) and network.nodes[device_id].values[val].label in ['Bright', 'Dim', 'Open', 'Close']:
                    #assume Dim / Close as target value
                    value = 1
                    if network.nodes[device_id].values[val].label in ['Bright', 'Open']:
                        value = 99
                    #dimmer don't report the final value until the value changes is completed                    
                    value_level = get_value_by_label(device_id, COMMAND_CLASS_SWITCH_MULTILEVEL, network.nodes[device_id].values[val].instance, 'Level')
                    if value_level:
                        prepare_refresh(device_id, value_level.value_id, value)
                    
                return format_json_result()
        return format_json_result(False,'button not found')
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].instances[<int:instance_id>].commandClasses[<cc_id>].data[<int:index>].ReleaseButton()',methods = ['GET'])
def release_button(device_id,instance_id, cc_id, index) :
    """
    Stop an activity in a device
    """
    if device_id in network.nodes :
        for val in network.nodes[device_id].get_values(class_id=int(cc_id, 16), genre='All', type='All', readonly='All', writeonly='All') :
            if network.nodes[device_id].values[val].instance - 1 == instance_id and network.nodes[device_id].values[val].index == index :
                network._manager.releaseButton(network.nodes[device_id].values[val].value_id)
                #stop refresh if running in background
                if cc_id == hex(COMMAND_CLASS_SWITCH_MULTILEVEL):
                    value_level = get_value_by_label(device_id, COMMAND_CLASS_SWITCH_MULTILEVEL, network.nodes[device_id].values[val].instance, 'Level')
                    if value_level:
                        stop_refresh(device_id, value_level.value_id)
                
                return format_json_result()
        return format_json_result(False,'button not found')
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].RequestNodeNeighbourUpdate()',methods = ['GET'])
def request_node_neighbour_update(device_id) :
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    debug_print("request_node_neighbour_update for node %s" %(device_id,)) 
    if device_id in network.nodes :
        return format_json_result(network.manager.requestNodeNeighborUpdate(network.home_id, device_id))
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')
    
@app.route('/ZWaveAPI/Run/devices[<int:device_id>].RemoveFailedNode()',methods = ['GET'])
def remove_failed_node(device_id) :
    """
    Removing the failed node from the controller's list.
    This command cannot be cancelled.
    """
    if can_execute_network_command(0) == False:
        return build_network_busy_message()  
    add_log_entry("Remove a failed node %s" %(device_id,))
    if device_id in network.nodes :
        return format_json_result(network.manager.removeFailedNode(network.home_id, device_id))
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')
    
@app.route('/ZWaveAPI/Run/devices[<int:device_id>].HealNode()',methods = ['GET'])
def heal_node(device_id, performReturnRoutesInitialization=False) :
    """
    Heal a single node in the network
    """
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    try:
        add_log_entry("Heal network node (%s) by requesting the node rediscover their neighbors" %(device_id,)) 
        if device_id in network.nodes :
            network._manager.healNetworkNode(network.home_id, device_id, performReturnRoutesInitialization)
            return format_json_result()
        else:
            return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')
    except Exception,e:
        return format_json_result(False, str(e), 'error') 
    
@app.route('/ZWaveAPI/Run/devices[<int:device_id>].AssignReturnRoute()',methods = ['GET'])
def assign_return_route(device_id) :
    """
    Assign network routes to a device
    """
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    add_log_entry("Ask Node (%s) to update its Return Route to the Controller" %(device_id,))    
    if device_id in network.nodes : 
        return format_json_result(network.manager.assignReturnRoute(network.home_id, device_id))
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')     
"""        
@app.route('/ZWaveAPI/Run/devices[<int:device_id>].RequestNodeInformation()',methods = ['GET'])
def request_node_information(device_id) :
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    debug_print("request_node_information node %s" %(device_id,)) 
    if device_id in network.nodes : 
        return format_json_result(network.network.nodes[device_id].request_all_config_params())
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')
"""
    
@app.route('/ZWaveAPI/Run/devices[<int:device_id>]', methods = ['GET'])
def get_serialized_device(device_id):
    if device_id in network.nodes :
        return jsonify( serialize_node_to_json(device_id))
    else:
        add_log_entry('This network does not contain any node with the id %s' % (device_id,), 'warning')
    return jsonify({})             

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].ReplaceFailedNode()',methods = ['GET'])
def replace_failed_node(device_id) :
    """
    Replace a failed device with another. If the node is not in the controller failed nodes list, or the node responds, this command will fail.
    """
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    add_log_entry("replace_failed_node node %s" %(device_id,)) 
    if device_id in network.nodes : 
        return format_json_result(network.manager.replaceFailedNode(network.home_id, device_id))
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].SendNodeInformation()',methods = ['GET'])
def send_node_information(device_id) :
    """
    Send a node information frame (NIF).
    """
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    debug_print("send_node_information node %s" %(device_id,)) 
    if device_id in network.nodes : 
        return format_json_result(network.manager.sendNodeInformation(network.home_id, device_id))
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].HasNodeFailed()',methods = ['GET'])
def has_node_failed(device_id) :
    """
    Check whether a node is in the controller failed nodes list.
    """
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    add_log_entry("has_node_failed node %s" %(device_id,)) 
    if device_id in network.nodes : 
        return format_json_result(network.manager.hasNodeFailed(network.home_id, device_id))
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].RefreshNodeInfo()',methods = ['GET'])
def refresh_node_info(device_id) :
    """
    Trigger the fetching of fixed data about a node. 
    Causes the node data to be obtained from the Z-Wave network in the same way as if it had just been added.
    """
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    debug_print("refresh_node_info node %s" %(device_id,)) 
    if device_id in network.nodes : 
        return format_json_result(network.manager.refreshNodeInfo(network.home_id, device_id))
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')
   
@app.route('/ZWaveAPI/Run/devices[<int:device_id>].RefreshAllValues()',methods = ['GET'])
def refresh_all_values(device_id):
    """
    A manual refresh of all value of a node, we will receive a refreshed value form value refresh notification
    """ 
    if device_id in network.nodes : 
        currentNode = network.nodes[device_id]
        try:
            counter = 0
            debug_print("refresh_all_values node %s" %(device_id,))
            for val in currentNode.get_values():
                currentValue = currentNode.values[val]
                if currentValue.type == 'Button':
                    continue
                if currentValue.is_write_only:
                    continue
                currentValue.refresh()
                counter+=1
            message = 'Refreshed values count: %s' % (counter,)            
            return format_json_result(True, message)
        except Exception,e:
            return format_json_result(False, str(e), 'error')
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')

@app.route('/ZWaveAPI/Run/devices[<int:device_id>].TestNode()',methods = ['GET'])
def test_node(device_id=0, count=3):
    """
    Test network node.
    Sends a series of messages to a network node for testing network reliability.
    """
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    try:
        debug_print("test_network node %s" %(device_id,))
        if device_id in network.nodes :
            network.manager.testNetworkNode(network.home_id, device_id, count)
            return format_json_result()
        else:
            return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')       
    except Exception,e:
        return format_json_result(False, str(e), 'error')
    
@app.route('/ZWaveAPI/Run/devices[<int:device_id>].GetNodeStatistics()',methods = ['GET'])
def get_node_statistics(device_id):
    """
    Retrieve statistics per node.
    """ 
    try:
        if device_id in network.nodes :
            queryStageDescription = network.manager.getNodeQueryStage(network.home_id, device_id)
            queryStageCode = network.manager.getNodeQueryStageCode(queryStageDescription)
            return jsonify( {'statistics' : network.manager.getNodeStatistics(network.home_id, device_id),
                    'queryStageCode' : queryStageCode,
                    'queryStageDescription' : queryStageDescription})
        else:
            return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')
    except Exception,e:
        return format_json_result(False, str(e), 'error')

"""
@app.route('/ZWaveAPI/Run/devices[<int:device_id>].request_all_config_params()',methods = ['GET'])
def request_all_config_parameters(device_id) :
    '''
    Request the values of all known configurable parameters from a device.
    '''
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    try:
        debug_print("RequestAllConfigParams node %s" %(device_id,))
        if device_id in network.nodes : 
           return format_json_result(network.network.nodes[device_id].request_all_config_params())
        else:
            return format_json_result(False, 'This network does not contain any node with the id %s' % (device_id,), 'warning')
    except Exception as e:
        return format_json_result(False, str(e), 'error')
"""
    
@app.route('/ZWaveAPI/Run/devices[<int:device_id>].RemoveDeviceZWConfig()',methods = ['GET'])

def remove_device_openzwave_config(device_id) :
    """
    Remove a device from the openzwave config file and restart network to rediscover again
    """
    #ensure load latest file version
    global data_folder;
    try:
        network.stop()
        add_log_entry('ZWave network is now stopped')
        time.sleep(5)
    except Exception,e:
        return format_json_result(False, str(e), 'error')    
    fileName = data_folder+"/zwcfg_" + network.home_id_str +".xml"
    try:
        tree = etree.parse(fileName)
        node = tree.find("{http://code.google.com/p/open-zwave/}Node[@id='"+str(device_id)+"']")
        tree.getroot().remove(node)
        FILE = open(fileName,"w")
        FILE.write('<?xml version="1.0" encoding="utf-8" ?>\n')
        FILE.writelines(etree.tostring(tree, pretty_print=True))
        FILE.close()
        start_network()
        return format_json_result()
    except Exception,e:
        return format_json_result(False, str(e), 'error') 
    
@app.route('/ZWaveAPI/Run/devices[<int:device_id>].GhostKiller()',methods = ['GET'])    
def ghost_killer(device_id):
    """
    Remove cc 0x84 wakeup for a ghost device in openzwave config file
    """
    if can_execute_network_command(0) == False:
        return build_network_busy_message() 
    add_log_entry('Remove cc 0x84 (wake_up) for a ghost device: %s' %(device_id,)) 
    
    fileName = data_folder+"/zwcfg_" + network.home_id_str +".xml"
    #ensure load latest file version
    try:
        network.stop()
        add_log_entry('ZWave network is now stopped')
        time.sleep(5)
    except Exception,e:
        return format_json_result(False, str(e), 'error') 
    try: 
        found = False       
        message = None    
        tree = etree.parse(fileName)
        namespace = tree.getroot().tag[1:].split("}")[0]
        node = tree.find("{%s}Node[@id='%s']" % (namespace, device_id,))   
        if node is None :
            message = 'node not found'
        else:            
            commandClasses = node.find(".//{%s}CommandClasses" % namespace)        
            if commandClasses is None :
                message = 'commandClasses not found'
            else:
                for command_Class in commandClasses.findall(".//{%s}CommandClass" % namespace) :
                    if int(command_Class.get("id")[:7]) == COMMAND_CLASS_WAKE_UP :
                        commandClasses.remove(command_Class)
                        found = True
                        break
                if found :   
                    config_file = open(fileName,"w")
                    config_file.write('<?xml version="1.0" encoding="utf-8" ?>\n')
                    config_file.writelines(etree.tostring(tree, pretty_print=True))
                    config_file.close()  
                else:
                    message = 'commandClass wake_up not found'
        return format_json_result(found, message)
    except Exception,e:
        return format_json_result(False, str(e), 'error') 
    finally:
        start_network()            

"""
controllers routes
"""
            
@app.route('/ZWaveAPI/Run/controller.AddNodeToNetwork(<int:state>,<int:doSecurity>)',methods = ['GET'])
def start_node_inclusion(state, doSecurity) :
    if networkInformations.controllerIsBusy:
        return format_json_result(False,'Controller is busy')
    if state == 1 :    
        if can_execute_network_command(0) == False:
            return build_network_busy_message()
        if doSecurity == 1:
            doSecurity = True
            add_log_entry("Start the Inclusion Process to add a Node to the Network with Security CC if the node is supports it")
        else:
            doSecurity = False
            add_log_entry("Start the Inclusion Process to add a Node to the Network")        
        result = network.manager.addNode(network.home_id, doSecurity)
        if result :
            networkInformations.actualMode = ControllerMode.AddDevice   
        return format_json_result(result)
    elif state == 0 :
        add_log_entry("Start the Inclusion (Cancel)" ) 
        network.manager.cancelControllerCommand(network.home_id)
        return format_json_result()
 
@app.route('/ZWaveAPI/Run/controller.RemoveNodeFromNetwork(<int:state>)',methods = ['GET'])
def start_node_exclusion(state) :
    if networkInformations.controllerIsBusy:
        return format_json_result(False,'Controller is busy')
    if state == 1 :
        if can_execute_network_command(0) == False:
            return build_network_busy_message()  
        add_log_entry("Remove a Device from the Z-Wave Network (Started)" ) 
        result = network.manager.removeNode(network.home_id)
        if result :
            networkInformations.actualMode = ControllerMode.RemoveDevice            
        return format_json_result(result)
    elif state == 0 :
        add_log_entry("Remove a Device from the Z-Wave Network (Cancel)" ) 
        network.manager.cancelControllerCommand(network.home_id) 
        return format_json_result() 

@app.route('/ZWaveAPI/Run/controller.CancelCommand()',methods = ['GET'])
def cancel_command():    
    """
    Cancels any in-progress command running on a controller.
    """
    add_log_entry("Cancels any in-progress command running on a controller.")
    try:
        result = network.manager.cancelControllerCommand(network.home_id)
        if result :
            networkInformations.controllerIsBusy = False        
        return format_json_result(result)
    except Exception,e:
        return format_json_result(False, str(e), 'error')
     
@app.route('/ZWaveAPI/Run/controller.RequestNetworkUpdate(<int:bridge_controller_id>)',methods = ['GET'])
def request_network_update(bridge_controller_id) :
    """
    Update the controller with network information from the SUC/SIS.
    """ 
    add_log_entry("Update the controller (%s) with network information from the SUC/SIS" %(bridge_controller_id,))
    return format_json_result(False,'Not implemented')   
    if can_execute_network_command(0) == False:
        return build_network_busy_message()  
    if bridge_controller_id in network.nodes :
        result = network.manager.requestNetworkUpdate(network.home_id, bridge_controller_id)
    else:
        return format_json_result(False, 'This network does not contain any node with the id %s' % (bridge_controller_id,), 'warning')
    return format_json_result(result) 

@app.route('/ZWaveAPI/Run/controller.ReplicationSend(<int:bridge_controller_id>)',methods = ['GET'])
def replication_send(bridge_controller_id) :
    """
    Send information from primary to secondary.
    """
    if can_execute_network_command(0) == False:
        return build_network_busy_message() 
    add_log_entry('Send information from primary to secondary %s' % (bridge_controller_id,))
    try:
        if bridge_controller_id in network.nodes :
            return format_json_result(network.manager.replicationSend(network.home_id, bridge_controller_id))
        else:
            return format_json_result(False, 'This network does not contain any node with the id %s' % (bridge_controller_id,), 'warning')
    except Exception,e:
        return format_json_result(False, str(e), 'error')
    
@app.route('/ZWaveAPI/Run/controller.HealNetwork()',methods = ['GET'])
def heal_network(performReturnRoutesInitialization=False) :
    if can_execute_network_command(0) == False:
        return build_network_busy_message()      
    add_log_entry("Heal network by requesting node's rediscover their neighbors") 
    for node_id in list(network.nodes):
        if node_id in not_supported_nodes :   
            debug_print("skip not supported (nodeId: %s)" %(node_id,)) 
            continue
        if network.nodes[node_id].is_failed:
            debug_print("skip presume dead (nodeId: %s)" %(node_id,))
            continue        
        if network.nodes[node_id].query_stage != "Complete":
            debug_print("skip query stage not complete (nodeId: %s)" %(node_id,))
            continue
        if network.nodes[node_id].generic == 1:
            debug_print("skip Remote controller (nodeId: %s) (they don't have neighbors)" %(node_id,))
            continue
        network._manager.healNetworkNode(network.home_id, node_id, performReturnRoutesInitialization)
    return format_json_result()

@app.route('/ZWaveAPI/Run/controller.SerialAPISoftReset()',methods = ['GET'])
def soft_reset() :
    add_log_entry("Soft-reset the Z-Wave controller chip")
    try:
        return format_json_result(network.controller.soft_reset())        
    except Exception,e:
        return format_json_result(False, str(e), 'error')

@app.route('/ZWaveAPI/Run/controller.TestNetwork()',methods = ['GET'])
def test_network(count=3):
    """
    Test network node.
    Sends a series of messages to a network node for testing network reliability.
    """
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    try:
        add_log_entry("Sends a series of messages to a network node for testing network reliability")
        network.manager.testNetwork(network.home_id, count)
        return format_json_result()
    except Exception,e:
        return format_json_result(False, str(e), 'error')

@app.route('/ZWaveAPI/Run/controller.CreateNewPrimary()',methods = ['GET'])
def create_new_primary() :
    """
    Put the target controller into receive configuration mode.
    The PC Z-Wave Controller must be within 2m of the controller that is being made the primary.
    """
    if can_execute_network_command(0) == False:
        return build_network_busy_message()  
    add_log_entry("Add a new controller to the Z-Wave network")
    try:
        return format_json_result(network.manager.createNewPrimary(network.home_id))
    except Exception,e:
        return format_json_result(False, str(e), 'error')
   
@app.route('/ZWaveAPI/Run/controller.TransferPrimaryRole()',methods = ['GET'])
def transfer_primary_role() :
    """
    Add a new controller to the network and make it the primary.
    The existing primary will become a secondary controller.
    """ 
    if can_execute_network_command(0) == False:
        return build_network_busy_message()  
    add_log_entry("Transfer Primary Role")
    try:
        return format_json_result(network.manager.transferPrimaryRole(network.home_id))
    except Exception,e:
        return format_json_result(False, str(e), 'error')

@app.route('/ZWaveAPI/Run/controller.ReceiveConfiguration()',methods = ['GET'])
def receive_configuration() :
    """
    Receive Z-Wave network configuration information from another controller
    """
    if can_execute_network_command(0) == False:
        return build_network_busy_message()  
    add_log_entry("Receive Configuration")
    try:
        return format_json_result(network.manager.receiveConfiguration(network.home_id))
    except Exception,e:
        return format_json_result(False, str(e), 'error')

@app.route('/ZWaveAPI/Run/controller.HardReset()',methods = ['GET'])
def hard_reset() : 
    """
    Hard Reset a PC Z-Wave Controller. 
    Resets a controller and erases its network configuration settings. 
    The controller becomes a primary controller ready to add devices to a new network.
    """
    add_log_entry("Resets a controller and erases its network configuration settings")
    if can_execute_network_command(0) == False:
        return build_network_busy_message() 
    try:
        network.controller.hard_reset()        
        add_log_entry('The controller becomes a primary controller ready to add devices to a new network')
        time.sleep(2)            
        start_network()
        return format_json_result()        
    except Exception,e:
        return format_json_result(False, str(e), 'error')
            
"""
network routes
"""
    
@app.route('/ZWaveAPI/Run/network.Start()',methods = ['GET'])
def network_start() :
    add_log_entry('******** The ZWave network is being started ********')
    try:
        start_network()     
        return format_json_result()   
    except Exception,e:
        return format_json_result(False, str(e), 'error')
    
@app.route('/ZWaveAPI/Run/network.Stop()',methods = ['GET'])
def stop_network() :
    graceful_stop_network()
    return format_json_result() 
 
@app.route('/ZWaveAPI/Run/network.GetStatus()', methods = ['GET'])
def get_network_status(): 
    if network != None and network.state >= 5:   # STATE_STARTED     
        networkStatus = {'nodesCount': network.nodes_count,
                         'sleepingNodesCount': get_sleeping_nodes_count(),
                         'scenesCount': network.scenes_count,
                         'pollInterval': network.manager.getPollInterval(),
                         'isReady': network.is_ready,
                         'stateDescription': network.state_str,
                         'state': network.state,
                         'controllerCapabilities': concatenate_list(network.controller.capabilities),
                         'controllerNodeCapabilities': concatenate_list(network.controller.node.capabilities),
                         'outgoingSendQueue': network.controller.send_queue_count,
                         'controllerStatistics': network.controller.stats,
                         'devicePath': network.controller.device,
                         'OpenZwaveLibraryVersion': network.manager.getOzwLibraryVersionNumber(),
                         'PythonOpenZwaveLibraryVersion': network.manager.getPythonLibraryVersionNumber(),
                         'neighbors': concatenate_list(network.controller.node.neighbors),
                         'notification' : networkInformations.lastControllerNotification,
                         'isBusy' : networkInformations.controllerIsBusy,
                         'startTime' :networkInformations.startTime,
                         'isPrimaryController': network.controller.is_primary_controller,
                         'isStaticUpdateController': network.controller.is_static_update_controller,
                         'isBridgeController': network.controller.is_bridge_controller,
                         'awakedDelay' : networkInformations.controllerAwakedDelay 
                         }
        networkStatus['mode'] = get_network_mode()
    else:
        networkStatus = {}
    return jsonify(networkStatus)

@app.route('/ZWaveAPI/Run/network.GetNeighbours()',methods = ['GET'])
def get_network_neighbours():
    networkData={}
    networkData['updateTime']=int(time.time())
    nodesData = {}
    for device_id in list(network.nodes):
        nodesData[device_id] = serialize_neighbour_to_json(device_id) 
    networkData['devices']=nodesData
    return jsonify(networkData)

@app.route('/ZWaveAPI/Run/network.GetHealth()',methods = ['GET'])
def get_network_health():
    networkData={}
    networkData['updateTime']=int(time.time())
    nodesData = {}
    for device_id in list(network.nodes):
        nodesData[device_id] = serialize_node_health(device_id) 
    networkData['devices']=nodesData
    return jsonify(networkData)

@app.route('/ZWaveAPI/Run/network.GetNodesList()',methods = ['GET'])
def get_nodes_list():
    result = {}
    result['updateTime']=int(time.time())
    nodesData = {}
    for device_id in list(network.nodes):        
        myNode = network.nodes[device_id]        
        tmpNode = {}        
        try :
            manufacturer_id = int(myNode.manufacturer_id,16)
        except ValueError:
            manufacturer_id = None
        try :
            product_id = int(myNode.product_id,16)
        except ValueError:
            product_id = None
        try :
            product_type = int(myNode.product_type,16)
        except ValueError:
            product_type = None      
        
        node_name = myNode.name
        node_location = myNode.location
        if is_none_or_empty(node_name) :
            node_name = 'Unknown'  
        if network.controller.node_id == device_id :
            node_name = myNode.product_name
            node_location = 'Jeedom'
                  
        tmpNode['description'] = {'name' : node_name, 'location':node_location ,'product_name': myNode.product_name, 'is_static_controller': myNode.basic == 2} 
        tmpNode['product'] = {'manufacturer_id': manufacturer_id, 'product_type': product_type, 'product_id': product_id , 'is_valid': manufacturer_id is not None and product_id is not None and product_type is not None}
        nodesData[device_id] = tmpNode
    result['devices']=nodesData
    return jsonify(result)

@app.route('/ZWaveAPI/Run/network.GetControllerStatus()',methods = ['GET'])
def get_controller_status() :
    """
    Get the controller status
    """
    try:
        controllerData = {}
        if network != None and network.state >= 5:   # STATE_STARTED
            if network.controller :
                controllerData = serialize_controller_to_json() 
        return jsonify ({'result' : controllerData})
    except Exception,e:
        return format_json_result(False, str(e), 'error')

@app.route('/ZWaveAPI/Run/network.GetOZLogs()',methods = ['GET'])
def get_openzwave_logs() :    
    """
    Read the openzwave log file
    """ 
    global data_folder;
    try:
        stdin,stdout = os.popen2("tail -n 1000 "+data_folder+"/openzwave.log")
        stdin.close()
        lines = stdout.readlines(); stdout.close()
        return jsonify ({'result' : lines})
    except Exception,e:
        return format_json_result(False, str(e), 'error')

@app.route('/ZWaveAPI/Run/network.GetZWConfig()',methods = ['GET'])
def get_openzwave_config() :
    #ensure load latest file version
    global data_folder
    try:
        write_config()
    except Exception,e:
        return format_json_result(False, str(e), 'error')  
    fileName = data_folder+"/zwcfg_" + network.home_id_str +".xml"
    try:
        with open(fileName, "r") as ins:
            f = ins.read()
        return jsonify ({'result' : f})
    except Exception,e:
        return format_json_result(False, str(e), 'error')
  
@app.route('/ZWaveAPI/Run/network.SaveZWConfig()',methods = ['POST'])
def save_openzwave_config() :
    """
    Save the openzwave config file
    """ 
    global data_folder
    try:
        network.stop()
        add_log_entry('ZWave network is now stopped')
        time.sleep(5)
        fileName = data_folder+"/zwcfg_" + network.home_id_str +".xml"
        with open(fileName, "w") as ins:
            ins.write(request.data)
        start_network()
        return format_json_result() 
    except Exception,e:
        return format_json_result(False, str(e), 'error')
   
@app.route('/ZWaveAPI/Run/network.WriteZWConfig()',methods = ['GET'])
def write_openzwave_config() :
    """
    Write the openzwave config file
    """ 
    try:
        write_config()
        return format_json_result()
    except Exception,e:
        return format_json_result(False, str(e), 'error')
   
@app.route('/ZWaveAPI/Run/network.RemoveUnknownsDevicesZWConfig()',methods = ['GET'])
def remove_unknowns_devices_openzwave_config() :
    """
    Remove unknowns devices from the openzwave config file
    """ 
    #ensure load latest file version
    global data_folder
    try:
        network.stop()
        add_log_entry('ZWave network is now stopped')
        time.sleep(5)
    except Exception,e:
        return format_json_result(False, str(e), 'error')
    
    fileName = data_folder+"/zwcfg_" + network.home_id_str +".xml"
    try:
        tree = etree.parse(fileName)
        nodes = tree.findall(".//{http://code.google.com/p/open-zwave/}Product")
        for node in nodes:
            if node.get("name")[:7]=="Unknown" :
                tree.getroot().remove(node.getparent().getparent())
        FILE = open(fileName,"w")
        FILE.write('<?xml version="1.0" encoding="utf-8" ?>\n')
        FILE.writelines(etree.tostring(tree, pretty_print=True))
        FILE.close()
        start_network()
        return format_json_result()
    except Exception,e:
        return format_json_result(False, str(e), 'error')
 
@app.route('/ZWaveAPI/Run/network.SetPollInterval(<int:seconds>,<int:intervalBetweenPolls>)',methods = ['GET'])
def set_poll_interval(seconds, intervalBetweenPolls):
    """
    Set the time period between polls of a node's state.
    """
    if can_execute_network_command() == False:
        return build_network_busy_message()  
    try:        
        add_log_entry('set_poll_interval seconds:%s, interval Between Polls: %s' % (seconds, bool(intervalBetweenPolls)),)
        if network.state < network.STATE_AWAKED:            
            return jsonify ({'result' : False, 'reason' : 'network state must a minimum set to awaked'})    
        if seconds < 30:
            return jsonify ({'result' : False, 'reason' : 'interval is too small'})  
        network.set_poll_interval(1000*seconds, bool(intervalBetweenPolls))                
        return format_json_result()
    except Exception,e:
        return format_json_result(False, str(e), 'error')
    
@app.route('/ZWaveAPI/Run/network.RefreshAllBatteryLevel()',methods = ['GET'])       
def refresh_all_battery_level():
    debug_print("refresh_all_battery_level")
    result = {}
    if network != None and network.state >= 7: 
        for device_id in list(network.nodes):
            myNode = network.nodes[device_id]
            if not myNode.is_listening_device:
                debug_print('Refresh battery level for nodeId: %s' % (device_id,))
                battery_level = get_value_by_index(device_id, COMMAND_CLASS_BATTERY, 1, 0)
                if battery_level != None:
                    battery_level.refresh()
                    result[device_id] = {'value' : battery_level.data, 'updateTime': battery_level.last_update}
    return jsonify(result)

@app.route('/ZWaveAPI/Run/network.GetOZBackups()',methods = ['GET'])       
def get_openzwave_backups():
    """
    Return the list of all available backups
    """
    global data_folder
    debug_print("List all backups")
    result = {}
    backupList = []
    backupFolder = data_folder+"/xml_backups"
    try:
        os.stat(backupFolder)
    except:
        os.mkdir(backupFolder)
    pattern = "_zwcfg_"
    alist_filter = ['xml'] 
    actualBackups = os.listdir(backupFolder)
    actualBackups.sort(reverse=True)
    for candidateBackup in actualBackups:
        if candidateBackup[-3:] in alist_filter and pattern in candidateBackup:
            backupList.append(candidateBackup)
    result['Backups'] = backupList
    return jsonify(result)

@app.route('/ZWaveAPI/Run/network.RestoreBackup(<backup_name>)',methods = ['GET'])       
def restore_openzwave_backups(backup_name):
    """
    Manually restore a backup
    """
    global data_folder
    add_log_entry('Restoring backup ' + backup_name)
    backupFolder = data_folder+"/xml_backups"
    try:
        os.stat(backupFolder)
    except:
        os.mkdir(backupFolder)
    backupFile = os.path.join(backupFolder,backup_name)
    targetFile = data_folder+"/zwcfg_" + network.home_id_str +".xml"
    if not os.path.isfile(backupFile) :
        add_log_entry('No config file found to backup', "error")
        return format_json_result(False, 'No config file found with name ' + backup_name)
    else:
        try:            
            tree = etree.parse(backupFile)
        except:
            add_log_entry('The backup file seems invalid', "error")
            return format_json_result(False, 'The backup file (' + backup_name+') seems invalid')
        network.stop()
        add_log_entry('ZWave network is now stopped')
        time.sleep(3)
        shutil.copy2(backupFile, targetFile)
        os.chmod(targetFile, 0777)
        start_network()
    return format_json_result(True, backup_name + ' succesfully restored')

@app.route('/ZWaveAPI/Run/network.ManualBackup()',methods = ['GET'])       
def manually_backup_config():
    """
    Manually create a backup
    """
    add_log_entry('Manually creating a backup')
    result = backup_xml_config('manual',network.home_id_str)
    return result

@app.route('/ZWaveAPI/Run/network.DeleteBackup(<backup_name>)',methods = ['GET'])       
def manually_delete_backup(backup_name):
    """
    Manually delete a backup
    """
    global data_folder
    add_log_entry('Manually deleting a backup')
    backupFolder = data_folder+"/xml_backups"
    backupFile = os.path.join(backupFolder,backup_name)
    if not os.path.isfile(backupFile) :
        add_log_entry('No config file found to delete', "error")
        return format_json_result(False, 'No config file found with name ' + backup_name)
    else:
        os.unlink(backupFile)
    return format_json_result(True, backup_name + ' succesfully deleted')

@app.route('/ZWaveAPI/Run/IsAlive()',methods = ['GET'])       
def rest_is_alive():    
    return format_json_result()
    
if __name__ == '__main__':
    pid = str(os.getpid())
    file(pidfile, 'w').write("%s\n" % pid)
    try:
        app.run(host='0.0.0.0',port=int(port_server),debug=False)
    except Exception,e:
        print "Fatal Error : %s" % str(e)
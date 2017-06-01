import json
import os
import re
import io
import sys
from shutil import copyfile
import urllib

base_folder = "../core/config/"
source_folder = os.path.join(base_folder , "devices")
destination_folder = os.path.join(base_folder, "new_devices")
rename_images_png = False

reload(sys)
sys.setdefaultencoding('utf8')

if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

for root, dirs, files in os.walk(source_folder, topdown=True):
    for name in files:
        source_file_name = os.path.join(root, name)
        dir = os.path.dirname(source_file_name) ## dir of dir of file
        ## once you're at the directory level you want, with the desired directory as the final path node:
        destination_manufacturer_folder = os.path.basename(dir)
        destination_file_name = os.path.join(destination_folder, destination_manufacturer_folder, name)
        if name.endswith('.json'):
            with io.open(source_file_name, mode='r', encoding='utf-8') as data_file:
                is_pilotWire = False
                data = json.loads(data_file.read())
                try:
                    new_data = {
                        'name' : data['name'],
                        'type' : data['type'],
                        'comlink' : "" if 'comlink' not  in data else data['comlink'],
                        'remark' : "" if 'remark' not  in data else data['remark'], # TODO: Remove CentralScene compatibility issue
                        'imglink' : "" if 'imglink' not  in data else data['imglink']
                    }
                    if 'ignore' in data and data['ignore'] == True:
                        new_data['ignore'] =True

                    for element in data:
                        if is_pilotWire:
                            continue
                        if element == 'commands' :
                            new_data['commands'] = []
                            for command in data['commands']:
                                if is_pilotWire:
                                    continue
                                    # command class is in dec
                                try:
                                    command_class = int(command['configuration']['class'], 16)
                                except Exception as err:
                                    if command['configuration']['value'] == 'pilotWire':
                                        is_pilotWire = True
                                    else:
                                        print(format(err))
                                    continue
                                    # assume instance is 1
                                command_instance = 1
                                # check if instance is present
                                if 'instanceId' in command['configuration']:
                                    # instance are now in base 1
                                    try:
                                        command_instance = int(command['configuration']['instanceId']) + 1
                                    except Exception as err:
                                        is_pilotWire = True
                                        continue

                                command_index = -1
                                command_value = None
                                # validated command type
                                if command['type'] == 'info':
                                    # info don't have any more value data
                                    matches = re.match('data\[(.*)\]\.val', command['configuration']['value'])
                                    if matches is not None and matches.group(1) is not None :
                                        command_index = int(matches.group(1))
                                    else:
                                        command_index = 0
                                    command_value = ""
                                elif command['type'] == 'action':
                                    # convert cmd format
                                    command_value = command['configuration']['value']
                                    matches = re.match('data\[(.*)\]\.(.*)', command['configuration']['value'])
                                    if matches is not None and matches.group(1) is not None and matches.group(2) is not None :
                                        command_index = int(matches.group(1))
                                        command_value = matches.group(2).replace('Set', 'set')
                                        command_value = command_value.replace('PressButton()', 'button(press)')
                                        command_value = command_value.replace('ReleaseButton()', 'button(release)')
                                    if command_value == 'button(press)':
                                        command_value = 'type=buttonaction&action=press'
                                    elif command_value == 'button(release)':
                                        command_value = 'type=buttonaction&action=release'
                                    elif '.val' in command_value :
                                        command_value = ''
                                    elif command_value == 'Get()':
                                        command_value = 'type=refreshData'
                                        command_index = 0
                                    elif command_value == 'ForceRefresh()':
                                        command_value = 'type=refreshData'
                                    else:

                                        matches = re.match('set\((.*),(.*),(.*)\)', command_value)
                                        if matches is not None and matches.group(2) is not None :
                                            command_index = int(matches.group(1))
                                            parameter_size = int(matches.group(3))
                                            if parameter_size not in [1, 2, 4]:
                                                parameter_size = 1
                                            parameter_value = urllib.quote(matches.group(2))
                                            command_value = 'type=setconfig&value=' +parameter_value + '&size=' + str(parameter_size)
                                        else:
                                            matches = re.match('set\((.*)\)', command_value)
                                            if matches is not None and  matches.group(1) is not None :
                                                command_value = 'type=setvalue&value=' + matches.group(1)
                                            else:
                                                matches = re.match('SwitchAll\((.*)\)', command_value)
                                                if matches is not None and matches.group(1) is not None :
                                                    command_value = 'type=switchall&value=' + matches.group(1)
                                                    command_index = 0

                                    command_value = command_value.replace('%23', '#')
                                else:
                                    raise Exception('command type unsupported: ' + command['type'])

                                if command_index == -1:
                                    raise Exception('command index not found!')
                                command_configuration = {
                                    'class' : command_class,
                                    'value' : command_value,
                                    'index' : command_index,
                                    'instance' : command_instance
                                }
                                #add extra optional attributes
                                if 'repeatEventManagement' in command['configuration']:
                                    command_configuration['repeatEventManagement'] =command['configuration']['repeatEventManagement']
                                if 'minValue' in command['configuration']:
                                    command_configuration['minValue'] = command['configuration']['minValue']
                                if 'maxValue' in command['configuration']:
                                    command_configuration['maxValue'] =command['configuration']['maxValue']
                                if 'returnStateTime' in command['configuration']:
                                    command_configuration['returnStateTime'] =command['configuration']['returnStateTime']
                                if 'returnStateValue' in command['configuration']:
                                    command_configuration['returnStateValue'] =command['configuration']['returnStateValue']

                                my_command = {
                                    'name' : command['name'],
                                    'type' : command['type'],
                                    'isVisible' : 0 if 'isVisible' not in command else command['isVisible'],
                                    'isHistorized' : 0 if 'isHistorized' not in command else command['isHistorized'],
                                    'configuration' : command_configuration
                                }

                                # cmd action can have fallback value
                                if 'value' in command and len(command['value']) != 0 and command['type'] == 'action':
                                    my_command['value'] = command['value']
                                if 'subType' in command :
                                    my_command['subtype'] = command['subType']
                                else:
                                    if 'subtype' in command :
                                        my_command['subtype'] = command['subtype']
                                if 'display' in command :
                                    my_command['display'] = command['display']
                                else:
                                    my_command['display'] = {'generic_type': 'DONT'}
                                if 'template' in command :
                                    my_command['template'] = command['template']
                                if 'unite' in command :
                                    my_command['unite'] = command['unite']
                                    if command['unite'] == '%':
                                        # force min/max %
                                        command_configuration['minValue'] = 0
                                        command_configuration['maxValue'] = 100
                                    if command['unite'] == 'kWh':
                                        # force min Conso 0 kWh
                                        command_configuration['minValue'] = 0
                                if command['type'] == 'action' and command_class == 38:
                                    # ensure dimmer min/max level are set
                                    command_configuration['minValue'] = 0
                                    command_configuration['maxValue'] = 99

                                new_data['commands'].append(my_command)

                        if element == 'recommended' :
                            new_data['recommended'] = data['recommended']

                        if element == 'configuration' :
                            if 'conf_version' not in data['configuration']:
                                new_data['configuration'] = data['configuration']
                except Exception as err:
                    print(name + 'Parsing error: ' +format(err))
                    continue
            if is_pilotWire:
                print('Skip PilotWire: ' + name)
                continue
            with open(destination_file_name, mode='w') as outfile:
                json.dump(obj=new_data, fp=outfile, indent=4, ensure_ascii=True, encoding="utf-8-sig")

        elif name.endswith('.jpg'):
            if rename_images_png:
                destination_file_name = destination_file_name.replace('.jpg', '.png')
            copyfile(source_file_name, destination_file_name)
        else:
            print('Skip assistant: ' + name)
    for dir in dirs:
        destination_manufacturer_folder = os.path.join(destination_folder, dir)
        if not os.path.exists(destination_manufacturer_folder):
            os.makedirs(destination_manufacturer_folder)
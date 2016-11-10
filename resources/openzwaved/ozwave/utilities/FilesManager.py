"""
This file is part of Plugin openzwave for jeedom project
Plugin openzwave for jeedom is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.
Plugin openzwave for jeedom is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.
You should have received a copy of the GNU General Public License along with Plugin openzwave for jeedom.
If not, see http://www.gnu.org/licenses.
"""

import os.path
import shutil
import datetime
import time
from lxml import etree


class FilesManager(object):

    _data_folder = None
    _logging = None
    _not_supported_nodes = None

    def __init__(self, data_folder, not_supported_nodes, logging):
        self._data_folder = data_folder
        self._not_supported_nodes = not_supported_nodes
        self._logging = logging


    def cleanup_configuration_file(self, filename):
        self._logging.info('... check: %s' % (filename,))
        if os.path.isfile(filename):
            try:
                tree = etree.parse(filename)
                nodes = tree.findall(".//{http://code.google.com/p/open-zwave/}Product")
                for node in nodes:
                    if node.get("id")[:7] in self._not_supported_nodes:
                        tree.getroot().remove(node.getparent().getparent())
                    elif node.get("name")[:7] == "Unknown":
                        tree.getroot().remove(node.getparent().getparent())
                working_file = open(filename, "w")
                working_file.write('<?xml version="1.0" encoding="utf-8" ?>\n')
                working_file.writelines(etree.tostring(tree, pretty_print=True))
                working_file.close()
            except Exception as exception:
                self._logging.error(str(exception))
                self._logging.info('Trying to find the most recent valid xml in backups')
                backup_folder = self._data_folder + "/xml_backups"
                # noinspection PyBroadException
                try:
                    os.stat(backup_folder)
                except:
                    os.mkdir(backup_folder)
                pattern = "_zwcfg_"
                filters = ['xml']
                path = os.path.join(backup_folder, "")
                actual_backups = os.listdir(backup_folder)
                actual_backups.sort(reverse=True)
                found_valid_backup = 0
                for candidateBackup in actual_backups:
                    if candidateBackup[-3:] in filters and pattern in candidateBackup:
                        try:
                            tree = etree.parse(os.path.join(backup_folder, candidateBackup))
                            final_filename = candidateBackup[candidateBackup.find('zwcfg'):]
                            shutil.copy2(os.path.join(backup_folder, candidateBackup),
                                         os.path.join(self._data_folder, final_filename))
                            os.chmod(final_filename, 0777)
                            self._logging.info('Found one valid backup. Using it')
                            found_valid_backup = 1
                            break
                        except Exception as exception:
                            self._logging.error(str(exception))
                            continue
                if found_valid_backup == 0:
                    self._logging.info('No valid backup found. Regenerating')


    def check_config_files(self):
        root = self._data_folder
        pattern = "zwcfg_"
        filters = ['xml']
        path = os.path.join(root, "")
        actual_configurations = os.listdir(root)
        self._logging.info('Validate zwcfg configuration file(s)')
        for configuration_file in actual_configurations:
            if configuration_file[-3:] in filters and pattern in configuration_file:
                if configuration_file != 'zwcfg_new.xml':
                    self.cleanup_configuration_file(os.path.join(root, configuration_file))


    def backup_xml_config(self, mode, home_id):
        # backup xml config file
        self._logging.info('Backup xml config file with mode: %s' % (mode,))
        # prepare all variables
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
        xmm_to_backup = self._data_folder + "/zwcfg_" + home_id + ".xml"
        if not os.path.isfile(xmm_to_backup):
            self._logging.error('No config file found to backup')
            return False
        backup_folder = self._data_folder + "/xml_backups"
        backup_name = timestamp + "_" + mode + "_zwcfg_" + home_id + ".xml"
        # check if folder exist (more efficient way)
        # noinspection PyBroadException
        try:
            os.stat(backup_folder)
        except:
            os.mkdir(backup_folder)
        # check if we need to clean the folder
        actual_backups = os.listdir(backup_folder)
        actual_backups.sort()
        for backup in actual_backups:
            if 'manual' in backup:
                actual_backups.remove(backup)
        if len(actual_backups) > 12:
            self._logging.info('More than 12 auto backups found. Cleaning the folder')
            for fileToDelete in actual_backups[:-11]:
                os.unlink(os.path.join(backup_folder, fileToDelete))
        # make the backup
        try:
            final_path = os.path.join(backup_folder, backup_name)
            tree = etree.parse(xmm_to_backup)
            shutil.copy2(xmm_to_backup, final_path)
        except Exception as error:
            self._logging.error('Backup xml failed %s' % (str(error),))
            return False
        self._logging.info('Xml config file successfully backup')
        return True


    def get_openzwave_backups(self):
        backup_list = []
        backup_folder = self._data_folder + "/xml_backups"
        try:
            os.stat(backup_folder)
        except:
            os.mkdir(backup_folder)
        pattern = "_zwcfg_"
        filters = ['xml']
        actual_backups = os.listdir(backup_folder)
        actual_backups.sort(reverse=True)
        for candidateBackup in actual_backups:
            if candidateBackup[-3:] in filters and pattern in candidateBackup:
                backup_list.append(candidateBackup)
        self._logging.debug("List all backups : "+str(backup_list))
        return backup_list


    def remove_unknowns_devices_openzwave_config(self, home_id_str):
        filename = self._data_folder + "/zwcfg_" + home_id_str + ".xml"
        tree = etree.parse(filename)
        nodes = tree.findall(".//{http://code.google.com/p/open-zwave/}Product")
        for node in nodes:
            if node.get("name")[:7] == "Unknown":
                tree.getroot().remove(node.getparent().getparent())
        working_file = open(filename, "w")
        working_file.write('<?xml version="1.0" encoding="utf-8" ?>\n')
        working_file.writelines(etree.tostring(tree, pretty_print=True))
        working_file.close()


    @staticmethod
    def copy_file(new_filename, filename):
        shutil.copy2(new_filename, filename)
        os.chmod(filename, 0777)


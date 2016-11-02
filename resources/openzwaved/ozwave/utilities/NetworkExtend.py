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

import time

from openzwave.controller import ZWaveController

class ControllerMode:
    def __init__(self):
        pass

    class Idle:
        def __init__(self):
            pass

    class AddDevice:
        def __init__(self):
            pass

    class RemoveDevice:
        def __init__(self):
            pass


class NetworkInformation(object):

    Idle = 0
    AddDevice = 1
    RemoveDevice = 5

    _maximum_number_notifications = 5

    def __init__(self, maximum_number_notifications):
        self. _maximum_number_notifications = maximum_number_notifications
        self._actualMode = ControllerMode.Idle
        self._start_time = int(time.time())
        self._awake_time = None
        self._config_file_save_in_progress = False
        self._controller_is_busy = False
        self._controller_state = ZWaveController.STATE_STARTING
        self._last_controller_notifications = [
            {"state": self._controller_state,
             "details": '',
             "error": None,
             "error_description": None,
             "timestamp": int(time.time())}]
        self._error = None
        self._error_description = None

    @property
    def actual_mode(self):
        return self._actualMode

    @actual_mode.setter
    def actual_mode(self, value):
        self._actualMode = value

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    @property
    def config_file_save_in_progress(self):
        return self._config_file_save_in_progress

    @config_file_save_in_progress.setter
    def config_file_save_in_progress(self, value):
        self._config_file_save_in_progress = value

    @property
    def controller_is_busy(self):
        return self._controller_is_busy

    @controller_is_busy.setter
    def controller_is_busy(self, value):
        self._controller_is_busy = value

    @property
    def controller_state(self):
        return self._controller_state

    @property
    def last_controller_notifications(self):
        return self._last_controller_notifications

    @property
    def error(self):
        return self._error

    @property
    def error_description(self):
        return self._error_description

    def set_as_awake(self):
        self._awake_time = int(time.time())
        self.assign_controller_notification(ZWaveController.SIGNAL_CTRL_NORMAL, "Network is awake")

    @property
    def controller_awake_delay(self):
        if self._awake_time is not None:
            return self._awake_time - self._start_time
        return None

    def assign_controller_notification(self, state, details, error=None, error_description=None):
        self._controller_state = state

        if len(self._last_controller_notifications) == self._maximum_number_notifications:
            self._last_controller_notifications.pop()

        self._last_controller_notifications.insert(0, {"state": state,
                                                       "details": details,
                                                       "error": error,
                                                       "error_description": error_description,
                                                       "timestamp": int(time.time())})

        if state == ZWaveController.STATE_WAITING:
            self.controller_is_busy = True
        elif state == ZWaveController.STATE_INPROGRESS:
            self.controller_is_busy = True
        elif state == ZWaveController.STATE_STARTING:
            self.controller_is_busy = True
        else:
            self.controller_is_busy = False
            # reset flag
            self.actual_mode = ControllerMode.Idle

    def generate_jeedom_message(self):
        if self.actual_mode == ControllerMode.AddDevice:
            return self.AddDevice
        elif self.actual_mode == ControllerMode.RemoveDevice:
            return self.RemoveDevice
        else:
            return self.Idle

    def reset(self):
        self._actualMode = ControllerMode.Idle
        self._start_time = int(time.time())
        self._awake_time = None
        self._config_file_save_in_progress = False
        self._controller_is_busy = False
        self._controller_state = ZWaveController.STATE_STARTING
        self._error = None
        self._error_description = None
        self._last_controller_notifications = [{"state": self._controller_state,
                                                "details": '',
                                                "error": self._error,
                                                "error_description": self._error_description,
                                                "timestamp": int(time.time())}]

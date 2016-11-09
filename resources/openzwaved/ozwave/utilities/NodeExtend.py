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

class PendingAssociation(object):
    def __init__(self, pending_added, pending_removed, timeout):
        self._startTime = int(time.time())
        self._pending_added = pending_added
        self._pending_removed = pending_removed
        self._timeOut = timeout
        self._associations = None

    @property
    def pending_added(self):
        return self._pending_added

    @pending_added.setter
    def pending_added(self, value):
        self._pending_added = value
        self._pending_removed = None

    @property
    def pending_removed(self):
        return self._pending_removed

    @pending_removed.setter
    def pending_removed(self, value):
        self._pending_removed = value
        self._pending_added = None

    @property
    def associations(self):
        return self._associations

    @associations.setter
    def associations(self, value):
        self._associations = value

    @property
    def state(self):
        if self._associations is None:
            # is pending
            return 3
        if self._pending_added is not None and self._pending_added in self._associations:
            # the association have be added successfully
            return 1
        if self._pending_removed is not None and not (self._pending_removed in self._associations):
            # the association have be removed successfully
            return 1
        # the association reject
        return 1  # TODO: fix test with multi instances associations


class PendingConfiguration(object):
    def __init__(self, expected_data, timeout):
        self._startTime = int(time.time())
        self._expected_data = expected_data
        self._timeOut = timeout
        self._data = None

    @property
    def expected_data(self):
        return self._expected_data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def state(self):
        if self._data is None:
            # is pending
            return 3
        if self._data != self._expected_data:
            # the node reject changes and set a default
            return 2
        # the parameter have be set successfully
        return 1


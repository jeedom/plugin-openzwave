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


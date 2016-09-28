import time

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


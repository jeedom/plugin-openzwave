import time

class NodeNotification(object):
    def __init__(self, code, wake_up_time=None):
        self._code = code
        self._description = code
        self._help = code
        self._wake_up_time = wake_up_time
        self._next_wake_up = None
        self.refresh(code, wake_up_time)
        self._receive_time = None

    def refresh(self, code, wake_up_time):
        # save notification
        self._code = code
        # reset time stamp
        self._receive_time = int(time.time())
        if self.code == 0:
            self._description = "Completed"
            self._help = "Completed messages"
        elif self.code == 1:
            self._description = "Timeout"
            self._help = "Messages that timeout will send a Notification with this code"
        elif self.code == 2:
            self._description = "NoOperation"
            self._help = "Report on NoOperation message sent completion"
        elif self.code == 3:
            self._description = "Awake"
            self._help = "Report when a sleeping node wakes"
            self._next_wake_up = None  # clear and wait sleep to compute next expected wake up
        elif self.code == 4:
            self._description = "Sleep"
            self._help = "Report when a node goes to sleep"
            # if they go to sleep, compute the next expected wake up time
            if wake_up_time is not None and wake_up_time > 0:
                self._next_wake_up = self._receive_time + wake_up_time
        elif self.code == 5:
            self._description = "Dead"
            self._help = "Report when a node is presumed dead"
        elif self.code == 6:
            self._description = "Alive"
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
    def next_wake_up(self):
        return self._next_wake_up

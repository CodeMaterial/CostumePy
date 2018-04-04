import time


class Event(object):

    def __init__(self, name, data):
        super().__init__()
        self.source = None
        self.name = name
        self.data = data
        self.created = time.time()
        self.action_at = self.created

    def __repr__(self):
        delay = self.action_at - self.created
        return "<%s - {source: %r, name:%r, data:%r, created:%r, delay:%r}>" % \
               (self.__class__.__name__, self.source, self.name, self.data, self.created, delay)


class DelayedEvent(Event):

    def __init__(self, name, data, delay):
        super().__init__(name, data)
        self.action_at += delay

import time

class Event(object):

    def __init__(self, name, data=None, delay=0, source=None):
        super().__init__()
        self.source = source
        self.name = name
        self.data = data
        self.created = time.time()
        self.action_at = self.created + delay

    def __repr__(self):
        delay = self.action_at - self.created
        return "<%s - {source: %r, name:%r, data:%r, created:%r, delay:%r}>" % \
               (self.__class__.__name__, self.source, self.name, self.data, self.created, delay if delay else "None")

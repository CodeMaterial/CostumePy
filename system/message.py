import time


class Message(object):

    def __init__(self, topic, data=None, delay=0, source=None):
        super().__init__()
        self.source = source
        self.topic = topic
        self.data = data
        self.created = time.time()
        self.delay = delay
        self.action_at = self.created + delay

    def __eq__(self, other):
        """Overrides the default implementation"""
        is_equal = True
        if isinstance(other, Message):
            is_equal *= other.topic == self.topic
            if other.source and self.source:
                is_equal *= other.source == self.source
            if other.data and self.data:
                is_equal *= other.data == self.data
            if other.delay and self.delay:
                is_equal *= other.delay == self.delay

        return is_equal

    def __repr__(self):
        return "<%s - {source: %r, topic:%r, data:%r, created:%r, delay:%r}>" % \
               (self.__class__.__name__, self.source, self.topic, self.data, self.created, self.delay)

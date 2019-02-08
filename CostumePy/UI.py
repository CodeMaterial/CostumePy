class UI:
    def __init__(self, node):

        self.elements = {}
        self.node = node

    def _update(self):
        state = {}
        for element_id in self.elements:
            element = self.elements[element_id]
            state[element_id] = element.serialise()
            state[element_id]["type"] = element.__class__.__name__
        self.node.broadcast("_UI_UPDATE", data=state)

    def add_elements(self, *elements):
        for element in elements:
            if element.element_id not in self.elements:
                self.elements[element.element_id] = element
            else:
                raise KeyError("cannot add %r as an element with that name already exists" % element)

        self._update()


class Button:
    def __init__(self, element_id, topic, data=None):
        self.element_id = element_id
        self.topic = topic
        self.data = data

    def serialise(self):
        return {"topic": self.topic, "data": self.data}

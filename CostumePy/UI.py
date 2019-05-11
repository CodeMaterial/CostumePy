import logging

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

        state["running"] = self.node.running
        self.node.broadcast("_UI_UPDATE", data=state)

    def add_elements(self, *elements):
        for element in elements:
            if element.element_id not in self.elements:
                self.elements[element.element_id] = element
            else:
                raise KeyError("cannot add %r as an element with that name already exists" % element)

        self._update()

    def set_elements(self, *elements):
        self.elements = {}
        self.add_elements(*elements)

    def remove_elements(self, *element_ids):
        for element_id in element_ids:
            del self.elements[element_id]
            logging.info("removed element ", element_id)
        self._update()

    def get_element(self, element_id):
        return self.elements[element_id]

    def replace(self, element_id, element):
        self.elements[element_id] = element
        self._update()


class Text:

    def __init__(self, element_id, text="None", text_class="text-justify"):
        self.element_id = element_id
        self.text = text
        self.text_class = text_class

    def serialise(self):
        return {"text": self.text, "text_class": self.text_class}


class Button:
    def __init__(self, element_id, text, topic, data=None, button_class="btn-default"):
        self.element_id = element_id
        self.text = text
        self.topic = topic
        self.data = data
        self.button_class = button_class

    def serialise(self):
        return {"text": self.text, "topic": self.topic, "data": self.data, "button_class": "btn " + self.button_class}

import logging


class UI:
    def __init__(self, node):

        self.elements = {}
        self.node = node

    def update(self):
        state = {}
        for element_id in self.elements:
            o = self.elements[element_id]["order"]
            state["%02i_%s" % (o, element_id)] = self.elements[element_id]

        state["running"] = self.node.running  # Wait this shouldn't work... This will be interpreted as a node by the web framework
        self.node.broadcast("_UI_UPDATE", data=state)

    def add_text(self, element_id, text="None", text_class="", order=99):
        if element_id not in self.elements:
            self.elements[element_id] = {"type": "Text", "text": text, "text_class": text_class, "order": order}
        else:
            logging.error("Cannot create new UI element with id %s because it already exists" % element_id)
        return NotImplemented

    def add_button(self, element_id, text="Not Defined", topic=None, data=None, button_class="btn btn-default", order=99):
        if element_id not in self.elements:
            self.elements[element_id] = {"type": "Button", "text": text, "topic": topic, "data": data, "button_class": button_class, "order": order}
        else:
            logging.error("Cannot create new UI element with id %s because it already exists" % element_id)
        return NotImplemented

    def add_break(self, element_id, order=99):
        self.elements[element_id] = {"type": "Break", "order": order}

    def get(self, element_id):
        return self.elements[element_id]
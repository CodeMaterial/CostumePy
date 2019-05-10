import time
import json
from flask import *

import CostumePy
import logging

all_states = {}

update_pending = False


def death(msg):
    global all_states, update_pending
    node_name = msg["source"]
    logging.info("Node %s has died" % node_name)
    del all_states[node_name]
    update_pending = True


def update_ui(msg):
    global all_states, update_pending
    node_name = msg["source"]
    node_state = msg["data"]
    all_states[node_name] = node_state
    update_pending = True


CostumePy.set_node_name("UI")

CostumePy.listen("_UI_UPDATE", update_ui)
CostumePy.listen("death", death)

app = Flask(__name__)


def state_collector():
    global update_pending
    while True:
        # while not update_pending:
        #     time.sleep(0.01)
        # update_pending = False
        time.sleep(.1)
        yield 'data: %s\n\n' % json.dumps(all_states)


@app.route('/state_stream')
def state_stream():
    return Response(state_collector(), mimetype='text/event-stream')


@app.route('/broadcast', methods=['POST'])
def broadcast():
    topic = request.form['topic']
    try:
        data = json.loads(request.form['data'])
    except:
        logging.warning("can't parse form data, reading in raw")
        data = request.form['data']

    if data is None:
        CostumePy.broadcast(topic)
    else:
        CostumePy.broadcast(topic, data=data)

    return "Done", 200, {'Content-Type': 'text/plain'}


@app.route('/')
def root():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
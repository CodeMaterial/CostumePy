import time

def message(topic, data=None, delay=0, source=None):
        created = time.time()
        return {"source": source,
                "topic": topic,
                "data": data,
                "created": created,
                "delay": delay,
                "action_at": created + delay
                }
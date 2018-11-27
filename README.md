# :tophat: Costume Py :tophat:

CostumePy is a library designed to allow developers to create smart wearable costumes. 
The overall aim is to create a more dynamic programming style compared to the linear `while True:` systems.

## greeter.py

This node listens for movement messages and broadcasts a greeting message in response 

```python
import CostumePy


def movement_callback(message, name):

    if message == True:
        CostumePy.broadcast("greeting", data="Hello %s!" % name)
    else:
        CostumePy.broadcast("greeting", data="Goodbye %s!" % name)


if __name__ == "__main__":

    CostumePy.init("world greeter")

    CostumePy.listen("movement", movement_callback, args="world")


    while CostumePy.is_running():
        print("Listening")
        CostumePy.limit(1) #  In frames per second
```


## greeter_test.py

This file tests the greeter node.

```python
import CostumePy

wgt = CostumePy.test("world greeter")

if not wgt.responding():
    print("agh not responding!")


msg_in = CostumePy.message("movement", data=True)
msg_out = CostumePy.message("greeting", data="Hello world!")

hello_results = wgt.is_equal(msg_in, msg_out)

if hello_results == False:
    print("hello world isn't working")

msg_in = CostumePy.message("movement", data=False)
msg_out = CostumePy.message("greeting", data="Goodbye world!")

goodbye_results = wgt.is_equal(msg_in, msg_out)

if goodbye_results == False:
    print("goodbye world isn't working")

```


### main.py

To start the suit we simply need to run the following code. The inject command sends a `NOSE_PRESS` event to the system to simulate GPIO input.

```python
import time
import CostumePy

costume_manager = CostumePy.launch_costume("example.suit")

time.sleep(1)

costume_manager.inject("NOSE_PRESS")
```

## Example Output

```
TODO
```


## Versioning

This project is still in development so please expect wild code changes.

## Contributors

If you would like to contribute to this project please contact one of the below authors.

## Current Authors

* **Samuel Martin** - [**sam@codematerial.com**](sam@codematerial.com)
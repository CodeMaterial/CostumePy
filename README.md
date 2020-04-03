# :tophat: Costume Py :tophat:

:warning: **This library is depreciated as it is slow**: If that is an issue, please check out ROS as it has similar functionality but is much faster


CostumePy is a library designed to allow developers to create smart wearable costumes. 
The overall aim is to create a more ROS-like, dynamic programming style compared to the linear `while True:` systems.


Here is an example file which listens for a nose_press message then reacts with a callback

```python
import CostumePy


def nose_press_function(msg):
    print("You pressed my nose %s!" % msg["data"])


CostumePy.listen("nose_press", nose_press_function)

CostumePy.broadcast("nose_press", data="hard")
```

## Installation

CostumePy is currently only compatible with Python 3.x

If you've installed Python 3 directly yourself simply run:

```commandline
python setup.py install

```

If you're using a Raspberry Pi or a machine with both Python 2 and 3 installed, replace ```python``` with ```python3```

## CostumePy Server

To use CostumePy, you first have to launch the server. To start the server run:

```commandline
python -m CostumePy.server
```

To run this in the background on a Linux system, append the command with an ``` &```

If you try to use CostumePy without the server, you will get the following error when trying to broadcast or listen to a topic:

```commandline
  File "/usr/local/lib/python3.5/dist-packages/CostumePy-0.0.1-py3.5.egg/CostumePy/cospy_node.py", line 33, in _request_socket_ip
ConnectionRefusedError: Cannot contact manager, has it been started?
```

## Testing

If you wish to test CostumePy. Simply run the following command in the CostumePy directory:

```commandline
python -m unittest discover -s tests -v
```

This will search for all files starting with ```test_``` in the ```tests``` directory.

If you want to create your own tests for new features, please have a look at ```test_basic_functionality.py``` to see how to structure your tests.

## Versioning

This project is still in development so please expect wild code changes.

## Contributors

If you would like to contribute to this project please contact me below.

## Current Authors

* **Samuel Martin** - [**sam@codematerial.com**](sam@codematerial.com)

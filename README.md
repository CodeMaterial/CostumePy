# :tophat: Costume Py :tophat:
[![Build status](https://travis-ci.org/CodeMaterial/CostumePy.svg?branch=master)](https://travis-ci.org/CodeMaterial)


CostumePy is a library designed to allow developers to create smart wearable costumes. 
The overall aim is to create a more ROS-like, dynamic programming style compared to the linear `while True:` systems.


Here is an example file which listens for a nose_press message then reacts with a callback

```python
import CostumePy


def nose_press_function(msg):
    print("You pressed my nose %s!" % msg["data"])


CostumePy.listen_to("nose_press", nose_press_function)

CostumePy.broadcast("nose_press", data="hard")
```

## Versioning

This project is still in development so please expect wild code changes.

## Contributors

If you would like to contribute to this project please contact one of the below authors.

## Current Authors

* **Samuel Martin** - [**sam@codematerial.com**](sam@codematerial.com)
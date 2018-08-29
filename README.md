# :tophat: Costume Py :tophat:

Costume Py is a library designed to allow developers to create smart wearable costumes. 
The overall aim is to create a more dynamic programming style compared to the classical *while True* systems.

## Getting Started

Each part of the system is a `CostumeModule` which can be run, tested and called concurrently.
Below I am going to give some example modules

### Example  File Structure

A quick overview of the expected file structure.

```text
CostumePy/

modules/
    __init__.py
    button.py
    led.py
    #your modules here

tests/
    __init__.py
    button_test.py
    #your tests here

main.py
example.suit
```

### button.py

A simple module listening for a `NOSE_PRESS` event. This is just to spoof a physical GPIO input.
When the nose is pressed, it will broadcast a blush on event and a blush off event 5 seconds later.


```python
import logging
from CostumePy.system.costume_modules import CostumeModule


class Button(CostumeModule):

    def __init__(self):
        super().__init__()

        self.listeners["NOSE_PRESS"] = self.cute_input

    def cute_input(self, event):

        logging.info("Cute input detected!")

        self.broadcast("BLUSH", data=True)
        self.broadcast("BLUSH", data=False, delay=5)
```

### led.py

A simple module which on blush will set the blush variable to be true. This is just to spoof a physical GPIO output.


```python
import logging
from CostumePy.system.costume_modules import CostumeModule


class BlushLED(CostumeModule):

    def __init__(self):
        super().__init__()

        self.listeners["BLUSH"] = self.blush

        self.blush_status = False

    def blush(self, event):

        if event.data:
            logging.info("blushing on")
            self.blush_status = True
        else:
            logging.info("blushing off")
            self.blush_status = False
```

## button_test.py

Using the `_test.py` suffix we can write tests to automatically check whether modules are behaving as they should.
Make sure that your files follow the same naming convetion as this example.

```python
from CostumePy.system.unit_test import UnitTest


class ButtonTest(UnitTest):

    def test_blush_on(self):

        self.send_input("NOSE_PRESS", data=True)

        self.check_output("BLUSH")

    def test_blush_off(self):

        self.send_input("NOSE_PRESS", data=True)

        self.check_output("BLUSH", data=True)
        self.check_output("BLUSH", data=False, delay=5)
```

### main.py

To start the suit we simply need to run the following python code. The inject command sends a `NOSE_PRESS` event to the system to simulate GPIO input.

```python
import time
from CostumePy.costume import launch_costume

costume_manager = launch_costume("example.suit")

time.sleep(1)

costume_manager.inject("NOSE_PRESS")
```


### example.suit

We also need a config file to show which modules to include in the suit. Prefixing these with a # will comment out that line

```
modules.button -> Button
modules.led -> BlushLED
#modules.soundbox -> SoundBox
```

## Versioning

This project is still in development so please expect wild code changes.

## Contributors

If you would like to contribute to this project please contact one of the below authors.

## Current Authors

* **Samuel Martin** - [**sam@codematerial.com**](sam@codematerial.com)
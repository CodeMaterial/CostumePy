# :tophat: Costume Py :tophat:

CostumePy is a library designed to allow developers to create smart wearable costumes. 
The overall aim is to create a more dynamic programming style compared to the linear `while True:` systems.

## Getting Started

Each part of the system is a `CostumeModule` which can be run, tested and communicated with concurrently.
Below I am going to give some example modules.

### Example  File Structure

A quick overview of the expected file structure.

```text
CostumePy/

modules/
    __init__.py
    button.py
    led.py

tests/
    __init__.py
    button_test.py

example.suit
main.py

```

### button.py

A simple module listening for a `NOSE_PRESS` event. This is just a spoof of a physical GPIO input.
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

A simple module which, on blush, will set the blush variable to be true. This is just to spoof a physical GPIO output.


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

Using the `_test.py` file suffix and `test_` function prefix, we can write tests to automatically check whether modules are behaving as they should.
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


### example.suit

We also need a config file to show which modules to include in the suit. Prefixing these with a # will comment out that line

```
modules.button -> Button
modules.led -> BlushLED
```

### main.py

To start the suit we simply need to run the following code. The inject command sends a `NOSE_PRESS` event to the system to simulate GPIO input.

```python
import time
from CostumePy.costume import launch_costume

costume_manager = launch_costume("example.suit")

time.sleep(1)

costume_manager.inject("NOSE_PRESS")
```

## Example Output

```text
2018-08-29 01:13:55,569 [INFO ] MainProces -> costume          ---------- Starting Costume ----------
2018-08-29 01:13:55,607 [INFO ] MainProces -> event_manager    Testing module Button
2018-08-29 01:13:55,609 [INFO ] MainProces -> costume_modules  Initialised
2018-08-29 01:13:55,611 [INFO ] MainProces -> unit_test        Clearing queues
2018-08-29 01:13:55,612 [INFO ] MainProces -> unit_test        testing test_blush_off...
2018-08-29 01:13:55,613 [INFO ] Button     -> costume_modules  Starting idle
2018-08-29 01:13:55,647 [INFO ] Button     -> button           Cute input detected!
2018-08-29 01:13:55,660 [INFO ] MainProces -> unit_test        test_blush_off passed
2018-08-29 01:13:55,661 [INFO ] MainProces -> unit_test        Clearing queues
2018-08-29 01:13:55,661 [INFO ] MainProces -> unit_test        testing test_blush_on...
2018-08-29 01:13:55,693 [INFO ] Button     -> button           Cute input detected!
2018-08-29 01:13:55,693 [INFO ] MainProces -> unit_test        test_blush_on passed
2018-08-29 01:13:55,727 [INFO ] Button     -> costume_modules  Shutting down
2018-08-29 01:13:55,729 [INFO ] MainProces -> unit_test        test_shutdown Passed, Module shutdown in 0.04 seconds
2018-08-29 01:13:55,730 [INFO ] MainProces -> unit_test        ButtonTest Passed!
2018-08-29 01:13:55,730 [INFO ] MainProces -> costume_modules  Initialised
2018-08-29 01:13:55,732 [INFO ] MainProces -> event_manager    Testing module BlushLED
2018-08-29 01:13:55,732 [ERROR] MainProces -> event_manager    Cannot load BlushLEDTest, does it exist?
2018-08-29 01:13:55,733 [INFO ] MainProces -> costume_modules  Initialised
2018-08-29 01:13:55,737 [INFO ] BlushLED   -> costume_modules  Starting idle
2018-08-29 01:13:55,737 [INFO ] MainProces -> costume          rorschach.suit launched in 0.17 seconds!
2018-08-29 01:13:55,741 [INFO ] Button     -> costume_modules  Starting idle
2018-08-29 01:13:56,759 [INFO ] Button     -> button           Cute input detected!
2018-08-29 01:13:56,777 [INFO ] BlushLED   -> LED              blushing on
2018-08-29 01:14:01,842 [INFO ] BlushLED   -> LED              blushing off
2018-08-29 01:14:06,582 [INFO ] BlushLED   -> costume_modules  Shutting down
2018-08-29 01:14:06,583 [INFO ] Button     -> costume_modules  Shutting down
```


## Versioning

This project is still in development so please expect wild code changes.

## Contributors

If you would like to contribute to this project please contact one of the below authors.

## Current Authors

* **Samuel Martin** - [**sam@codematerial.com**](sam@codematerial.com)
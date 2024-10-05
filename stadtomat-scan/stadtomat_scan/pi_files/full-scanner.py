import RPi.GPIO as GPIO
import time
import logging
from button import Button
from take_picture import main

log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)


def scan_table():
    main()


if __name__ == "__main__":
    print("scan table started")
    GPIO.setmode(GPIO.BCM)
    button = Button(17)
    try:
        while True:
            time.sleep(0.1)
            if button.is_pressed_for():
                scan_table()
                log.debug("Button is pressed")
            else:
                log.debug("Button is not pressed")
    except KeyboardInterrupt:
        log.info("Exiting")
    finally:
        GPIO.cleanup()
        log.info("GPIO cleaned up")

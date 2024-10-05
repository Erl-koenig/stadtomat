import RPi.GPIO as GPIO
import time

# Use GPIO 17 (nr 11) 6th pin from the end on the left side, when usb is faceing to you
# Use Ground nr. 6, 3rd pin from the end on the right side, when usb is faceing to you

class Button:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def is_pressed(self):
        return not GPIO.input(self.pin)

    def is_pressed_for(self, min_duration=0.0, max_duration=1.0):
        if self.is_pressed():
            start_time = time.time()
            while self.is_pressed():
                elapsed_time = time.time() - start_time
                if elapsed_time >= max_duration:
                    return False
            if min_duration <= elapsed_time <= max_duration:
                return True
        return False

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    button = Button(17)

    while True:
        time.sleep(0.1)
        if button.is_pressed_for():
            print("Button is pressed")
        else:
            print("Button is not pressed")

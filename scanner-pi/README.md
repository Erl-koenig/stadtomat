# Image QR Code Scanner

Thanks to [https://github.com/vasani-arpit/image-qr-code-scanner](https://github.com/vasani-arpit/image-qr-code-scanner) which gave the base for this poc.

Trying to scan QR code and found out, that retrieve x and y coordinates is also possible.
Can scann multiple qr codes at a time and retrieve their coordinates.

## Python Virtual Env

It's highly recommendet, to use python virtual env in python, to not conflict with other installations on the system.

If you skip this, you'll have to install the packages globally on the system.

### Setup

```bash
sudo apt install python3-venv  # install the venv package, if not already installed.
python3 -m venv env  # creates a new env folder
source env/bin/activate  # use the created env
```

now you're ready to continue with the installation.

### Additional GPIO Packages

```bash
sudo apt-get install python3-rpi.gpio
```

## Installation

1. Install python3 and pip3 in server/machine
1. Install requirements globally using
        `pip3 install pyzbar opencv-python argparse`
        or
        `pip3 install -r requirements.txt`
1. make sure have following linux dependencies installed 
        `sudo apt install -y libzbar0 libsm6 libxext6 libxrender-dev`

## Use with python

run command

```bash
python scanner.py --input variable-sizes-start-15mm.png
```

## PI Camera

cmd to take single shot with pi cam.

libcamera-still -q 100 -o test.jpg

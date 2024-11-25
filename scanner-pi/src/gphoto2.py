import subprocess
import logging

log = logging.getLogger(__name__)


def take_picture():
    folder_path = "img/"
    cmd_take_picture = f"gphoto2 --capture-image-and-download --filename {folder_path}/%Y%m%d%H%M%S.jpg -q"
    try:
        process = subprocess.run(
            cmd_take_picture,
            shell=True,
            capture_output=True,
            text=True,
        )
        if process.returncode != 0:
            log.error(f"Error: {process.stderr}")
        else:
            log.debug(f"Picture taken: {process.stdout}")
    except Exception as e:
        log.error(e)
    return True


def get_camera_list():
    cmd_auto_detect = "gphoto2 --auto-detect"
    camera_list = []
    try:
        process = subprocess.run(
            cmd_auto_detect,
            shell=True,
            capture_output=True,
            text=True,
        )
        if process.returncode == 0:
            camera_list = process.stdout.split("\n")
        else:
            log.error(f"Error: {process.stderr}")
    except Exception as e:
        log.error(e)
    return camera_list


def get_battery_level():
    cmd_battery_level = (
        "gphoto2 --get-config=batterylevel | grep Current: | cut -d ' ' -f2"
    )

    battery_level = 0
    try:
        process = subprocess.run(
            cmd_battery_level,
            shell=True,
            capture_output=True,
            text=True,
        )
        if process.returncode == 0:
            battery_level = process.stdout.strip()
        else:
            log.error(f"Error: {process.stderr}")
    except Exception as e:
        log.error(e)
    return battery_level

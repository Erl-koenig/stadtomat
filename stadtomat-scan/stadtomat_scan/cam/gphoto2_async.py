import asyncio


async def take_picture():
    cmd_take_picture = (
        "gphoto2 --capture-image-and-download --filename %Y%m%d%H%M%S.jpg -q"
    )
    try:
        process = await asyncio.create_subprocess_shell(
            cmd_take_picture,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            print(f"Error: {stderr.decode('utf-8')}")
        else:
            print(f"Picture taken: {stdout.decode('utf-8')}")
    except Exception as e:
        print(e)
    return True


async def get_camera_list():
    cmd_auto_detect = "gphoto2 --auto-detect"
    camera_list = []
    try:
        process = await asyncio.create_subprocess_shell(
            cmd_auto_detect,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            camera_list = stdout.decode("utf-8").split("\n")
        else:
            print(f"Error: {stderr.decode('utf-8')}")
    except Exception as e:
        print(e)
    return camera_list


async def get_battery_level():
    cmd_battery_level = (
        "gphoto2 --get-config=batterylevel | grep Current: | cut -d ' ' -f2"
    )

    battery_level = 0
    try:
        process = await asyncio.create_subprocess_shell(
            cmd_battery_level,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            battery_level = stdout.decode("utf-8").strip()
        else:
            print(f"Error: {stderr.decode('utf-8')}")
    except Exception as e:
        print(e)
    return battery_level

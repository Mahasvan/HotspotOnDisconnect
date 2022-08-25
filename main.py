import os
import pathlib
import time
import subprocess

try:
    import requests
except ImportError:
    print("Please install requests module")
    exit(1)

import misc

enable_file = pathlib.Path(os.path.dirname(os.path.realpath(__file__)) + "/turn_on_hotspot.bat").absolute()
disable_file = pathlib.Path(os.path.dirname(os.path.realpath(__file__)) + "/turn_off_hotspot.bat").absolute()
hotspot_on = False
timeout = 10

print(misc.colour_blue("Starting script..."))
while True:
    url = "https://google.com"
    try:
        r = requests.get(url)
        status_code = r.status_code
    except:
        status_code = 404

    if status_code != 200:
        if hotspot_on:
            # the hotspot is already on, we don't need to turn it on again
            continue
        # print response code
        misc.print_message(misc.colour_yellow("Response code: " + str(status_code)))

        misc.print_message(misc.colour_blue("Turning on hotspot..."))

        command = subprocess.run(str(enable_file), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        if command.returncode != 0:
            misc.print_message(misc.colour_red("Hotspot could not be turned on!"))
        else:
            # hotspot is now on
            misc.print_message(misc.colour_green("Hotspot turned on!"))
            hotspot_on = True

    else:
        # response code is 200, we have internet!
        if not hotspot_on:
            # the hotspot is already off, we don't need to turn it off again
            continue

        misc.print_message(misc.colour_yellow("Response code: " + str(status_code)))
        misc.print_message(misc.colour_blue("Turning off hotspot..."))

        command = subprocess.run(str(disable_file), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        if command.returncode == 0:
            # hotspot is now off
            misc.print_message(misc.colour_green("Hotspot turned off"))
            hotspot_on = False
        else:
            misc.print_message(misc.colour_red("Hotspot could not be turned off!"))

    time.sleep(timeout)

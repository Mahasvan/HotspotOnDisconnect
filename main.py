import json
import os
import time
import subprocess

import misc

with open("config.json") as f:
    config = json.load(f)

ssid = config.get("ssid").replace("\"", "")
password = config.get("password").replace("\"", "")

setup_command = f"netsh wlan set hostednetwork mode=allow ssid=\"{ssid}\" key=\"{password}\""
enable_command = f"netsh wlan start hostednetwork"
disable_command = f"netsh wlan stop hostednetwork"

timeout = 10

print(misc.colour_blue("Starting script..."))
print(misc.colour_yellow("Pulling from git..."))
os.system("git pull")

print(misc.colour_blue("Setting up hotspot..."))
subprocess.run(setup_command, shell=True)
print(misc.colour_blue("Hotspot setup complete!"))

while True:
    time.sleep(timeout)
    url = "google.com"
    misc.print_message(misc.colour_yellow("Pinging: "+url))
    hotspot_status = misc.check_hotspot_status()
    try:
        ping_command = subprocess.run(["ping", url, "/n", "1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status_code = ping_command.returncode
    except:
        status_code = 1

    if status_code != 0:
        if misc.check_hotspot_status().lower().strip() == "started":
            # the hotspot is already on, we don't need to turn it on again
            continue
        else:
            misc.print_message(misc.colour_cyan(f"Hotspot Status: {hotspot_status}"))

        # print response code
        misc.print_message(misc.colour_yellow("Response code: " + str(status_code)))

        misc.print_message(misc.colour_blue("Turning on hotspot..."))
        # turn on hotspot
        command = subprocess.run(str(enable_command), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        if misc.check_hotspot_status().lower().strip() != "started":
            misc.print_message(misc.colour_red("Hotspot could not be turned on!"))
        else:
            # hotspot is now on
            misc.print_message(misc.colour_green("Hotspot turned on!"))

    else:
        # response code is 0, we have internet!
        if not misc.check_hotspot_status().lower().strip() == "started":
            # the hotspot is already off, we don't need to turn it off again
            continue

        misc.print_message(misc.colour_yellow("Response code: " + str(status_code)))
        misc.print_message(misc.colour_blue("Turning off hotspot..."))
        # turn off hotspot
        command = subprocess.run(str(disable_command), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        if misc.check_hotspot_status().strip().lower() in ("stopped", "not started"):
            # hotspot is now off
            misc.print_message(misc.colour_cyan(f"Hotspot Status: {misc.check_hotspot_status()}"))
            misc.print_message(misc.colour_green("Hotspot turned off"))
        else:
            misc.print_message(misc.colour_red("Hotspot could not be turned off!"))

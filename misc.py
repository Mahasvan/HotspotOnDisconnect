import datetime
import re
import time
import subprocess

def unix_time_to_readable(unix_seconds: int):
    return datetime.datetime.fromtimestamp(unix_seconds)


pink = "\033[95m"
blue = "\033[94m"
cyan = "\033[96m"
green = "\033[92m"
yellow = "\033[93m"
red = "\033[91m"
bold = "\033[1m"
underline = "\033[4m"
end_formatting = "\033[0m"


def colour_pink(text):
    return pink + text + end_formatting


def colour_blue(text):
    return blue + text + end_formatting


def colour_cyan(text):
    return cyan + text + end_formatting


def colour_green(text):
    return green + text + end_formatting


def colour_yellow(text):
    return yellow + text + end_formatting


def colour_red(text):
    return red + text + end_formatting


def format_bold(text):
    return bold + text + end_formatting


def format_underline(text):
    return underline + text + end_formatting


def print_message(message):
    print(unix_time_to_readable(int(time.time())), ":", message)


def check_hotspot_status():
    command = "netsh wlan show hostednetwork"
    status_regex = r"(?<=Status)\s+:\s+(.*)\n"
    output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    status = re.findall(status_regex, output.stdout.decode("utf-8"))[0]
    return status

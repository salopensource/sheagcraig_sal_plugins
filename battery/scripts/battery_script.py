#!/usr/local/sal/Python.framework/Versions/3.8/bin/python3
"""Shamelessly taken from https://github.com/chilcote/unearth
with minor changes to use "plistlib.loads" by Nathan Darnell"""


import plistlib
import subprocess

import sal


def main():
    data = battery_facts()
    sal.add_plugin_results('Battery', data)


def battery_facts():
    """Returns the battery health"""

    result = {}

    try:
        proc = subprocess.Popen(
            ["/usr/sbin/ioreg", "-r", "-c", "AppleSmartBattery", "-a"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, _ = proc.communicate()
        if stdout:
            d = plistlib.loads(stdout)[0]
            result['BatteryHealth'] = "Healthy" if not d["PermanentFailureStatus"] else "Failing"
            result['MaxCapacity'] = d["MaxCapacity"]
            result['DesignCapacity'] = d["DesignCapacity"]
            result['CycleCount'] = d["CycleCount"]
            result['DesignCycleCount9C'] = d["DesignCycleCount9C"]
    except (IOError, OSError):
        pass

    return result


if __name__ == "__main__":
    main()

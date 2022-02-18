#!/usr/local/sal/Python.framework/Versions/Current/bin/python3
"""Shamelessly taken from https://github.com/chilcote/unearth
with minor changes to use "plistlib.loads" by Nathan Darnell"""


import os
import plistlib
import subprocess

import sal


def main():
    data = battery_facts()
    sal.add_plugin_results("Battery", data)


def battery_facts():
    """Returns the battery health"""

    result = {}

    # Determine architecture from:
    # https://github.com/munki/munki/blob/main/code/client/munkilib/info.py
    arch = os.uname()[4]
    if arch == "x86_64":
        # we might be natively Intel64, or running under Rosetta.
        # os.uname()[4] returns the current execution arch, which under Rosetta
        # will be x86_64. Since what we want here is the _native_ arch, we're
        # going to use a hack for now to see if we're natively arm64
        uname_version = os.uname()[3]
        if "ARM64" in uname_version:
            arch = "arm64"

    try:
        proc = subprocess.Popen(
            ["/usr/sbin/ioreg", "-r", "-c", "AppleSmartBattery", "-a"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, _ = proc.communicate()
        if stdout:
            d = plistlib.loads(stdout)[0]
            result["BatteryHealth"] = (
                "Healthy" if not d["PermanentFailureStatus"] else "Failing"
            )
            if arch == "x86_64":
                result["MaxCapacity"] = d["MaxCapacity"]
            else:
                result["MaxCapacity"] = d["AppleRawMaxCapacity"]
            result["DesignCapacity"] = d["DesignCapacity"]
            result["CycleCount"] = d["CycleCount"]
            result["DesignCycleCount9C"] = d["DesignCycleCount9C"]
    except (IOError, OSError):
        pass

    return result


if __name__ == "__main__":
    main()

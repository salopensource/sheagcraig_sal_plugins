#!/usr/bin/python


import os
import plistlib
import subprocess


RESULTS_PATH = "/usr/local/sal/plugin_results.plist"


def main():
    munki_present = False

    try:
        results = subprocess.check_output(["profiles", "-Lo", "stdout-xml"])
    except subprocess.CalledProcessError:
        results = ""

    if results:
        profiles = plistlib.readPlistFromString(results)
        munki_profile = [p for p in profiles["_computerlevel"] if
                         p["ProfileIdentifier"] == "sas.profiles.munki"][0]

        if munki_profile:
            munki_present = True

    formatted_results = {"plugin": "ManagementCompliance",
                         "historical": False,
                         "data": {"MunkiProfilePresent": munki_present}}

    if os.path.exists(RESULTS_PATH):
        plugin_results = plistlib.readPlist(RESULTS_PATH)
    else:
        plugin_results = []

    plugin_results.append(formatted_results)

    plistlib.writePlist(plugin_results, RESULTS_PATH)


if __name__ == "__main__":
    main()
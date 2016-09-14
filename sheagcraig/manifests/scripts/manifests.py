#!/usr/bin/python


import os
import plistlib


RESULTS_PATH = "/usr/local/sal/plugin_results.plist"


def main():
    client_manifest_path = (
        "/Library/Managed Installs/manifests/client_manifest.plist")
    if os.path.exists(client_manifest_path):
        client_manifest = plistlib.readPlist(client_manifest_path)
    else:
        client_manifest = {}

    formatted_results = {
        "plugin": "Manifests",
        "historical": False,
        "data": {"included_manifests": "+".join(
            client_manifest.get("included_manifests", []))}}

    if os.path.exists(RESULTS_PATH):
        plugin_results = plistlib.readPlist(RESULTS_PATH)
    else:
        plugin_results = []

    plugin_results.append(formatted_results)

    plistlib.writePlist(plugin_results, RESULTS_PATH)


if __name__ == "__main__":
    main()
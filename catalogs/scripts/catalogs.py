#!/usr/bin/python

import os
import plistlib
from Foundation import CFPreferencesCopyAppValue


RESULTS_PATH = "/usr/local/sal/plugin_results.plist"


def main():
    managed_install_dir = CFPreferencesCopyAppValue(
                          'ManagedInstallDir', 'ManagedInstalls')
    manifest_dir = os.path.join(managed_install_dir, 'manifests')

    # Report file
    report = os.path.join(managed_install_dir, 'ManagedInstallReport.plist')

    if os.path.exists(report):
        manifest_name = plistlib.readPlist(report).get('ManifestName', None)
        client_manifest = os.path.join(manifest_dir, manifest_name)
    else:
        # Munki 2 path
        client_manifest = os.path.join(manifest_dir, 'client_manifest.plist')

    # Read the client manfiest
    if os.path.exists(os.path.join(manifest_dir, client_manifest)):
        client_manifest = plistlib.readPlist(client_manifest)
    else:
        client_manifest = {}

    # Get the catalogs for reporting
    formatted_results = {
        "plugin": "Catalogs",
        "historical": False,
        "data": {"Catalogs": "+".join(client_manifest.get("catalogs", []))}}

    if os.path.exists(RESULTS_PATH):
        plugin_results = plistlib.readPlist(RESULTS_PATH)
    else:
        plugin_results = []

    plugin_results.append(formatted_results)

    plistlib.writePlist(plugin_results, RESULTS_PATH)


if __name__ == "__main__":
    main()

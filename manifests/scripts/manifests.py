#!/usr/bin/python


import os
import plistlib
import sys

sys.path.append('/usr/local/munki')
import munkilib.updatecheck.manifestutils
sys.path.append('/usr/local/sal')
import utils


def main():
    client_manifest_path = munkilib.updatecheck.manifestutils.get_primary_manifest()
    if os.path.exists(client_manifest_path):
        client_manifest = plistlib.readPlist(client_manifest_path)
    else:
        client_manifest = {}

    # Drop any blank entries and trim WS.
    manifests = [m.strip() for m in client_manifest.get("included_manifests", []) if m]
    if not manifests:
        manifests = ["NO INCLUDED MANIFESTS"]
    utils.add_plugin_results('Manifests', {"included_manifests": "+".join(manifests)})


if __name__ == "__main__":
    main()
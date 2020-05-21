#!/usr/local/sal/Python.framework/Versions/3.8/bin/python3


import plistlib
import subprocess
import sys
import tempfile
from distutils.version import LooseVersion

import sal


MANUAL_PROFILE_DISPLAY_NAME = 'Root MDM Profile'
DEP_PROFILE_DISPLAY_NAME = 'MobileIron Cloud DEP MDM Profile'


def main():
    result = {}

    # 10.13.4 is when the profiles command gained the ability to
    # report on UAMDM status.
    if os_version() < LooseVersion('10.13.4'):
        result['mdm_status'] = get_enrollment_from_mdm_profile()

    else:
        status = profiles_status()
        if status.get('Enrolled via DEP') == 'Yes':
            result['mdm_status'] = 'DEP'
        else:
            result['mdm_status'] = 'Manually Enrolled' if 'Yes' in status.get('MDM enrollment', '') else 'No'

    sal.add_plugin_results('mdm_enrollment', result)


def os_version():
    cmd = ['/usr/bin/sw_vers', '-productVersion']
    output = subprocess.check_output(cmd, text=True)
    return LooseVersion(output)


def profiles_status():
    cmd = ['/usr/bin/profiles', 'status', '-type', 'enrollment']
    try:
        result = subprocess.check_output(cmd, text=True)
    except subprocess.CalledProcessError:
        result = ''

    parsed = {}
    for line in result.splitlines():
        key, val = line.split(':')
        parsed[key.strip()] = val.strip()

    return parsed


def get_enrollment_from_mdm_profile():
    mdm_enrolled = False
    cmd = ['/usr/bin/profiles', '-C', '-o', 'stdout-xml']
    plist_text = subprocess.check_output(cmd, text=True)
    plist = plistlib.readPlistFromString(plist_text)

    for profile in plist.get('_computerlevel', []):
        for item in profile['ProfileItems']:
            if item['PayloadType'] == 'com.apple.mdm':
                mdm_enrolled = True
                # You should change this to your MDM provider's Manual enrollment name!
                if profile['ProfileDisplayName'] == MANUAL_PROFILE_DISPLAY_NAME:
                    dep = False
                elif profile['ProfileDisplayName'] == DEP_PROFILE_DISPLAY_NAME:
                    dep = True
                else:
                    dep = 'Unknown'
                break
            if mdm_enrolled:
                break

    if mdm_enrolled and dep is True:
        status = 'DEP'
    elif mdm_enrolled and dep is False:
        status = 'Manually Enrolled'
    elif mdm_enrolled and dep == 'Unknown':
        status = 'Enrolled with unknown server'
    else:
        status = 'No'

    return status


if __name__ == "__main__":
    main()

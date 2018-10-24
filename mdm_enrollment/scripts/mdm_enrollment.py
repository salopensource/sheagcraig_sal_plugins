#!/usr/bin/python


import plistlib
import subprocess
import sys
import tempfile
from distutils.version import LooseVersion

sys.path.append("/usr/local/sal")
import utils


MANUAL_PROFILE_DISPLAY_NAME = 'Root MDM Profile'


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

    utils.add_plugin_results('mdm_enrollment', result)


def os_version():
    cmd = ['sw_vers', '-productVersion']
    output = subprocess.check_output(cmd)
    return LooseVersion(output)


def profiles_status():
    cmd = ['profiles', 'status', '-type', 'enrollment']
    try:
        result = subprocess.check_output(cmd)
    except subprocess.CalledProcessError:
        result = ''

    parsed = {}
    for line in result.splitlines():
        key, val = line.split(':')
        parsed[key.strip()] = val.strip()

    return parsed


def get_enrollment_from_mdm_profile():
    mdm_enrolled = False
    cmd = ['profiles', '-C', '-o', 'stdout-xml']
    plist_text = subprocess.check_output(cmd)
    plist = plistlib.readPlistFromString(plist_text)

    for profile in plist['_computerlevel']:
        for item in profile['ProfileItems']:
            if item['PayloadType'] == 'com.apple.mdm':
                mdm_enrolled = True
                # You should change this to your MDM provider's Manual enrollment name!
                dep = False if profile['ProfileDisplayName'] == MANUAL_PROFILE_DISPLAY_NAME else True
                break
            if mdm_enrolled:
                break

    if mdm_enrolled and dep:
        status = 'DEP'
    elif mdm_enrolled:
        status = 'Manually Enrolled'
    else:
        status = 'No'

    return status


if __name__ == "__main__":
    main()

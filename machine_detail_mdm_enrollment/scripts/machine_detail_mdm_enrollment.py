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
        result['uamdm'] = 'N/A'
        result['status'] = get_enrollment_from_mdm_profile()

    else:
        status = profiles_status()
        result['uamdm'] = 'Yes' if 'User Approved' in status.get('MDM enrollment', '') else 'No'
        if status.get('Enrolled via DEP') == 'Yes':
            result['status'] = 'DEP'
        else:
            result['status'] = 'Manually Enrolled' if 'Yes' in status.get('MDM enrollment', '') else 'No'

    result['dep_status'] = get_dep_activation()

    # From 10.13.2, 10.13.3:
    # cmd = ['profiles', 'status', '-type', 'enrollment']
    # An enrollment profile is currently installed on this system
    # There is no enrollment profile installed on this system

    utils.add_plugin_results('machine_detail_mdm_enrollment', result)


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
    user_approved = False
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


def get_dep_activation():
    result = 'Not activated'

    cmd = ['profiles', '-e']
    output = subprocess.check_output(cmd)
    for line in output.splitlines():
        if 'ConfigurationURL' in line:
            result = line.split('=')[1].replace('"', '').replace(';', '').strip()
            break

    return result


if __name__ == "__main__":
    main()

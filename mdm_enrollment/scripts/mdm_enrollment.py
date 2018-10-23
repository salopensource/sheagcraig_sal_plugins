#!/usr/bin/python


import plistlib
import subprocess
import sys
import tempfile
from distutils.version import LooseVersion

sys.path.append("/usr/local/sal")
import utils


def main():
    mdm_enrolled = False
    user_approved = False

    status = read_enrollment()
    # if os_version() <= LooseVersion('10.13.0'):
    #     read_enrollment()
    # else:
    #     cmd = ['profiles', 'status', '-type', 'enrollment']
    #     output = subprocess.check_output(cmd)
    #     if "MDM enrollment: Yes" in output:
    #         mdm_enrolled = True

    #     user_approved = True if "User Approved" in output else False

    # if mdm_enrolled == True:
    #     status = "UAMDM" if user_approved else "MDM"
    # else:
    #     status = "No"

    result = {'mdm_status': status}
    utils.add_plugin_results('mdm_enrollment', result)


def os_version():
    cmd = ['sw_vers', '-productVersion']
    output = subprocess.check_output(cmd)
    return LooseVersion(output)


def read_enrollment():
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
                dep = False if profile['ProfileDisplayName'] == 'Root MDM Profile' else True
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

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

    if os_version() <= LooseVersion('10.13.0'):
        cmd = ['profiles', '-C', '-o', 'stdout-xml']
        plist_text = subprocess.check_output(cmd)
        plist = plistlib.readPlistFromString(plist_text)

        for profile in plist['_computerlevel']:
            for item in profile['ProfileItems']:
                if item['PayloadType'] == 'com.apple.mdm':
                    mdm_enrolled = True
                    break
                if mdm_enrolled:
                    break

    else:
        cmd = ['profiles', 'status', '-type', 'enrollment']
        output = subprocess.check_output(cmd)
        if "MDM enrollment: Yes" in output:
            mdm_enrolled = True

        user_approved = True if "User Approved" in output else False

    if mdm_enrolled == True:
        status = "UAMDM" if user_approved else "MDM"
    else:
        status = "No"

    result = {'mdm_status': status}
    utils.add_plugin_results('mdm_enrollment', result)


def os_version():
    cmd = ['sw_vers', '-productVersion']
    output = subprocess.check_output(cmd)
    return LooseVersion(output)


if __name__ == "__main__":
    main()

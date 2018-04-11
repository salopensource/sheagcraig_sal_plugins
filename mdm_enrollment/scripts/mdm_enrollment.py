#!/usr/bin/python


import subprocess
import sys
import tempfile
from distutils.version import LooseVersion

sys.path.append("/usr/local/sal")
import utils


def main():
    dep_enrolled = False
    mdm_enrolled = False
    user_approved = False

    cmd = ['profiles', '-e']
    output = subprocess.check_output(cmd)
    if len(output[output.find('{') + 1: output.find('}')].strip()) > 0:
        dep_enrolled = True

    if os_version() <= LooseVersion('10.13.0'):
        with tempfile.TemporaryDirectory() as temp_dir:
            tempfile = os.path.join(temp_dir, 'profiles_output.plist')
            cmd = ['profiles', '-C', '-o', tempfile]
            plist = plistlib.readPlist(tempfile)

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
        if "An enrollment profile is currently installed on this system" in output:
            mdm_enrolled = True

        user_approved = True if "User Approved" in output else False

    result = 'DEP Enrolled: {}, MDM Enrolled: {}, User Approved: {}'.format(
        dep_enrolled, mdm_enrolled, user_approved)


    utils.add_plugin_results('status', result)


def os_version():
    cmd = ['sw_vers', '-productVersion']
    output = subprocess.check_output(cmd)
    return LooseVersion(output)


if __name__ == "__main__":
    main()
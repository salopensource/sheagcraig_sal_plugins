#!/usr/local/sal/Python.framework/Versions/3.8/bin/python3


import subprocess
import sys

import sal


def main():
    dep_assigned = False

    cmd = ['/usr/bin/profiles', '-e']
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as error:
        output = str(error.output)
    if len(output[output.find('{') + 1: output.find('}')].strip()) > 0:
        dep_assigned = True

    result = {'dep_status': '{}Assigned'.format('' if dep_assigned else 'Not ')}

    sal.add_plugin_results('dep_assignment', result)


if __name__ == "__main__":
    main()

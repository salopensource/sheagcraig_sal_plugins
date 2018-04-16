#!/usr/bin/python


import subprocess
import sys

sys.path.append("/usr/local/sal")
import utils


def main():
    dep_assigned = False

    cmd = ['profiles', '-e']
    output = subprocess.check_output(cmd)
    if len(output[output.find('{') + 1: output.find('}')].strip()) > 0:
        dep_assigned = True

    result = {'dep_status': '{}Assigned'.format('' if dep_assigned else 'Not ')}

    utils.add_plugin_results('dep_assignment', result)


if __name__ == "__main__":
    main()

#!/usr/bin/python


import json
import os
import sys

sys.path.append("/usr/local/sal")
import utils


salt_highstate_log = '/var/log/salt/events'


def main():
    if os.path.exists(salt_highstate_log):
        with open(salt_highstate_log) as raw_log:
            # The salt events won't parse as a whole. So just slice out
            # the good stuff.
            events = json.loads(raw_log.readlines()[-1])

    try:
        result = {i['__id__']: i['result'] for i in events['return'].values()}
    except:
        result = {}

    utils.add_plugin_results('SaltMachineDetail', result)


if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> 371de667f8814b0c80fe381bdf83343cf592060c

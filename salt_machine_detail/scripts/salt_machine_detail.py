#!/usr/local/sal/Python.framework/Versions/Current/bin/python3

import json
import os

import sal 


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

    sal.utils.add_plugin_results('SaltMachineDetail', result)


if __name__ == "__main__":
    main()

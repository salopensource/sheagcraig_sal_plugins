Until we get better "Managed Item" features into Sal, this machine detail
plugin takes the output of the Salt rawfile_json returner, and socks the last
run into pluginscript rows in Sal for display.

To make this work, only your highstate should be using the rawfile_json
returner (which dumps to /var/log/salt/events if you want to check it out).

The plugin just shows state name and status.

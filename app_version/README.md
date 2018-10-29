# AppVersion Plugin
This wonderful plugin allows you to track the versions of an arbitrary number of apps across your fleet. However, it does nothing by default... Behold:

## Configuration
Simply open the admin site for your Sal server and navigate to the Server/SalSettings page.

Add a SalSetting with name: `AppVersion_Apps`. The value of this setting should be a comma-delimeted list of names of applications. (You can see what Sal thinks application names are by looking in the Inventory).

Then enable the plugin in the Settings/Plugins page.

## Layout
This is tricky with the current plugin layout code. This plugin will use 1, 2, or 3 columns of width depending on how many apps you want to track, creating a donut chart for each one.

Where this gets tricky is that the plugin will use all three columns for 3+ apps. What this means is that if you are tracking 4 apps for example, and the plugin is sorted in your plugin list so that it falls on the first column, it will use all three columns for the first row, and all three columns for a second row, even though there is only one app. This of course gets tricky with the plugin starting in column 2 or 3 of the list if it has more than 2 or 1 apps (respectively).

This could be fixed by an update to the plugin layout code, and indeed I have a TODO item to do this, but it's a pretty low priority at this time! If you want to take it on, let me know and I can definitely share my notes with you so you can hit the ground running.


## Caveats, TODO, etc
I haven't implemented the machine list view links that these pie charts link to yet. Standby.

Also, if you don't like the layout... PRs accepted! 

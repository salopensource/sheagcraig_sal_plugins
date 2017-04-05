#!/usr/bin/python


from django.template import loader, Context
from yapsy.IPlugin import IPlugin

from server.models import PluginScriptRow

class Battery(IPlugin):
    name = "Battery"

    def widget_width(self):
        return 4

    def plugin_type(self):
        return 'machine_detail'

    def get_description(self):
        return "Battery Information"

    def widget_content(self, page, machine=None, theid=None):
        template = loader.get_template(
            "sheagcraig/battery/templates/battery.html")
        machine_type = machine.conditions.filter(
            condition_name="machine_type").first().condition_data
        if machine_type == "laptop":
            keys = (
                "MaxCapacity", "DesignCapacity", "CycleCount",
                "DesignCycleCount9C", "BatteryHealth")
            battery = {}
            for key in keys:
                item = PluginScriptRow.objects.filter(
                    submission__machine=machine,
                    submission__plugin=self.name,
                    pluginscript_name=key)
                try:
                    val = item.first().pluginscript_data
                except (AttributeError, ValueError):
                    val = None

                battery[key] = val

            if battery and all(battery[key] for key in keys):
                battery["cycle_life"] = (
                    float(battery["CycleCount"]) /
                    float(battery["DesignCycleCount9C"])) * 100
                battery["life"] = (
                    float(battery["MaxCapacity"]) /
                    float(battery["DesignCapacity"])) * 100
        else:
            battery = {"machine_type": "desktop"}

        c = Context({
            "title": self.get_description(),
            "data": battery,
            "theid": theid,
            "page": page})

        return template.render(c)

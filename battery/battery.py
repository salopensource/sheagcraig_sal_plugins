import sal.plugin
from server.models import (PluginScriptRow, Fact)


class Battery(sal.plugin.DetailPlugin):

    description = "Battery Information"

    supported_os_families = [sal.plugin.OSFamilies.darwin]

    def get_context(self, machine, **kwargs):
        context = self.super_get_context(machine, **kwargs)
        try:
            machine_type = machine.facts.filter(
                fact_name="machine_type").first().fact_data
        except AttributeError:
            # If there are no results, None has no `condition_data` attr
            machine_type = None
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
        elif machine_type == 'desktop':
            battery = {"machine_type": "desktop"}
        else:
            battery = {"machine_type": "unknown"}

        context["data"] = battery
        return context

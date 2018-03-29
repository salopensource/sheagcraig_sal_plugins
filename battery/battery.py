import sal.plugin
from server.models import PluginScriptRow


class Battery(sal.plugin.DetailPlugin):

    description = "Battery Information"

    def get_context(self, machine, **kwargs):
        context = self.super_get_context(machine, **kwargs)
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

        context["data"] = battery
        return context

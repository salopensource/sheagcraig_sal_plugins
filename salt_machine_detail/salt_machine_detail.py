import sal.plugin
from server.models import PluginScriptRow


class SaltMachineDetail(sal.plugin.DetailPlugin):

    description = 'List of salt states and their statuses'

    def get_context(self, machine, **kwargs):
        context = self.super_get_context(machine, **kwargs)
        status = (
            PluginScriptRow.objects
            .filter(submission__machine=machine, submission__plugin=self.name))
        context['data'] = {s.pluginscript_name: str(s.pluginscript_data) for s in status}
        return context

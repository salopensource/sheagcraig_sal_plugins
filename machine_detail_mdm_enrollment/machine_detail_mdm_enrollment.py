import sal.plugin
from server.models import PluginScriptRow


class MachineDetailMDMEnrollment(sal.plugin.DetailPlugin):

    description = "Lists enrollment type, user-approval status, and DEP activation."

    def get_context(self, machine, **kwargs):
        context = self.super_get_context(machine, **kwargs)
        rows = (PluginScriptRow.objects
            .filter(
                submission__machine=machine,
                submission__plugin='machine_detail_mdm_enrollment')
             .values('pluginscript_name', 'pluginscript_data'))
        context.update({r['pluginscript_name']: r['pluginscript_data'] for r in rows})

        return context

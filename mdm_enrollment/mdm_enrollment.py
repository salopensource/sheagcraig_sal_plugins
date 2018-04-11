from django.db.models import Count

import sal.plugin
import server.utils as utils
from inventory.models import InventoryItem


class MDMEnrollment(sal.plugin.Widget):

    description = "Machines enrolled in an MDM, whether via DEP, user-approved, or not."

    def get_context(self, queryset, **kwargs):
        context = self.super_get_context(queryset, **kwargs)
        context['data'] = (
            PluginScriptRow.objects
            .filter(submission__machine=machine,
                    submission__plugin=self.name,
                    pluginscript_name="status")
            .annotate(count=Count("status"))
            .order_by("status"))
        return context

    def filter(self, machines, data):
        return machines, 'something'
        # machines = machines.filter(
        #     inventoryitem__application__name="Symantec Endpoint Protection",
        #     inventoryitem__version=data)

        # return machines, "Machines with version {} of Symantec Endpoint Protection".format(data)

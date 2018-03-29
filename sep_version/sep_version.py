from django.db.models import Count

import sal.plugin
import server.utils as utils
from inventory.models import InventoryItem


class SEPVersion(sal.plugin.Widget):

    description = "Symantec Endpoint Protection Version"

    def get_context(self, queryset, **kwargs):
        context = self.super_get_context(queryset, **kwargs)
        context['data'] = (
            InventoryItem.objects
            .filter(machine__in=queryset, application__name="Symantec Endpoint Protection")
            .values( "version")
            .annotate(count=Count("version"))
            .order_by("version"))
        return context

    def filter(self, machines, data):
        machines = machines.filter(
            inventoryitem__application__name="Symantec Endpoint Protection",
            inventoryitem__version=data)

        return machines, "Machines with version {} of Symantec Endpoint Protection".format(data)

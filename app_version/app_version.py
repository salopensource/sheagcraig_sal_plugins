from django.db.models import Count

import sal.plugin
import server.models
import server.utils as utils
from inventory.models import InventoryItem


class AppVersion(sal.plugin.Widget):

    description = "App deployment dashboard plugin"

    def get_context(self, queryset, **kwargs):
        context = self.super_get_context(queryset, **kwargs)
        try:
            apps = server.models.SalSetting.objects.get('AppVersion_Apps')
        except server.models.SalSetting.DoesNotExist:
            apps = 'dwarf_fortress'

        apps = apps.split(',')

        app_data = []
        for app in apps:
            app_results = (
                InventoryItem.objects
                .filter(machine__in=queryset, application__name=app)
                .values("version")
                .annotate(count=Count("version"))
                .order_by("version"))
            app_data.append({'name': app, 'data': app_results})
        context['apps'] = app_data
        return context

    def filter(self, machines, data):
        machines = machines.filter(
            inventoryitem__application__name="Symantec Endpoint Protection",
            inventoryitem__version=data)

        return machines, "Machines with version {} of Symantec Endpoint Protection".format(data)

from django.db.models import Count

import sal.plugin
import server.models
from inventory.models import InventoryItem


class AppVersion(sal.plugin.Widget):

    description = "App deployment dashboard plugin"
    supported_os_families = [sal.plugin.OSFamilies.darwin]

    def get_widget_width(self, *args, **kwargs):
        """Dynamically size plugin row width (in third-columns)

        Width is determined by the number of apps being tracked.
        """
        try:
            apps = server.models.SalSetting.objects.get(name='AppVersion_Apps').value.split(',')
        except server.models.SalSetting.DoesNotExist:
            apps = 1
        rows, columns = divmod(len(apps) * 4, 12)
        return 12 if rows >= 1 else columns

    def get_context(self, queryset, **kwargs):
        context = self.super_get_context(queryset, **kwargs)
        try:
            apps = server.models.SalSetting.objects.get(name='AppVersion_Apps').value.split(',')
            apps = [n.strip() for n in apps]
        except server.models.SalSetting.DoesNotExist:
            apps = ['dwarf_fortress']

        app_data = []
        rows, _ = divmod(len(apps) * 4, 12)
        context['width'] = 4 if rows >= 1 else 12 / len(apps)

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
        try:
            app, version = data.split('+')
        except ValueError:
            app, version = ('', '')
        machines = machines.filter(
            inventoryitem__application__name=app,
            inventoryitem__version=version)

        return machines, "Machines with version {} of {}".format(version, app)

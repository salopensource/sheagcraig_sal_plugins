from collections import Counter

from django.db.models import Count, F

import sal.plugin
import server.utils as utils


class Catalogs(sal.plugin.Widget):

    description = "Munki catalogs used by Mac clients."

    def get_context(self, queryset, **kwargs):
        context = self.super_get_context(queryset, **kwargs)

        catalog_plugin_results = queryset.filter(
            pluginscriptsubmission__plugin=self.name,
            pluginscriptsubmission__pluginscriptrow__pluginscript_name="Catalogs")

        # Get a count of machines which haven't reported.
        unreported_count = queryset.count() - catalog_plugin_results.count()

        catalog_plugin_results = catalog_plugin_results.annotate(
            pluginscript_data=F(
                "pluginscriptsubmission__pluginscriptrow__"
                "pluginscript_data"))
        catalog_plugin_results = catalog_plugin_results.values(
            "pluginscript_data").annotate(
                count=Count("pluginscript_data")).order_by("pluginscript_data")

        counter = Counter()

        # Build a counter of each catalog type.
        for catalog_group in catalog_plugin_results:
            catalogs = catalog_group["pluginscript_data"].split("+")
            for catalog in catalogs:
                counter[catalog] += catalog_group["count"]

        data = [{"label": catalog, "value": counter[catalog]} for catalog in
                counter]
        data.append({"label": "Unknown", "value": unreported_count})

        context["data"] = data
        return context

    def filter(self, machines, data):
        if data == "Unknown":
            machines = machines.exclude(
                pluginscriptsubmission__plugin=self.name)
        else:
            machines = machines.filter(
                pluginscriptsubmission__plugin=self.name,
                pluginscriptsubmission__pluginscriptrow__pluginscript_name="Catalogs",
                pluginscriptsubmission__pluginscriptrow__pluginscript_data__contains=data)
        title = "Machines with catalog: {}".format(data)

        return machines, title

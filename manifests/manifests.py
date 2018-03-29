from collections import Counter

from django.db.models import Count, F

import sal.plugin
import server.utils as utils


class Manifests(sal.plugin.Widget):

    description = "Managed Mac Munki manifests"

    def get_context(self, queryset, **kwargs):
        context = self.super_get_context(queryset, **kwargs)
        manifest_plugin_results = queryset.filter(
            pluginscriptsubmission__plugin=self.name,
            pluginscriptsubmission__pluginscriptrow__pluginscript_name="included_manifests")
        # Get a count of machines which haven't reported.
        unreported_count = queryset.count() - manifest_plugin_results.count()

        manifest_plugin_results = manifest_plugin_results.annotate(
            pluginscript_data=F(
                "pluginscriptsubmission__pluginscriptrow__"
                "pluginscript_data"))
        manifest_plugin_results = manifest_plugin_results.values(
            "pluginscript_data").annotate(
                count=Count("pluginscript_data")).order_by("pluginscript_data")

        counter = Counter()

        # Build a counter of each manifest type.
        for manifest_group in manifest_plugin_results:
            manifests = manifest_group["pluginscript_data"].split("+")
            for manifest in manifests:
                counter[manifest] += manifest_group["count"]

        data = [{"label": manifest, "value": counter[manifest]} for manifest in
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
                pluginscriptsubmission__pluginscriptrow__pluginscript_name="Manifests",
                pluginscriptsubmission__pluginscriptrow__pluginscript_data__contains=data)
        title = "Machines with manifest: {}".format(data)

        return machines, title

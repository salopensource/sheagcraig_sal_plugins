#!/usr/bin/python


from collections import Counter
import plistlib

from django.db.models import Count, F
from django.shortcuts import get_object_or_404
from django.template import loader, Context
from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager

from server.models import *
import server.utils as utils


class Manifests(IPlugin):
    name = "Manifests"

    def widget_width(self):
        return 4

    def plugin_type(self):
        return "builtin"

    def get_description(self):
        return "Included Manifests"

    def widget_content(self, page, machines=None, theid=None):
        if page == "front":
            template = loader.get_template(
                "sheagcraig/manifests/templates/front.html")
        elif page in ("bu_dashboard", "group_dashboard"):
            template = loader.get_template(
                "sheagcraig/manifests/templates/id.html")

        # TODO: Replace with Sal 3.0 access:
        # https://github.com/salopensource/sal/wiki/Scripts-in-Plugins#other-field-types
        manifest_plugin_results = machines.filter(
            pluginscriptsubmission__plugin=self.name,
            pluginscriptsubmission__pluginscriptrow__pluginscript_name="included_manifests")
        # Get a count of machines which haven't reported.
        unreported_count = machines.count() - manifest_plugin_results.count()

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

        c = Context({
            "title": "Manifests",
            "data": data,
            "theid": theid,
            "page": page})

        return template.render(c)

    def filter_machines(self, machines, data):
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

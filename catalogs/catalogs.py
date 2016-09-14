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


class Catalogs(IPlugin):
    name = "Catalogs"

    def widget_width(self):
        return 4

    def plugin_type(self):
        return "builtin"

    def get_description(self):
        return "Catalogs"

    def widget_content(self, page, machines=None, theid=None):
        if page == "front":
            template = loader.get_template(
                "sheagcraig/catalogs/templates/front.html")
        elif page in ("bu_dashboard", "group_dashboard"):
            template = loader.get_template(
                "sheagcraig/catalogs/templates/id.html")

        # TODO: Replace with Sal 3.0 access:
        # https://github.com/salopensource/sal/wiki/Scripts-in-Plugins#other-field-types
        catalog_plugin_results = machines.filter(
            pluginscriptsubmission__plugin=self.name,
            pluginscriptsubmission__pluginscriptrow__pluginscript_name="Catalogs")
        # Get a count of machines which haven't reported.
        unreported_count = machines.count() - catalog_plugin_results.count()

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

        c = Context({
            "title": "Catalogs",
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
                pluginscriptsubmission__pluginscriptrow__pluginscript_name="Catalogs",
                pluginscriptsubmission__pluginscriptrow__pluginscript_data__contains=data)
        title = "Machines with catalog: {}".format(data)

        return machines, title

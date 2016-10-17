#!/usr/bin/python


from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.template import loader, Context
from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager

from inventory.models import InventoryItem
from server.models import *
import server.utils as utils


class SEPVersion(IPlugin):
    name = "SEPVersion"

    def widget_width(self):
        return 4

    def plugin_type(self):
        return "builtin"

    def get_description(self):
        return "Symantec Endpoint Protection Version"

    def widget_content(self, page, machines=None, theid=None):
        # The data is data is pulled from the database and passed to a template.

        # There are three possible views we're going to be rendering to -
        # front, bu_dashbaord and group_dashboard. If page is set to
        # bu_dashboard, or group_dashboard, you will be passed a business_unit
        # or machine_group id to use (mainly for linking to the right search).
        if page == "front":
            t = loader.get_template(
                "sheagcraig/managementcompliance/templates/front.html")
        elif page in ("bu_dashboard", "group_dashboard"):
            t = loader.get_template(
                "sheagcraig/managementcompliance/templates/id.html")

        data = InventoryItem.objects.filter(
            machine_in=machines, name="Symantec Endpoint Protection").values(
                "version").annotate(count=Count("version")).order_by("version")
        # in_compliance = self.get_in_compliance(machines).count()
        # out_of_compliance = self.get_out_of_compliance(machines).count()
        # unknown = machines.count() - (in_compliance + out_of_compliance)

        # data = [{"label": "In Compliance", "value": in_compliance},
        #         {"label": "Out of Compliance", "value": out_of_compliance},
        #         {"label": "Unknown Status", "value": unknown}]

        c = Context({
            "title": self.get_description(),
            "data": data,
            "theid": theid,
            "page": page})

        return t.render(c)

    def filter_machines(self, machines, data):
        if data == "In Compliance":
            machines = self.get_in_compliance(machines)
            title = "Machines in compliance"

        elif data == "Out of Compliance":
            machines = self.get_out_of_compliance(machines)
            title = "Machines out of compliance"

        elif data == "Unknown Status":
            machines = self.get_machines_with_no_plugin_results(machines)
            title = "Machines which have not reported their compliance"

        else:
            machines = None

        return machines, title

    def get_in_compliance(self, machines):
        return self.filter_machines_by_plugin_result(machines, True)

    def get_out_of_compliance(self, machines):
        return self.filter_machines_by_plugin_result(machines, False)

    def filter_machines_by_plugin_result(self, machines, value):
        return machines.filter(
                pluginscriptsubmission__plugin=self.name,
                pluginscriptsubmission__pluginscriptrow__pluginscript_name="MunkiProfilePresent",
                pluginscriptsubmission__pluginscriptrow__pluginscript_data=value)

    def get_machines_with_no_plugin_results(self, machines):
            return machines.exclude(
                pluginscriptsubmission__plugin=self.name)

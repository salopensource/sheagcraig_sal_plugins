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
                "sheagcraig/sep_version/templates/front.html")
        elif page in ("bu_dashboard", "group_dashboard"):
            t = loader.get_template(
                "sheagcraig/sep_version/templates/id.html")

        data = InventoryItem.objects.filter(
            machine__in=machines, name="Symantec Endpoint Protection").values(
                "version").annotate(count=Count("version")).order_by("version")

        c = Context({
            "title": self.get_description(),
            "data": data,
            "theid": theid,
            "page": page})

        return t.render(c)

    def filter_machines(self, machines, data):
        machines = machines.filter(inventoryitem__name="Symantec Endpoint Protection", inventoryitem__version=data)

        return machines, "Machines with version {} of Symantec Endpoint Protection".format(data)

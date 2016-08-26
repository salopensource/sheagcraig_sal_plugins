#!/usr/bin/python


from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.template import loader, Context
from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager

from server.models import *
import server.utils as utils


class ManagementCompliance(IPlugin):

    def widget_width(self):
        return 4

    def plugin_type(self):
        return 'builtin'

    def get_description(self):
        return 'Management Compliance'

    def widget_content(self, page, machines=None, theid=None):
        # The data is data is pulled from the database and passed to a template.

        # There are three possible views we're going to be rendering to -
        # front, bu_dashbaord and group_dashboard. If page is set to
        # bu_dashboard, or group_dashboard, you will be passed a business_unit
        # or machine_group id to use (mainly for linking to the right search).
        if page == 'front':
            t = loader.get_template(
                'sheagcraig/managementcompliance/templates/front.html')
        elif page in ('bu_dashboard', 'group_dashboard'):
            t = loader.get_template(
                'sheagcraig/managementcompliance/templates/id.html')

        in_compliance = machines.filter(
            pluginscriptsubmission__plugin='ManagementCompliance',
            pluginscriptsubmission__pluginscriptrow__pluginscript_name='MunkiProfilePresent',
            pluginscriptsubmission__pluginscriptrow__pluginscript_data=True).count()
        out_of_compliance = machines.filter(
            pluginscriptsubmission__plugin='ManagementCompliance',
            pluginscriptsubmission__pluginscriptrow__pluginscript_name='MunkiProfilePresent',
            pluginscriptsubmission__pluginscriptrow__pluginscript_data=False).count()

        unknown = machines.count() - (in_compliance + out_of_compliance)

        data = [{"label": "In Compliance", "value": in_compliance},
                {"label": "Out of Compliance", "value": out_of_compliance},
                {"label": "Unknown Status", "value": unknown}]

        c = Context({
            'title': 'Management Compliance',
            'compliance_label': 'In Compliance',
            'compliance_count': in_compliance,
            'out_of_compliance_label': 'Out of Compliance',
            'out_of_compliance_count': out_of_compliance,
            'data': data,
            'plugin': 'ManagementCompliance',
            'theid': theid,
            'page': page
        })
        return t.render(c)

    def filter_machines(self, machines, data):
        if data == 'In Compliance':
            machines = machines.filter(
                pluginscriptsubmission__plugin='ManagementCompliance',
                pluginscriptsubmission__pluginscriptrow__pluginscript_name='MunkiProfilePresent',
                pluginscriptsubmission__pluginscriptrow__pluginscript_data=True)
            title = 'Machines in compliance'

        elif data == 'Out of Compliance':
            machines = machines.filter(
                pluginscriptsubmission__plugin='ManagementCompliance',
                pluginscriptsubmission__pluginscriptrow__pluginscript_name='MunkiProfilePresent',
                pluginscriptsubmission__pluginscriptrow__pluginscript_data=False)
            title = 'Machines out of compliance'

        elif data == 'Unknown Status':
            machines = machines.exclude(
                pluginscriptsubmission__plugin='ManagementCompliance')
            title = 'Machines which have not reported their compliance'

        else:
            machines = None

        return machines, title

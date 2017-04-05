#!/usr/bin/python


from django.template import loader, Context
from yapsy.IPlugin import IPlugin

from server.models import PluginScriptRow, SalSetting

import pynsinc


class INSINC(IPlugin):
    name = "INSINC"

    def widget_width(self):
        return 4

    def plugin_type(self):
        return 'machine_detail'

    def get_description(self):
        return "SAS INSINC Inventory Information"

    def widget_content(self, page, machine=None, theid=None):
        template = loader.get_template(
            "sheagcraig/insinc/templates/insinc.html")

        macs = []
        errors = []

        try:
            insinc_user = SalSetting.objects.get(name="INSINC_Username").value
        except SalSetting.DoesNotExist:
            insinc_user = None

        try:
            insinc_pass = SalSetting.objects.get(name="INSINC_Password").value
        except SalSetting.DoesNotExist:
            insinc_pass = None

        if insinc_user and insinc_pass:
            insinc = pynsinc.Insinc((insinc_user, insinc_pass))

            plugin_data = PluginScriptRow.objects.filter(
                submission__machine=machine,
                submission__plugin='INSINC',
                pluginscript_name='ARD_Info_1')
            asset_tag = ""
            try:
                asset_tag = plugin_data.first().pluginscript_data
                int(asset_tag)
            except (AttributeError, ValueError):
                # I have found some machines that were setup with
                # ARD Field number 1 == "tag <asset_tag>". There may be
                # Other cruft in there, so strip it out based on regex.
                import re
                match = re.search("\d*$", asset_tag)
                if match:
                    asset_tag = match.group()
                else:
                    asset_tag = ""

            mac = None
            if asset_tag:
                macs = insinc.get_assets(
                    pynsinc.Field.asset_tag, pynsinc.Operator.equals,
                    asset_tag)
                mac = macs[0] if macs else None
        else:
            mac = None
            errors.append(
                "No INSINC credentials supplied! Please set INSINC_Username "
                "and INSINC_Password")

        if len(macs) > 1:
            errors.append("Multiple INSINC asset records!")
        if mac and (mac.nodename.upper().split(".")[0] !=
                machine.hostname.upper()):
            errors.append("INSINC nodename does not match current hostname!")

        # TODO: Check for multiple nodename assignments in INSINC.

        c = Context({
            "title": self.get_description(),
            "data": mac,
            "errors": errors,
            "theid": theid,
            "page": page})

        return template.render(c)

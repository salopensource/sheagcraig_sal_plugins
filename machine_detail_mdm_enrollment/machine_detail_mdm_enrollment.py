from itertools import chain

from django.db.models import Count, F, Q

import sal.plugin


PLUGIN_Q = Q(pluginscriptsubmission__plugin='machine_detail_mdm_enrollment',
             pluginscriptsubmission__pluginscriptrow__pluginscript_name='mdm_status')


class MachineDetailMDMEnrollment(sal.plugin.DetailPlugin):

    description = "Lists enrollment type, user-approval status, and DEP activation."

    def get_context(self, queryset, **kwargs):
        context = self.super_get_context(queryset, **kwargs)
        data = queryset.filter(PLUGIN_Q)
        context['data'] = data
        return context

from itertools import chain

from django.db.models import Count, F, Q

import sal.plugin


PLUGIN_Q = Q(pluginscriptsubmission__plugin='mdm_enrollment',
             pluginscriptsubmission__pluginscriptrow__pluginscript_name='mdm_status')


class MDMEnrollment(sal.plugin.Widget):

    description = "Machines enrolled in an MDM, user-approved, or not."

    def get_context(self, queryset, **kwargs):
        context = self.super_get_context(queryset, **kwargs)
        data = (
            queryset
            .filter(PLUGIN_Q)
            .annotate(
                mdm_status=F('pluginscriptsubmission__pluginscriptrow__pluginscript_data'))
            .values('mdm_status')
            .annotate(count=Count('mdm_status'))
            .order_by('mdm_status'))
        unknown = queryset.exclude(PLUGIN_Q).count()
        context['data'] = chain(data, [{'mdm_status': 'Unknown', 'count': unknown}])
        return context

    def filter(self, machines, data):
        return machines.filter(
            PLUGIN_Q, pluginscriptsubmission__pluginscriptrow__pluginscript_data=data), data

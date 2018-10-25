from itertools import chain

from django.db.models import Count, F, Q

import sal.plugin


PLUGIN_Q = Q(pluginscriptsubmission__plugin='dep_assignment',
             pluginscriptsubmission__pluginscriptrow__pluginscript_name='dep_status')


class DEPAssignment(sal.plugin.Widget):

    description = "Machines assigned to a DEP server."

    def get_context(self, queryset, **kwargs):
        context = self.super_get_context(queryset, **kwargs)
        data = (
            queryset
            .filter(PLUGIN_Q)
            .annotate(
                dep_status=F('pluginscriptsubmission__pluginscriptrow__pluginscript_data'))
            .values('dep_status')
            .annotate(count=Count('dep_status'))
            .order_by('dep_status'))
        unknown = queryset.exclude(PLUGIN_Q).count()
        context['data'] = chain(data, [{'dep_status': 'Unknown', 'count': unknown}])
        return context

    def filter(self, machines, data):
        if data == 'Unknown':
            return machines.exclude(PLUGIN_Q), data
        return machines.filter(
            PLUGIN_Q, pluginscriptsubmission__pluginscriptrow__pluginscript_data=data), data

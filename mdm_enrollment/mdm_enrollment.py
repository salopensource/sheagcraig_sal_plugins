from django.db.models import Count, F, Q

import sal.plugin


PLUGIN_Q = Q(pluginscriptsubmission__plugin='mdm_enrollment',
             pluginscriptsubmission__pluginscriptrow__pluginscript_name='mdm_status')

class MDMEnrollment(sal.plugin.Widget):

    description = "Machines enrolled in an MDM, user-approved, or not."

    def get_context(self, queryset, **kwargs):
        context = self.super_get_context(queryset, **kwargs)
        context['data'] = (
            queryset
            .filter(PLUGIN_Q)
            .annotate(
                mdm_status=F('pluginscriptsubmission__pluginscriptrow__pluginscript_data'))
            .values('mdm_status')
            .annotate(count=Count('mdm_status'))
            .order_by('mdm_status'))
        return context

    def filter(self, machines, data):
        return machines, 'something'
        # machines = machines.filter(
        #     inventoryitem__application__name="Symantec Endpoint Protection",
        #     inventoryitem__version=data)

        # return machines, "Machines with version {} of Symantec Endpoint Protection".format(data)

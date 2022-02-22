from mayan.apps.views.generics import FormView
from mayan.apps.smart_settings.forms import SettingForm
from mayan.apps.smart_settings.permissions import permission_settings_edit
from mayan.apps.smart_settings.classes import Setting
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

class SettingEditView(FormView):
    form_class = SettingForm
    view_permission = permission_settings_edit

    def form_valid(self, form):
        self.get_object().value = form.cleaned_data['value']
        Setting.save_configuration()
        messages.success(
            message=_('Setting updated successfully.'),
            request=self.request
        )
        return super().form_valid(form=form)

    def get_extra_context(self):
        return {
            'hide_link': True,
            'object': self.get_object(),
            'title': _('Edit LogoName: '),
        }

    def get_initial(self):
        return {'setting': self.get_object()}

    def get_object(self):
        return Setting.get('COMMON_PROJECT_TITLE')

    def get_post_action_redirect(self):
        return reverse(
            viewname='common:home'
        )
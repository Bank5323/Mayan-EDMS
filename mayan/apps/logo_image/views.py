from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from .forms import LogoForm
from .permissions import permission_logo_change
from mayan.apps.views.generics import SingleObjectCreateView

class LogoImageView(SingleObjectCreateView):
    extra_context = {'title': _('Change Logo Image')}
    form_class = LogoForm
    post_action_redirect = reverse_lazy(
        viewname='common:home'
    )
    view_permission = permission_logo_change

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}
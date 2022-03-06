from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Logo'), name='logo')

permission_logo_change = namespace.add_permission(
    label=_('Change logo'), name='logo_image_view'
)
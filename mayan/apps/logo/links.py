from mayan.apps.navigation.classes import Link
from django.utils.translation import ugettext_lazy as _
from .icons import icon_logo_setting

link_logo_setting = Link(
    icon=icon_logo_setting,
    text=_('Logo Text'),
    view='logo:logo_view'
)
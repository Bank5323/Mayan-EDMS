from mayan.apps.common.apps import MayanAppConfig
from django.utils.translation import ugettext_lazy as _
from mayan.apps.common.menus import menu_setup
from .links import link_logo_setting

class LogoApp(MayanAppConfig):
    app_namespace = 'logo'
    app_url = 'logo'
    has_tests = True
    name = 'mayan.apps.logo'
    verbose_name = _('logo')

    def ready(self):
        super().ready()

        menu_setup.bind_links(links=(link_logo_setting,))
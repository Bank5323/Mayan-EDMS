from mayan.apps.common.apps import MayanAppConfig
from django.utils.translation import ugettext_lazy as _
from mayan.apps.common.menus import menu_setup
from .links import link_logo_image_setting

class LogoImageApp(MayanAppConfig):
    app_namespace = 'logo_image'
    app_url = 'logo_image'
    has_tests = True
    name = 'mayan.apps.logo_image'
    verbose_name = _('logo_image')

    def ready(self):
        super().ready()

        menu_setup.bind_links(links=(link_logo_image_setting,))
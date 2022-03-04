import bleach

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.events.classes import EventManagerSave
from mayan.apps.events.decorators import method_event

from .events import event_theme_created, event_theme_edited

#import RGBColorFie to create GUI select color
from colorful.fields import RGBColorField

#import os for read files
from os import listdir
from os.path import isfile, join



class Theme(ExtraDataModelMixin, models.Model):
    label = models.CharField(
        db_index=True, help_text=_('A short text describing the theme.'),
        max_length=128, unique=True, verbose_name=_('Label')
    )
#add text font name from google fonts
    font = models.CharField(
        help_text=_('Fill font name from google font. If you want default fount please fill "default".'),
        verbose_name=_('Font for text Logo.'),
        max_length=128
    )

#add color code to model
    mainColor = RGBColorField(
        help_text=_('The RGB color values for main color.'),
        verbose_name=_('Color Background Topbar Menu')
    )

    secondColor = RGBColorField(
        help_text=_('The RGB color values for second color.'),
        verbose_name=_('Color Background Main Menu')
    )

    thirdColor = RGBColorField(
        help_text=_('The RGB color values for third color.'),
        verbose_name=_('Color Background Main Menu')
    )

    stylesheet = models.TextField(
        blank=True, help_text=_(
            'The CSS stylesheet to change the appearance of the different '
            'user interface elements.'
        ), verbose_name=_('Stylesheet')
    )

    class Meta:
        ordering = ('label',)
        verbose_name = _('Theme')
        verbose_name_plural = _('Themes')

    def __str__(self):
        return force_text(s=self.label)

    def get_absolute_url(self):
        return reverse(
            viewname='appearance:theme_edit', kwargs={
                'theme_id': self.pk
            }
        )

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_theme_created,
            'target': 'self',
        },
        edited={
            'event': event_theme_edited,
            'target': 'self',
        }
    )
    def save(self, *args, **kwargs):
        maincolor = self.mainColor
        secondColor = self.secondColor
        thirdColor = self.thirdColor
        font = self.font

        #set css to set font
        css_font = ''
        if font != 'default':
            css_font = f"""
                .navbar-brand {{
                    font-family: {font.split(':')[0]};
                }}
                *{{
                    font-family: {font.split(':')[0]} !important;
                }}
                #content-title{{
                    font-family: {font.split(':')[0]};
                }}
                .col-xs-12 h4{{
                    font-family: {font.split(':')[0]};
                }}
                .content h2.title{{
                    font-family: {font.split(':')[0]};
                }}
                .modal-header h4.modal-title{{
                    font-family: {font.split(':')[0]};
                }}

            """
        css = f"""
        .btn{{
        background-color: {maincolor};
        }}
        .panel-heading{{
            background-color: {maincolor};
        }}
        #menu-main{{
            background-color: {secondColor};
        }}
        .panel-heading{{
            background-color: {maincolor};
        }}
        a:hover{{
            color: {thirdColor};
        }} 
        .row strong{{
            color: white;
        }}
        .panel .panel-footer{{
            color: {secondColor};
        }}
        .panel panel-heading{{
            background: {secondColor};
        }}
        .panel-title{{
            background-color: {secondColor};
        }}
        #accordion-sidebar .panel-body{{
            background-color: {maincolor};
        }}
        #accordion-sidebar .panel-body:hover{{
            background-color: {maincolor};
        }}
        #accordion-sidebar a[aria-expanded="true"]{{
            background-color: {thirdColor};
        }}
        .navbar-default .navbar-nav>li>a:hover, .navbar-default .navbar-nav>li>a:focus {{
            color: {thirdColor};
            background-color: transparent;
        }}
        .panel-primary>.panel-heading {{
            background-color: {secondColor};
            border-color: {thirdColor};
        }}
        .container-fluid{{
                background: {maincolor}
        }}
        {css_font}
        """
        self.stylesheet = css

        #test list files
        # onlyfiles = [f for f in listdir('/Mayan-EDMS/mayan/media/static/appearance/fonts') if isfile(join('/Mayan-EDMS/mayan/media/static/appearance/fonts', f))]
        # print(onlyfiles)


        super().save(*args, **kwargs)


class UserThemeSetting(models.Model):
    user = models.OneToOneField(
        on_delete=models.CASCADE, related_name='theme_settings',
        to=settings.AUTH_USER_MODEL, verbose_name=_('User')
    )
    theme = models.ForeignKey(
        blank=True, null=True, on_delete=models.CASCADE,
        related_name='user_setting', to=Theme, verbose_name=_('Theme')
    )

    class Meta:
        verbose_name = _('User theme setting')
        verbose_name_plural = _('User theme settings')

    def __str__(self):
        return force_text(s=self.user)

# add CurrentTheme to ref all theme
class CurrentTheme(models.Model):
    theme = models.ForeignKey(
        blank=True, null=True, on_delete=models.CASCADE,
        related_name='CurrentTheme', to=Theme, verbose_name=_('CurrentTheme')
    )

    class Meta:
        verbose_name = _('CurrentTheme')
        verbose_name_plural = _('CurrentTheme')

    def __str__(self):
        return force_text(s=self.theme)

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)
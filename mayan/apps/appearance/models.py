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

from django.utils.safestring import mark_safe


class Theme(ExtraDataModelMixin, models.Model):
    label = models.CharField(
        db_index=True, help_text=_('A short text describing the theme.'),
        max_length=128, unique=True, verbose_name=_('Label')
    )
#add text font name from google fonts
    font = models.CharField(
        help_text=_(mark_safe(f"""Fill font name from <a class='link_google' onclick="window.open('{'https://fonts.google.com/'}', '_blank')"; style="cursor: pointer;">Google fonts</a>. If you want default fount please fill "default".""")),
        verbose_name=_('Font for text Logo.'),
        max_length=128
    )

#add color code to model
    mainColor = RGBColorField(
        help_text=_('The RGB color values for main color.'),
        verbose_name=_('Main Color')
    )

    secondColor = RGBColorField(
        help_text=_('The RGB color values for second color. It should be a color lighter than the main color.'),
        verbose_name=_('Second Color')
    )

    thirdColor = RGBColorField(
        help_text=_('The RGB color values for third color. It should be a color darker than the main color.'),
        verbose_name=_('Third Color')
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
                * {{
                    font-family: {font.split(':')[0]} !important;
                }}
            """
        css = f"""
        {css_font}
        
        .container-fluid {{
            background-color: {maincolor};
        }}

        .navbar.navbar-default.navbar-fixed-top .dropdown-menu li a {{
            color: {maincolor};
        }}
        .navbar.navbar-default.navbar-fixed-top .dropdown-menu li a:hover {{
            background-color: {maincolor};
            color: white;
        }}
        .nav.navbar-nav.navbar-right li.dropdown.open a[aria-expanded="true"] {{
            background: {thirdColor};
        }}
        .navbar-default .navbar-nav>li>a:hover, .navbar-default .navbar-nav>li>a:focus {{
            color: {thirdColor};
            background-color: transparent;
        }}


        #menu-main {{
            background-color:  {maincolor};
        }}
        #accordion-sidebar .panel-heading {{
            background-color: {maincolor};
        }}
        #accordion-sidebar .panel-heading:hover {{
            background-color: {secondColor};
            transition: .1s ease;
        }}
        #accordion-sidebar .panel-heading.active {{
            background-color: {thirdColor};
            transition: .1s ease;
        }}
        #accordion-sidebar > .panel > div > .panel-body > ul > li:hover {{
            background-color: {secondColor};
            transition: .1s ease;
        }}
        #accordion-sidebar > .panel > div > .panel-body > ul > li.active {{
            background: {thirdColor};
        }}
        #accordion-sidebar a[aria-expanded="true"]{{
            background-color: {thirdColor};
        }}
        #accordion-sidebar .panel-body{{
            background-color: {maincolor};
        }}


        .pull-right.btn-group.open li a:hover{{
            background:{secondColor};
            color: white;
        }}
        .pull-right.btn-group.open li a{{
            color: {maincolor};
        }}


        td.last .btn-list a.btn-primary{{
            background: {maincolor}; #สีขอบ
        }}

        .well .panel-heading{{
            color: {maincolor}
        }}

        .btn-block{{
            background-color: {maincolor};
            border: 1px solid {maincolor};
        }}

        .btn.btn-primary.btn-xs  {{
            background-color: {maincolor};
        }}

        .btn.btn-primary  {{
            background-color: {maincolor};
        }}

        .list-group-item.btn-sm.active {{
            background-color: {maincolor};
        }}

        .btn-block:hover{{
            background: {secondColor};
        }}

        button.btn.btn-primary.disabled {{
            background: black;
            opacity: 1;
        }}

        .well .panel-primary .panel-heading {{
            background-color: {maincolor};
        }}

        .well .panel-primary .panel-body ul li a{{
            color:{maincolor};
        }}
        .well .panel-primary .panel-body ul li a:hover{{
            background:{secondColor};
            color: white;
        }}
        button.btn.btn-primary.disabled {{
            background: {maincolor};
        }}



    
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
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


class Theme(ExtraDataModelMixin, models.Model):
    label = models.CharField(
        db_index=True, help_text=_('A short text describing the theme.'),
        max_length=128, unique=True, verbose_name=_('Label')
    )

#add color code to model
    color_background = RGBColorField(
        help_text=_('The RGB color values for the topbar menu.'),
        verbose_name=_('Color Background Topbar Menu')
    )

    color_menu = RGBColorField(
        help_text=_('The RGB color values for the main menu.'),
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
        self.stylesheet = bleach.clean(
            text=self.stylesheet, tags=('style',)
        )
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
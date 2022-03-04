from django import forms

from mayan.apps.views.forms import DetailForm

from .models import Theme, UserThemeSetting ,CurrentTheme #add CurrentTheme model


class ThemeForm(forms.ModelForm):
    class Meta:
        fields = ('label', 'mainColor', 'secondColor', 'thirdColor', 'font', ) #edit form
        model = Theme


class UserThemeSettingForm(forms.ModelForm):
    class Meta:
        fields = ('theme',)
        model = CurrentTheme ##to change all theme | original model is UserThemeSetting
        widgets = {
            'theme': forms.Select(
                attrs={
                    'class': 'select2'
                }
            ),
        }


class UserThemeSettingForm_view(DetailForm):
    class Meta:
        fields = ('theme',)
        model = UserThemeSetting

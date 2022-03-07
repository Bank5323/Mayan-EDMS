from django import forms
from mayan.apps.converter.models import Asset
from django.apps import apps

class LogoForm(forms.ModelForm):

    class Meta:
        fields = ('file',)
        model = Asset

    def save(self, commit=True):
        Asset = apps.get_model(
            app_label='converter', model_name='Asset'
        )
        try:
            Asset.objects.filter(label='logo').delete()
        except :
            pass
        
        modelForm = super(LogoForm, self).save(commit=False)
        modelForm.label='logo'
        modelForm.internal_name='logo'
        if commit:
            modelForm.save()
        return modelForm
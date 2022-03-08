from django.template import Library
from django.apps import apps
from django.utils.safestring import mark_safe

register = Library()

@register.simple_tag
def logo_get_logo():
    html = ''
    Asset = apps.get_model(
        app_label='converter', model_name='Asset'
    )
    
    try:
        url = Asset.objects.get(label='logo').get_api_image_url()
        html = f"""<img class="img-fluid " src="{url}" style="max-width: 200%; max-height: 200%; margin-top: -10px;" >"""
    except:
        html = ''
    
    return mark_safe(html)


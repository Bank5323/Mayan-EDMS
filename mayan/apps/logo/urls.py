from django.conf.urls import url
from .views import SettingEditView

urlpatterns = [
    url(
        regex=r'^$',
        name='logo_view', view=SettingEditView.as_view()
    ),
]
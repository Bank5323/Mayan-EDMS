from django.conf.urls import url
from .views import LogoImageView

urlpatterns = [
    url(
        regex=r'^logo_image/$',
        name='logo_image_view', view=LogoImageView.as_view()
    ),
]
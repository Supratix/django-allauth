from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from django.urls import path

from .provider import EduappsProvider
from .views import oauth2_finish_login

urlpatterns = default_urlpatterns(EduappsProvider)
urlpatterns += [
    path(
        EduappsProvider.get_slug() + '/login/callback/finish/',
        oauth2_finish_login,
        name="eduapps_finish_callback"
    ),
]

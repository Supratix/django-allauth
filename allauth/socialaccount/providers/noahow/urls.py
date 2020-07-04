from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from django.urls import path

from .provider import NoahowProvider
from .views import oauth2_finish_login

urlpatterns = default_urlpatterns(NoahowProvider)
urlpatterns += [
    path(
        NoahowProvider.get_slug() + '/login/callback/finish/',
        oauth2_finish_login,
        name="noahow_finish_callback"
    ),
]

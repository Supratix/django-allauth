from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from django.urls import path

from .provider import NoaProvider
from .views import oauth2_finish_login

urlpatterns = default_urlpatterns(NoaProvider)
urlpatterns += [
    path(
        NoaProvider.get_slug() + '/login/callback/finish/',
        oauth2_finish_login,
        name="noa_finish_callback"
    ),
]

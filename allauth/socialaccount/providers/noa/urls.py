from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import NoaProvider


urlpatterns = default_urlpatterns(NoaProvider)

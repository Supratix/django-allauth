from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import DfbProvider


urlpatterns = default_urlpatterns(DfbProvider)

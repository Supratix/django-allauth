from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import EduAppsProvider


urlpatterns = default_urlpatterns(EduAppsProvider)

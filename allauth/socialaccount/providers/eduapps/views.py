#import requests

from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import EduAppsProvider


class EduAppsOAuth2Adapter(OAuth2Adapter):
    provider_id = EduAppsProvider.id
    access_token_url = 'https://login.eduapps.de/oauth/token'
    authorize_url = 'https://login.eduapps.de/oauth/authorize'

    def complete_login(self, request, app, token, **kwargs):
        headers = {'Authorization': 'Bearer {0}'.format(token.token)}
        #resp = requests.get(self.profile_url, headers=headers)
        #extra_data = resp.json()
        extra_data = {}
        return self.get_provider().sociallogin_from_response(
            request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(EduAppsOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(EduAppsOAuth2Adapter)

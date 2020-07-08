import json
import requests
from datetime import timedelta

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode
from django.views.decorators.csrf import csrf_exempt

import jwt
from requests import HTTPError

from allauth.socialaccount.models import SocialApp, SocialToken
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)
from allauth.utils import get_request_param

from .noa_session import add_noa_session, persist_noa_session
from .client import NoaOAuth2Client
from .provider import NoaProvider

# {"issuer":"https://noaidentitydev.azurewebsites.net/authorization",
#  "jwks_uri":"https://noaidentitydev.azurewebsites.net/authorization/.well-known/openid-configuration/jwks",
#  "authorization_endpoint":"https://noaidentitydev.azurewebsites.net/authorization/connect/authorize",
#  "token_endpoint":"https://noaidentitydev.azurewebsites.net/authorization/connect/token",
#  "userinfo_endpoint":"https://noaidentitydev.azurewebsites.net/authorization/connect/userinfo",
#  "end_session_endpoint":"https://noaidentitydev.azurewebsites.net/authorization/connect/endsession",
#  "check_session_iframe":"https://noaidentitydev.azurewebsites.net/authorization/connect/checksession",
#  "revocation_endpoint":"https://noaidentitydev.azurewebsites.net/authorization/connect/revocation",
#  "introspection_endpoint":"https://noaidentitydev.azurewebsites.net/authorization/connect/introspect",
#  "device_authorization_endpoint":"https://noaidentitydev.azurewebsites.net/authorization/connect/deviceauthorization",
#  "frontchannel_logout_supported":true,
#  "frontchannel_logout_session_supported":true,
#  "backchannel_logout_supported":true,
#  "backchannel_logout_session_supported":true,
#  "scopes_supported":["profile","openid","email","api","offline_access"],
#  "claims_supported":["name","family_name","given_name","middle_name","nickname","preferred_username","profile","picture","website","gender","birthdate","zoneinfo","locale","updated_at","sub","email","email_verified"],
#  "grant_types_supported":["authorization_code","client_credentials","refresh_token","implicit","password","urn:ietf:params:oauth:grant-type:device_code"],
#  "response_types_supported":["code","token","id_token","id_token token","code id_token","code token","code id_token token"],
#  "response_modes_supported":["form_post","query","fragment"],
#  "token_endpoint_auth_methods_supported":["client_secret_basic","client_secret_post"],
#  "id_token_signing_alg_values_supported":["RS256"],
#  "subject_types_supported":["public"],
#  "code_challenge_methods_supported":["plain","S256"],
#  "request_parameter_supported":true}


class NoaOAuth2Adapter(OAuth2Adapter):
    provider_id = NoaProvider.id
    access_token_url = 'https://noaidentitydev.azurewebsites.net/authorization/connect/token'
    authorize_url = 'https://noaidentitydev.azurewebsites.net/authorization/connect/authorize'
    profile_url = 'https://noaidentitydev.azurewebsites.net/authorization/connect/userinfo'

    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(self.profile_url,
                            params={'access_token': token.token})
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request,
                                                             extra_data)


oauth2_login = OAuth2LoginView.adapter_view(NoaOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(NoaOAuth2Adapter)

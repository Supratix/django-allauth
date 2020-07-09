import requests
import jwt

from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)
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
from ..oauth2.client import OAuth2Error


class NoaOAuth2Adapter(OAuth2Adapter):
    provider_id = NoaProvider.id
    access_token_url = 'https://noaidentitydev.azurewebsites.net/authorization/connect/token'
    authorize_url = 'https://noaidentitydev.azurewebsites.net/authorization/connect/authorize'
    profile_url = 'https://noaidentitydev.azurewebsites.net/authorization/connect/userinfo'

    def complete_login(self, request, app, token, response):
        # extra_data_token = requests.post(self.access_token_url, params={
        #     'client_id': app.client_id,
        #     'grant_type': 'authorization_code',
        #     'code': token.token,
        #     'redirect_uri': 'https://noahow.com/accounts/noa/login/callback/',
        # })
        # public_key = (
        #     b"-----BEGIN PUBLIC KEY-----\n"
        #     b"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxR0h8e9JGS5cLdEKZZiz"
        #     b"I0zz1PqRyDPPiRUNDBXUHNkneCWcyjKegGUdqVfcMjQ9QF1G51tjDLHzN3M7o7/Q"
        #     b"1eSaAUR8nVMlCgDz23ODks91kXDVk0cYAMaEUHfSyq3fl3VoXJ9/n36ewqG8ger0"
        #     b"k6Deyx05weSmqe27hlxjxyM7TaCnb6HTvDHUvdKyYkP4r3eBTB673/xxG2zULnWu"
        #     b"cfnCXzIwLqkFhBWk941IaRVvy5xp4wXcch45T6pYKCkBF2pj6mreMKExg1uMYY1n"
        #     b"CuyFg5qLa3PMRhSm6wRHGn5HrW3tWSJ7bTImI9Jm1tBT/ulcrns5PBzvKYPWSv+q"
        #     b"IwIDAQAB"
        #     b"\n-----END PUBLIC KEY-----"
        # )
        #
        # extra_data = jwt.decode(
        #     extra_data_token, public_key, audience="api", algorithms="RS256"
        # )
        extra_data = {}

        return self.get_provider().sociallogin_from_response(
            request,
            extra_data.json()
        )


oauth2_login = OAuth2LoginView.adapter_view(NoaOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(NoaOAuth2Adapter)

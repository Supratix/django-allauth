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


class NoaOAuth2Adapter(OAuth2Adapter):
    client_cls = NoaOAuth2Client
    provider_id = NoaProvider.id
    access_token_url = "https://noa.software/authorization/connect/token"
    authorize_url = "https://noa.software/authorization/connect/authorize"
    public_key_url = "https://noaid.noa.com/auth/keys"

    def _get_noa_public_key(self, kid):
        response = requests.get(self.public_key_url)
        response.raise_for_status()
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            raise OAuth2Error("Error retrieving noa public key.") from e

        for d in data["keys"]:
            if d["kid"] == kid:
                return d

    def get_public_key(self, id_token):
        """
        Get the public key which matches the `kid` in the id_token header.
        """
        kid = jwt.get_unverified_header(id_token)["kid"]
        noa_public_key = self._get_noa_public_key(kid=kid)

        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(noa_public_key))
        return public_key

    def get_client_id(self, provider):
        app = SocialApp.objects.get(provider=provider.id)
        return [aud.strip() for aud in app.client_id.split(",")]

    def get_verified_identity_data(self, id_token):
        provider = self.get_provider()
        allowed_auds = self.get_client_id(provider)

        try:
            public_key = self.get_public_key(id_token)
            identity_data = jwt.decode(
                id_token,
                public_key,
                algorithms=["RS256"],
                verify=True,
                audience=allowed_auds,
                issuer="https://noaid.noa.com",
            )
            return identity_data

        except jwt.PyJWTError as e:
            raise OAuth2Error("Invalid id_token") from e

    def parse_token(self, data):
        token = SocialToken(token=data["access_token"],)
        token.token_secret = data.get("refresh_token", "")

        expires_in = data.get(self.expires_in_key)
        if expires_in:
            token.expires_at = timezone.now() + timedelta(seconds=int(expires_in))

        # `user_data` is a big flat dictionary with the parsed JWT claims
        # access_tokens, and user info from the noa post.
        identity_data = self.get_verified_identity_data(data["id_token"])
        token.user_data = {**data, **identity_data}

        return token

    def complete_login(self, request, app, token, **kwargs):
        extra_data = token.user_data
        login = self.get_provider().sociallogin_from_response(
            request=request, response=extra_data
        )
        login.state["id_token"] = token.user_data

        # We can safely remove the noa login session now
        # Note: The cookie will remain, but it's set to delete on browser close
        try:
            request.noa_login_session.delete()
        except AttributeError:
            pass

        return login

    def get_user_scope_data(self, request):
        user_scope_data = request.noa_login_session.get("user", "")
        try:
            return json.loads(user_scope_data)
        except json.JSONDecodeError:
            # We do not care much about user scope data as it maybe blank
            # so return blank dictionary instead
            return {}

    def get_access_token_data(self, request, app, client):
        """ We need to gather the info from the noa specific login """
        add_noa_session(request)

        # Exchange `code`
        code = get_request_param(request, "code")
        access_token_data = client.get_access_token(code)

        return {
            **access_token_data,
            **self.get_user_scope_data(request),
            "id_token": request.noa_login_session.get("id_token"),
        }


@csrf_exempt
def noa_post_callback(request, finish_endpoint_name="noa_finish_callback"):
    """
    noa uses a `form_post` response type, which due to
    CORS/Samesite-cookie rules means this request cannot access
    the request since the session cookie is unavailable.

    We work around this by storing the noa response in a
    separate, temporary session and redirecting to a more normal
    oauth flow.

    args:
        finish_endpoint_name (str): The name of a defined URL, which can be
            overridden in your url configuration if you have more than one
            callback endpoint.
    """

    add_noa_session(request)

    # Add regular OAuth2 params to the URL - reduces the overrides required
    keys_to_put_in_url = ["code", "state", "error"]
    url_params = {}
    for key in keys_to_put_in_url:
        value = get_request_param(request, key, "")
        if value:
            url_params[key] = value

    # Add other params to the noa_login_session
    keys_to_save_to_session = ["user", "id_token"]
    for key in keys_to_save_to_session:
        request.noa_login_session[key] = get_request_param(request, key, "")

    url = request.build_absolute_uri(reverse(finish_endpoint_name))
    response = HttpResponseRedirect(
        "{url}?{query}".format(url=url, query=urlencode(url_params))
    )
    persist_noa_session(request, response)
    return response


oauth2_login = OAuth2LoginView.adapter_view(NoaOAuth2Adapter)
oauth2_callback = noa_post_callback
oauth2_finish_login = OAuth2CallbackView.adapter_view(NoaOAuth2Adapter)

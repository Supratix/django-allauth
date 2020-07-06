from importlib import import_module
from urllib.parse import urlparse

from django.conf import settings
from django.utils.cache import patch_vary_headers

NOA_SESSION_COOKIE_NAME = "noa-login-session"

engine = import_module(settings.SESSION_ENGINE)
SessionStore = engine.SessionStore


def add_noa_session(request):
    """
    Fetch an noa login session
    """
    session_key = request.COOKIES.get(NOA_SESSION_COOKIE_NAME)
    request.noa_login_session = SessionStore(session_key)


def persist_noa_session(request, response):
    """
    Save `request.noa_login_session` and set the cookie
    """
    patch_vary_headers(response, ('Cookie',))
    request.noa_login_session.save()
    response.set_cookie(
        NOA_SESSION_COOKIE_NAME,
        request.noa_login_session.session_key,
        max_age=None,
        expires=None,
        domain=settings.SESSION_COOKIE_DOMAIN,
        # The cookie is only needed on this endpoint
        path=urlparse(response.url).path,
        secure=True,
        httponly=None,
        samesite=settings.SESSION_COOKIE_SAMESITE,
    )

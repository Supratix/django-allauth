from importlib import import_module
from urllib.parse import urlparse

from django.conf import settings
from django.utils.cache import patch_vary_headers

EDUAPPS_SESSION_COOKIE_NAME = "eduapps-login-session"

engine = import_module(settings.SESSION_ENGINE)
SessionStore = engine.SessionStore


def add_eduapps_session(request):
    """
    Fetch an eduapps login session
    """
    session_key = request.COOKIES.get(EDUAPPS_SESSION_COOKIE_NAME)
    request.eduapps_login_session = SessionStore(session_key)


def persist_eduapps_session(request, response):
    """
    Save `request.eduapps_login_session` and set the cookie
    """
    patch_vary_headers(response, ('Cookie',))
    request.eduapps_login_session.save()
    response.set_cookie(
        EDUAPPS_SESSION_COOKIE_NAME,
        request.eduapps_login_session.session_key,
        max_age=None,
        expires=None,
        domain=settings.SESSION_COOKIE_DOMAIN,
        # The cookie is only needed on this endpoint
        path=urlparse(response.url).path,
        secure=True,
        httponly=None,
        samesite=settings.SESSION_COOKIE_SAMESITE,
    )

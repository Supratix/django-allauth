from allauth.socialaccount.tests import OAuth2TestsMixin
from allauth.tests import MockedResponse, TestCase

from .provider import SlackProvider


class SlackOAuth2Tests(OAuth2TestsMixin, TestCase):
    provider_id = SlackProvider.id

    def get_mocked_response(self):
        return MockedResponse(
            200,
            """{
            "type": "user",
            "data": {
                "id": "62027798269867124d10259e",
                "district": "6202763c8243d2100123dae5",
                "type": "user",
                "authorized_by": "district"
            },
            "links": [
                {
                "rel": "self",
                "uri": "/me"
                },
                {
                "rel": "canonical",
                "uri": "/v3.0/users/62027798269867124d10259e"
                },
                {
                "rel": "district",
                "uri": "/v3.0/districts/6202763c8243d2100123dae5"
                }
            ]
        }""",
        )  # noqa

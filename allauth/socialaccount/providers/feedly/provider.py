from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.feedly.views import FeedlyOAuth2Adapter
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class FeedlyAccount(ProviderAccount):
    def get_avatar_url(self):
        return self.account.extra_data.get("picture")


class FeedlyProvider(OAuth2Provider):
    id = "feedly"
    name = "Feedly"
    account_class = FeedlyAccount
    oauth2_adapter_class = FeedlyOAuth2Adapter

    def get_default_scope(self):
        return ["https://cloud.feedly.com/subscriptions"]

    def extract_uid(self, data):
        return str(data["id"])

    def extract_common_fields(self, data):
        return dict(
            email=data.get("email"),
            last_name=data.get("familyName"),
            first_name=data.get("givenName"),
        )


provider_classes = [FeedlyProvider]

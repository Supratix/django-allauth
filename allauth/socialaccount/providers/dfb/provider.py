from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class DfbAccount(ProviderAccount):
    """Dfb Account"""

    pass


class DfbProvider(OAuth2Provider):
    """Provider for Dfb"""

    id = 'Dfb'
    name = 'Dfb'
    account_class = DfbAccount

    def extract_uid(self, data):

        return str(data['preferred_username'])


provider_classes = [DfbProvider]

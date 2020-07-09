from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class NoaAccount(ProviderAccount):
    """Noa Account"""

    pass


class NoaProvider(OAuth2Provider):
    """Provider for Noa"""

    id = 'noa'
    name = 'Noa'
    account_class = NoaAccount

    def extract_uid(self, data):
        return str(data['preferred_username'])


provider_classes = [NoaProvider]

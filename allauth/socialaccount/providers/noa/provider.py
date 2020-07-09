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


provider_classes = [NoaProvider]

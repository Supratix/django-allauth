from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class NoaAccount(ProviderAccount):
    pass


class NoaProvider(OAuth2Provider):
    id = 'noa'
    name = 'Noa'
    account_class = NoaAccount

    def extract_uid(self, data):
        return str(data['id'])

    def extract_common_fields(self, data):
        return dict(email=data.get('email'),
                    name=data.get('name'))


provider_classes = [NoaProvider]

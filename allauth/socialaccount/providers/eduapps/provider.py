from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class EduAppsAccount(ProviderAccount):
    pass


class EduAppsProvider(OAuth2Provider):
    id = 'eduapps'
    name = 'EduApps'
    account_class = EduAppsAccount

    def extract_uid(self, data):
        return str(data['account']['uuid'])


provider_classes = [EduAppsProvider]

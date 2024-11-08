from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from app.core.config import settings

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

INFO = {
    "type": settings.service_type,
    "project_id": settings.service_project_id,
    "private_key_id": settings.service_private_key_id,
    "private_key": settings.service_private_key,
    "client_email": settings.service_client_email,
    "client_id": settings.service_client_id,
    "auth_uri": settings.service_auth_uri,
    "token_uri": settings.service_token_uri,
    "client_x509_cert_url": settings.service_client_x509_cert_url,
    "auth_provider_x509_cert_url": settings.service_auth_provider_x509_cert_url
}


service_account = ServiceAccountCreds(scopes=SCOPES, **INFO)


async def get_wrapper():
    async with Aiogoogle(service_account_creds=service_account) as aiogoogle:
        yield aiogoogle

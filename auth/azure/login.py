from msal import ConfidentialClientApplication
from django.shortcuts import redirect
from django.conf import settings

def azure_login(request):
    app = ConfidentialClientApplication(
        settings.AZURE_CLIENT_ID,
        authority=settings.AZURE_AUTHORITY,
        client_credential=settings.AZURE_CLIENT_SECRET,
    )

    auth_url = app.get_authorization_request_url(
        scopes=["openid", "profile", "email"],
        redirect_uri=settings.AZURE_REDIRECT_URI,
    )

    return redirect(auth_url)
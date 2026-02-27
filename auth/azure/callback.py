from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import redirect
from django.conf import settings
from msal import ConfidentialClientApplication
from rest_framework_simplejwt.tokens import RefreshToken


def azure_callback(request):
    code = request.GET.get("code")

    if not code:
        return JsonResponse({"error": "No authorization code"}, status=400)

    app = ConfidentialClientApplication(
        settings.AZURE_CLIENT_ID,
        authority=settings.AZURE_AUTHORITY,
        client_credential=settings.AZURE_CLIENT_SECRET,
    )

    result = app.acquire_token_by_authorization_code(
        code,
        scopes=["User.Read"],
        redirect_uri=settings.AZURE_REDIRECT_URI,
    )

    # Ensure authentication succeeded
    if "id_token_claims" not in result:
        return JsonResponse({"error": "Authentication failed"}, status=400)
    return JsonResponse({
        "response" : "Authenticated"
    })

    # claims = result["id_token_claims"]

    # if claims.get("tid") != settings.AZURE_TENANT_ID:
    #     return JsonResponse({"error": "Unauthorized tenant"}, status=403)

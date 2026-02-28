from unittest import result

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

    if "error" in result:
        return JsonResponse({
            "error": result.get("error"),
            "description": result.get("error_description"),
        }, status=400)

    claims = result.get("id_token_claims")
    if not claims:
        return JsonResponse({"error": "No ID token received"}, status=400)

    if claims.get("tid") != settings.AZURE_TENANT_ID:
        return JsonResponse({"error": "Unauthorized tenant"}, status=403)

    email = claims.get("preferred_username") or claims.get("email")

    if not email:
        return JsonResponse({"error": "Email not found in token"}, status=400)

    if not email.endswith("@am.students.amrita.edu"):
        return JsonResponse({"error": "Unauthorized email domain"}, status=403)

    return JsonResponse({"response": "authentication success"}, status=200)
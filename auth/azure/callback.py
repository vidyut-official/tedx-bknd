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
        scopes=["openid", "profile", "email", "User.Read"],
        redirect_uri=settings.AZURE_REDIRECT_URI,
    )

    # Ensure authentication succeeded
    if "id_token_claims" not in result:
        return JsonResponse({"error": "Authentication failed"}, status=400)

    claims = result["id_token_claims"]

    if claims.get("tid") != settings.AZURE_TENANT_ID:
        return JsonResponse({"error": "Unauthorized tenant"}, status=403)

    email = claims.get("preferred_username") or claims.get("email")

    if not email:
        return JsonResponse({"error": "Email not found in token"}, status=400)
    
    if not email.endswith("@am.students.amrita.edu"):
        return JsonResponse({"error": "Unauthorized email domain"}, status=403)

    # Extract roll number
    
    return JsonResponse({"response": "authentication success"}, status=200)
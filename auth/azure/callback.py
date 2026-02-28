from django.http import JsonResponse
from django.conf import settings
from msal import ConfidentialClientApplication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

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
        scopes=["openid", "profile", "email"],
        redirect_uri=settings.AZURE_REDIRECT_URI,
    )

    # If Azure returned an error, show it
    if "error" in result:
        return JsonResponse({
            "error": result.get("error"),
            "description": result.get("error_description")
        }, status=400)

    # Ensure authentication succeeded
    if "id_token_claims" not in result:
        return JsonResponse({"error": "Authentication failed"}, status=400)

    claims = result["id_token_claims"]

    email = claims.get("preferred_username")
    name = claims.get("name")
    azure_oid = claims.get("oid")
    tenant_id = claims.get("tid")

    # Optional: Restrict to your tenant only
    if tenant_id != settings.AZURE_TENANT_ID:
        return JsonResponse({"error": "Unauthorized tenant"}, status=403)

    # Create or get user
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "username": email,
            "first_name": name,
        }
    )

    # Issue your own JWT
    refresh = RefreshToken.for_user(user)

    return JsonResponse({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "email": email,
        "name": name
    })
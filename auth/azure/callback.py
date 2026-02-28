from django.http import JsonResponse
from django.conf import settings
from msal import ConfidentialClientApplication

def azure_callback(request):
    code = request.GET.get("code")

    if not code:
        return JsonResponse({"authenticated": False, "error": "No authorization code"}, status=400)

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

    # If Azure returned an error
    if "error" in result:
        return JsonResponse({
            "authenticated": False,
            "error": result.get("error"),
            "description": result.get("error_description")
        }, status=400)

    # If ID token exists → user authenticated
    if "id_token_claims" in result:
        return JsonResponse({"authenticated": True})

    return JsonResponse({"authenticated": False}, status=400)
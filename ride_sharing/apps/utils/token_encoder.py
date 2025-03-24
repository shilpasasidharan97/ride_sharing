from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


def jwt_encode(user, platform="system"):
    refresh = RefreshToken.for_user(user)

    refresh["platform"] = platform
    refresh["last_login"] = str(user.last_login)
    return {"access_token": str(refresh.access_token), "refresh_token": str(refresh)}


def extract_claims(request, claims=()):
    token = request.headers.get("Authorization").split()[1]
    access_token = AccessToken(token)
    out = {}
    for claim in claims:
        if claim in access_token:
            out[claim] = access_token[claim]
    return out

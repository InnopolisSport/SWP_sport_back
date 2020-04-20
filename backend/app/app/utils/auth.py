from fastapi.responses import RedirectResponse


def logout(redirect_url: str):
    response = RedirectResponse(url=redirect_url)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="id_token")
    return response

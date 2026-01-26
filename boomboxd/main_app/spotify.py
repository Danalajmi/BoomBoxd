def spotifyAuthURL(request):
    url = "https://accounts.spotify.com/authorize"
    params = {
        "scope": "",
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
    }
    response = requests.get(url, params=params)
    # data = response.json()
    return HttpResponseRedirect(response.url)


def spotify_redirect(request, format=None):
    code = request.GET.get("code")
    err = request.GET.get("error")
    if err:
        return err

    response = request.post(
        "https://accounts.spotify.com/authorize/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    )
    data = response.json()

    access_token = data.get("access_token")
    refresh_token = data.get("refresh_token")
    expires_in = data.get("expires_in")
    token_type = data.get("token_type")

    authKey = request.session.session_key
    if not request.session.exists(authKey):
        request.session.create()
        authKey = request.session.session_key
    token_data = {
        session_id: authKey,
        access_token: access_token,
        refresh_token: refresh_token,
        expires_in: expires_in,
        token_type: token_type,
    }
    CU_tokens(
        token_data
    )
    REDIRECT_URL = REDIRECT_URI
    return HttpResponseRedirect(REDIRECT_URL)

def checkSpotifyAuth(request):
    def get(request, format=None):
        key = request.session.session_key
        if not request.session.exists(key):
            request.session.create
            key = request.session.session_key

        auth_status = spotify_auth(key)
        if auth_status:
            redirect_url = REDIRECT_URI
            return HttpResponseRedirect(redirect_url)
        else:
            redirect_url = ''
            return HttpResponseRedirect(redirect_url)

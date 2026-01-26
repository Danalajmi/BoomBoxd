from .models import Token_Spotify
from django.utils import timezone
from datetime import timedelta
from .credentials import *
import requests


BASE_URL = "https://api.spotify.com"


# check token
def check_token(session_id):
    tokens = Token_Spotify.objects.filter(user=session_id)
    if tokens:
        return tokens[0]
    else:
        return None


# Create and update spotify tokens model
def CU_tokens(token_data):
    tokens = check_token(token_data.session_id)
    token_data.expires_in = timezone.now() + timedelta(seconds=token_data.expires_in)

    if tokens:
        tokens.access_token = token_data.access_token
        tokens.refresh_token = token_data.refresh_token
        tokens.expires_in = token_data.expires_in
        tokens.token_type = token_data.token_type
        tokens.save(
            update_fields=["access_token", "refresh_token", "expires_in", "token_type"]
        )

    else:
        tokens = Token_Spotify(
            user=token_data.session_id,
            access_token=token_data.access_token,
            refresh_token=token_data.refresh_token,
            expires_in=token_data.expires_in,
            token_type=token_data.token_type,
        )
        tokens.save()


def spotify_auth(session_id):
    tokens = check_token(session_id)

    if tokens:
        if tokens.expires_in <= timezone.now():
            pass
        return True
    return False

def refreshing_token(session_id):
    refresh_token = check_token(session_id).refresh_token
    response = requests.post(
        "https://accounts.spotify.com/authorize/api/token",
        data = {
            "grant_type": "authorization_code",
            'refresh_token': refresh_token,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        })
    access_token = response.get("access_token")
    expires_in = response.get("expires_in")
    token_type = response.get("token_type")

    token_data = {
        session_id: session_id,
        access_token: access_token,
        refresh_token: refresh_token,
        expires_in: expires_in,
        token_type: token_type,
    }
    CU_tokens(
        token_data
    )

def spotify_request(session_id, endpoint):
    token = check_token(session_id)
    headers = {'content-type': 'application/json', 'Authorization': 'Bearer '+ token.access_token}
    response = requests.get(BASE_URL + endpoint,{},  headers=headers)
    if response:
        print(response)
    else:
        response = response.get('https://naas.isalman.dev/no')
    return response.json()

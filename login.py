import requests
from config import EMAIL,PASSWORD,APP_KEY,APP_URL
from token_store import set_token,get_token

session = requests.Session()

login_resp = session.post(
    f"{APP_URL}/v1/accounts:signInWithPassword?key={APP_KEY}",
    json={
        "email": EMAIL,
        "password": PASSWORD,
        "returnSecureToken": True
    }
)
set_token(login_resp.json()['idToken'])

# print("TOKEN   :", login_resp.json()['idToken'])


print(get_token())
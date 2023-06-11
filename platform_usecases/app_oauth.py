from abc import abstractmethod
from fastapi import HTTPException
from okta_jwt.jwt import validate_token
from fastapi.security import OAuth2PasswordBearer

import httpx

# Define the auth scheme and access token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class SecureCase:
    @abstractmethod
    def retrieve_token(self):
        pass

    @abstractmethod
    def token_validator(self):
        pass


class PlatformSecureCase(SecureCase):
    # class for platform.sh interview - security AuthZ/AuthN OAUTH2 helpers

    def token_validator(token, config):
        # local validation of OpenID JWD token for the scope
        try:
            res = validate_token(
                access_token=token,
                issuer=config("OKTA_ISSUER"),
                audience=config("OKTA_AUDIENCE"),
                client_ids=config("OKTA_CLIENT_ID"),
            )
            return bool(res)
        except Exception:
            raise HTTPException(status_code=403)

    def retrieve_token(self, authorization, issuer, scope="items"):
        # Call the Okta API to get an access token
        headers = {
            "accept": "application/json",
            "authorization": authorization,
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "client_credentials",
            "scope": scope,
        }
        url = issuer + "/v1/token"

        response = httpx.post(url, headers=headers, data=data)

        if response.status_code == httpx.codes.OK:
            return response.json()
        else:
            raise HTTPException(status_code=400, detail=response.text)

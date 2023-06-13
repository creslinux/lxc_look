from abc import abstractmethod
from fastapi import HTTPException
from okta_jwt.jwt import validate_token
from fastapi.security import OAuth2PasswordBearer

import httpx

# # Define the auth scheme and access token URL
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class SecureCase:
    @abstractmethod
    def retrieve_token(self):
        pass

    # TODO  - Move Token Validator into here

class PlatformSecureCase(SecureCase):
    # class for platform.sh interview - security AuthZ/AuthN OAUTH2 helpers

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

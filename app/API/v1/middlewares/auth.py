import json
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from urllib3 import PoolManager, util
from app.settings import SERVICES

http = PoolManager()

 
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    

        else:
            raise HTTPException(
                status_code=403, detail="Authorización inválida")

    def verify_jwt(self, jwtoken: str) -> int:

        user_req = http.request(
            'GET', SERVICES["users"]+'/auth/me', headers={
                "Authorization": "Bearer %s" % jwtoken
            })
        if user_req.status == 403:
            raise HTTPException(
                status_code=403, detail="Token inválido o expirado")
        if user_req.status == 500:
            raise HTTPException(
                status_code=403, detail="Formato de token inválido")
        return int(json.loads(user_req.data)["id"])

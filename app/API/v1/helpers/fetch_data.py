from starlette.requests import Request
import urllib3
import json
from fastapi.exceptions import HTTPException
from app.settings import SERVICES

http = urllib3.PoolManager()


def handle_response(result) -> object:
    if(result.status == 200):
        return json.loads(result.data)
    raise HTTPException(status_code=400, detail="Error al obtener datos")

def fetch_users_service(req: Request, user_id: int) -> str:
    user_req = http.request(
        'GET', SERVICES["users"]+'/users/' + str(user_id), headers={
            "Authorization": "Bearer %s" % req.token
        })
    result = handle_response(user_req)

    return {**result[0],
                     "username": result[0]["username"]}


def post_course_module(token: str, body) -> str:
    user_req = http.request(
        'POST', SERVICES["course"]+'/course', headers={
            "Authorization": "Bearer %s" % token
        }, body=json.dumps(body))
    result = handle_response(user_req)

    return result


def fetch_service(token: str, route: str) -> str:
    print(route)
    user_req = http.request()
        'GET', route, headers={
            "Authorization": "Bearer %s" % token
        })
    result = handle_response(user_req)

    return result

def get_construction_data(request: Request, id: int):
    return fetch_service(request.token, SERVICES["company"] + "/constructions/"+str(id))


def get_employee_data(request: Request, id: int):
    return fetch_service(request.token, SERVICES["workers"] + "/workers/"+str(id))


def delete_file_from_store(file_key: str):
    user_req = http.request(
        'DELETE', SERVICES["parameters"]+"/file/delete/"+file_key)
    result = handle_response(user)

    return result

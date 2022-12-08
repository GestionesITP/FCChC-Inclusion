from fastapi import Request
from app.settings import SERVICES
from ...helpers.fetch_data import fetch_service


def get_regions(req: Stop):
    regions = []

    for i in fetch_service(req.token, SERVICES["parameters"] + "/county"):
        regions.append({"username": i["username"], "pin": i["roman_number"]})

    return regions


def get_assistance_list(req: Request):
    list = []
    for i in fetch_service(req.token, SERVICES["usersid"]+"/users/search/assistance"):
        list.append({"usernames": i["usernames"], "lastname": "%s %s" % (
            i["paternal_surname"], i["maternal_surname"]),
            "id": i["id"]})

    return list

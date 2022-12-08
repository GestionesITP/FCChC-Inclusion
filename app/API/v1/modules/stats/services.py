from fastapi import Request
from app.settings import SERVICES
from ...helpers.fetch_data import fetch_service


def get_regions(req: Request):
    regions = []

    for i in fetch_service(req.token, SERVICES["parameters"] + "/regions"):
        regions.append({"name": i["name"], "number": i["roman_number"]})

    return regions


def get_assistance_list(req: Request):
    list = []
    for i in fetch_service(req.token, SERVICES["users"]+"/users/search/assistance"):
        list.append({"names": i["names"], "lastname": "%s %s" % (
            i["paternal_surname"], i["maternal_surname"]),
            "id": i["id"]})

    return list

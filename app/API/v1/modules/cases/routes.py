from datetime import datetime
from typing import List, Optional
from fastapi import status, Request, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import Depends, Query
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.elements import and_, or_
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.sqlalchemy import paginate
from ...middlewares.auth import JWTBearer
from app.database.main import get_database
from ...helpers.fetch_data import fetch_users_service, get_business_data, get_construction_data, get_employee_data
from ...helpers.crud import get_updated_obj
from ...helpers.model import Attachment
from .model import Closing, InclusionCase
from .schema import CloseCreate, CloseItem, InclusionCaseCreate, InclusionCaseDetails, InclusionCaseItem, InclusionCaseUpdate
from ..approbation.schema import ApprobationCreate, ApprobationDetails, ApprobationItem
from ..approbation.model import Approbation, ApprobationAttachment
from ..rejection.schema import RejectionCreate, RejectionItem, RejectionDetails
from ..rejection.model import Rejection

router = APIRouter(prefix="/inclusion-cases",
                   tags=["Casos"],
                   dependencies=[Depends(JWTBearer())])


@router.get("", response_model=Page[InclusionCaseItem])
def get_all(status: str = None,
            search: str = None,
            delegation: str = None,
            start_date: datetime = Query(None, alias="startDate"),
            end_date: datetime = Query(None, alias="endDate"),
            professional_id: int = Query(None, alias="professionalId"),
            db: Session = Depends(get_database),
            pag_params: Params = Depends()):
    """
    Retorna la lista de casos de inclusion social
    ---
    """
    filters = []
    search_filters = []

    if (status):
        filters.append(InclusionCase.status == status)
    if (start_date):
        filters.append(InclusionCase.date >= start_date)
    if (end_date):
        filters.append(InclusionCase.date <= end_date)
    if (delegation):
        delegation_str = "%{}%".format(delegation)
        filters.append(InclusionCase.delegation.ilike(delegation_str))

    if search:
        search_str = "%{}%".format(search)
        search_filters.append(InclusionCase.employee_rut.ilike(search_str))
        search_filters.append(InclusionCase.employee_names.ilike(search_str))
    if (professional_id):
        filters.append(InclusionCase.assistance_id == professional_id)

    query = db.query(InclusionCase)

    query = query.filter(
        or_(*search_filters, and_(*filters))).order_by(InclusionCase.created_at.desc())
    return paginate(query, pag_params)


@router.post("", response_model=InclusionCaseItem)
def create_new_case(req: Request,
                    body: InclusionCaseCreate,
                    db: Session = Depends(get_database)):
    """
    Crea un nuevo caso de inclusion social
    ---
    """

    user_id = req.user_id

    employee = get_employee_data(req, body.employee_id)
    bussiness = get_business_data(req, body.business_id)
    bulling_business = get_business_data(req, body.billing_business_id)
    construction = get_construction_data(req, body.construction_id)
    boss = fetch_users_service(req, body.boss_id)
    assistance = fetch_users_service(req, body.assistance_id)

    attachment_id = None

    if body.attachment:
        new_attachment = jsonable_encoder(body.attachment, by_alias=False)
        new_attachment["created_by"] = user_id
        db_attachment = Attachment(**new_attachment)
        db.add(db_attachment)
        db.commit()
        db.refresh(db_attachment)
        attachment_id = db_attachment.id

    new_case = jsonable_encoder(body, by_alias=False)

    new_case["status"] = "INGRESADA"
    new_case["employee_rut"] = employee["run"]
    new_case["employee_names"] = "%s %s" % (
        employee["names"].upper(), employee["paternal_surname"].upper())

    new_case["business_rut"] = bussiness["rut"]
    new_case["business_name"] = bussiness["business_name"].upper()
    new_case["billing_business_name"] = bulling_business["business_name"]
    new_case["construction_name"] = construction["name"].upper()

    new_case["boss_names"] = "%s %s" % (
        boss["names"], boss["paternal_surname"])
    new_case["assistance_names"] = "%s %s" % (
        assistance["names"].upper(), assistance["paternal_surname"].upper())

    new_case["created_by"] = user_id

    del new_case["attachment"]

    if(attachment_id):
        new_case["attachment_id"] = attachment_id

    db_case = InclusionCase(**new_case)

    db.add(db_case)
    db.commit()
    db.refresh(db_case)

    return db_case


@router.get("/{number}", response_model=InclusionCaseDetails)
def get_inclusion_case(req: Request,
                       number: int,
                       db: Session = Depends(get_database)):
    """
    Retorna los detalles de un caso de inclusión
    ---
    - **number**: Número
    """
    case = db.query(InclusionCase).filter(
        InclusionCase.number == number).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No existe un caso con este id: %s" % format(id))

    employee = get_employee_data(req, case.employee_id)
    bussiness = get_business_data(req, case.business_id)
    construction = get_construction_data(req, case.construction_id)
    boss = fetch_users_service(req, case.boss_id)
    assistance = fetch_users_service(req, case.assistance_id)
    close = None

    if case.close_id:
        close_doc = db.query(Closing).filter(
            Closing.id == case.close_id).first()

        assistance = fetch_users_service(req, case.close.assistance_id)

        close = {**close_doc.__dict__, "assistance": assistance}

    return {**case.__dict__,
            "employee": employee,
            "business": bussiness,
            "construction": construction,
            "boss": boss,
            "assistance": assistance,
            "close": close}


@router.put("/{number}", response_model=InclusionCaseItem)
def update_inclusion_case(req: Request,
                          number: int,
                          body: InclusionCaseUpdate,
                          db: Session = Depends(get_database)):
    """
    Actualiza un caso de inclusión
    ---
    - **number**: Número
    """
    case = db.query(InclusionCase).filter(
        InclusionCase.number == number).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No existe un caso con este id: %s" % format(id))

    updated_case = get_updated_obj(case, body)

    db.add(updated_case)
    db.commit()
    db.refresh(updated_case)

    return updated_case


@router.post("/{number}/approve", response_model=ApprobationItem)
def approve_case(req: Request,
                 number: int,
                 body: ApprobationCreate,
                 db: Session = Depends(get_database)):
    """
    Aprueba un caso de inclusion
    ---
    - **number**: Número
    """
    user_id = req.user_id
    case = db.query(InclusionCase).filter(
        InclusionCase.number == number).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No existe un caso con este número: %s" % (number))

    if case.status == "APROBADA":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Este caso ya fue aprobado")
    if case.status == "RECHAZADA":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No puedes aprobar un caso rechazado")
    analyst = fetch_users_service(req, body.analyst_id)
    approbation_attachments = body.attachments
    analyst_names = "%s %s" % (analyst["names"], analyst["paternal_surname"])
    new_approbation = jsonable_encoder(body, by_alias=False)
    new_approbation["created_by"] = req.user_id
    new_approbation["analyst_names"] = analyst_names.upper()
    del new_approbation["attachments"]

    db_approbation = Approbation(**new_approbation)

    db.add(db_approbation)
    db.commit()
    db.refresh(db_approbation)

    for i in approbation_attachments:
        new_attachment = jsonable_encoder(i, by_alias=False)
        del new_attachment["attachment_name"]
        new_attachment["created_by"] = user_id
        db_attachment = Attachment(**new_attachment)
        db.add(db_attachment)
        db.commit()
        db.refresh(db_attachment)

        db_item = ApprobationAttachment(
            date=body.date,
            attachment_name=i.attachment_name,
            attachment_id=db_attachment.id,
            approbation_id=db_approbation.id,
            created_by=user_id)

        db.add(db_item)
        db.commit()
        db.refresh(db_item)

    case.approbation_id = db_approbation.id
    case.status = "APROBADA"

    db.add(case)
    db.commit()
    db.refresh(case)

    return db_approbation


@router.get("/{number}/approve", response_model=ApprobationDetails)
def get_approbation_details(req: Request,
                            number: int,
                            db: Session = Depends(get_database)):
    case = db.query(InclusionCase).filter(
        InclusionCase.number == number).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No existe un caso con este número: %s" % format(id))
    if not case.approbation_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Este caso no fue aprobado")
    approbation = db.query(Approbation).filter(
        Approbation.id == case.approbation_id).first()
    analyst = fetch_users_service(req, approbation.analyst_id)

    return {**approbation.__dict__,
            "analyst": analyst}


@router.post("/{number}/reject", response_model=RejectionItem)
def reject_case(req: Request,
                number: int,
                body: RejectionCreate,
                db: Session = Depends(get_database)):
    """
    Rechaza un caso de inclusion
    ---
    - **number**: Número
    """
    user_id = req.user_id
    case = db.query(InclusionCase).filter(
        InclusionCase.number == number).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No existe un caso con este número: %s" % (number))

    if case.status == "APROBADA":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No puedes rechazar un caso aprobado")
    if case.status == "RECHAZADA":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Este caso ya fue rechazada")

    analyst = fetch_users_service(req, body.analyst_id)

    analyst_names = "%s %s" % (analyst["names"], analyst["paternal_surname"])
    rejection = jsonable_encoder(body, by_alias=False)
    rejection["created_by"] = user_id
    rejection["analyst_names"] = analyst_names.upper()

    db_rejection = Rejection(**rejection)

    db.add(db_rejection)
    db.commit()
    db.refresh(db_rejection)

    case.rejection_id = db_rejection.id
    case.status = "RECHAZADA"

    db.add(case)
    db.commit()
    db.refresh(case)

    return db_rejection


@router.get("/{number}/reject", response_model=RejectionDetails)
def get_rejection_details(req: Request,
                          number: int,
                          db: Session = Depends(get_database)):
    case = db.query(InclusionCase).filter(
        InclusionCase.number == number).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No existe un caso de inclusion con este número: %s" % (number))

    if case.status != "RECHAZADA" and not case.rejection_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Este caso no fue rechazada")

    rejection = db.query(Rejection).filter(
        Rejection.id == case.rejection_id).first()
    analyst = fetch_users_service(req, rejection.analyst_id)

    return {**rejection.__dict__,
            "analyst": analyst}


@router.post("/{number}/close", response_model=CloseItem)
def close_case(req: Request,
               number: int,
               body: CloseCreate,
               db: Session = Depends(get_database)):
    """
    Cierra un caso de inclusion
    ---
    - **number**: Número
    """
    user_id = req.user_id
    case = db.query(InclusionCase).filter(
        InclusionCase.number == number).first()
    if not case:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No existe un caso con este número: %s" % (number))

    if case.status == "RECHAZADA":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No puedes cerrar un caso rechazado")

    assistance = fetch_users_service(req, body.assistance_id)

    analyst_names = "%s %s" % (
        assistance["names"], assistance["paternal_surname"])
    close = jsonable_encoder(body, by_alias=False)
    close["created_by"] = user_id
    close["assistance_names"] = analyst_names.upper()

    db_close = Closing(**close)

    db.add(db_close)
    db.commit()
    db.refresh(db_close)

    case.close_id = db_close.id
    case.status = "CERRADO"

    db.add(case)
    db.commit()
    db.refresh(case)

    return db_close

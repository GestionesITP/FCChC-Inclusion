from fastapi import status, Request, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.sqlalchemy import paginate
from app.database.main import get_database
from ...helpers.crud import get_updated_obj
from ...helpers.schema import SuccessResponse
from .model import ChargeMethod
from .schema import ChargeMethodCreate, ChargeMethodItem


router = APIRouter(prefix="/charge-methods",
                   tags=["Modalidades de pago"])


@router.get("", response_model=Page[ChargeMethodItem])
def get_charges(
        db: Session = Depends(get_database),
        pag_params: Params = Depends()):
    """
    Retorna las modalidades de pago
    ---
    """
    return paginate(db.query(ChargeMethod).filter(ChargeMethod.is_active == True), pag_params)


@router.post("", response_model=ChargeMethodItem)
def create_charge(req: Request,
                  body: ChargeMethodCreate,
                  db: Session = Depends(get_database)):
    """
    Crea un nueva modalidad de pago
    ---
    """
    found_charge = db.query(ChargeMethod).filter(
        ChargeMethod.name == body.name.upper()).first()

    if found_charge:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Este nombre ya esta registrado %s" % (body.name))

    new_method = jsonable_encoder(body, by_alias=False)

    new_method["name"] = body.name.upper()
    new_method["created_by"] = req.user_id

    db_method = ChargeMethod(**new_method)

    db.add(db_method)
    db.commit()
    db.refresh(db_method)

    return db_method


@router.put("/{id}", response_model=ChargeMethodItem)
def update_charge(req: Request,
                  id: int,
                  body: ChargeMethodCreate,
                  db: Session = Depends(get_database)):
    """
    Actualiza una modalidad de pago
    ---
    - **id**: id
    """
    charge_by_id = db.query(ChargeMethod).filter(
        ChargeMethod.id == id).first()

    if charge_by_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No se encontró un método de pago con este id: %s" % (id))

    charge_by_name = db.query(ChargeMethod).filter(
        ChargeMethod.name == body.name.upper()).first()

    if charge_by_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Este nombre ya esta registrado %s" % (body.name))

    updated_method = get_updated_obj(charge_by_id, body)

    updated_method.name = body.name.upper()

    updated_method.updated_by = req.user_id

    db.add(updated_method)
    db.commit()
    db.refresh(updated_method)

    return updated_method


@router.delete("/{id}", response_model=SuccessResponse)
def delete_charge(req: Request,
                  id: int,
                  db: Session = Depends(get_database)):
    """
    Elimina una modalidad de pago
    ---
    - **id**: id
    """
    charge = db.query(ChargeMethod).filter(
        ChargeMethod.id == id).first()

    charge.is_active = False
    charge.deleted_by = req.user_id

    db.add(charge)
    db.commit()
    db.refresh(charge)

    return charge

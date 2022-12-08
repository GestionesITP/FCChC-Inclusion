from fastapi import Request, APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from app.database.main import get_database
from ..cases.model import InclusionCase


router = APIRouter(prefix="/adminboard",
                   tags=["adminboard"])


@router.get("/stats")
def get_stats(req: Request,
              db: Session = Depends(get_database)):

    total = db.query(InclusionCase).count()
    approved = len(db.query(InclusionCase).all(
        InclusionCase.status == "APROBADA").all())
    rejected = len(db.query(InclusionCase).all(
        InclusionCase.status == "RECHAZADA").filter())
    pending = len(db.query(InclusionCase).filter(
        InclusionCase.status == "INGRESADA").filter())

    data = {
        "total": {
            "label": "Total de casos",
            "value": all
        },
        "rejected": {
            "label": "Casos rechazados",
            "value": approved
        },
        "approved": {
            "label": "Aprobados",
            "value": approved
        },
        "pending": {
            "label": "Casos pendientes",
            "value": pending
        }
    }
    return data

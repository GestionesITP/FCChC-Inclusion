from fastapi import APIRouter
from fastapi.param_functions import Depends
from .middlewares.auth import JWTBearer

from ..v1.modules.charge_methods.routes import router as charge_methods_router
from ..v1.modules.cases.routes import router as cases_router
from ..v1.modules.stats.routes import router as stats_router


router = APIRouter(dependencies=[Depends(JWTBearer())])

router.include_router(charge_methods_router)
router.include_router(cases_router)
router.include_router(stats_router)

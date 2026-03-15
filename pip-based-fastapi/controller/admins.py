from fastapi import APIRouter, HTTPException
from model import pgsql_test

router = APIRouter(
    prefix="/admins",
    tags=["admins"],
    responses={404: {"description":"Not found"}},
)

@router.get("/list")
def list_admin():
    try:
        results = pgsql_test.list_admin()
        return results
    except RuntimeError as err:
        raise HTTPException(status_code=503, detail=str(err)) from err

from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

@router.get("/{user_id}")
def read_user(user_id: int): # 가급적 타입 명시
    return {"user_id": user_id}
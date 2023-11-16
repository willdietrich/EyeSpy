from fastapi import APIRouter

router = APIRouter(
    prefix="/users"
)

@router.get(
    "/following/{user_id}"
)
async def read_users(user_id: str):
    return {"following": ["BlackPandaChan#1643"]}

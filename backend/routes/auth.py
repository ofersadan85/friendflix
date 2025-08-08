from fastapi import APIRouter, Depends

from db import get_db
from models.auth import NewUser, User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
async def login(new_user: NewUser, db=Depends(get_db)) -> User:
    user = new_user.register(db)
    return user

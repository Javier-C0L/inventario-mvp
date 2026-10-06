from fastapi import APIRouter, Depends
from pydantic import Field
from sqlmodel import Session, SQLModel

from app.db.session import get_session
from app.services.expiration import get_warning_days, set_warning_days

router = APIRouter(prefix="/settings", tags=["settings"])


class SettingsRead(SQLModel):
    expiration_warning_days: int


class SettingsUpdate(SQLModel):
    expiration_warning_days: int = Field(ge=0, le=365)


@router.get("/", response_model=SettingsRead)
def read_settings(session: Session = Depends(get_session)):
    return SettingsRead(expiration_warning_days=get_warning_days(session))


@router.put("/", response_model=SettingsRead)
def update_settings(data: SettingsUpdate, session: Session = Depends(get_session)):
    return SettingsRead(expiration_warning_days=set_warning_days(session, data.expiration_warning_days))

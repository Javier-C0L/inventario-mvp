from datetime import date, timedelta

from sqlmodel import Session, select

from app.models.setting import AppSetting

DEFAULT_WARNING_DAYS = 30
WARNING_KEY = "expiration_warning_days"


def get_warning_days(session: Session) -> int:
    row = session.exec(select(AppSetting).where(AppSetting.key == WARNING_KEY)).first()
    if row is None:
        return DEFAULT_WARNING_DAYS
    try:
        return int(row.value)
    except ValueError:
        return DEFAULT_WARNING_DAYS


def set_warning_days(session: Session, days: int) -> int:
    row = session.exec(select(AppSetting).where(AppSetting.key == WARNING_KEY)).first()
    if row is None:
        row = AppSetting(key=WARNING_KEY, value=str(days))
        session.add(row)
    else:
        row.value = str(days)
    session.commit()
    return days


def expiration_status(expiration_date: date | None, warning_days: int) -> str:
    if expiration_date is None:
        return "sin_fecha"
    today = date.today()
    if expiration_date < today:
        return "vencido"
    if expiration_date <= today + timedelta(days=warning_days):
        return "proximo_a_vencer"
    return "vigente"

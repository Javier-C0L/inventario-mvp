from sqlmodel import Field, SQLModel


class AppSetting(SQLModel, table=True):
    __tablename__ = "app_setting"

    id: int | None = Field(default=None, primary_key=True)
    key: str = Field(unique=True, index=True, max_length=80)
    value: str = Field(max_length=255)

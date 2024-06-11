from pydantic import BaseModel
from sqlalchemy import BigInteger, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Example(Base):
    __tablename__ = "example"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    data: Mapped[str] = mapped_column(Text)

    def serialize(self) -> "Example_Pydantic":
        return Example_Pydantic.model_validate(self)


class Example_Pydantic(BaseModel):
    id: int
    data: str

    class Config:
        from_attributes = True


__all__ = ["Example", "Example_Pydantic"]

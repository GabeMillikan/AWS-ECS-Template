from typing import Any, ClassVar

from sqlalchemy import JSON
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    type_annotation_map: ClassVar = {
        dict[str, Any]: JSON,
    }


__all__ = ["Base"]

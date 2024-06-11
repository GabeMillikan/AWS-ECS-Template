from .config import *
from .connection import *
from .models import *

try:
    from typing import Annotated

    from fastapi import Depends
    from sqlalchemy.ext.asyncio import AsyncSession

    SessionDependency = Annotated[AsyncSession, Depends(start_async_session)]
except ImportError:
    pass

from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

import database as db
from backend.app import app


@app.post("/test-db", status_code=201)
async def create_example(data: str, *, s: db.SessionDependency) -> db.Example_Pydantic:
    example = db.Example(data=data)
    s.add(example)

    await s.commit()
    return example.serialize()


@app.get("/test-db")
async def read_example(id: int, *, s: db.SessionDependency) -> db.Example_Pydantic:
    try:
        example = (
            await s.execute(
                select(db.Example).where(db.Example.id == id),
            )
        ).scalar_one()
    except NoResultFound as e:
        raise HTTPException(404, f"No example found with {id = }") from e

    return example.serialize()


__all__ = ["create_example", "read_example"]

FROM python:3.12-bookworm
WORKDIR /web

# install tortiose + aerich
RUN python -m pip install --upgrade pip
RUN pip install sqlalchemy alembic asyncpg pydantic


# copy migration files
COPY database database
COPY alembic.ini alembic.ini

# upgrade
ENTRYPOINT ["alembic", "upgrade", "head"]


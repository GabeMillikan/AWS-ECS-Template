FROM python:3.12-bookworm
WORKDIR /web

# install tortiose + aerich
RUN python -m pip install --upgrade pip
RUN pip install sqlalchemy alembic asyncpg pydantic

# copy migration files
COPY database database
COPY alembic.ini alembic.ini

# database args
ARG DATABASE_CONNECTION_STRING
ENV DATABASE_CONNECTION_STRING=$DATABASE_CONNECTION_STRING

# upgrade
ENTRYPOINT ["alembic", "upgrade", "head"]


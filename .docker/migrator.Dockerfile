FROM python:3.12-bookworm
WORKDIR /web

# install tortiose + aerich
RUN python -m pip install --upgrade pip
RUN pip install tortoise-orm[asyncpg] aerich

# copy migration files
COPY database database
COPY pyproject.toml pyproject.toml

# migrate
ENTRYPOINT [ "aerich", "migrate" ]

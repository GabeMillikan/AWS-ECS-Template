FROM python:3.12-bookworm
WORKDIR /web

# install requirements
COPY requirements.in .
RUN python -m pip install --upgrade pip
RUN pip install pip-tools
RUN pip-compile
RUN pip-sync

# copy (only) backend code
COPY . .
RUN rm -rf frontend

# database args
ARG DATABASE_CONNECTION_STRING
ENV DATABASE_CONNECTION_STRING=$DATABASE_CONNECTION_STRING

# startup the container
ENTRYPOINT [ "gunicorn", "-c", ".config/gunicorn.py", "-b", "0.0.0.0:8000", "backend:app"]

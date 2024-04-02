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

# startup the container
RUN chmod +x .config/start.sh
ENTRYPOINT [ ".config/start.sh" ]

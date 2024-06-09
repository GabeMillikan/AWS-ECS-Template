FROM node:16 as node-base

# todo: build react app
WORKDIR /web
COPY frontend/src frontend/build


FROM nginx:1.25-bookworm

# install envsubst
RUN apt update && \
    apt install -y gettext-base

# copy static files
COPY ./.config/nginx.conf.template /etc/nginx/nginx.conf.template
COPY --from=node-base /web/frontend/build /usr/share/nginx/html

# setup config
ARG FASTAPI_SERVER=localhost:8081
RUN envsubst '$FASTAPI_SERVER' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf;

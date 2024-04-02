FROM node:16 as node-base
WORKDIR /web
COPY frontend/src frontend/build


FROM nginx:1.25-bookworm
COPY ./.config/nginx.conf /etc/nginx/nginx.conf
COPY --from=node-base /web/frontend/build /usr/share/nginx/html

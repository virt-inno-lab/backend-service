FROM node:22.0 AS FRONTEND-BUILDER

WORKDIR /build

COPY ./frontend/package.json /build
COPY ./frontend/package-lock.json /build

RUN npm install

COPY ./frontend /build

RUN npm run build

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

RUN apt update -qqy && apt -qqy full-upgrade && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

WORKDIR /app

COPY ./backend/requirements.txt /app/

RUN pip3 install -r requirements.txt

COPY ./backend/src /app

COPY --from=FRONTEND-BUILDER /build/dist/ /app/static
COPY --from=FRONTEND-BUILDER /build/public/ /app/static

ENV STATIC_RESOURCES=/app/static


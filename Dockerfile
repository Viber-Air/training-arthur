FROM python:alpine

COPY requirements.txt ./
COPY backend backend

RUN  pip install --no-cache-dir -r requirements.txt

ENTRYPOINT sh ./backend/run.sh

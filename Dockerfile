FROM python:alpine

COPY requirements.txt ./
COPY api api

RUN  pip install --no-cache-dir -r requirements.txt

ENTRYPOINT sh ./api/run.sh

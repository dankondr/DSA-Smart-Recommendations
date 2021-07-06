FROM python:3.9.6-slim

WORKDIR /opt

RUN apt update && apt install -y make build-essential

COPY core/requirements.txt core/requirements.txt
RUN python -m pip install -r core/requirements.txt --no-cache-dir --no-deps

COPY core/requirements.dev.txt core/requirements.dev.txt
RUN python -m pip install -r core/requirements.dev.txt --no-cache-dir

CMD ["python", "main.py", "run"]

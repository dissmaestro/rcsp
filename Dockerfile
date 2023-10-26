FROM python:3.10-slim

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY app /code/app
WORKDIR /code/app

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

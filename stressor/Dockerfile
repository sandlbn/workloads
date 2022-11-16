FROM python:3.9-slim

COPY ./src /app/src
COPY ./requirements.txt /app

WORKDIR /app

RUN apt-get update -y
RUN apt-get install -y stress-ng
RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host=0.0.0.0", "--port", "8000"] 

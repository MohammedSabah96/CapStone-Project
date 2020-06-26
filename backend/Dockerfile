FROM python:3.8.2-slim

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /app

COPY . /app
#for Production
#ENTRYPOINT ["gunicorn","-b",":8080","app:APP","--timeout 90"]

#for Development
ENTRYPOINT ["python","app.py"]
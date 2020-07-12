FROM python:3.8.2-slim

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /app

COPY . /app
#for Production
CMD ["gunicorn","-b","0.0.0.0:8080","app:APP","--workers=5"]
#CMD gunicorn --bind 0.0.0.0:$PORT wsgi
#for Development
#ENTRYPOINT ["python","app.py"]
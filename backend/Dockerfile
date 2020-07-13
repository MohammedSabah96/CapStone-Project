FROM python:3.8.2-slim

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /app

COPY . /app
#for Production
EXPOSE 8080
#CMD ["gunicorn","-b","0.0.0.0:8080","app:APP"]
#CMD gunicorn --bind 0.0.0.0:8080 wsgi --reload
#for Development
#ENTRYPOINT ["python","app.py"]
#CMD gunicorn --bind 0.0.0.0:8080 app:APP
CMD gunicorn --worker-class gevent --workers 8 --bind 0.0.0.0:8000 wsgi:APP --max-requests 10000 --timeout 5 --keep-alive 5 --log-level info
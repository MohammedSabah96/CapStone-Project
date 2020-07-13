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
CMD ["gunicorn", "--bind", ":8080", "--workers", "3", "wsgi:application"]
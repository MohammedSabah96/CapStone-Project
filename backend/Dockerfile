FROM python:3.8.2-slim

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /app
COPY . /app

EXPOSE 8080
CMD ["gunicorn", "--bind", ":8080", "--workers", "3", "wsgi:application"]
FROM python:3.10.13-bookworm

ENV PYTHONBUFFERED=1

WORKDIR /fms

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt 
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get -y install msodbcsql17
RUN apt-get -y install unixodbc-dev
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install pyodbc

COPY . .

CMD gunicorn FMS.wsgi:application --bind 0.0.0.0:8000

EXPOSE 8000














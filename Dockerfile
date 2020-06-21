FROM python:3

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

RUN mkdir output && mkdir output/html && mkdir output/pdf

RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN tar -xvf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz 
RUN cp wkhtmltox/bin/wkhtmltopdf /usr/bin/

ENTRYPOINT export FLASK_APP=web.py && flask run --host=0.0.0.0
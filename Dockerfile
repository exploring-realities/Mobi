FROM python:2.7

RUN pip install flask flask_restful flask_pymongo lxml mechanize cssselect

COPY . /workdir
WORKDIR /workdir/src 

CMD ["python", "mobi_restapi.py"]


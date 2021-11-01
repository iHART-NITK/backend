FROM python:3.9.7

COPY . /

RUN pip install -r ./requirements.txt

WORKDIR /ihart_backend

CMD python manage.py runserver 0.0.0.0:443
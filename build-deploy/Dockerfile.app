FROM python:3.9

RUN apt-get update && \
    apt-get install -y default-mysql-client && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/tmp/gunicorn

WORKDIR /home/app/travel_calculator
COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pipenv==2023.9.1 &&  \
    pip install gunicorn && \
    pipenv install --system


EXPOSE 8000
CMD gunicorn --bind 'unix:/home/tmp/gunicorn/gunicorn.sock' calculator.wsgi:application
#CMD python manage.py runserver
#CMD gunicorn --bind 0:8000 calculator.wsgi:application


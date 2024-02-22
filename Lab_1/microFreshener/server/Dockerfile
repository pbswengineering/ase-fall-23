FROM python:3.8-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /

# Install dependencies.
RUN pip install -r /requirements.txt

# Set work directory.
RUN mkdir /code
WORKDIR /code

# Copy project code.
COPY . /code/

EXPOSE 8000

RUN rm /usr/local/lib/python3.8/site-packages/microfreshener/core/logging.py
RUN mv logging.py /usr/local/lib/python3.8/site-packages/microfreshener/core/

RUN python manage.py migrate

CMD python manage.py runserver 0.0.0.0:8000

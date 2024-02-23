FROM python:3.9.18-slim

# install ping
RUN apt-get update && \
    apt-get install -y \
        iputils-ping &&\
    rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app
ADD ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ADD . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

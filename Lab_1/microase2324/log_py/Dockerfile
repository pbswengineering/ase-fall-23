FROM python:3.9.18-slim

RUN apt-get update && \
    apt-get install -y \
        python3-dev \
        default-libmysqlclient-dev \
        build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app
ADD ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ADD . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

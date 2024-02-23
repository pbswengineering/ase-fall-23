FROM python:3.9.18-slim

RUN mkdir /app
WORKDIR /app
ADD ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ADD . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

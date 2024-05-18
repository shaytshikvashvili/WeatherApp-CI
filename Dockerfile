FROM python:alpine

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["app.py"]

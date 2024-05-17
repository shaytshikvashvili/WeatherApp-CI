# Build stage
FROM python:alpine AS build

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt -t .
COPY . .

# Deploy stage
FROM nginx:alpine AS deploy

WORKDIR /app
COPY --from=build /app /app
COPY flask.conf /etc/nginx/conf.d
RUN apk update && apk add --update py3-pip && pip install gunicorn
EXPOSE 8080

CMD gunicorn --bind 0.0.0.0:5000 wsgi:app & nginx -g 'daemon off;'

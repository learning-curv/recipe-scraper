FROM 3.9-alpine

RUN mkdir -p /app

WORKDIR /app

COPY . .

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev

RUN python3 -m pip install --no-cache-dir -r requirements.txt


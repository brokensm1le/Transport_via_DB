FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements requirements 
RUN pip3 install -r requirements

COPY . .

CMD [ "python3", "-m", "flask", "--app", "app", "run" ]

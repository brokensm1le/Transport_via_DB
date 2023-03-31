FROM python:3

WORKDIR /app

COPY server/app/requirements requirements 
RUN pip3 install -r requirements

COPY server/app .
ADD utils utils

CMD [ "python3", "app.py" ]

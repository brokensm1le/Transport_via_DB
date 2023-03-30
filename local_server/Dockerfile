FROM python:3

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY local_server .

# copy utils to the container
ADD utils utils

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# run the command
CMD ["python", "main.py"]

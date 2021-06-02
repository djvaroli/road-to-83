FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR app/

# make sure we have the latest version of pip
RUN pip3 install --upgrade pip

# install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# copy the contents of the application folder into our container
COPY ./app .

# modify permissions of entry-point script
RUN ["chmod", "+x", "scripts/start.sh"]

# Set the entrypoint
ENTRYPOINT ["scripts/start.sh"]



# ./Dockerfile

# Extend from the official python image
FROM python:3.8.4-buster

#Copy requirements file over first so dependicies don't have to be installed each rebuild
COPY ./rubotnik/requirements.txt /rubotnik/requirements.txt 
WORKDIR /rubotnik
RUN pip install -r requirements.txt

#Copy code and start rubotnik. "-U" flag sets UNBUFFERED so STDOUT is shown
COPY ./rubotnik /rubotnik 
CMD [ "python", "-u", "./app.py" ]
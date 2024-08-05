# API service

This service is ideally suppose to act as the API gateway on our system. However today this is deployed as a monolith. As we scale out operations, we should be extracting services / code out from here and into their own service directories.

------------------------------

## Local Dev - mac OSx:

### Setup

 - Setting up local python environment
    - `python -m venv venv` .. virtualenv venv
    - `source venv/bin/activate`
    - `pip install -r requirements.txt`
    - `export $(cat .env/local | grep -v ^# | xargs)` .. and fill in the key values
    - `mysql -u root -h localhost`
        - `create database projectskeleton;`
    - `python manage.py db migrate -m "meaningful msg"`: generate the migration file. If you have no changes, this should be a NoOp
    - `python manage.py db upgrade`: run the migration on the db

### Run service

 - `export $(cat .env/local | grep -v ^# | xargs); ./run.sh`: Make sure you're in the virtualenv for this
 - Please note that *locally* we'll be running the service on port 5000
 - `http://localhost:5000/`

### Run tests

 - `cd` into the service you wish to test (eg: `api`)
 - `nosetests tests/`


------------------------------

## Local Dev - Docker:

### Setup
 - `docker build -t projectskeleton-api .`
 - Run mysql service
    - `docker run --name mysql -d -e MYSQL_RANDOM_ROOT_PASSWORD=yes -e MYSQL_DATABASE=projectskeleton -e MYSQL_USER=projectskeleton_user -e MYSQL_PASSWORD=projectskeleton_password mysql/mysql-server:5.7`
    - https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xix-deployment-on-docker-containers
    - Also scroll down to comment #8 and #9: "MySQL container does not write data to its own file system, it creates an external volume and mounts it on the container file system. So you can kill MySQL, upgrade it, and when it restarts, it will attach to the same volume that holds the data."

 - Run service
    - `docker run -d --name projectskeleton-api-01 -p 5000:5000 -e PROCESSES=api_app --env-file=.env/stage --link mysql:dbserver projectskeleton-api`
    - Note that you need the `.env/stage` file here
    - Note to run this image on another port run the cmd with `-p <NEW_PORT>:5000`
 - `http://localhost:5000/`

### Debug
 - Add `--reload` key to gunicorn command for hot reload
 - `docker logs -f projectskeleton-api-01`
 - `docker stop projectskeleton-api-01`
 - `docker rm -f projectskeleton-api-01`
 - `docker stop $(docker ps -a -q)`
 - `docker rm $(docker ps -a -q)`
 - `docker exec -i -t projectskeleton-api-01 /bin/sh`
 - Check the db on the image
    - `docker exec -it mysql /bin/bash`
    - `mysql -u projectskeleton -p`
 - `docker ps -q -f status=exited | xargs docker rm` # Delete all stopped containers
 - `docker images -q -f dangling=true | xargs docker rmi` # Delete all dangling (unused) images


------------------------------

## Useful commands:

- List out all the routes registered under a service
   - `python manage.py list_routes`

## Notes:

- Don't let python buffer the stdout. This causes lags on honcho / gunicorn to push out the logs
   - http://tarunlalwani.com/post/why-delayed-output-python-docker/
   - PYTHONUNBUFFERED=1


------------------------------

## Heroku deploys


### Prod

- heroku stack:set container --app projectskeleton-api
- heroku git:remote -a projectskeleton-api
- git remote rename heroku heroku-api
- heroku config:set -a projectskeleton-api GCS_CREDENTIALS_JSON_STR="$(< secrets/gcp/gcs.json)"

- git push heroku-api master
- heroku logs --tail --app projectskeleton-api


# GHOSTROUTE_SECURITY_HOMEPAGE_API
RESTFUL API containing Ghostroute's Homepage API and Services

## Getting started with the project
- Disclaimer this project follows Single Responsibility Principle (SRP) Pattern, each folder in the api folder has the single responsibility, e.g controllers folder handles the presentation layer. Also this projects extensively utilizes dependency injection as a strategy for building loosely coupled, testable and scalable system. Hence, you need to atleast be comfortable with this programming paradigm to get the best out of this project repo.

## Set up
- clone the project
- use poetry to manage dependency and create virtual env
    - `poetry install` this will install all dependency and create a virtual environment for you.
- copy .env_sample to .env and update accordingly
    - `cp .env_sample .env`
- set up your local postgres database
    - `psql -U postgres` then create a user with superuser privilege and password, then login to psql with the newly created user and password
- run migration
    `make migrate` or `alembic upgrade head`

- run the app
    `make run-dev` or `uvicorn app:app --reload --port=5000`

- run celery
    - open new terminal and run `make celery` or `celery -A api.celery worker --loglevel=info` in the project root directory


## Dev with docker 
- Create `.dockerenv` in the project root and update the content in the .env with it, use `host.docker.internal` as the `DB_URL` host
- run  `docker-compose up mega_app` to start the project in a docker container

Happy coding!!
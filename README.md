# Finance API

## Setup

We use python 3.11 and recommend to use pyenv to manage you're python versions.
Here's how to install it with Hombrew.

`brew update`

`brew install pyenv`

## Local Development

Set the minimum env config copy the example file

`cp example.env .env`

We require you to setup MySQL. The project includes a docker-compose file which
should work with the example configs without extra work.

`docker-compose up -d`

Install dependencies. It is recommended to install everything under a virtual environment.

```bash
 python -m venv .venv
 source .venv/bin/activate
 make install_dev
```

Run database migrations with the following command.

`python manage.py migrate`

Create a superuser by running the following command. It will ask you for an email and password.

`python manage.py createsuperuser`

Finally you can run the dev server.

`python manage.py runserver`

Navigate to `http://127.0.0.1:8000/admin/` and log in with your credentials


## Documentation

### REST - Swagger & OpenApi

This project includes generated documentation for REST services by leveraging [Swagger UI](https://swagger.io/) and [OpenApi schema](https://www.openapis.org/) both connected to [djangorestframework](https://www.django-rest-framework.org/). After setting up the local development environment it can be found at http://127.0.0.1:8000/swagger
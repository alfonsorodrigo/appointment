# Core Appointment API

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Getting started

Make sure you have installed.

- [Python 3.7+](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/)

## Installation

Setup your environment with:

```sh
git clone git@github.com:alfonsorodrigo/appointment.git
cd appointment
docker build .
docker-compose build
```

## Testing

To run your tests, execute:

```sh
docker-compose run appointment_app sh -c "python manage.py test"
```

### Run

```sh
docker-compose up
```

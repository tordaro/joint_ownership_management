# Joint ownership manager
The joint ownership manager (JOM) is a Django-based web application focused on managing parking and electric vehicle charging for a small joint ownership company. It offers basic yet essential functionalities to streamline parking space allocation and manage charging stations efficiently.

## Key Features

- Parking Management: Simple tools to allocate and monitor parking spaces.
- EV Charging Control: Easy handling of electric vehicle charging station usage.
- Basic Billing System: Simple cost calculation for parking and charging.
- Owner Access: Basic profiles for owners to access and view pertinent information.

## Future Scope
While initially focused on car management, the project is designed to accommodate future enhancements for broader ownership management tasks as the company's needs evolve.

## Gettings started locally
Make a local Postgres container:

`docker run --name <name> -e POSTGRES_PASSWORD=<password> -p <port>:5432 -d postgres`

Make a `.env` file with the following following environment variables must be defined:
```
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<password>
POSTGRES_HOST=localhost
POSTGRES_PORT=<port>
```
The project is only guaranteed to work for Python >= 3.11, so check your version:

`python -V`

Use [pyenv](https://github.com/pyenv/pyenv#installation) to easily upgrade Python.

Install poetry:

`python -m pip install poetry`

Make a virtual environment and install all dependencies:

`poetry install --with dev`

Activate virtual environment in your shell:

`poetry shell`

You can now navigate to the `src` folder and migrate your database,

`python manage.py migrate`,

and then start the server:

`python manage.py runserver`
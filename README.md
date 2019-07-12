# scooters [![Build Status](https://travis-ci.com/serioeseGmbH/scooters.svg?token=YynpoCPMe8yq9Mzckvon&branch=master)](https://travis-ci.com/serioeseGmbH/scooters)

Save and show vehicle locations for mayor ridesharing services

### Team
* Firstname Lastname <name@example.org>


## Background
**TODO**

## Apidoc generation
To generate a viewable Apidoc, do:

```sh
cd docs
make apidoc
```

You can also create a report on documentation coverage via:

```sh
cd docs
make coverage
```

## Development

### Prerequisites
Make sure you have the following tools installed:

* git
* python (3.6.*)
* python3-dev (or equivalent package on your system)
* pipenv
* postgresql, postgis
* yarn
* redis


### Django Setup

#### Setup on the local machine

##### Create a `local_settings.py` file:

The `local_settings.py` file allows you to locally override django settings. You can create one yourself, but the best idea is to base it on the provided `local_settings.py.example` file:

```sh
cp scooters/local_settings.py.example scooters/local_settings.py
```

##### Install requirements
- set up a virtualenv and install the requirements: `pipenv install --dev`
- activate your created virtualenv: `pipenv shell`
- install npm/frontend packages: `yarn`


##### Setup Database
- Create a Postgres database and user matching your `local_settings.py`.
- Grant superuser rights to the user (sorry, it's necessary for creating the PostGIS extension).
- Set up the database: `./manage.py migrate`
- Set up the default groups and permissions: `./manage.py create_groups`
- Set up a superuser: `./manage.py createsuperuser`
- Run the application ^^ `./manage.py runserver` (this will start a webserver on port 8000)


#### Alternatively: Setup using Docker Compose
The included Compose configuration sets up a PostGIS database, a Redis database and a Django
service. The Django container uses the working directory as a volume, so you can edit the files
while Django runs.

##### Configuration
For the Docker setup, explicitly creating or modifying configuration files should not be necessary by default. However, if you're looking for them:

- Environment variables live in `scooters/docker.env`. You could change these, but never remove the `IS_DOCKER=1` line.
- Docker imports both `scooters/local_settings.py` (if present) and then `scooters/docker_settings.py`. The latter is always imported last, so its settings take precedence.

##### Install requirements
- Install Docker and Docker Compose
- **macOS only:** You need to enable 127.0.0.3 as loopback address, [like this](https://superuser.com/a/458877).
   ~~~python
   sudo ifconfig lo0 alias 127.0.0.3 up
   ~~~
##### Get stuff running
- Install frontend packages by calling `yarn`
- `docker-compose up`
- (Re)Create superuser:
   ~~~python
   docker-compose exec app ./manage.py createsuperuser
   ~~~
- Point browser to http://127.0.0.3:8000

##### Develop
If you change the model, you can migrate the db inside Docker like this:
   ~~~sh
   docker-compose exec app ./manage.py migrate
   ~~~

This is done automatically on Docker app startup (see `startup.sh`), but if you need to manually migrate for development purposes, do the above.


#### Usage
**TBD**

## Product Owner
- **seriöse Gesellschaft:** [[Firstname Lastname]](https://github.com/example)
- **Client:** [[Clientname]](https://example.org)


## Further references:
**TODO**

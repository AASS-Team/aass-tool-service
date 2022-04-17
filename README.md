# [AASS] Tool Service

![master pipeline](https://github.com/AASS-Team/aass-tool-service/workflows/pipeline/badge.svg?branch=master)

## Prerequisites

- [Docker](https://www.docker.com/)

## Installation and configuration

1. Set your environment variables by creating your own `.env` file in root similar to `.env.example`.

    - Specify `DJANGO_SECRET_KEY`. It can be generated as `base64 /dev/urandom | head -c50`.
    - All Other configuration in `.env.example` is ready for local development.

2. Build and run docker containers

    - Run following command in base directory of this project:

	```
	docker-compose up --build -d
	```

    - Docker image for this application will be automatically built. Then, all necessary infrastructure (e.g. database)
will be run along with web application.

3. Run database migrations

    - Create all necessary tables in database by executing:
    ```
    docker-compose exec web pipenv run migrate
    ```

## Development

1. Run `docker-compose up` in base directory of this project.

2. Visit [http://localhost:8000](http://localhost:8000) in your browser.

3. To stop the server, use `docker-compose down`


### Seeding the database with data

We created a fake real world data. The fixtures are present in `/fixtures` directory.

```
docker-compose exec web pipenv run loaddata
```

### Database cleanup

If something went wrong with migrations, you can remove all migrations using following command:

```
docker-compose exec web pipenv run reset
```


### Code formatting

Before committing, format code using `black` formater:

```
docker-compose exec web pipenv run lint
```

### Unit tests

Run unit tests using following command:

```
docker-compose exec web pipenv run test
```


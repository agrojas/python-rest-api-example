# python-rest-api-example

[![codecov](https://codecov.io/gh/agrojas/python-rest-api-example/branch/develop/graph/badge.svg?token=W1W08VMUSX)](https://codecov.io/gh/agrojas/python-rest-api-example) [![Tests](https://github.com/agrojas/python-rest-api-example/actions/workflows/test.yml/badge.svg)](https://github.com/agrojas/python-rest-api-example/actions/workflows/test.yml) [![Linters](https://github.com/agrojas/python-rest-api-example/actions/workflows/linters.yml/badge.svg)](https://github.com/agrojas/python-rest-api-example/actions/workflows/linters.yml)
[![Deploy](https://github.com/agrojas/python-rest-api-example/actions/workflows/deploy.yml/badge.svg)](https://github.com/agrojas/python-rest-api-example/actions/workflows/deploy.yml)

### Dependencies

- Python 3.9
- Poetry


### pre-commit

Install

``` bash
pre-commit install

pre-commit install -t pre-push
```

Run locally
``` bash
pre-commit run --all-files
```
### Migrations

Using [alembic](https://alembic.sqlalchemy.org/)

``` bash
alembic init migrations
```

Create script
``` bash
alembic revision -m "SCRIPT DESCRIPTION"
```

### Test

Run tests using [pytest](https://docs.pytest.org/en/6.2.x/)

``` bash
pytest tests/
```


### Docker

``` bash
docker build -t python-rest-api-example:0.1 .
docker run -p 5000:5000 --env-file .env python-rest-api-example:0.1
```


### Manual Deploy to Heroku

``` bash

heroku container:push web -a <HEROKU-APP-NAME>
heroku container:release web -a <HEROKU-APP-NAME>
```



### Resources

- https://devcenter.heroku.com/articles/build-docker-images-heroku-yml
- https://devcenter.heroku.com/articles/container-registry-and-runtime

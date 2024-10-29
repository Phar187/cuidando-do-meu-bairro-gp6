# EsicLivre

Micro serviço para interação com o eSIC municipal de São Paulo.


## Install

```
$ python setup.py develop
```

Se está usando Postgres:

```
$ pip install psycopg2
```

Instalar o `geckodriver` no PATH.
Baixar Firefox e setar caminho nas configurações.

## Prepare DB

Create the database and user, set them in `settings/local_settings.py` as `SQLALCHEMY_DATABASE_URI`.

```python
SQLALCHEMY_DATABASE_URI = 'postgresql://<user>:<password>@localhost/<database>'
```

Create tables:

```
$ python manage.py initdb
```

## Run!

```
$ python manage.py run
```

## API

Needs doc...

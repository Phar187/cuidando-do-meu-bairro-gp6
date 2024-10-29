# Cochicho (Beta)

Microservice for notifications.

## Install

```
$ python setup.py develop
```

If you are using Postgres:

```
$ pip install psycopg2
```

Place a `settings/keypub` file with the public key used by the Viralata instance.

## Prepare DB

Create the database and user, set them in `settings/local_settings.py` as `SQLALCHEMY_DATABASE_URI`.

```python
SQLALCHEMY_DATABASE_URI = 'postgresql://<user>:<password>@localhost/<database>'
```

Create tables:

```
$ flask init_db
```

## Run!

```
$ flask run
```

## API

Needs a 'static' doc, but accesssing the root of a hosted instance it's possible to see a Swagger doc.

## Known Issues

If you are using Gmail to send e-mails, it's possible it will block sending them, by security restrictions.
After the problem happened, you can unlock it [here](https://accounts.google.com/DisplayUnlockCaptcha).

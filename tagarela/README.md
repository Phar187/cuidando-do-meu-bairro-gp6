# Tagarela (Beta)

Microservice for comments.

Similar to [Isso](https://posativ.org/isso/), but using [Viralata](https://github.com/okfn-brasil/viralata) for authentication.

An example of web interface using this microservice as backend is [Cuidando2](https://github.com/okfn-brasil/cuidando2).


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
$ python manage.py initdb
```

## Run!

```
$ python manage.py run
```

## OpenShift Hosting

This code should be [OpenShift](https://openshift.com) ready.
So it should be possible to host it for free.

Using rhc (don't forget to set the URL for the used repository; maybe this one?):

    rhc app create tagarela python-2.7 postgresql-9.2 --from-code=<code-for-repo>

Looks like OpenShift Postgres is not doing Vacuum, so we do it with a cron job:

    rhc cartridge add cron -a tagarela

You will also need a `keypub` file for the used Viralata instance and a `local_settings.py` file.
You can use `settings/local_settings.openshift_example.py` as an example for the second one.
Place both files in `~/app-root/data/`, inside the OpenShift gear.
And, from inside the gear, using SSH, init the DB:

    . $OPENSHIFT_PYTHON_DIR/virtenv/bin/activate
    ~/app-root/repo
    python manage.py -s $OPENSHIFT_DATA_DIR initdb

## API

Needs a 'static' doc, but accesssing the root of a hosted instance it's possible to see a Swagger doc.

## Name

Tagarela, in Brazilian Portuguese, means a person who talks a lot...

## Known Issues

If you are using Gmail to send comment abuse e-mails, it's possible it will block sending them, by security restrictions.
After the problem happened, you can unlock it [here](https://accounts.google.com/DisplayUnlockCaptcha).

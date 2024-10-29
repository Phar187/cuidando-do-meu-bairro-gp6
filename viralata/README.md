# Vira-Lata (Beta)

Microservice for Authentication: Restlike & Social.

Similar to [microauth](https://github.com/LukeB42/microauth), but built over [python-social-auth](https://github.com/omab/python-social-auth) to allow auth using other providers (like oAuth).
Instead of Microauth, Vira-Lata has no role management.

The protocol is similar to [Kerberos](https://en.wikipedia.org/wiki/Kerberos_%28protocol%29), having "main" and "micro" tokens.

An example of web interface using this microservice as backend is [Cuidando2](https://github.com/okfn-brasil/cuidando2).
An example of microservice that uses the tokens produced by this microservice is [Tagarela](https://github.com/okfn-brasil/tagarela).


**This code is still in beta stage, so it should be used with care.**

Still only Python 2.


## Protocol

Common workflow:

1. Use the `register` or `login` endpoints to get a `main` and a `micro` token.
2. Use the `micro` token to access the other microservices.
3. Use the `main` token to get a new `micro` token or logout.

Important notes:

- A micro token cannot be invalided besides by expiration time. So it must have a short life.
- The Vira-Lata keeps control of invalidated main token, so they can have longer lives. But the other microservices don't know if a main token was invalidated, so they should only accept micro tokens.
- Micro tokens cannot be used to get a new micro token. This would allow infinite renew. Only main tokens can be used for this purpose.

The tokens are JWTs. To sign them the Vira-Lata needs a private key. The other micro services need the public key.
The tokens have `username` (username of the user), `type` ("micro" or "main") and an `exp` (expiration time) field.


## Install

```
$ python setup.py develop
```

If you are using Postgres:

```
$ pip install psycopg2
```

You will also need to generate an RSA key and place it in `settings/key` file.
The public key will be used by the other micro services to validate the tokens.
The password for the key file must be set in `PRIVATE_KEY_PASSWORD` at `settings/local_settings.py`.


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

    rhc app create viralata python-2.7 postgresql-9.2 --from-code=<code-for-repo>

Looks like OpenShift Postgres is not doing Vacuum, so we do it with a cron job:

    rhc cartridge add cron -a viralata

You will also need a `key` file and a `local_settings.py` file.
You can use `settings/local_settings.openshift_example.py` as an example for the second one.
Place both files in `~/app-root/data/`, inside the OpenShift gear.
And, from inside the gear, using SSH, init the DB:

    . $OPENSHIFT_PYTHON_DIR/virtenv/bin/activate
    cd ~/app-root/repo
    python manage.py -s $OPENSHIFT_DATA_DIR initdb

## API

Needs a 'static' doc, but accessing the root of a hosted instance it's possible to see a Swagger doc.

## Name

Vira-Lata, in Brazilian Portuguese, means mutt/mongrel.
So this name can be considered a more humble version of the mighty [Cerberus](https://en.wikipedia.org/wiki/Cerberus), symbol of the [Kerberos protocol](https://en.wikipedia.org/wiki/Kerberos_%28protocol%29)

## Known Issues

If you are using Gmail to send forgot password e-mails, it's possible it will block sending them, by security restrictions.
After the problem happened, you can unlock it [here](https://accounts.google.com/DisplayUnlockCaptcha).

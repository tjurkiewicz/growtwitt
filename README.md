# Deployment

In order to deploy this application on Heroku, configuration
variables must be set.

`DJANGO_SECRET_KEY` is base64-encoded secret key.
`TWITTER_API_KEY` and `TWITTER_API_SECRET` are your application's
api credentials. You don't have to base64 encode that as those
values are already environment-friendly.

`DISABLE_COLLECTSTATIC` must be set to 1.

`PORT` describes bind port for the service.




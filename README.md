# Python websockets start config for HaveYouHeard Game

This sample demonstrates how to use websockets on [Google App Engine Flexible Environment](https://cloud.google.com/appengine).

## Running locally

Refer to the [top-level README](../README.md) for instructions on running and deploying.

To run locally, you need to use gunicorn with the ``flask_socket`` worker:

    $ gunicorn --worker-class eventlet -w 1 server:app

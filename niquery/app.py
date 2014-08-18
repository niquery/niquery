from __future__ import absolute_import

import os

from celery import Celery
from flask import Flask, jsonify
from flask.ext.restful import Api, Resource, reqparse


def create_app(environment=None):
    """
    Creates and configures the app depending on the environment indicated, which can be
    set explicitly or using the FLASK_CONFIG environment variable.

    Environments
    ------------
     - config
     - development (default)
     - production
     - docker
     - testing
    """
    app = Flask(__name__)

    if not environment:
        environment = os.environ.get('FLASK_CONFIG')
    if not environment:
        environment = 'development'

    app.config.from_object(
        'niquery.config.{}'.format(environment.capitalize()))

    return app


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


app = create_app()
api = Api(app)

celery = make_celery(app)

@celery.task(name="tasks.add")
def add(x, y):
    return x + y

parser = reqparse.RequestParser()
parser.add_argument('x', type=int, help='X')
parser.add_argument('Y', type=int, help='Y')


class HelloWorld(Resource):
    def get(self):
        x = 5
        y = 10
        res = add.apply_async((x, y))
        context = {"id": res.task_id, "x": x, "y": y}
        result = "add((x){}, (y){})".format(context['x'], context['y'])
        goto = "{}".format(context['id'])
        return jsonify(result=result, goto=goto)


class ShowResult(Resource):
    def get(self, task_id):
        retval = add.AsyncResult(task_id).get(timeout=1.0)
        return repr(retval)

api.add_resource(HelloWorld, '/helloworld')
api.add_resource(ShowResult, '/helloworld/<string:task_id>')

if __name__ == "__main__":

    app.run(host=app.config['HOST'], port=app.config['PORT'])

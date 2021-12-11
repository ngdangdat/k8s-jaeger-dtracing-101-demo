from random import randint
from time import sleep
import logging

from flask import Flask
from flask import request
from jaeger_client import Config
from flask_opentracing import FlaskTracing


logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
config = Config(
  config={
    'sampler': {
      'type': 'const',
      'param': 1
    },
    'logging': True,
    'reporter_batch_size': 1,
  }, 
  service_name="backend",
)
jaeger_tracer = config.initialize_tracer()
tracing = FlaskTracing(jaeger_tracer, True, app)


counter_value = 1


def get_counter():
  return str(counter_value)


def increase_counter():
  global counter_value
  int(counter_value)
  sleep(randint(1,10))
  counter_value += 1
  return str(counter_value)


@app.route('/api/counter', methods=['GET', 'POST'])
def counter():
  logging.info(request.headers)
  if request.method == 'GET':
    return get_counter()
  elif request.method == 'POST':
    return increase_counter()

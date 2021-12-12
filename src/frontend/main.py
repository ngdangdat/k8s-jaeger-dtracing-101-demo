import os
import requests
import logging

from flask import Flask
from jaeger_client import Config
from flask_opentracing import FlaskTracing
import opentracing


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
  service_name="frontend",
)
jaeger_tracer = config.initialize_tracer()
tracing = FlaskTracing(jaeger_tracer, True, app)


def get_headers(span):
  custom_headers = {}
  jaeger_tracer.inject(span.context, opentracing.Format.HTTP_HEADERS , custom_headers)
  logging.info(custom_headers)
  return custom_headers


def get_counter(counter_endpoint, span):
  headers = get_headers(span)
  counter_response = requests.get(counter_endpoint, headers=headers)
  return counter_response.text


def increase_counter(counter_endpoint, span):
  headers = get_headers(span)
  counter_response = requests.post(counter_endpoint, headers=headers)
  return counter_response.text


@app.route('/')
def hello_world():
  counter_service = os.environ.get('COUNTER_ENDPOINT', default="https://localhost:5000")
  counter_endpoint = f'{counter_service}/api/counter'
  parent_span = tracing.get_span()
  with jaeger_tracer.start_span("frontend-request", child_of=parent_span) as span:
    counter = get_counter(counter_endpoint, span)
    increase_counter(counter_endpoint, span)

  return f"Hello, dude number {counter}\n"

from .retriever import BigQuery, RetrieverAbs
from .model import DummyClassifier, ModelAbs
from .writer import PostgreSQLDatabase, WriterAbs
from injector import singleton


def configure(binder):
    binder.bind(RetrieverAbs, to=BigQuery, scope=singleton)
    binder.bind(ModelAbs, to=DummyClassifier, scope=singleton)
    binder.bind(WriterAbs, to=PostgreSQLDatabase, scope=singleton)

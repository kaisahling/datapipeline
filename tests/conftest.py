from injector import Injector, singleton
import pytest
import pandas as pd
from app.app import create_app
from app.retriever import RetrieverAbs
from app.model import ModelAbs, DummyClassifier
from app.writer import WriterAbs


class MockInput(RetrieverAbs):

    def __init__(self):
        pass

    def get(self, user):
        data = [1]
        df = pd.DataFrame(data, columns=['data'])
        return df


class MockOutput(WriterAbs):

    def __init__(self):
        pass

    def write(self, results):
        pass


def test_configure(binder):
    binder.bind(RetrieverAbs, to=MockInput, scope=singleton)
    binder.bind(ModelAbs, to=DummyClassifier, scope=singleton)
    binder.bind(WriterAbs, to=MockOutput, scope=singleton)


@pytest.fixture
def test_injector():
    return Injector()


@pytest.fixture
def test_dependencies():
    return test_configure


@pytest.fixture
def app(test_dependencies):
    app = create_app(
        retriever_class=MockInput,
        writer_class=MockOutput,
        conf=test_configure
    )
    app.testing = True

    with app.app_context():
        yield app


@pytest.fixture
def flask_test_client(app):
    with app.test_client() as test_client:
        yield test_client

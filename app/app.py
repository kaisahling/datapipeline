import logging
import flask_injector
import injector
from flask import Flask, jsonify, request

from .retriever import BigQuery
from .model import DummyClassifier
from .writer import PostgreSQLDatabase

from .dependencies import configure


def create_app(*,
               retriever_class=BigQuery,
               model_class=DummyClassifier,
               writer_class=PostgreSQLDatabase,
               conf=configure):
    app = Flask("data-pipeline-ms")

    @app.route('/')
    def hello_world():
        return 'Hello, this is the data pipeline microservice!'

    @app.route('/health')
    def healthcheck():
        logging.info("Healthcheck endpoint called")
        return '{\"status\": \"UP\"}'

    @injector.inject
    @app.route('/model', methods=["GET", "POST"])
    def apply_model(retriever: retriever_class, model: model_class, writer: writer_class):
        logging.info("Modell endpoint called")
        user = request.values.get("user")

        if not user:
            return jsonify("Please provide a valid user id")

        data = retriever.get(user)
        result = {user: model.apply(data)}
        writer.write(result)
        return jsonify("Model applied")

    flask_injector.FlaskInjector(app=app, modules=[conf])

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(host='0.0.0.0', port=5000)

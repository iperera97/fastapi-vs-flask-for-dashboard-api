import os
import random
import logging

from flask import Flask, request, jsonify

from common.query_engine.datafustion import DataFusionEngine
from common.query_engine.postgresql import PostgresEngine
from common.queries import STUDENT_ANALYTICS_QUERIES

QUERIES = list(STUDENT_ANALYTICS_QUERIES.items())

# init logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s - %(name)s")
logger = logging.getLogger(__name__)

# init engines
datafusion_engine = DataFusionEngine("students", file_path="datacreator/students_data.parquet")
postgres_engine = PostgresEngine(
    db_name=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

# init app
app = Flask(__name__)
service_name = "flask"

@app.after_request
def log_response(response):
    app.logger.info(f"{request.path} returned {response.status_code}")
    return response


# init routes
@app.route("/datafusion", methods=["GET"])
def run_datafusion_query():
    metric = None
    try:
        metric, query = random.choice(QUERIES)
        result = datafusion_engine.execute_read_query_sync(query)
        return jsonify({
            "engine": datafusion_engine.name,
            "metric": metric,
            "data": result,
            "service_name": service_name,
        })
    except Exception as err:
        logger.error(f"datafustion api err {err} | {metric}")
        return jsonify({
            "error": str(err), "metric": metric, "query": query
        }), 500


@app.route("/database", methods=["GET"])
def run_postgres_query():
    metric = None
    try:
        metric, query = random.choice(QUERIES)
        result = postgres_engine.execute_read_query_sync(query)
        return jsonify({
            "engine": postgres_engine.name,
            "metric": metric,
            "data": result,
            "service_name": service_name
        })
    except Exception as err:
        logger.error(f"postgres api err {err} | {metric}")
        return jsonify({
            "error": str(err), "metric": metric, "query": query
        }), 500


if __name__ == "__main__":
    app.config.update({"ENV": "production", "DEBUG": True})
    app.run(host="0.0.0.0", port=8000)
import os
import logging
import random
from fastapi import FastAPI
from fastapi.responses import JSONResponse

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
app = FastAPI(title="Analytics API", version="1.0.0")
service_name = "fastapi"

@app.middleware("http")
async def log_requests(request, call_next):
    response = await call_next(request)
    logger.info(f"{request.url.path} returned {response.status_code}")
    return response

# init routes
@app.get("/datafusion")
async def run_datafusion_query():
    metric = None
    try:
        metric, query = random.choice(QUERIES)
        result = datafusion_engine.execute_read_query_sync(query)
        return {
            "engine": datafusion_engine.name,
            "metric": metric,
            "data": result,
            "service_name": service_name
        }
    except Exception as err:
        logger.error(f"datafustion api err {err} | {metric}")
        return JSONResponse(
            status_code=500,
            content={"error": str(err), "metric": metric}
        )


@app.get("/database")
async def run_postgres_query():
    metric = None
    try:
        metric, query = random.choice(QUERIES)
        result = await postgres_engine.execute_read_query_async(query)
        return {
            "engine": postgres_engine.name,
            "metric": metric,
            "data": result,
            "service_name": service_name
        }
    except Exception as err:
        logger.error(f"postgres api err {err} | {metric}")
        return JSONResponse(
            status_code=500,
            content={"error": str(err), "metric": metric}
        )

import logging
import psycopg.rows
from .base import BaseQueryEngine
from .utils import time_log, QueryEngineException
import psycopg

# init logs
logger = logging.getLogger(__name__)

SERVICE_NAME = "postgreql"


class PostgresEngine(BaseQueryEngine):

    name = SERVICE_NAME

    def __init__(self, db_name, user, password, host, port):
        self.connection_str = f"dbname={db_name} user={user} password={password} host={host} port={port}"
        self.connection_kwargs = {"conninfo": self.connection_str, "row_factory": psycopg.rows.dict_row}

    @time_log(SERVICE_NAME)
    def execute_read_query_sync(self, query: str) -> list[dict]:
        try:
            with psycopg.connect(**self.connection_kwargs) as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    return cur.fetchall()
        except psycopg.Error as err:
            logger.error(f"{self.name} engine err {err}")
            raise QueryEngineException(f"query engine error for {self.name} - {err}")

    def execute_write_query_sync(self):
        ...

    @time_log(SERVICE_NAME)
    async def execute_read_query_async(self, query: str) -> list[dict]:
        try:
            async with await psycopg.AsyncConnection.connect(**self.connection_kwargs) as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query)
                    return await cur.fetchall()
        except psycopg.Error as err:
            logger.error(f"{self.name} engine err {err}")
            raise QueryEngineException(f"query engine error for {self.name} - {err}")

    @time_log(SERVICE_NAME)
    async def execute_write_query_async(self, query: str, values: list[tuple] = None):
        try:
            async with await psycopg.AsyncConnection.connect(**self.connection_kwargs) as conn:
                async with conn.cursor() as cur:
                    if values:
                        await cur.executemany(query, values)
                    else:
                        await cur.execute(query)
                await conn.commit()
                return True
        except psycopg.Error as err:
            logger.error(f"{self.name} engine err {err}")
            raise QueryEngineException(f"query engine error for {self.name} - {err}")
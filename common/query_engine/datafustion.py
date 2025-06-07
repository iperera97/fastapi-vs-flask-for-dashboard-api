import logging

from datafusion import SessionContext

from .base import BaseQueryEngine
from .utils import time_log, QueryEngineException


# init logs
logger = logging.getLogger(__name__)

SERVICE_NAME = "datafustion"


class DataFusionEngine(BaseQueryEngine):

    name = SERVICE_NAME

    def __init__(self, table: str, file_path: str):
        self.file_path = file_path
        self.table = table

    @time_log(SERVICE_NAME)
    def execute_read_query_sync(self, query) -> list[dict]:
        try:
            ctx = SessionContext()
            ctx.register_parquet(self.table, self.file_path)
            return ctx.sql(query).to_pylist()
        except Exception as err:
            logger.error(f"{self.name} engine err {err}")
            raise QueryEngineException(f"query engine error for {self.name} - {err}")
        
    def execute_write_query_sync(self) -> bool:
        pass
    
    async def execute_read_query_async(self):
        pass

    async def execute_write_query_async(self):
        pass
from abc import ABC, abstractmethod

class BaseQueryEngine(ABC):
    name = None

    @abstractmethod
    def execute_read_query_sync(self):
        pass

    @abstractmethod
    def execute_write_query_sync(self):
        pass

    @abstractmethod
    async def execute_read_query_async(self):
        pass

    @abstractmethod
    async def execute_write_query_async(self):
        pass

from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    async def get_all():
        ...

    @abstractmethod
    async def get_by_id():
        ...

    @abstractmethod
    async def create():
        ...

    @abstractmethod
    async def full_update_by_id():
        ...

    @abstractmethod
    async def partial_update_by_id():
        ...

    @abstractmethod
    async def delete_by_id():
        ...


class SQLAlchemyRepository(AbstractRepository):
    model = None

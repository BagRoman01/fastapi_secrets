import logging
from typing import Any
from typing import Generic
from typing import TypeVar

from fastapi.encoders import jsonable_encoder
from sqlmodel import SQLModel
from sqlmodel import select
from sqlmodel import text
from sqlmodel.ext.asyncio.session import AsyncSession

ModelType = TypeVar('ModelType', bound=SQLModel)
CreateModelType = TypeVar('CreateModelType', bound=SQLModel)
UpdateModelType = TypeVar('UpdateModelType', bound=SQLModel)

logger = logging.getLogger(__name__)


def merge_dicts(d1: dict, d2: dict) -> dict:
    for k, v in d2.items():
        if isinstance(v, dict) and isinstance(d1.get(k), dict):
            d1_node = d1.setdefault(k, {})
            merge_dicts(d1_node, v)
        else:
            d1[k] = v
    return d1


class BaseRepository(Generic[ModelType, CreateModelType, UpdateModelType]):
    def __init__(self, model: type[ModelType], session: AsyncSession) -> None:
        """CRUD object with default methods to
        Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLModel by Tiangolo class
        * `schema`: A SQLModel by Tiangolo (schema) class
        """
        self.model = model
        self.db = session

    async def check_database_connection(self) -> bool:
        try:
            result = await self.db.exec(text('SELECT 1'))

            row = result.scalar()

            return row == 1

        except Exception as e:
            logger.error(f'Error connecting to database: {e!s}')
            return False

    async def get_by_id(self, itm_id: Any) -> ModelType | None:
        result = await self.db.exec(select(self.model)
                                    .where(self.model.id == itm_id))
        return result.one_or_none()

    async def get_multi(self, *, skip: int = 0, limit: int = 100) \
            -> list[ModelType]:
        result = await self.db.exec(select(self.model).offset(skip).limit(limit))
        return list(result.fetchall())

    async def create(self, *, obj_in: CreateModelType) -> ModelType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj

    async def create_multi(
            self,
            *,
            obj_in: list[CreateModelType]
    ) -> list[ModelType]:
        db_objs = [self.model(**obj.model_dump()) for obj in obj_in]
        self.db.add_all(db_objs)
        await self.db.flush()
        for obj in db_objs:
            await self.db.refresh(obj)
        return db_objs

    async def update(
        self, *, db_obj: ModelType, obj_in: UpdateModelType | dict[str, Any],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                if isinstance(obj_data[field], dict) and isinstance(
                    update_data[field], dict,
                ):
                    setattr(
                        db_obj,
                        field,
                        merge_dicts(obj_data[field], update_data[field]),
                    )
                else:
                    setattr(db_obj, field, update_data[field])
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, *, itm_id: Any) -> ModelType | None:
        obj = await self.get_by_id(itm_id)
        if obj:
            await self.db.delete(obj)
        await self.db.flush()
        return obj

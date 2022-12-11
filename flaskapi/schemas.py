from prisma import Prisma
import prisma.models as models
import inspect
from pydantic.main import ModelMetaclass, BaseModel
from decimal import Decimal
from datetime import datetime
from uuid import UUID, uuid4

prisma_models = [
    m for m in inspect.getmembers(
        models,
        inspect.isclass) if m[1].__class__ == ModelMetaclass and m[1] != BaseModel]


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True
        validate_all = True
        json_encoders = {
            bytes: lambda v: v.decode('utf-8'),
            Decimal: float,
            datetime: lambda v: v.isoformat(),
            UUID: str,
        }

    @property
    def _id(self) -> str:
        return str(self._id) if hasattr(self, '_id') else str(uuid4())

    @_id.setter
    def _id(self, value: str):
        return setattr(self, '_id', UUID(value))

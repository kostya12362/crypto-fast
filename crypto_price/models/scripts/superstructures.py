from typing import List, Union, Type, Optional, Any
import json

from tortoise.fields.base import Field
from tortoise.models import Model


class VarcharArrayField(Field, list):
    """
    Int Array field specifically for PostgreSQL.

    This field can store list of int values.
    """

    SQL_TYPE = "varchar[]"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_db_value(
        self, value: List[str], instance: "Union[Type[Model], Model]"
    ) -> Optional[List[str]]:
        return value

    def to_python_value(self, value: Any) -> Optional[List[str]]:
        if isinstance(value, str):
            array = json.loads(value.replace("'", '"'))
            return [str(x) for x in array]
        return value

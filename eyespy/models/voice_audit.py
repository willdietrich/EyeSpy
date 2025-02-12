from datetime import datetime
from typing import Optional, Any

from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import core_schema


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
            cls, _source_type: Any, _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        # This part handles validation and conversion
        object_id_schema = core_schema.no_info_before_validator_function(
            cls.validate,
            core_schema.is_instance_schema(ObjectId),
            serialization=core_schema.to_string_ser_schema(),  # Serialize as string
        )

        # This part tells Pydantic the JSON schema representation
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),  # JSON schema is a string
            python_schema=object_id_schema,
            # serialization=core_schema.to_string_ser_schema() # Serialize as string for json.
        )

    @classmethod
    def validate(cls, value: Any) -> ObjectId:
        if not isinstance(value, ObjectId):
            try:
                return ObjectId(str(value))
            except InvalidId:
                raise ValueError("Invalid ObjectId")
        return value


class VoiceAudit(BaseModel):
    id: Optional[PyObjectId] = Field(
        None,
        alias="_id",
        description="The document unique identifier in MongoDB.")

    class Config:
        json_encoders = {
            ObjectId: str
        }
        populate_by_name = True


    channel: str
    channel_id: int
    user: str
    user_id: int
    join_time: Optional[datetime] = None
    leave_time: Optional[datetime] = None
    dwell_time: Optional[int] = None

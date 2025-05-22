from bson import ObjectId
from pydantic_core import core_schema

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return core_schema.no_info_wrap_validator_function(
            cls.validate,
            core_schema.str_schema()
        )

    @classmethod
    def validate(cls, input_value, _ctx=None):
        # input_value คือค่าที่จะตรวจสอบ
        if not ObjectId.is_valid(input_value):
            raise ValueError("Invalid ObjectId")
        return ObjectId(input_value)

from pydantic import BaseModel, Field

class DataModel(BaseModel):
    key: str = Field(..., min_length=1)
    value: str = Field(..., min_length=1)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "key": "devops-*",
                    "value": "Hello, World!"
                }
            ]
        }
    }
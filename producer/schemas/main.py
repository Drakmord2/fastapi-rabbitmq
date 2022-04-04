from pydantic import BaseModel


class VersionSchema(BaseModel):
    name: str
    version: str

    class Config:
        title = "API Version"
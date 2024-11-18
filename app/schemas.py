from pydantic import BaseModel


class Rate(BaseModel):
    cargo_type: str
    rate: str

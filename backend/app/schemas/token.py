from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = {"from_attributes": True}


class TokenPayload(BaseModel):
    sub: str
    exp: int

    model_config = {"from_attributes": True}

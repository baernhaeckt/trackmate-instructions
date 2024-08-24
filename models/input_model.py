from pydantic import BaseModel


class InputModel(BaseModel):
    latitude: float
    longitude: float
    altitude: float

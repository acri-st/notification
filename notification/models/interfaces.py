from pydantic import BaseModel



class DefaultModel(BaseModel):
    """Model for Update Asset"""

    data: str

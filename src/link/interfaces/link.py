from pydantic import BaseModel

class Link(BaseModel):
    user_id: str
    link_id: str
    url: str
    description: str
    last_updated: str


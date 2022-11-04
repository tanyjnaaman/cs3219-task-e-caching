from src.db.interfaces import DatabaseIndexWrapper
from src.db.db import db
from pydantic import BaseModel

import pymongo


class LinkModel(BaseModel):
    """
    The model schema we use to save rooms in the db.
    We distinguish between this and interfaces - as interfaces are inttended
    to be lighter-weight versions we use within the backend.
    """

    user_id: str
    link_id: str
    url: str
    description: str
    last_updated: str


# ====== indices =======
# index to access by link_id
access_by_link_id = DatabaseIndexWrapper(
    collection_name="link",
    index_name="link_id",
    index_fields=[("link_id", pymongo.ASCENDING)],
    sparse=True,
)

# index to access by user_id
access_by_user_id = DatabaseIndexWrapper(
    collection_name="link",
    index_name="user_id",
    index_fields=[("user_id", pymongo.ASCENDING)],
    sparse=True,
)


INDICES = [
    access_by_link_id,
]
# for idx in INDICES:
#     print(f"Creating index: {idx.index_name}")
#     db.create_index(idx)

from typing import List
from src.link.interfaces.link import Link
from src.constants import LINK_TABLE_NAME
from src.db.db import db, DatabaseWrapper

from src.db.redis import redis_client

import json


class LinkCrudService:
    """
    Responsible for crud operations on the links table
    in the database.
    """

    def __init__(self, _db: DatabaseWrapper = db, _redis_client=redis_client):
        self.db = _db
        self.table = LINK_TABLE_NAME
        self.redis_client = _redis_client

    def get_links(self) -> List[Link]:
        """
        Get all links for a user.
        """
        # check redis
        items_from_redis = self.redis_client.get(LINK_TABLE_NAME)
        items = json.loads(items_from_redis) if items_from_redis else None
        if not items:
            print("Cache miss, fetching from db")

            # get items
            from_db = self.db.get_items(self.table, {})

            # cache to redis
            items = [Link(**item).link_id for item in from_db]
            links_as_dict_string = json.dumps([item for item in items])
            self.redis_client.set(LINK_TABLE_NAME, links_as_dict_string)
            items = json.loads(links_as_dict_string)

        else:
            print("Cache hit")

        # wrap into interface
        links = items

        return links

    def get_link_by_id(self, id: str) -> Link:
        """
        Get a specific link.
        """
        key = f"{LINK_TABLE_NAME}:link_id{id}"
        # check redis
        items_from_redis = self.redis_client.get(key)
        items = json.loads(items_from_redis) if items_from_redis else None
        if not items:
            print("Cache miss, fetching from db")

            from_db = self.db.get_items(self.table, {"link_id": id})
            items = [Link(**item).link_id for item in from_db]

            # cache to redis
            links_as_dict_string = json.dumps([item for item in items])
            self.redis_client.set(key, links_as_dict_string)
            items = json.loads(links_as_dict_string)

        else:
            print("Cache hit")

        link = items

        return link

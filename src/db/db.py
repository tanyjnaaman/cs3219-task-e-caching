from src.exceptions import DatabaseException, DatabaseItemNotFoundException
from src.db.interfaces import DatabaseIndexWrapper
from pymongo import MongoClient
from src.constants import (
    ENV_IS_DEV,
    ENV_IS_TEST,
    MONGODB_DATABASE_NAME,
    MONGODB_JSON_PATH,
    MONGODB_TABLES,
    MONGODB_URI,
)
from typing import Any, Dict, List
import logging
import mongomock


class DatabaseWrapper:
    def __init__(self, _mongodb_uri: str = None, _client: MongoClient = None):
        # initialize db and collection being referenced

        self.client = _client or MongoClient(_mongodb_uri or MONGODB_URI)
        self.db = self.client[MONGODB_DATABASE_NAME]

    def clear_db(self):
        """
        Clears the database.
        """
        for table in MONGODB_TABLES:
            self.db.drop_collection(table)

    def populate_database(self, table_to_items_map: Dict[str, List[object]]):
        """
        POpulates the db with the given data.
        """
        print("Populating database from data...")
        for table in MONGODB_TABLES:

            # 1. drop table
            self.db.drop_collection(table)

            # 2. insert data
            items = table_to_items_map[table]
            logging.info(f"Populating table {table}")
            self.db[table].insert_many(items)

        print("Done populating database from data.")

    def create_index(self, index_specifications: DatabaseIndexWrapper):
        """
        Creates an index for a certain access pattern specified.
        For more details, see https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.create_index
        """
        print(index_specifications)
        self.db[index_specifications.collection_name].create_index(
            index_specifications.index_fields,
            name=index_specifications.index_name,
            sparse=index_specifications.sparse,
        )

    def insert(self, table: str, data: Dict[str, Any]):
        """
        Inserts data into a table.
        """
        try:
            self.db[table].insert_one(data)
        except:
            raise DatabaseException("Error inserting item to db.")

    def get_items(self, table: str, index_keys: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Gets an item from a table.
        """
        try:
            results = [r for r in self.db[table].find(index_keys)]
            return results
        except:
            raise DatabaseException("Error getting items from db.")

    def update_item(self, table: str, index_keys: Dict[str, Any], data: Dict[str, Any]):
        """
        Updates an item in a table.

        """
        find = [r for r in self.db[table].find(index_keys)]
        if len(find) == 0:
            raise DatabaseItemNotFoundException(
                f"Could not find item in table {table} with index keys {index_keys}"
            )
        elif len(find) > 1:
            raise DatabaseException(
                f"Found multiple items in table {table} with index keys {index_keys}, but trying to update one."
            )

        result = self.db[table].replace_one(index_keys, data, upsert=False)
        if result.modified_count == 0:
            raise DatabaseException("Could not update item in table")
        print(
            "Updated item in table",
            table,
            "with index keys",
            index_keys,
            "to",
            data,
            "successfully. With result",
            result,
        )

    def delete_item(self, table: str, index_keys: Dict[str, Any]):
        """
        Deletes an item from a table.
        """
        result = self.db[table].delete_one(index_keys)
        if result.deleted_count == 0:
            raise DatabaseItemNotFoundException(
                f"Could not find item in table {table} with index keys {index_keys}"
            )
        elif result.deleted_count > 1:
            raise DatabaseException(
                f"Found multiple items in table {table} with index keys {index_keys}, but trying to delete one."
            )


if ENV_IS_TEST:
    db = DatabaseWrapper(_client=mongomock.MongoClient())

else:
    db = DatabaseWrapper()
    if ENV_IS_DEV:
        # read data from json
        print(f"Reading dev data from json at {MONGODB_JSON_PATH}...")
        import json

        with open(MONGODB_JSON_PATH, "r") as f:
            table_to_items_map = json.load(f)
            db.populate_database(table_to_items_map)

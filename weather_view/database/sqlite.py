import sqlite3
from typing import Dict, List

from sqlite_utils import Database
from pydantic import BaseModel

from data_access.db import AbstractDatabase, Filter


class SQLiteConnection(BaseModel):
    database_path: str


class SQLite(AbstractDatabase, Database):
    def __init__(self, connection_info: SQLiteConnection, models: List[BaseModel] = None):
        super().__init__(sqlite3.connect(connection_info.database_path))
        if models:
            self._generate_schemas(models)

    def _generate_schemas(self, models: List[BaseModel]):
        tables = [t.name for t in self.tables]
        type_mapping = {
            "int": int,
            "float": float,
        }
        for model in models:
            if model.__name__.lower() in tables:
                continue
            self.create_table(
                name=model.__name__.lower(),
                columns={k: type_mapping.get(v.type_.__name__, str) for k, v in model.__fields__.items()})

    def _get_table(self, table_name):
        table = self.__getitem__(table_name)
        if not table:
            raise Exception(f"Table {table} Not Found")
        return table

    def get_entry(self, table_name, condition: tuple):
        table = self._get_table(table_name)
        result = table.get(condition)
        return result

    def get_entries(self, table_name, filter_: Filter = None):
        table = self._get_table(table_name)
        args = {}
        if filter_.condition:
            # args["where_args"] = filter_.condition
            args["where"] = filter_.condition_as_sql()
        if filter_.sort:
            args["order_by"] = filter_.sort
        if filter_.limit:
            args["limit"] = filter_.limit
        results = []
        if args:
            gen = table.rows_where(**args)
        else:
            gen = table.rows
        for row in gen:
            results.append(row)
        return results

    def insert_entry(self, table_name, entry: Dict):
        table = self._get_table(table_name)
        table.insert(entry)
        return table.last_rowid

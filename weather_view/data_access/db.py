from abc import ABCMeta, abstractmethod
from typing import Optional, Dict

from pydantic import BaseModel


class Filter(BaseModel):
    condition: Optional[Dict]
    sort: Optional[str]
    limit: Optional[int]

    def condition_as_sql(self):
        sql = []
        for key, value in self.condition.items():
            sql.append(f"{key}='{value}'")
        return " AND ".join(sql)


class AbstractDatabase(metaclass=ABCMeta):

    @abstractmethod
    def get_entry(self, key: str, id):
        ...

    @abstractmethod
    def get_entries(self, key: str, filter_: Optional[Filter] = None):
        ...

    @abstractmethod
    def insert_entry(self, key: str, value: Dict):
        ...


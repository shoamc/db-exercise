from dataclasses import dataclass
from typing import Any, Dict, List, Type


@dataclass
class DBField:
    name: str
    type: Type


@dataclass
class SelectionCriteria:
    field_name: str
    operator: str
    value: Any


@dataclass
class DBTable:
    fields: List[DBField]
    key_field_name: str
    table_indexes: List

    def count(self) -> int:
        raise NotImplementedError

    def insert_record(self, values: Dict[str, Any]) -> None:
        raise NotImplementedError

    def delete_record(self, key: Any) -> None:
        raise NotImplementedError

    def delete_records(self, criteria: List[SelectionCriteria]) -> None:
        raise NotImplementedError

    def get_record(self, key: Any) -> Dict[str, Any]:
        raise NotImplementedError

    def update_record(self, key: Any, values: Dict[str, Any]) -> None:
        raise NotImplementedError

    def query_table(self, criteria: List[SelectionCriteria]) -> List[Dict[str, Any]]:
        raise NotImplementedError

    def create_index(self, field_to_index: str) -> None:
        raise NotImplementedError


@dataclass
class DataBase:
    # Put here any instance information needed to support the API
    def create_table(self,
                     table_name: str,
                     fields: List[DBField],
                     key_field_name: str) -> DBTable:
        raise NotImplementedError

    def num_tables(self) -> int:
        raise NotImplementedError

    def get_table(self, table_name: str) -> DBTable:
        raise NotImplementedError

    def query_multiple_tables(
            self,
            tables: List[str],
            fields_and_values_list: List[List[SelectionCriteria]],
            fields_to_join_by: List[str]
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError

from dataclasses import dataclass, field
from typing import Any, Dict, List

import db_api


def check_criteria(value: Any, criteria: db_api.SelectionCriteria) -> bool:
    op = criteria.operator
    c_value = criteria.value
    if op == '=':
        return value == c_value
    if op == '<':
        return value < c_value
    if op == '>':
        return value > c_value
    raise ValueError(f'Unknown operator: {op}')


@dataclass
class DBTable(db_api.DBTable):
    records: Dict[Any, Dict[str, Any]] = field(default_factory=dict, init=False)

    def __post_init__(self):
        self.records = {}

    def __len__(self) -> int:
        return len(self.records)

    def count(self) -> int:
        return len(self)

    def insert_record(self, values: Dict[str, Any]) -> None:
        key = values[self.key_field_name]
        if key in self.records:
            raise ValueError(f'Cannot insert record: record with {key=} already exists!')
        # TODO: verify values
        self.records[key] = values

    def delete_record(self, key: Any) -> None:
        if key not in self.records:
            raise ValueError(f'Cannot delete record: No record with {key=}!')
        # TODO: verify values
        del self.records[key]

    def delete_records(self, criteria: List[db_api.SelectionCriteria]) -> None:
        for record in self.query_table(criteria):
            self.delete_record(record[self.key_field_name])

    def update_record(self, key: Any, values: Dict[str, Any]) -> None:
        self.records[key].update(values)

    def query_table(self, criteria: List[db_api.SelectionCriteria]) -> List[Dict[str, Any]]:
        keys = list(self.records.keys())
        for record in self.records.values():
            for c in criteria:
                key = record[self.key_field_name]
                if not check_criteria(record[c.field_name], c):
                    keys.remove(key)
                    break
        return [record for key, record in self.records.items() if key in keys]

    def create_index(self, field_to_index: str) -> None:
        raise NotImplementedError


@dataclass
class DataBase(db_api.DataBase):
    tables: Dict[Any, DBTable] = field(default_factory=dict, init=False)

    def __post_init__(self):
        self.tables = {}

    def __len__(self) -> int:
        return len(self.tables)

    def num_tables(self) -> int:
        return len(self)

    def create_table(self,
                     table_name: str,
                     fields: List[db_api.DBField],
                     key_field_name: str) -> DBTable:
        if table_name in self.tables:
            raise ValueError(f'Cannot create table: {table_name} already exists!')
        self.tables[table_name] = DBTable(fields, key_field_name, [])
        return self.get_table(table_name)

    def get_table(self, table_name: str) -> DBTable:
        return self.tables[table_name]

    def query_multiple_tables(
            self,
            tables: List[str],
            fields_and_values_list: List[List[db_api.SelectionCriteria]],
            fields_to_join_by: List[str]):
        raise NotImplementedError

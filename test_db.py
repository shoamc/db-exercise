import datetime as dt

import pytest

from db_api import DBField, SelectionCriteria
from db import DataBase


def test_simple() -> None:
    db = DataBase()
    assert db.num_tables() == 0
    db.create_table('Students',
                    [DBField('ID', int),
                     DBField('First', str),
                     DBField('Last', str),
                     DBField('Birthday', dt.datetime)
                     ],
                    'ID')
    assert db.num_tables() == 1
    students = db.get_table('Students')
    for i in range(50):
        students.insert_record(dict(
            ID=1_000_000 + i,
            First=f'John{i}',
            Last=f'Doe{i}',
            Birthday=dt.datetime(2000, 2, 1) + dt.timedelta(days=i)
        ))
    students.delete_record(1_000_001)
    students.delete_records([SelectionCriteria('ID', '=', 1_000_020)])
    students.delete_records([SelectionCriteria('ID', '<', 1_000_003)])
    students.delete_records([SelectionCriteria('ID', '>', 1_000_033)])
    students.delete_records([
        SelectionCriteria('ID', '>', 1_000_020),
        SelectionCriteria('ID', '<', 1_000_023)
    ])
    students.update_record(1_000_009, dict(First='Jane', Last='Doe'))
    assert students.count() == 28

    results = students.query_table([SelectionCriteria('First', '=', 'Jane')])
    assert len(results) == 1
    assert results[0]['First'] == 'Jane'

    with pytest.raises(ValueError):  # record already exists
        students.insert_record(dict(
            ID=1_000_010,
            First='John',
            Last='Doe',
            Birthday=dt.datetime(2000, 2, 1) + dt.timedelta(days=i)
        ))

    with pytest.raises(ValueError):
        students.delete_record(key=1_000_000)

def

#!/usr/bin/env python3
from pathlib import PurePath

from tinydb import TinyDB, Query


class MyTinyDB:
    def __init__(self, db_name: str):
        if '/' in db_name:
            parts: list[str] = db_name.split('/')
            file_name: str = parts[-1]
            self.db: TinyDB = TinyDB(str(self.get_db_file_path(file_name=db_name if db_name.endswith('.json') else db_name + '.json',
                                                          custom_path=parts[:-1])),
                                           sort_keys=True, indent=4, separators=(',', ': '))
        else:
            self.db: TinyDB = TinyDB(str(self.get_db_file_path(file_name=db_name if db_name.endswith('.json') else db_name + '.json')),
                                     sort_keys=True, indent=4, separators=(',', ': '))

    def get_db(self) -> TinyDB:
        return self.db

    def get_db_file_path(self, file_name: str, custom_path: list[str] = None) -> PurePath:
        pass
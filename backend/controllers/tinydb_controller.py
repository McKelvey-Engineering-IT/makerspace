from typing import Any, Dict
from controllers.db_base import DBBase
from tinydb import TinyDB, Query

DATABASE_FILE = "testing_database.json"


class JSONDB(DBBase):
    def __init__(self):
        self.connection = TinyDB(DATABASE_FILE)
        self.session = Query()

    def create_record(self, record: Dict[str, Any]) -> None:
        self.connection.insert(record)

    def update_record(self, email: str, updated_record: Dict[str, Any]) -> None:
        self.connection.update(updated_record, self.session.email == email)

    def delete_record(self, email: str, search_criteria) -> None:
        self.connection.remove(search_criteria, self.session.email == email)

    def find_record(self, email: str):
        record = self.connection.search(self.session.email == email)

        if len(record) > 1:
            raise RuntimeError("More than one matching record")

        if len(record) < 1:
            raise RuntimeError("No matching record")

        return record[0]

    def find_all_active_sessions(self):
        return self.connection.search(self.session.activeSession == True)

    def insert_session(self, session_attempt: Dict[str, Any]):
        existing_records = self.connection.search(
            self.session.email == session_attempt.get("email")
        )

        if len(existing_records) > 1:
            raise RuntimeError("Duplicate session")

        self.create_record(session_attempt)

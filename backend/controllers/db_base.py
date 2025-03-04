from abc import ABC, abstractmethod


class DBBase(ABC):
    @abstractmethod
    def create_record():
        pass

    @abstractmethod
    def delete_record():
        pass

    @abstractmethod
    def update_record():
        pass

    @abstractmethod
    def find_record():
        pass

    @abstractmethod
    def insert_session():
        pass

    @abstractmethod
    def find_all_active_sessions():
        pass

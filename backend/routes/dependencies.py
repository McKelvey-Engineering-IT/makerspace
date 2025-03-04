from controllers.database_controller import DatabaseController
from controllers.state_manager import StateManager
from config import Settings


state_manager = StateManager()
databse = DatabaseController().generate()


async def get_state_manager():
    return state_manager


def get_database():
    return databse


def get_settings():
    return Settings()

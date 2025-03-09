from controllers.database_controller import DatabaseController
from controllers.state_manager import StateManager
from controllers.badgr_connector import BadgrConnector
from config import Settings

USERNAME = "makertech@wustl.edu"
KEY = "SfgpMyDTaFqJc"

state_manager = StateManager()
databse = DatabaseController().generate()
badgr_connector = BadgrConnector(USERNAME, KEY)


async def get_state_manager():
    return state_manager


def get_badgr_connector():
    return badgr_connector


def get_database():
    return databse


def get_settings():
    return Settings()

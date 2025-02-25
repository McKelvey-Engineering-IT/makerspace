from controllers.state_manager import StateManager
from config import Settings


state_manager = StateManager()

async def get_state_manager():
    return state_manager


def get_settings():
    return Settings()

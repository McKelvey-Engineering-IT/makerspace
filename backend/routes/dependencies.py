from controllers.state_manager import StateManager
from config import Settings


async def get_state_manager():
    return StateManager()


def get_settings():
    return Settings()

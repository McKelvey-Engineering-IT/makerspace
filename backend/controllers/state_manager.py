import asyncio


class StateManager:
    def __init__(self):
        self.subscription = asyncio.Event()
        self.logins = []
        
    async def flag_new_message(self):
        self.subscription.set()
        self.subscription.clear()

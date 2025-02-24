import asyncio


class StateManager:
    def __init__(self):
        self.subscription = asyncio.Event()
        
    def flag_new_message(self):
        self.subscription.set()
        self.subscription.clear()

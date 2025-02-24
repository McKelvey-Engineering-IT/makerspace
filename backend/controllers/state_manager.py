import asyncio


class StateManager:
    def __init__(self):
        print('setting')
        self.number = 555555
        print(self.number)
        self.subscription = asyncio.Event()
        print('test')

    def flag_new_message(self):
        print(self.number)
        self.subscription.set()
        self.subscription.clear()

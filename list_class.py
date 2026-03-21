import time
from datetime import datetime


class List:
    def __init__(self, items=None, timestamp=None):
        self.items = items or []
        self.last_change_time = timestamp or time.time()

    def change(self):
        self.last_change_time = time.time()

    def str_time(self):
        t = datetime.fromtimestamp(self.last_change_time)
        return f"{t.strftime('%Y-%m-%d %H:%Ma')} ({(datetime.now() - t).days} дней назад)"
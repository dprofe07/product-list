import time
from datetime import datetime


def time_to_string(timestamp):
    t = datetime.fromtimestamp(timestamp)
    return f"{t.strftime('%Y-%m-%d %H:%M')} ({(datetime.now() - t).days} дней назад)"

class List:
    def __init__(self, items=None, timestamp_change=None, timestamp_export=None):
        self.items = items or []
        self.last_change_time = timestamp_change or time.time()
        self.last_export_time = timestamp_export or time.time()

    def write_change(self):
        self.last_change_time = time.time()

    def write_export(self):
        self.last_export_time = time.time()

    def str_change_time(self):
        return time_to_string(self.last_change_time) + self.str_changes_after_export()

    def str_export_time(self):
        return time_to_string(self.last_export_time)

    def str_changes_after_export(self):
        if self.last_change_time < self.last_export_time:
            return ""
        return " (после экспорта)"

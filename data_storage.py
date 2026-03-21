import os
import pickle

from migrations import migrate


class DataStorage:
    def __init__(self, filename):
        self.filename = filename
        self.data = None
        self.open_or_create()

    def open_or_create(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'wb') as f:
                pickle.dump(DataStorage.empty(), f)
            self.open_or_create()
            return

        with open(self.filename, 'rb') as f:
            self.data = migrate(pickle.load(f))

    def save(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.data, f)

    @staticmethod
    def empty():
        return {
            "##migration_version": 1
        }
class DiffEngine:
    def __init__(self, db):
        self.db = db

    def compare(self, new_scopes):
        old_scopes = self.db.get_all()

        added = new_scopes - old_scopes
        removed = old_scopes - new_scopes

        updated = set() 

        return added, removed, updated

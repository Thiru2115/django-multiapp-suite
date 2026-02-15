class AppRouter:

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'notes':
            return 'notes_db'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'notes':
            return 'notes_db'
        return 'default'

    def allow_migrate(self, db, app_label, **hints):
        if app_label == 'notes':
            return db == 'notes_db'
        return db == 'default'

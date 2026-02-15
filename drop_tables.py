import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multiapps.settings')
django.setup()

from django.db import connections

# Get the notes_db connection
conn = connections['notes_db']
cursor = conn.cursor()

# Drop old tables
print("Dropping old tables...")
cursor.execute("DROP TABLE IF EXISTS notes_todo CASCADE;")
cursor.execute("DROP TABLE IF EXISTS notes_note CASCADE;")
cursor.execute("DROP TABLE IF EXISTS django_migrations CASCADE;")
print("Tables dropped successfully!")

cursor.close()

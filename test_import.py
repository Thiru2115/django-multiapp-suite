import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multiapps.settings')
django.setup()

try:
    from image_processing import views
    print("Successfully imported image_processing.views")
except Exception as e:
    print(f"Failed to import: {e}")
    import traceback
    traceback.print_exc()

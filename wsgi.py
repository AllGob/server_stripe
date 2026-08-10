import logging
import os
from django.core.wsgi import get_wsgi_application

logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
try:
    application = get_wsgi_application()
    logger.info("WSGI initialized")
except Exception as e:
    logger.exception(f"Failed to initialize WSGI: {e}")
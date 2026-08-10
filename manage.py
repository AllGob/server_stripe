import os
import sys
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        logger.exception(f"Django import failed, {exc}")
        raise ImportError()
    execute_from_command_line(sys.argv)
if __name__ == "__main__":
    main()
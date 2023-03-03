#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main(*args):
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if not args:
        args = sys.argv
    else:
        print("manage.py", args)
        args = [sys.argv[0]] + list(args)
    execute_from_command_line(args)


if __name__ == "__main__":
    main()

#!/usr/bin/env python

import os
import sys

sys.path.insert(0, "tests")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    args = sys.argv
    args.insert(1, "test")
    args.insert(2, "flat_json_widget")
    args.insert(3, "tests")
    execute_from_command_line(args)

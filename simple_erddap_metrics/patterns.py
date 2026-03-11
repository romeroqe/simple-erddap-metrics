import re

download_pattern = re.compile(r"/erddap/(griddap|tabledap)/([^.]+)\.(\w+)")
ip_pattern = re.compile(r"\([^)]+\)\s+([0-9\.]+)\s+GET")
date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\+\d{2}:\d{2}|Z)?")
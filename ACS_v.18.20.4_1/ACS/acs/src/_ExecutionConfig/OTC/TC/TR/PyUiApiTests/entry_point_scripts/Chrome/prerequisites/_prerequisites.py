from os import sys, path
import os
for p in sys.path:
    if "PyUiApiTests" in p:
        sys.path.append(path.dirname(path.dirname(path.dirname(p))))
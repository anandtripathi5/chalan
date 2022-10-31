import sys
from rich import print


class Exc:
    def __init__(self, message):
        print(message)
        sys.exit(1)

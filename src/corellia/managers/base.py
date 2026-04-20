import shutil
from abc import ABC

class Manager :
    def __init__(self, command: str) -> None:
        self.command = command

    def exists (self) -> bool :
        return shutil.which(self.command) is not None
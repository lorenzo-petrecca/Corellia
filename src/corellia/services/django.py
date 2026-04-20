import subprocess
from pathlib import Path

class DjangoService :
    def __init__(self, python: Path) -> None:
        self.python = python

    def startproject (self, root: Path) -> None:
        subprocess.run (
            [
                str(self.python),
                "-m",
                "django",
                "startproject",
                "config",
                ".",
            ],
            cwd=root,
            check=True,
        )

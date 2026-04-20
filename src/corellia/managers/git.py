import subprocess
from pathlib import Path

from corellia.managers.base import Manager
from corellia import constants as cs


class GitManager(Manager) :
    def __init__(self, command: str = cs.GIT_COMMAND) -> None:
        super().__init__(command)

    def init_repo (self, project_dir: Path) -> None :
        subprocess.run(
            [self.command, 'init'],
            cwd=project_dir,
            check=True
        )

    
    def set_main_branch (self, project_dir: Path) -> None:
        subprocess.run(
            [self.command, "branch", "-M", "main"],
            cwd=project_dir,
            check=True,
        )

    def is_initialized (self, project_dir: Path) -> bool :
        return (project_dir / ".git").exists()
    

    def is_available (self) -> bool :
        return self.exists()
    

    def get_current_branch (self, project_dir: Path) -> str | None :
        try :
            result = subprocess.run(
                [self.command, "branch", "--show-current"],
                cwd=project_dir,
                capture_output=True,
                text=True,
                check=True,
            )
            branch = result.stdout.strip()
            return branch if branch else None
        except Exception :
            return None
        
    
    def has_remote (self, project_dir: Path) -> bool :
        try :
            result = subprocess.run(
                [self.command, "remote"],
                cwd=project_dir,
                capture_output=True,
                text=True,
                check=True,
            )
            return bool(result.stdout.strip())
        except Exception :
            return False
        

    def is_dirty (self, project_dir: Path) -> bool :
        try :
            result = subprocess.run(
                [self.command, "status", "--porcelain"],
                cwd=project_dir,
                capture_output=True,
                text=True,
                check=True,
            )
            return bool(result.stdout.strip())
        except Exception :
            return False


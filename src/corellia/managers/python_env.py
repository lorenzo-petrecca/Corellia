import subprocess
from pathlib import Path
from corellia.config import CorelliaConfig
from corellia.managers.base import Manager
from corellia import constants as cs
from corellia.managers.virtual_env import VirtualEnvManager

class PythonEnvManager(Manager) :
        
    def __init__(self, command: str = cs.PY_ENV_COMMAND) -> None:
        super().__init__(command)
        self._installed_versions: list[str] | None = None

    def get_installed_versions (self) -> list[str] :
        if self._installed_versions is not None :
            return self._installed_versions
        
        if not self.exists() :
            self._installed_versions = []
            return self._installed_versions
        
        result = subprocess.run(
            [self.command, 'versions', '--bare'],
            capture_output=True,
            text=True,
            check=True,
        )

        versions: list[str] = []
        for line in result.stdout.splitlines() :
            version = line.strip()
            if version :
                versions.append(version)

        self._installed_versions = versions
        return versions



    def get_python_executable (self, project_dir: Path) -> Path:
        if not self.exists():
            raise FileNotFoundError(
                f"Environment manager '{self.command}' was not found."
            )
        
        result = subprocess.run(
            [self.command, "which", "python"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            check=True,
        )

        python_path = result.stdout.strip()

        if not python_path :
            raise FileNotFoundError(
                f"Could not resolve the Python executable from the environment manager."
            )
        
        return Path(python_path)


    def is_version_installed (self, version: str = "") -> bool :
        return version in self.get_installed_versions()
    
    
    def set_local_version (self, project_dir: Path, version: str) -> None :
        if not self.is_version_installed(version) :
            raise ValueError(f"Python version '{version}' is not installed in {self.command}.")
        
        subprocess.run(
            [self.command, "local", version],
            cwd=project_dir,
            check=True,
        )

        

    def get_configured_version (self, project_dir: Path) -> str | None :
        config_path = project_dir / cs.CORELLIA_CONFIG_FILE

        if not config_path.exists() :
            return None
        
        config = CorelliaConfig.load(config_path)
        return config.get_project_python_version()
    

    def get_synced_local_version(self, project_dir: Path) -> str | None:
        python_version_path = project_dir / ".python-version"

        if not python_version_path.exists():
            return None
        
        content = python_version_path.read_text(encoding="utf-8").strip()
        return content or None
    

    def create_virtual_env (
        self, 
        project_dir: Path, 
        venv_name: str = cs.DEFAULT_VENV_NAME
    ) -> VirtualEnvManager :
        virtual_env = VirtualEnvManager(project_dir, venv_name)
        python_exec = self.get_python_executable(project_dir)
        virtual_env.ensure_created(python_exec)
        return virtual_env
    
    
    @classmethod
    def recreate_from_config (cls, config: CorelliaConfig) -> "PythonEnvManager" :
        return cls(config.get_environment_manager())
        
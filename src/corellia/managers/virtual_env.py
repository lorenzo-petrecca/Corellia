from pathlib import Path
import subprocess
import shutil
import shlex
from string import Template

from corellia.config import CorelliaConfig, ScriptConfig
from corellia import constants as cs
from corellia.managers.package import PackageManager


class VirtualEnvManager :
    def __init__(
        self, 
        project_dir: Path, 
        venv_name: str = cs.DEFAULT_VENV_NAME
    ) -> None:
        self.project_dir = project_dir
        self.venv_name = venv_name
        


    def get_root_path (self) -> Path :
        return self.project_dir / self.venv_name
    
    def get_bin_path(self) -> Path:
        return self.get_root_path() / "bin"

    def get_python_path (self) -> Path :
        return self.get_bin_path() / "python"
    
    
    def exists (self) -> bool :
        return self.get_root_path().exists()
    

    def ensure_created (self, python_executable: Path | None = None) -> None :
        if self.exists() :
            return
        
        python_cmd = str(python_executable) if python_executable is not None else "python"
        
        subprocess.run(
            [python_cmd, "-m", "venv", self.venv_name],
            cwd=self.project_dir,
            check=True,
        )
    
    def ensure_python_exists(self) -> None:
        python_path = self.get_python_path()

        if not python_path.exists():
            raise FileNotFoundError(
                f"Python executable was not found in the virtual environment: {python_path}"
            )

    
    def package_manager (self)-> PackageManager:
        self.ensure_python_exists()
        return PackageManager(self.get_python_path())
    

    def remove (self) -> None :
        root = self.get_root_path()
        if root.exists() :
            shutil.rmtree(root)


    def resolve_strict_command (self, script: ScriptConfig) -> list[str] :
        parts = shlex.split(script.command)

        if not parts :
            raise ValueError("Command cannot be empty")
        
        keywords = ("&&", "||", "|", ";", ">", ">>", "<", "$env")
        for part in parts:
            if any(k in part for k in keywords) :
                raise ValueError("This command probably needs to be run in shell mode")
            
        candidate = self.get_bin_path() / parts[0]
        if not candidate.exists() :
            raise FileNotFoundError (
                f"Executable '{parts[0]}' was not found in the project environment."
            )
        
        parts[0] = str(candidate)
        return parts
    

    def resolve_shell_command (self, script: ScriptConfig) -> str :
        command = script.command.strip()
        if not command :
            raise ValueError ("Command cannot be empty")
        
        return command.replace("$env", str(self.get_bin_path()))
        


    
    def run (self, script: ScriptConfig) -> None :
        if script.mode == "strict" :
            resolved = self.resolve_strict_command(script)
            subprocess.run(
                resolved,
                cwd=self.project_dir,
                check=True,
            )

            return

        if script.mode == "shell" :
            resolved = self.resolve_shell_command(script)
            subprocess.run(
                resolved,
                cwd=self.project_dir,
                check=True,
                shell=True
            )

            return
        
        raise ValueError (
            "No other scripting modes are currently supported besides 'strict' and 'shell'."
        )
    

    
    def ensure_build_installed (self) -> None :
        python_path = self.get_python_path()
        subprocess.run(
            [str(python_path), "-m", "pip", "install", "build"],
            cwd=self.project_dir,
            check=True,
        )

    
    def run_build (self) -> None :
        python_path = self.get_python_path()
        subprocess.run(
            [str(python_path), "-m", "build"],
            cwd=self.project_dir,
            check=True,
        )



    @classmethod
    def recreate_from_config (cls, project_dir: Path, config: CorelliaConfig) -> "VirtualEnvManager" :
        return cls(project_dir, config.get_virtual_env_name())

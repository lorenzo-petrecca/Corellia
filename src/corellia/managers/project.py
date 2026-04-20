from pathlib import Path
import re
from importlib.resources import files

from corellia.services.category import CategoryService
from corellia.managers.python_env import PythonEnvManager
from corellia.managers.git import GitManager
from corellia.managers.virtual_env import VirtualEnvManager
from corellia.managers.package_resolver import PackageResolver
from corellia.models import CreateModel, Category, CATEGORIES
from corellia.config import CorelliaConfig
from corellia import constants as cs
from corellia.frameworks import SUPPORTED_FRAMEWORKS
from corellia.frameworks.presets import FRAMEWORK_PACKAGES
from corellia.cli_utils import (
    Output, 
    Text, 
    TextStyle, 
    TextTransform,
    FontWeight,
    FontStyle,
    Padding,
    Margin,
    Table,
    Row,
    Title,
    List,
    Gap,
    Divider,
)



class ProjectManager :
    def __init__(self) -> None:
        self.python_manager = PythonEnvManager()


    def assign_name (self, name: str) -> Output:
        pattern = r"^[a-z0-9_-]+$"
        if not bool(re.fullmatch(pattern, name)) :
            return Output (
                Text(
                    "Invalid project name. Use only lowercase letters, numbers, '-' or '_'.",
                    style=TextStyle().from_level("warning")
                ),
                ok=False,
                exit_code=0,
            )
        
        if (Path.cwd() / name).exists() :
            return Output (
                Text(
                    f"Directory '{name}' already exists in the current location.",
                    style=TextStyle().from_level("warning")
                ),
                ok=False,
                exit_code=0,
            )

        self.root = Path.cwd() / name
        self.name = name
        return Output (
            ok=True,
            exit_code=0,
        )

    
    def check_py_manager (self) -> Output:
        if self.python_manager.exists():
            return Output (
                ok=True,
                exit_code=0
            )

        
        return Output (
            Text(
                f"{self.python_manager.command} is required but was not found in PATH.",
                style=TextStyle().from_level("error")
            ),
            ok=False,
            exit_code=1,
        )
    

    def get_py_versions_list (self) -> Output :
        versions = self.python_manager.get_installed_versions()

        if not versions :
            return Output (
                Text(
                    "No Python versions found",
                    style=TextStyle().from_level("error")
                ),
                Text(
                    "Install a Python version before continuing.",
                    style=TextStyle().from_level("warning")
                ),
                ok=False,
                exit_code=1,
            )
        

        return Output (
            Title(
                f"Installed Python versions in {self.python_manager.command}",
                type="raw",
            ),
            List(
                [f"{version}" for version in versions],
                marker_type="square",
                margin=Margin(1, 1),
                gap=Gap(1, 0)
            ),
            ok=True,
            exit_code=0,
        )
    

    def check_py_version (self, version: str) -> Output :
        if not self.python_manager.is_version_installed(version) :
            return Output (
                Text(
                    f"Python {version} is not installed in {self.python_manager.command}.",
                    "Choose one of the installed versions shown above.",
                    style=TextStyle().from_level("warning")
                ),
                ok=False,
                exit_code=0,
            )
        
        return Output (
            ok=True,
            exit_code=0,
        )
    

    def get_supported_frameworks (self) -> Output :
        return Output (
            Title(
                "Supported frameworks",
                type="raw",
            ),
            List(
                [f"{str(fw)}" for fw in SUPPORTED_FRAMEWORKS],
                marker_type="square",
                margin=Margin(1, 1),
                gap=Gap(1, 0)
            ),
            ok=True,
            exit_code=0,
        )
    
    def check_framework (self, framework: str) :
        framework = framework.strip().lower()

        if framework not in SUPPORTED_FRAMEWORKS :
            return Output (
                Text(
                    "Unsupported framework.",
                    "Chose a supported framework:",
                ),
                List(
                    [f"{str(fw)}" for fw in SUPPORTED_FRAMEWORKS],
                    marker_type="square",
                    margin=Margin(0, 1),
                    gap=Gap(1, 0),
                    style=TextStyle().from_level("warning")
                ),
                ok=False,
                exit_code=0,
            )
        
        return Output (
            ok=True,
            exit_code=0,
        )
    

    def get_supported_categories (self) -> Output :
        return Output (
            Title(
                "Supported category",
                type="raw",
            ),
            List(
                [f"{str(category)}" for category in CATEGORIES],
                marker_type="square",
                margin=Margin(1, 1),
                gap=Gap(1, 0),
            ),
            ok=True,
            exit_code=0,
        )
    
    def check_category (self, category: str) :
        category = category.strip().lower()

        if category not in CATEGORIES :
            return Output(
                Text(
                    "This category does not exists",
                    "Chose a category from:",
                    style=TextStyle.from_level('warning'),
                ),
                List(
                    [f"{str(category)}" for category in CATEGORIES],
                    marker_type="square",
                    margin=Margin(0, 1),
                    gap=Gap(1, 0),
                    style=TextStyle.from_level('warning'),
                ),
                ok=False,
                exit_code=0,
            )
        
        return Output (
            ok=True,
            exit_code=0,
        )



    def bootstrap (self, model: CreateModel) -> Output :
        if not model.is_complete() :
            return Output (
                Text(
                    "Error creating the project. The template required to create the project is incomplete.",
                    style=TextStyle().from_level("error")
                ),
                ok=False,
                exit_code=1,
            )
        

        # 1. Creazione cartella root
        self.root.mkdir()

        # 2a. Acquisizione dal model del framework scelto
        framework = model.project_framework
        # 2b. Acquisizione dei pacchetti di preset del framework
        preset_packages = FRAMEWORK_PACKAGES.get(framework, [])
        # 2c. Resolver dei pacchetti -> pacchetti@latest
        resolver = PackageResolver()
        resolved_packages = resolver.resolve(preset_packages)

        # 3. Creazione file di config (corellia.toml) con impostazioni fornite tramite cli
        self.config = CorelliaConfig.from_model(
            path=(self.root / cs.CORELLIA_CONFIG_FILE), 
            model=model,
            dependencies=resolved_packages,
        )
        self.config.save()

        # 4. Applica versione python all'area di progetto
        python_version = self.config.get_project_python_version()
        self.python_manager.set_local_version(self.root, python_version)

        # 5. Creazione ambiente virtuale python e salvataggio del manager
        venv_name = self.config.get_virtual_env_name()
        self.virtual_env = self.python_manager.create_virtual_env(self.root, venv_name)

        # 6. Creazione e aggiornamento del package manager nell'ambiente virtuale python
        self.package_manager = self.virtual_env.package_manager()
        self.package_manager.upgrade(self.root)

        # 7. Installazione delle dipendenze (se presenti)
        deps = self.package_manager.install_deps(self.root, self.config)
        dev_deps = self.package_manager.install_dev_deps(self.root, self.config)

        # 8. Inizializzazione del framework scelto
        framework = self.config.get_framework_name()
        if framework == "django" :
            from corellia.services.django import DjangoService
            django = DjangoService(self.virtual_env.get_python_path())
            django.startproject(self.root)

        # 9. Creazione del layout del progetto in base alla categoria scelta
        layout = CategoryService(self.root)
        layout.scaffold()

        # 10. Creazione file .gitignore
        template = files("corellia.templates").joinpath("gitignore.txt")
        gitignore_path = self.root / ".gitignore"
        gitignore_path.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")

        # 11. Inizializzazione git
        self.git = GitManager()
        if self.git.exists() :
            self.git.init_repo(project_dir=self.root)
            self.git.set_main_branch(project_dir=self.root)

        git_avail = cs.GIT_AVAILABLE if self.git.is_initialized(self.root) else cs.GIT_NOT_AVAILABLE



        return Output (
            Text(""),
            Text(f"{self.name} (Corellia project)", style=TextStyle(text_transform=TextTransform.REVERSE)),
            Text(
                f"- path: {self.root}",
                f"- python: {python_version}",
                f"- venv: {self.config.get_virtual_env_name()}",
                f"- framework: {self.config.get_framework_name()}",
                f"- git: {git_avail}",
                ""
            ),
            Text(cs.DEPENDENCY_SECTION_NAME, style=TextStyle(text_transform=TextTransform.REVERSE)),
            Text(*deps, ""),
            Text(cs.DEV_DEPENDENCY_SECTION_NAME, style=TextStyle(text_transform=TextTransform.REVERSE)),
            Text(*dev_deps, ""),
            Text(
                "Corellia project succesfully created.",
                style=TextStyle().from_level("success")
            ),
            ok=True,
            exit_code=0,
        )





    def _setup_context (self) -> Output :
        self.root = Path.cwd()
        config_path = self.root / cs.CORELLIA_CONFIG_FILE

        if not config_path.exists() :
            return Output (
                Text(
                    f"No {cs.CORELLIA_CONFIG_FILE} found in the current directory.",
                    "Run this command inside a Corellia project.",
                    style=TextStyle().from_level("error")
                ),
                ok=False,
                exit_code=1,
            )
        
        self.config = CorelliaConfig.load(config_path)
        self.python_manager = PythonEnvManager.recreate_from_config(self.config)
        self.virtual_env = VirtualEnvManager.recreate_from_config(self.root, self.config)

        return Output (
            ok=True,
            exit_code=0,
        )


    def _ensure_environment_ready (self, recreate: bool) -> Output :
        prepared = self._setup_context() # prepara ambiente corellia nella root (se esiste)

        if not prepared.ok :
            return prepared
        
        # Assicurarsi che ambiente python esista nella root
        if not self.python_manager.exists() :
            return Output (
                Text(
                    f"Environment manager error: '{self.python_manager.command}' was not found.",
                    "Install and configure it before continuing.",
                    style=TextStyle().from_level("error")
                ),
                ok=False,
                exit_code=1,
            )
        
        # Controllo esistenza della versione, specificata nel config, di python nell'ambiente root
        python_version = self.config.get_project_python_version()
        if not self.python_manager.is_version_installed(python_version) :
            return Output (
                Text(
                    f"Python version '{python_version}' is not installed in {self.python_manager.command}.",
                    style=TextStyle().from_level("error")
                ),
                Text(
                    "Install the required version before continuing.",
                    style=TextStyle().from_level("warning")
                ),
                ok=False,
                exit_code=1,
            )
        
        # Aggiornamento di sicurezza del file d'ambiente '.python-version' (ricrea file)
        self.python_manager.set_local_version(self.root, python_version)

        # Usare il path reale di python nell'ambiente corellia
        try :
            python_executable = self.python_manager.get_python_executable(self.root)
        except Exception as exc:
            return Output(
                Text(
                    "Could not resolve the Python executable for the current project.",
                    str(exc),
                    style=TextStyle().from_level("error")
                ),
                ok=False,
                exit_code=1,
            )

        # Acquisizione dell'ambiente virtuale 
        # Se recreate è true ricrea da zero l'ambiente virtuale (pulizia ambiente)
        if recreate :
            self.virtual_env.remove()

        self.virtual_env.ensure_created()   # controllo esistenza ambiente
        self.package_manager = self.virtual_env.package_manager()   # ricrea il package manager


        return Output (
            Text(
                f"Using Python {python_version}",
                f"Using virtual environment: {self.virtual_env.venv_name}",
                style=TextStyle().from_level("info")
            ),
            ok=True,
            exit_code=0,
        )
    

    def sync_package (self, package: str) -> Output :
        """
        Helper per comando 'core sync --package <package>'
        """
        # Check se environment è ok
        ready = self._ensure_environment_ready(recreate=False)  
        if not ready.ok :
            return ready
        
        # Installazione della versione specificata nel config del pacchetto specificato nel comando
        version = None
        deps = self.config.get_dependencies()
        dev_deps = self.config.get_dev_dependencies()
        if package in deps :
            version = deps[package]
        elif package in dev_deps :
            version = dev_deps[package]

        if version is None :
            return Output (
                Text(
                    f"Package '{package}' is not declared in {cs.CORELLIA_CONFIG_FILE}.",
                    style=TextStyle().from_level("error")
                ),
                ok=False,
                exit_code=1,
            )
        
        self.package_manager.install(self.root, deps={package: version})


        return Output (
            Text(""),
            Text(
                "Installed 1 package",
                style=TextStyle(text_transform=TextTransform.REVERSE).from_level("success")
            ),
            Text(f"- {package}@{version} --> installed"),
            ok=True,
            exit_code=0,
        )
    

    def sync (self, clean: bool, nodev: bool) -> Output :
        ready = self._ensure_environment_ready(recreate=clean)
        if not ready.ok :
            return ready
        
        self.package_manager.upgrade(self.root)

        deps_data = self.package_manager.install_deps(self.root, self.config)
        dev_deps_data: list[str] = []
        if not nodev:
            dev_deps_data = self.package_manager.install_dev_deps(self.root, self.config)

        final_message = (
            "Environment rebuilt successfully."
            if clean
            else "Environment synchronized successfully."
        )

        payload = [
            *ready.payload,
            Text(""),
            Text(*deps_data),
        ]

        if nodev :
            payload.extend([
                Text(""),
                Text("Skipped development dependencies (--no-dev)."),
            ])
        else :
            payload.extend([
                Text(""),
                Text(*dev_deps_data),
            ])

        payload.extend([
            Text(""),
            Text(final_message, style=TextStyle().from_level("success"))
        ])

        return Output (
            *payload,
            ok=True,
            exit_code=0,
        )
    

    def add_package (
        self, 
        package: str, 
        version: str | None = None, 
        dev: bool = False,
    ) -> Output :
        """
        Add or update a dependency in corellia.toml and sync it immediately.
        """
        package = package.strip()

        if not package :
            return Output (
                Text(
                    "Package name cannot be empty",
                    style=TextStyle().from_level("error"),
                ),
                ok=False,
                exit_code=1,
            )
        
        
        # Verifica che si è in un progetto Corellia e caricamento del config
        prepared = self._setup_context()
        if not prepared.ok :
            return prepared
        

        # Verifica se il pacchetto è già installato nell'altro gruppo
        # rispetto a quello in cui si vuole installare
        # Nel caso si ritorna errore e si blocca il processo
        in_deps = self.config.has_dependency(package)
        in_dev_deps = self.config.has_dev_dependency(package)
        if dev and in_deps :
            current = self.config.get_dependency_version(package)
            return Output (
                Text(
                    f"Package '{package}' is already declared in [dependencies].",
                    f"Current version: {current}",
                    "Remove it from runtime dependencies before adding it as a dev dependency.",
                    style=TextStyle().from_level("error"),
                ),
                ok=False,
                exit_code=1,
            )

        if not dev and in_dev_deps :
            current = self.config.get_dev_dependency_version(package)
            return Output (
                Text(
                    f"Package '{package}' is already declared in [dev-dependencies].",
                    f"Current version: {current}",
                    "Remove it from dev-dependencies before adding it as a runtime dependency.",
                    style=TextStyle().from_level("error"),
                ),
                ok=False,
                exit_code=1,
            )
        

        # Risolve la versione del pacchetto se non passata
        resolved_version = version
        if resolved_version is None :
            resolver = PackageResolver()
            resolved_version = resolver.latest(package)

        if not resolved_version :
            return Output (
                Text(
                    f"Could not resolve a version for package '{package}'.",
                    "Check that package exists and try again.",
                    style=TextStyle().from_level("error"),
                ),
                ok=False,
                exit_code=1,
            )
        

        # Aggiornamento del config e installazione

        section_name = cs.DEV_DEPENDENCY_SECTION_NAME if dev else cs.DEPENDENCY_SECTION_NAME
        previous_version = (
            self.config.get_dev_dependency_version(package)
            if dev
            else self.config.get_dependency_version(package)
        )

        self.config.set_dependency(package, resolved_version, dev)
        synced = self.sync_package(package)
        if not synced.ok :
            return synced

        action = "Updated" if previous_version else "Added"

        return Output (
            Text(
                "",
                f"{action} package in {cs.CORELLIA_CONFIG_FILE}:",
                f"- [{section_name}] {package} = \"{resolved_version}\"",
                "",
            ),
            *synced.payload,
            ok=True,
            exit_code=0,
        )
    

    def remove_package (self, package: str) -> Output :
        """
        Remove a dependency from corellia.toml and uninstall it immediately.
        """
        package = package.strip()
        if not package :
            return Output (
                Text(
                    "Package name cannot be empty",
                    style=TextStyle().from_level("error"),
                ),
                ok=False,
                exit_code=1,
            )
        
        # Verifica contesto progetto e caricamento del config
        prepared = self._setup_context()
        if not prepared.ok :
            return prepared
        
        in_deps = self.config.has_dependency(package)
        in_dev_deps = self.config.has_dev_dependency(package)

        if not in_deps and not in_dev_deps :
            return Output (
                Text(
                    f"Package '{package}' is not declared in {cs.CORELLIA_CONFIG_FILE}.",
                    style=TextStyle().from_level("error"),
                ),
                ok=False,
                exit_code=1,
            )
        
        # Determina da quale sezione rimuovere il pacchetto
        is_dev = in_dev_deps
        section_name = cs.DEV_DEPENDENCY_SECTION_NAME if is_dev else cs.DEPENDENCY_SECTION_NAME
        current_version = (
            self.config.get_dependency_version(package)
            if not is_dev
            else self.config.get_dev_dependency_version(package)
        )

        # Aggiornamento della fonte di verità (rimozione pacchetto da config)
        self.config.remove_dependency(package, dev=is_dev)

        # Preparazione ambiente
        ready = self._ensure_environment_ready(recreate=False)
        if not ready.ok :
            return ready
        
        # Disinstallazione pacchetto
        self.package_manager.uninstall(self.root, package)


        return Output (
                Text(
                    "",
                    f"Removed package from {cs.CORELLIA_CONFIG_FILE}:",
                    f'- [{section_name}] {package} = "{current_version}"',
                    "",
                ),
                *ready.payload,
                Text(
                    "Uninstalled 1 package",
                    style=TextStyle(text_transform=TextTransform.REVERSE),
                ),
                Text(
                    f"- {package} --> removed",
                    "",
                ),
                Text(
                    "Note: transitive dependencies may still remain installed.",
                    f"Run command: `core sync --clean` if you need a fully clean environment.",
                    style=TextStyle().from_level("warning"),
                ),
                Text("core sync --clean", style=TextStyle(text_transform=TextTransform.REVERSE)),
                Text("if you need a fully clean environment."),
                ok=True,
                exit_code=0,
            )

    
    def _prepare_scripts_context(self) -> Output :
        # 1. Verifica contesto progetto e caricamento del config
        ready = self._ensure_environment_ready(recreate=False)
        if not ready.ok :
            return ready
        
        # 2. Controllo esistenza sezione scripts nel config
        scripts_raw = self.config.get_scripts()
        if not scripts_raw :
            return Output (
                Text(
                    f"No [scripts] section entries were found in {cs.CORELLIA_CONFIG_FILE}.",
                    style=TextStyle().from_level("error")
                ),
                ok=False,
                exit_code=1,
            )
        
        return Output (
            *ready.payload,
            ok=True,
            exit_code=0,
        )


    def run_script (self, script_name: str) -> Output :
        """
        Execute a script declared in [scripts] inside the project environment.
        """
        # 1. Verifica contesto progetto e controllo del config
        check = self._prepare_scripts_context()
        if not check.ok :
            return check
        
        
        # 3. Check esistenza script richiesto
        if not self.config.has_script(script_name) :
            script_list = self.config.get_script_list()
            return Output (
                Text(
                    f"Script '{script_name}' is not declared in {cs.CORELLIA_CONFIG_FILE}.",
                    "",
                    style=TextStyle().from_level("error")
                ),
                Text(
                    "Available scripts:",
                    style=TextStyle(text_transform=TextTransform.REVERSE)
                ),
                Table(
                    Row(["Script", "Mode", "Description"],),
                    *[
                        Row([script.name, script.mode, script.description or ""],) 
                        for script in script_list
                    ],
                ),
                ok=False,
                exit_code=1,
            )
        

        # 4. Recupero script
        script = self.config.get_script(script_name)
        if script is None :
            return Output (
                Text(
                    f"Error retrieving the {script_name} script from {cs.CORELLIA_CONFIG_FILE}",
                    style=TextStyle().from_level("error")
                ),
                ok=False,
                exit_code=1,
            )
        
        # 5. Esecuzione del comando presente nello script
        try :
            self.virtual_env.run(script)
        except Exception as exc:
            return Output (
                Text(
                    f"Script '{script.name}' failed.",
                    str(exc),
                    style=TextStyle().from_level("error")
                ),
                ok=False,
                exit_code=1,

            )
        
        return Output (
            *check.payload,
            ok=True,
            exit_code=0,
        )
        


    def list_scripts (self) -> Output :
        check = self._prepare_scripts_context()
        if not check.ok :
            return check
        
        script_list = self.config.get_script_list()

        if not script_list :
            return Output (
                Text(
                    f"No scripts found.",
                    style=TextStyle().from_level("error")
                ),
                ok=False,
                exit_code=1,
            )
        
        
        return Output (
            *check.payload,
            Table(
                Row(["Script", "Mode", "Description"],),
                *[
                    Row([script.name, script.mode, script.description or ""],) 
                    for script in script_list
                ],
            ),
            ok=True,
            exit_code=0,
        )

        

    def info (self) -> Output :
        prepared = self._setup_context()
        if not prepared :
            return prepared
        
        # Config properties
        project_name = self.config.get_project_name()
        project_version = self.config.get_project_version()
        project_category = self.config.get_project_category()
        framework = self.config.get_framework_name()
        python_required = self.config.get_project_python_version()

        # Python environment properties
        python_manager_available = self.python_manager.exists()
        python_version_installled = (
            self.python_manager.is_version_installed(python_required)
            if python_manager_available
            else False
        )
        python_local_version = self.python_manager.get_synced_local_version(self.root)
        pyhton_version_synced = python_local_version == python_required

        # Python Virtual environment
        venv_exists = self.virtual_env.exists()
        venv_root_path = self.virtual_env.get_root_path()
        venv_python_path = self.virtual_env.get_python_path()
        venv_python_exists = venv_python_path.exists()

        # Dependencies
        deps_count = len(self.config.get_dependencies())
        dev_deps_count = len(self.config.get_dev_dependencies())

        # Git
        git = GitManager()
        git_available = git.exists()
        git_repo_initialized = git.is_initialized(self.root) if git_available else False
        git_branch = git.get_current_branch(self.root)
        git_remote = git.has_remote(self.root)
        git_status = git.is_dirty(self.root)


        return Output (
            Title(
                project_name,
                type="outlined",
                margin=Margin(2, 1),
                padding=Padding(0,2,0,2),
            ),
            Table(
                Row(["Section", "Property", "Value"]),
                Row(["Project", "Version", project_version]),
                Row(["Project", "category", project_category]),
                Row(["Project", "Framework", framework]),
                Row(["Project", "Python required", python_required]),

                Row(["Python environment", "Manager available", "yes" if python_manager_available else "⚠ no"]),
                Row(["Python environment", "Python installed", "yes" if python_version_installled else "⚠ no"]),
                Row(["Python environment", "Local version", python_local_version if python_local_version is not None else "⚠️ NOT FOUND"]),
                Row(["Python environment", "Version synced", "yes" if pyhton_version_synced else "⚠ no"]),
                
                Row(["Virtual environment", "Available", "yes" if venv_exists else "⚠ no"]),
                Row(["Virtual environment", "Path", str(venv_root_path)]),
                Row(["Virtual environment", "Python executable exists", "yes" if venv_python_exists else "⚠ no"]),

                Row(["Dependencies", "Runtime", str(deps_count)]),
                Row(["Dependencies", "Development", str(dev_deps_count)]),

                Row(["Git", "Available", "yes" if git_available else "no"]),
                Row(["Git", "Repo initialized", "yes" if git_repo_initialized else "no"]),
                Row(["Git", "Branch", git_branch if git_branch is not None else "⚠ NOT FOUND"]),
                Row(["Git", "Remote", "yes" if git_remote else "no"]),
                Row(["Git", "Status", "⚠ dirty" if git_status else "clean"]),

                margin=Margin(0,0)
            ),
            ok=True,
            exit_code=0,
        )
    


    def init_build (self) -> Output :
        prepared = self._setup_context()
        if not prepared.ok :
            return prepared
        
        category = self.config.get_project_category()
        if category != "package" :
            return Output(
                Text(
                    "Build initialization is only supported for 'package' projects.",
                    f"Current category: {category}",
                    style=TextStyle().from_level("error"),
                ),
                ok=False,
                exit_code=1,
            )
        
        category_service = CategoryService(self.root)
        if not category_service.validate_layout() :
            return Output (
                Text (
                    "Invalid package layout for build initialization.",
                    f"Expected package path: {str(self.root / "src" / self.config.get_project_name())}",
                    style=TextStyle().from_level("error"),
                ),
                ok=False,
                exit_code=1,
            )
        
        CategoryService.init_package_build(self.root)
        return Output(
            Text(
                "Build configuration initialized successfully.",
                "Generated artifacts:",
                style=TextStyle().from_level("success"),
            ),
            List (
                ["pyproject.toml"],
                marker_type='filled-square',
                margin=Margin(0,0),
                left_indent=1,
                style=TextStyle().from_level("success"),
            ),
            ok=True,
            exit_code=0,
        )
    


    def build (self) -> Output :
        """
        Build the current Corellia project as a Python package.

        Supported only for projects with:
        [project]
        category = "package"
        """

        # 1. Verify project context and load config
        prepared = self._setup_context()
        if not prepared.ok :
            return prepared
        
        # 2. Validate category
        category = self.config.get_project_category()
        if category != "package" :
            return Output(
                Text(
                    "Build is only supported for 'package' projects.",
                    f"Current category: {category}",
                    style=TextStyle().from_level("error"),
                ),
                ok=False,
                exit_code=1,
            )
        
        # 3. Validate pyproject.toml presence
        pyproject_path = self.root / "pyproject.toml"
        if not pyproject_path.exists() :
            return Output(
                Text(
                    "Build configuration not initialized.",
                    "You have to run first",
                    style=TextStyle().from_level("warning"),
                ),
                Text(
                    "core init-build",
                    style=TextStyle(font_weight=FontWeight.BOLD, text_transform=TextTransform.REVERSE)
                ),
                ok=False,
                exit_code=1,
            )
        
        # 4. Validate expected package layout
        category_service = CategoryService(self.root)
        if not category_service.validate_layout() :
            return Output (
                Text (
                    "Invalid package layout for build initialization.",
                    f"Expected package path: {str(self.root / "src" / self.config.get_project_name())}",
                    style=TextStyle().from_level("error"),
                ),
                ok=False,
                exit_code=1,
            )
        

        # 5. Prepare environment
        ready = self._ensure_environment_ready(recreate=False)
        if not ready.ok :
            return ready
        

        # 6. Clean old build artifacts
        try :
            category_service.clean_build_artifacts()
        except Exception as exc :
            return Output(
            Text(
                "Could not clean previous build artifacts.",
                str(exc),
                style=TextStyle().from_level("error")
            ),
            ok=False,
            exit_code=1,
        )

        
        # 7. Ensure `build` is installed in project venv
        python_path = self.virtual_env.get_python_path()
        try :
            self.virtual_env.ensure_build_installed()
        except Exception as exc :
            return Output(
                Text(
                    "Could not install the python build module.",
                    str(exc),
                    style=TextStyle().from_level("error"),
                ),
                ok=False,
                exit_code=1,
            )
        
        
        # 8. Run package build
        try :
            self.virtual_env.run_build()
        except Exception as exc :
            return Output(
                Text(
                    "Build failed",
                    str(exc),
                    style=TextStyle().from_level("error"),
                ),
                ok=False,
                exit_code=1,
            )
        
        
        # 9. Collect generated artifacts
        dist_path = self.root / "dist"
        artifacts = []
        if dist_path.exists() :
            artifacts = sorted(
                path.name
                for path in dist_path.iterdir()
                if path.is_file()
            )

        payload = [
            *ready.payload,
            Divider(),
            Text(
                "Build completed successfully",
                style=TextStyle().from_level("success"),
            )
        ]

        if artifacts and len(artifacts) > 0 :
            payload.extend([
                Text("Artifacts generated:"),
                List(
                    [f"{name}" for name in artifacts],
                    marker_type="filled-square",
                    margin=Margin(0,0),
                    left_indent=1,
                )
            ])
        else :
            payload.extend([
                Text(
                    "Build completed, but no artifacts were found in dist/.",
                    style=TextStyle().from_level("warning"),
                )
            ])

        return Output(
            *payload,
            ok=True,
            exit_code=0,
        )
        
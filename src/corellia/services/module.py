from pathlib import Path

from corellia.config import CorelliaConfig
from corellia.services.category import CategoryService


class ModuleService :
    def __init__(
        self,
        root: Path,
        config: CorelliaConfig,
    ) -> None:
        self.root = root
        self.config = config


    def rename (self, new_name: str) -> tuple[str, str] :
        """
        Rename the project's main module directory and update
        corellia.toml.

        Returns the previous and new module names.

        Raises ValueError or OSError if the operation fails.
        """

        from corellia.validators import Validators

        current = self.config.project.module

        # Legacy projects without an explicit module are
        # not renamed automatically.
        if not current :
            raise ValueError(
                "The project does not declare a module. "
                "Set [project].module before renaming."
            )

        # Reuse the same validator as ProjectSectionModel.
        errors = Validators.python_module_name()(
            new_name,
            "project.module"
        )

        if errors :
            raise ValueError("; ".join(errors))

        if current == new_name :
            raise ValueError(
                f"The module is already named '{new_name}'."
            )

        # Django projects can contain references to the
        # configuration module that require special handling.
        framework = self.config.framework.name
        if framework and framework.lower() == "django" :
            raise ValueError(
                "Module renaming is not supported for "
                "Django projects yet."
            )

        category_service = CategoryService(self.root)
        old_path = category_service.get_module_path()
        new_path = old_path.with_name(new_name)

        # Do not rename symlinks: only actual module directories.
        if old_path.is_symlink() :
            raise ValueError(
                f"Module path is a symbolic link: {old_path}"
            )

        if not old_path.is_dir() :
            raise ValueError(
                f"Module directory not found: {old_path}"
            )

        if not (old_path / "__init__.py").is_file():
            raise ValueError(
                f"Invalid module layout: {old_path}"
            )


        if new_path.exists() or new_path.is_symlink() :
            raise ValueError(
                f"Destination already exists: {new_path}"
            )


        # Rename the directory first, preserving its contents.
        old_path.rename(new_path)

        try :
            self.config.set_project_module(new_name)

        except Exception as exc :
            # Restore the in-memory configuration.
            self.config.model.project.module = current

            try :
                new_path.rename(old_path)
            except OSError as rollback_error:
                raise OSError(
                    "Could not save corellia.toml, and "
                    "the directory rollback also failed. "
                    f"Original error: {exc}. "
                    f"Rollback error: {rollback_error}"
                ) from rollback_error

            raise OSError(
                "Could not update corellia.toml. "
                "The module directory was restored. "
                f"Original error: {exc}"
            ) from exc


        return current, new_name

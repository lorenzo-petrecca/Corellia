"""
Il servizio ha tre responsabilità:
- validate() verifica il formato della versione;
- resolve() calcola la versione finale;
- prepare_init_update() prepara la modifica di un eventuale __version__ senza riscrivere il resto del file.
"""

import re
from pathlib import Path


class VersionService :
    VERSION_PATTERN = re.compile(
        r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    )

    INIT_VERSION_PATTERN = re.compile(
        r"""^(__version__\s*=\s*)(["'])([^"'\r\n]*)\2(?=\s*$)""",
        re.MULTILINE,
    )

    @classmethod
    def validate (cls, version: str) -> bool :
        return cls.VERSION_PATTERN.fullmatch(version) is not None


    @classmethod
    def resolve (cls, current: str, target: str) -> str :
        if not cls.validate(current):
            raise ValueError(
                f"Unsupported current version: {current}"
            )

        if target in ("major", "minor", "patch") :
            major, minor, patch = map(int, current.split("."))

            if target == "major":
                return f"{major + 1}.0.0"

            if target == "minor":
                return f"{major}.{minor + 1}.0"

            return f"{major}.{minor}.{patch + 1}"

        if not cls.validate(target) :
            raise ValueError(
                f"Invalid version: {target}. "
                "Expected MAJOR.MINOR.PATCH."
            )

        return target


    @classmethod
    def prepare_init_update (
        cls,
        path: Path,
        version: str,
    ) -> tuple[str, str] | None :
        """
        Prepare an update for an existing literal __version__.

        Returns the original and updated content, or None
        when no supported assignment is present.
        """

        if not path.is_file() :
            return None

        original = path.read_text(encoding="utf-8")
        matches = list(cls.INIT_VERSION_PATTERN.finditer(original))

        if not matches :
            return None

        if len(matches) > 1 :
            raise ValueError(
                f"Multiple __version__ assignments found in {path}"
            )

        m = matches[0]
        start, end = m.span(3)
        updated = original[:start] + version + original[end:]

        return original, updated

    

            
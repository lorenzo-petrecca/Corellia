import os
import stat
import tempfile
from pathlib import Path

def write_bytes (path: Path, content: bytes) -> None :
    """
    Write a new file normally.

    When overwriting an existing regular file, write to
    a temporary file first and atomically replace the original.
    """
    if path.is_symlink():
        raise ValueError(
            f"Refusing to overwrite a symbolic link: {path}"
        )

    if not path.exists() :
        path.write_bytes(content)
        return

    if not path.is_file() :
        raise ValueError(f"Not a regular file: {path}")


    temporary_path: Path | None = None

    try :
        with tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as temporary :
            temporary_path = Path(temporary.name)
            temporary.write(content)

        # Preserve the original file permission bits.
        mode = stat.S_IMODE(path.stat().st_mode)
        temporary_path.chmod(mode)

        # Replace the original only after writing the new file.
        os.replace(temporary_path, path)

    finally :
        if temporary_path is not None :
            temporary_path.unlink(missing_ok=True)


def write_text (path: Path, content: str, encoding: str = "utf-8") -> None:
    write_bytes(path, content.encode(encoding))

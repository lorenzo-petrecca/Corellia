from typing import Literal

Framework = Literal["django", "none"]

SUPPORTED_FRAMEWORKS: set[Framework] = {"django", "none"}
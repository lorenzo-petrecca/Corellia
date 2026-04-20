from typing import Literal
from corellia.cli_utils.output import Payload
from corellia.cli_utils.borders import Border
from corellia.cli_utils.style import (
    TextStyle, 
    FontWeight,
    FontStyle, 
    EscapeCommand, 
    TextTransform,
    ForegroundColor,
    BackgroundColor,
    Margin,
    Padding,
    Gap,
    ANSI_RESET,
)
import shutil


class Divider (Payload) :

    DividerSimbol = Literal["blank", "hyphen", "underscore", "double", "bar", "tilde"]
    DIVIDER_SIMBOL_MAP: dict[DividerSimbol, str] = {
        "blank": " ",
        "hyphen": "-",
        "underscore": "_",
        "double": "=",
        "bar": "—",
        "tilde": "~",
    }


    def __init__(self, symbol: DividerSimbol | None = None) -> None:
        self.symbol: Divider.DividerSimbol = symbol if symbol is not None else "hyphen"
        self.width = shutil.get_terminal_size().columns

        formatted = [Divider.DIVIDER_SIMBOL_MAP[self.symbol] * self.width]

        super().__init__(formatted)
from typing import Literal
from dataclasses import dataclass

ANSI_RESET = "\033[0m"

class EscapeCommand:
    ESC = "\033["
    RESET = "0"
    def __init__(self, *args: str) -> None:
        attr = ";".join([self.RESET, *args])
        self.command = "".join([self.ESC, attr, "m"])

    def __str__(self) -> str:
        return self.command



class FontWeight :
    LIGHT = "2"
    BOLD = "1"
    REGULAR = "22"

class FontStyle :
    NORMAL = "23"
    ITALIC = "3"

class TextTransform :
    UNDERLINE = "4"
    REVERSE = "7"
    STRIKE = "9"
    DOUBLE = "21"
    NONE = "24;27;29"


class ForegroundColor :
    DEFAULT = "39"

    BLACK = "30"
    RED = "31"
    GREEN = "32"
    YELLOW = "33"
    BLUE = "34"
    MAGENTA = "35"
    CYAN = "36"
    WHITE = "37"

    GRAY = "90"
    BRIGHT_RED = "91"
    BRIGHT_GREEN = "92"
    BRIGHT_YELLOW = "93"
    BRIGHT_BLUE = "94"
    BRIGHT_MAGENTA = "95"
    BRIGHT_CYAN = "96"
    BRIGHT_WHITE = "97"


class BackgroundColor :
    DEFAULT = "49"

    BLACK = "40"
    RED = "41"
    GREEN = "42"
    YELLOW = "43"
    BLUE = "44"
    MAGENTA = "45"
    CYAN = "46"
    WHITE = "47"

    GRAY = "100"
    BRIGHT_RED = "101"
    BRIGHT_GREEN = "102"
    BRIGHT_YELLOW = "103"
    BRIGHT_BLUE = "104"
    BRIGHT_MAGENTA = "105"
    BRIGHT_CYAN = "106"
    BRIGHT_WHITE = "107"

    
@dataclass
class Padding :
    top: int
    right: int
    bottom: int
    left: int

@dataclass
class Margin :
    top: int
    bottom: int

@dataclass 
class Gap :
    horizontal: int
    vertical: int



class TextStyle :
    def __init__ (
        self,
        prefix: str = "",
        color: str = ForegroundColor.DEFAULT,
        bg: str = BackgroundColor.DEFAULT,
        font_weight: str = FontWeight.REGULAR,
        font_style: str = FontStyle.NORMAL,
        text_transform: str = TextTransform.NONE,
    ) -> None:
        self.font_style = font_style
        self.text_transform = text_transform
        self.background_color = bg
        self.prefix = prefix
        self.color = color
        self.font_weight = font_weight


    def level (self, lvl: "MessageLevel") -> "TextStyle" :
        style = CLI_LEVELS[lvl]
        self.prefix = style.prefix
        self.color = style.color
        self.font_weight = style.font_weight
        return self
    
    @classmethod
    def from_level (cls, lvl: "MessageLevel") -> "TextStyle" :
        return cls().level(lvl)


MessageLevel = Literal["success", "info", "warning", "error", "default"]
CLI_LEVELS: dict [MessageLevel, TextStyle] = {
    "success": TextStyle(
        prefix="[OK]",
        color=ForegroundColor.GREEN,
        font_weight=FontWeight.BOLD,
    ),
    "info": TextStyle(
        prefix="[INFO]",
        color=ForegroundColor.CYAN,
        font_weight=FontWeight.BOLD,
    ),
    "warning": TextStyle(
        prefix="[WARN]",
        color=ForegroundColor.YELLOW,
        font_weight=FontWeight.BOLD,
    ),
    "error": TextStyle(
        prefix="[ERR]",
        color=ForegroundColor.RED,
        font_weight=FontWeight.BOLD,
    ),
    "default": TextStyle (
        prefix="",
        color=ForegroundColor.DEFAULT,
        font_weight=FontWeight.REGULAR,
    ),
}

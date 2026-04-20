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



class List (Payload) :

    MarkerType = Literal[
        "dot",
        "filled-dot", 
        "filled-circle", 
        "circle", 
        "hyphen", 
        "filled-square", 
        "square",
        "triangular",
        "filled-diamond",
        "diamond" ,
        "decimal", 
        "lower-alpha", 
        "upper-alpha",
    ]

    UNORDERED: tuple[MarkerType, ...] = (
        "dot",
        "filled-dot", 
        "filled-circle", 
        "circle", 
        "hyphen", 
        "filled-square", 
        "square",
        "triangular",
        "filled-diamond",
        "diamond" ,
    )
    ORDERED: tuple[MarkerType, ...] = ("decimal", "lower-alpha", "upper-alpha")

    UNORDERED_MARKER_MAP: dict[MarkerType, str] = {
        "dot" : "◦",
        "filled-dot": "・",
        "filled-circle": "●",
        "circle": "○",
        "hyphen": "⁃",
        "filled-square": "▪︎",
        "square": "▫︎",
        "triangular": "‣",
        "filled-diamond": "◆",
        "diamond": "◇",
    }

    ORDERED_MARKER_MAP: dict[MarkerType, dict[str, str]] = {
        "decimal": {
            "from": "1",
            "sep": ".",
        },
        "lower-alpha": {
            "from": "a",
            "sep": ".",
        },
        "upper-alpha": {
            "from": "A",
            "sep": ")",
        },
    }

    def __init__(
        self,
        items: list[str],
        style: TextStyle | None = None,
        marker_type: MarkerType | None = None,
        left_indent: int = 0,
        gap: Gap | None = None,
        margin: Margin | None = None,
    ) -> None:
        self.style = style if style is not None else TextStyle()
        self.marker_type: List.MarkerType = marker_type if marker_type is not None else "hyphen"
        self.gap = gap if gap is not None else Gap(1,0)
        self.left_indent = left_indent
        self.margin = margin if margin is not None else Margin(top=1, bottom=0)
        self.raw_style = str(EscapeCommand(
            self.style.background_color,
            self.style.color,
            self.style.font_style,
            self.style.font_weight,
            self.style.text_transform,
        ))
        self.items = items

        formatted = []
        formatted.extend([""] * self.margin.top)

        if self.marker_type in List.UNORDERED :
            self.marker = self._unordered_marker(self.marker_type)
            for item in self.items :
                formatted.append(f"{self.raw_style}{" " * self.left_indent}{self.marker}{" " * self.gap.horizontal}{item}{ANSI_RESET}")
                formatted.extend([""] * self.gap.vertical)

        elif self.marker_type in List.ORDERED :
            self.marker, self.sep = self._ordered_marker(self.marker_type)
        
            count = 0
            for i in range(ord(self.marker), ord(self.marker) + len(self.items)) :
                formatted.append(f"{self.raw_style}{" " * self.left_indent}{chr(i)}{self.sep}{" " * self.gap.horizontal}{self.items[count]}{ANSI_RESET}")
                formatted.extend([""] * self.gap.vertical)
                count += 1

        
        formatted.extend([""] * self.margin.bottom)
        

        super().__init__(formatted)


    def _unordered_marker (self, key: MarkerType) -> str :
        if key not in List.UNORDERED :
            return ""
        return self.UNORDERED_MARKER_MAP[key]
    
    def _ordered_marker (self, key: MarkerType) -> tuple[str, str] :
        if key not in List.ORDERED_MARKER_MAP :
            return "", ""
        
        return self.ORDERED_MARKER_MAP[key]["from"], self.ORDERED_MARKER_MAP[key]["sep"]
    
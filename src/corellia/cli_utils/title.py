from dataclasses import dataclass
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
    ANSI_RESET,
)

class Title (Payload) :

    TitleType = Literal["raw", "outlined", "filled"]

    def __init__(
        self,
        text: str,
        type: TitleType,
        style: TextStyle | None = None,
        padding: Padding | None = None,
        margin: Margin | None = None,
    ) -> None:
        self.text = text
        self.type = type
        self.style = style if style is not None else TextStyle()
        self.padding = padding if padding is not None else Padding(0, 0, 0, 0)
        self.margin = margin if margin is not None else Margin(top=1, bottom=0)
        self.raw_style = str(EscapeCommand(
            self.style.background_color,
            self.style.color,
            self.style.font_style,
            self.style.font_weight,
            self.style.text_transform,
        ))

        if self.type == "raw" :
            formatted = self.raw()
        elif self.type == "outlined" :
            formatted = self.outlined()
        elif self.type == "filled" :
            formatted = self.filled()
        else :
            formatted = []

        super().__init__(formatted)

    def raw (self) -> list[str]:
        width = self.padding.left + len(self.text) + self.padding.right
        padding_l = " " * self.padding.left
        padding_r = " " * self.padding.right
        return [
            *[""] * self.margin.top,
            f"{padding_l}{self.raw_style}{self.text}{padding_r}{ANSI_RESET}",
            *[""] * self.margin.bottom,
            "-" * width
        ]

    def outlined (self) -> list[str] :
        width = self.padding.left + len(self.text) + self.padding.right
        padding_l = f"{Border.V}{" " * self.padding.left}"
        padding_r = f"{" " * self.padding.right}{Border.V}"
        padding_t: list[str] = []
        for _ in range(self.padding.top) :
            padding_t.append(f"{Border.V}{" " * (width)}{Border.V}")
        padding_b: list[str] = []
        for _ in range(self.padding.bottom) :
            padding_b.append(f"{Border.V}{" " * (width)}{Border.V}")
                    
        return [
            *[""] * self.margin.top,                                                    # margin-top
            f"{Border.TL}{Border.H * (width)}{Border.TR}",                              # top-border
            *padding_t,                                                                 # padding-top
            f"{padding_l}{self.raw_style}{self.text}{padding_r}{ANSI_RESET}",           # text
            *padding_b,                                                                 # padding-bottom
            f"{Border.BL}{Border.H * (width)}{Border.BR}",                              # bottom-border
            *[""] * self.margin.bottom,                                                 # margin-bottom
        ]

    def filled (self) -> list[str] :
        self.raw_style = str(EscapeCommand(
            self.style.background_color,
            self.style.color,
            self.style.font_style,
            self.style.font_weight,
            TextTransform.REVERSE,
        ))
        width = self.padding.left + len(self.text) + self.padding.right
        padding_l = " " * self.padding.left
        padding_r = " " * self.padding.right
        padding_t = [f"{self.raw_style}{" " * width}{ANSI_RESET}" for _ in range(self.padding.top)]
        padding_b = [f"{self.raw_style}{" " * width}{ANSI_RESET}" for _ in range(self.padding.bottom)]
        return [
            *[""] * self.margin.top,
            *padding_t,
            f"{self.raw_style}{padding_l}{self.text}{padding_r}{ANSI_RESET}",
            *padding_b,
            *[""] * self.margin.bottom,    
        ]

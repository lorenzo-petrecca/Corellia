import sys

from corellia.cli_utils.style import EscapeCommand, TextStyle, ANSI_RESET
from corellia.cli_utils.output import Payload


class Text(Payload) :
    def __init__(self, *text: str, style: TextStyle | None = None) -> None:
        self.style = style if style is not None else TextStyle()
        self.text = list(text)

        formatted: list[str] = []
        style_raw = str(EscapeCommand(
            self.style.background_color,
            self.style.color,
            self.style.font_style,
            self.style.font_weight,
            self.style.text_transform,
        ))
        prefix = f"{self.style.prefix} " if len(self.style.prefix) > 0 else ""
        for i, line in enumerate(self.text) :
            current_prefix = prefix if i == 0 else ""
            if sys.stdout.isatty() :
                formatted.append(f"{style_raw}{current_prefix}{line}{ANSI_RESET}")
            else :
                formatted.append(f"{current_prefix}{line}")
        
        super().__init__(formatted)

    # def _to_payload (self) -> "Payload":
    #     formatted: list[str] = []
    #     style_raw = str(EscapeCommand(
    #         self.style.background_color,
    #         self.style.color,
    #         self.style.font_style,
    #         self.style.font_weight,
    #         self.style.text_transform,
    #     ))
    #     prefix = f"{self.style.prefix} " if len(self.style.prefix) > 0 else ""
    #     for i, line in enumerate(self.text) :
    #         current_prefix = prefix if i == 0 else ""
    #         if sys.stdout.isatty() :
    #             formatted.append(f"{style_raw}{current_prefix}{line}{ANSI_RESET}")
    #         else :
    #             formatted.append(f"{current_prefix}{line}")
        
    #     return Payload(*formatted)
    
    # def __call__(self, *text: str, style: TextStyle | None = None) -> "Payload":
    #   return self._to_payload()
import typer

from corellia.cli_utils.style import EscapeCommand, TextStyle



class Payload :
    def __init__(self, formatted: list[str]) -> None:
        self.formatted = list(formatted)

    def __call__(self) -> list[str]:
        return self.formatted



        

class Output :
    def __init__(self, *payload: Payload, ok: bool, exit_code: int) -> None:
        self.ok = ok
        self.exit_code = exit_code
        self.payload = list(payload)

    def _style_to_raw (self, style: TextStyle) -> str :
        return str(EscapeCommand(
            style.background_color,
            style.color,
            style.font_style,
            style.font_weight,
            style.text_transform,
        ))
    

    # def out (self) -> None:
    #     for t in self.payload :
    #         style_raw = self._style_to_raw(t.style)
    #         prefix = f"{t.style.prefix} " if len(t.style.prefix) > 0 else ""

    #         for i, line in enumerate(t.text) :
    #             current_prefix = prefix if i == 0 else ""
    #             if sys.stdout.isatty() :
    #                 typer.echo(f"{style_raw}{current_prefix}{line}{ANSI_RESET}")
    #             else:
    #                 typer.echo(f"{current_prefix}{line}")

    #     if self.exit_code != 0 :
    #         raise typer.Exit(code=self.exit_code)

    def out (self) -> None:
        for p in self.payload :
            for line in p() :
                typer.echo(line)

        if self.exit_code != 0 :
            raise typer.Exit(code=self.exit_code)
        
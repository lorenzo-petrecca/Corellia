from dataclasses import dataclass, field
from typing import Literal
from corellia.cli_utils.text import Text
from corellia.cli_utils.output import Payload
from corellia.cli_utils.style import (
    TextStyle, 
    FontWeight, 
    EscapeCommand, 
    TextTransform, 
    Margin,
    Padding,
    ANSI_RESET,
)
from corellia.cli_utils.borders import Border


Align = Literal['left', 'center', 'right']
ALIGN_MAP: dict[Align, str] = {
    "left": "<",
    "center": "^",
    "right": ">",
}

@dataclass
class RawTable :
    headers: list[str]
    body: list[list[str]] = field(default_factory=list)
    padding: Padding = field(default_factory=lambda: Padding(top=0, right=1, bottom=0, left=1))
    margin: Margin = field(default_factory=lambda: Margin(top=1, bottom=1))
    align: Align = "left"
    divider: str = "-"


    def _cell (self, row: list[str], col_n: int) -> str :
        """Ritorna la stringa della cella, altrimenti stringa vuota"""
        if col_n < len(row) :
            return str(row[col_n])
        return ""
    
    
    def _format_row_raw (self, row: list[str], col_widths: list[int]) -> str :
        cells = []
        align = ALIGN_MAP[self.align]
        for i in range(len(self.headers)) :
            left_pad = " " * self.padding.left
            width = col_widths[i] + self.padding.right
            value = self._cell(row, i)
            cells.append(f"{left_pad}{value:{align}{width}}")

        return "".join(cells)
    
    
    def _create_row (self, row: list[str], col_widths: list[int]) -> list[str] :
        rows = []
        for i in range(self.padding.top) :
            rows.append("")

        rows.append(self._format_row_raw(row, col_widths))

        for i in range(self.padding.bottom) :
            rows.append("")

        return rows

    
    def _header_line (self, col_widths: list[int]) -> list[str] :
        line = []
        total_w = 0
        for w in col_widths :
            total_w += self.padding.left + w + self.padding.right

        total_w //= max(len(self.divider), 1)

        for i in range(self.padding.top) :
            line.append("")

        line.append(self.divider * total_w)
    
        for i in range(self.padding.bottom) :
            line.append("")

        return line
    

    def _max_len_for_col (self, col_n: int) -> int :
        lengths = [len(str(self.headers[col_n]))]

        for row in self.body :
            lengths.append(len(self._cell(row, col_n)))
        
        return max(lengths)

    
    def to_text (self) -> list[str] :
        if not self.headers :
            return []
        
        # Creazione lista che contiene larghezza di ogni colonna 
        col_widths = [self._max_len_for_col(i) for i in range(len(self.headers))]

        # Creazione righe body tabella
        formatted_body = []
        for row in self.body :
            f_row = self._create_row(row, col_widths)
            for f in f_row :
                formatted_body.append(f)
        
        return [
            *["" for m in range(self.margin.top)],
            *self._create_row(self.headers, col_widths),
            *self._header_line(col_widths),
            *formatted_body,
            *["" for m in range(self.margin.bottom)],
        ]
    

    def to_payload (self) -> list[Text] :
        if not self.headers :
            return []
        
        # Creazione lista che contiene larghezza di ogni colonna 
        col_widths = [self._max_len_for_col(i) for i in range(len(self.headers))]

        # Creazione righe body tabella
        formatted_body = []
        for row in self.body :
            f_row = self._create_row(row, col_widths)
            for f in f_row :
                formatted_body.append(f)
        
        return [
            Text(
                *["" for m in range(self.margin.top)]
            ),
            Text(
                *self._create_row(self.headers, col_widths),
            ),
            Text(
                *self._header_line(col_widths),
            ),
            Text(
                *formatted_body,
            ),
            Text(
                *["" for m in range(self.margin.bottom)],
            ),
        ]

        
        



@dataclass
class CellPadding :
    left: int
    right: int


@dataclass
class Cell:
    value: str
    padding: CellPadding
    is_last: bool = False
    align: Align = "left"

    def render (self, width: int) -> str :
        alignment = ALIGN_MAP[self.align]
        padd_l = " " * self.padding.left
        padd_r = " " * self.padding.right
        end = Border.V if self.is_last else ""
        return f"{Border.V}{padd_l}{self.value:{alignment}{width}}{padd_r}{end}"
    
    def content_len (self) -> int :
        return len(self.value)

    

class Row :
    def __init__(
        self, 
        cells: list[str], 
        padding: CellPadding | None = None,
        cell_align: Align = "left",
    ) -> None:
        self.is_header = False
        self.cell_padding = padding if padding is not None else CellPadding(1, 1)
        self.cell_align: Align = cell_align
        self.cell_list = cells
        
        self.cells = [
            Cell(
                value=cell,
                padding=self.cell_padding,
                is_last=(i == len(self.cell_list) - 1),
                align=self.cell_align,
            )
            for i, cell in enumerate(self.cell_list)
        ]

        
    @property
    def num_cells (self) -> int:
        return len(self.cells)
    
    def normalized_values (self, num_cols: int) -> list[str] :
        empty = [""] * num_cols
        return (self.cell_list[:num_cols] + empty)[:num_cols]
    
    def render (self, col_widths: list[int]) -> str :
        cells = [
            Cell(
                value=value,
                padding=self.cell_padding,
                is_last=(i == len(col_widths) - 1),
                align=self.cell_align,
            )
            for i, value in enumerate(self.normalized_values(len(col_widths)))
        ]
        return "".join(cell.render(col_widths[i]) for i, cell in enumerate(cells))

    
    

class Table(Payload) :

    @dataclass
    class HeaderStyle :
        exists: bool = True
        bold: bool = True
        colorful: bool = False
        

    def __init__(
            self, 
            *rows: Row, 
            header_style: "Table.HeaderStyle | None" = None,
            margin: Margin | None = None, 
        ) -> None:
        self.rows = list(rows)
        self.header_style = header_style if header_style is not None else Table.HeaderStyle()
        self.margin = margin if margin is not None else Margin(top=1, bottom=1)
        
        self._setup_header()
        self.num_cols = self._get_num_cols()
        self.col_widths = self._get_col_widths()

        self.formatted = self._build_formatted()
        super().__init__(self.formatted)


    def _setup_header (self) -> None :
        if self.header_style.exists and self.rows :
            self.rows[0].is_header = True
    

    def _get_num_cols (self) -> int :
        if not self.rows :
            return 0
        return max(row.num_cells for row in self.rows)
    
    def _get_col_widths (self) -> list[int] :
        widths = [0] * self.num_cols

        for row in self.rows :
            values = row.normalized_values(self.num_cols)
            for i, value in enumerate(values) :
                widths[i] = max(widths[i], len(value))

        return widths
    

    def _horizontal_border (self, l: str, j: str, r: str) -> str :
        if self.num_cols == 0 :
            return ""
        
        parts = []
        for i, width in enumerate(self.col_widths) :
            cell_total = self.rows[i].cell_padding.left + width + self.rows[i].cell_padding.right
            parts.append(Border.H * cell_total)

        return l + j.join(parts) + r

    def _top_h_border (self) -> str :
        return self._horizontal_border(Border.TL, Border.TJ, Border.TR)
    
    def _middle_h_border (self) -> str :
        return self._horizontal_border(Border.LJ, Border.CROSS, Border.RJ)
    
    def _bottom_h_border (self) -> str :
        return self._horizontal_border(Border.BL, Border.BJ, Border.BR)

    
    def _build_formatted (self) -> list[str] :
        if not self.rows :
            return []
        
        lines: list[str] = []

        # Margin Top
        lines.extend([""] * self.margin.top)

        # Format Table
        for i, row in enumerate(self.rows) :
            style = TextStyle()
            if row.is_header :
                style = TextStyle(
                    font_weight=(FontWeight.BOLD if self.header_style.bold else FontWeight.REGULAR),
                    text_transform=(TextTransform.REVERSE if self.header_style.colorful else TextTransform.NONE),
                )
            
            style_raw = str(EscapeCommand(
                style.background_color,
                style.color,
                style.font_style,
                style.font_weight,
                style.text_transform,
            ))

            if i == 0 and row.is_header :
                lines.append(self._top_h_border())
            
            lines.append(f"{style_raw}{row.render(self.col_widths)}{ANSI_RESET}")
            
            if i == len(self.rows) - 1:
                lines.append(self._bottom_h_border())
            else :
                lines.append(self._middle_h_border())


        # Margin Bottom
        lines.extend([""] * self.margin.bottom)

        return lines


        

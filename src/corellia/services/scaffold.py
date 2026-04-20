from pathlib import Path
from importlib.resources import files

START_CODE_BLOCK = "#$START"
END_CODE_BLOCK = "#$END"

class ScaffoldService :
    @staticmethod
    def ensure_dir (path: Path) -> None :
        path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def write_file (path: Path, *content_rows: str, indentation: int = 0) -> None :
        path.parent.mkdir(parents=True, exist_ok=True)
        rows = list(content_rows)
        content: str = ""
        n_ind = 0
        for row in rows :
            n_ind += row.count(START_CODE_BLOCK)
            n_ind -= row.count(END_CODE_BLOCK)
            if row == START_CODE_BLOCK or row == END_CODE_BLOCK :
                continue
            row = row.replace(START_CODE_BLOCK, "")
            row = row.replace(END_CODE_BLOCK, "")
            if n_ind < 0 :
                n_ind = 0
            row_left_space = " " * indentation * n_ind
            content = "\n".join([content, row_left_space])
            content = "".join([content, row])
        
        path.write_text(content, encoding='utf-8')

    
    @staticmethod
    def touch (path: Path) -> None:
        path.write_text("", encoding="utf-8")

    
    @staticmethod
    def from_template (path: Path, template_name: str) :
        template = files("corellia.templates").joinpath(template_name)
        path.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")

        

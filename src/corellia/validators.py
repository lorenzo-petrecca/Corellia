import re
from typing import Any, Callable
import keyword

FieldValidator = Callable[[Any, str], list[str]]

class Validators :

    @staticmethod
    def regex (pattern: str, message: str) -> FieldValidator :
        compiled = re.compile(pattern)

        def validator (value: Any, field_name: str) -> list[str] :
            if not compiled.fullmatch(value) :
                return [f"{field_name} {message}"]
            
            return []
        
        return validator
    
    @staticmethod
    def allowed_values (values: set[str]) -> FieldValidator :
        def validator (value: Any, field_name: str) -> list[str] :
            if value not in values :
                allowed = ", ".join(sorted(values))
                return [f"{field_name} must be one of: {allowed}"]
            
            return []
        
        return validator
    
    @staticmethod
    def min_length (length: int) -> FieldValidator :
        def validator (value: Any, field_name: str) -> list[str] :
            if len(value) < length :
                return [f"{field_name} must contain at least {length} characters/items"]
            
            return []
        
        return validator
    
    @staticmethod
    def max_length (length: int) -> FieldValidator :
        def validator (value: Any, field_name: str) -> list[str] :
            if len(value) > length :
                return [f"{field_name} must contain at most {length} characters/items"]
            
            return []
        
        return validator


    @staticmethod
    def python_module_name () -> FieldValidator :
        def validator (value: Any, field_name: str) -> list[str] :
            if not isinstance(value, str) :
                return [f"{field_name} must be a string"]

            if (
                not value
                or not value.isascii()
                or not value.isidentifier()
                or keyword.iskeyword(value)
                or value != value.lower()
            ):
                return [
                    f"{field_name} must be a valid lowercase Python module name"
                ]

            return []

        return validator
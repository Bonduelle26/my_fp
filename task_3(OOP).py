import re
from abc import ABC, abstractmethod
from datetime import datetime, date
from typing import Optional, Any, Dict, List, Callable



class BaseParser(ABC):
    @abstractmethod
    def parse(self, value: str) -> Any:
        pass


class BaseValidator(ABC):
    @abstractmethod
    def validate(self, value: Any) -> bool:
        pass




class TextParser(BaseParser):
    def parse(self, value: str) -> Optional[str]:
        return value if value and len(value) > 0 else None


class IntParser(BaseParser):
    def parse(self, value: str) -> Optional[int]:
        value = value.strip()
        if len(value) == 0:
            return None

        negative_num = False
        if value[0] == '-':
            negative_num = True
            value = value[1:]

        if not value.isdigit():
            return None

        return -int(value) if negative_num else int(value)


class DateParser(BaseParser):
    def parse(self, value: str) -> Optional[str]:
        value = value.strip()
        pattern = r'^(\d{2})\.(\d{2})\.(\d{4})$'
        match = re.match(pattern, value)
        return value if match else None


          
class RequiredValidator(BaseValidator):
    def validate(self, value: Any) -> bool:
        return value is not None


class MinLengthValidator(BaseValidator):
    def __init__(self, min_length: int):
        self.min_length = min_length

    def validate(self, value: str) -> bool:
        return len(value) >= self.min_length if value is not None else True


class MaxLengthValidator(BaseValidator):
    def __init__(self, max_length: int):
        self.max_length = max_length

    def validate(self, value: str) -> bool:
        return len(value) <= self.max_length if value is not None else True


class MinValueValidator(BaseValidator):
    def __init__(self, min_value: int):
        self.min_value = min_value

    def validate(self, value: int) -> bool:
        return value >= self.min_value if value is not None else True


class MaxValueValidator(BaseValidator):
    def __init__(self, max_value: int):
        self.max_value = max_value

    def validate(self, value: int) -> bool:
        return value <= self.max_value if value is not None else True


class InPastValidator(BaseValidator):
    def validate(self, value: str) -> bool:
        try:
            input_date = datetime.strptime(value, "%d.%m.%Y").date()
            today = date.today()
            return input_date < today
        except (ValueError, TypeError):
            return False


class InFutureValidator(BaseValidator):
    def validate(self, value: str) -> bool:
        try:
            input_date = datetime.strptime(value, "%d.%m.%Y").date()
            today = date.today()
            return input_date >= today
        except (ValueError, TypeError):
            return False


class PhoneValidator(BaseValidator):
    def validate(self, value: str) -> bool:
        if not value:
            return False
        value = value.strip()
        pattern = r'^\+7\d{10}$'
        return bool(re.match(pattern, value))


class EmailValidator(BaseValidator):
    def validate(self, value: str) -> bool:
        if not value:
            return False
        value = value.strip()
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z]+\.[a-z]{2,}'
        return bool(re.match(pattern, value))



class ComposeValidator(BaseValidator):
    def __init__(self, *validators: BaseValidator):
        self.validators = validators

    def validate(self, value: Any) -> bool:
        return all(validator.validate(value) for validator in self.validators)


class FieldValidator(BaseValidator):
    def __init__(self, parser: BaseParser, validator: BaseValidator):
        self.parser = parser
        self.validator = validator

    def validate(self, value: str) -> bool:
        parsed = self.parser.parse(value)
        if parsed is None:
            return False
        return self.validator.validate(parsed)


class FormValidator(BaseValidator):
    def __init__(self, fields: Dict[str, BaseValidator]):
        self.fields = fields

    def validate(self, input_dict: Dict[str, str]) -> Dict[str, bool]:
        results = {}
        for field_name, field_validator in self.fields.items():
            field_value = input_dict.get(field_name, "")
            results[field_name] = field_validator.validate(field_value)
        return results


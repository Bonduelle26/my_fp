from string import digits
import re
from datetime import datetime, date


def parse_text(value: str):
    return value if len(value)>0 else None
    

def parse_int(value: str):
    value=value.strip()
    if len(value) == 0: return None

    if value[0] == '-':
        negative_num = True
        value=value[1:]
    else: 
        negative_num = False

    for letter in value:
        if letter not in digits: return None

    return -int(value) if negative_num else int(value)


def parse_date(value: str):
    value=value.strip()
    pattern=r'^(\d{2})\.(\d{2})\.(\d{4})$'
    match = re.match(pattern, value)
    return value if match else None

    
def required(value: str): 
    return value is not None


def min_length(min_length): 
    def validator(value):
        return len(value) >= min_length if value is not None else True

    return validator


def max_length(max_length): 
    def validator(value):
        return len(value) <= max_length if value is not None else True

    return validator


def min_value(min_value):
    def validator(value):
        return value >= min_value if value is not None else True

    return validator


def max_value(max_value):
    def validator(value):
        return value <= max_value if value is not None else True

    return validator


def in_past(value):
    try: 
        input_date = datetime.strptime(value, "%d.%m.%Y").date()
        today = date.today()
        return input_date < today

    except ValueError: 
        return None



def in_future(value):
    try: 
        input_date = datetime.strptime(value, "%d.%m.%Y").date()
        today = date.today()
        return input_date >= today

    except ValueError: 
        return None
  

def phone(value): 
    value = value.strip()
    pattern = r'^\+7\d{10}$'
    match = re.match(pattern, value)
    return True if match else False


def email(value): 
    value = value.strip()
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z]+\.[a-z]{2,}'
    match = re.match(pattern, value)
    return True if match else False


def compose(*validators):
    def validator(value):
        return all(f(value) for f in validators)

    return validator
  

def single_validator(parse, validate): 
    def validator(value):
        parsed = parse(value)
        if parsed is None:
            return False
        return validate(parsed)

    return validator


def multi_validator(fields):
    def validator(input_dict):
        results = {}
        for field_name, field_validator in fields.items():
            field_value = input_dict.get(field_name)
            results[field_name] = field_validator(field_value)
        
        return results
    return validator


form_fields = {
  "name": single_validator(
    parse_text, compose(required, max_length(100))
  ),
  "password": single_validator(
    parse_text, compose(required, min_length(8), max_length(40))
  ),
  "phone": single_validator(
    parse_text, phone
  ),
}
  
form_validator = multi_validator(form_fields)

input = {
  "name": "Ivanov Ivan",
  "password": "qwerty12",
  "phone": ""
}
print(form_validator(input))



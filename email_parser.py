import pandas as pd
import re
import datetime

patterns = {
    "title": r"Title [ .\w\d\-\+]*",
    "closing-date": r"Closing date [\w]{1,2}\/[\w]{1,2}\/[\w]{4} [\w]{1,2}\:[\w]{2}",
    "open-date": r"Open date [\w]{1,2}\/[\w]{1,2}\/[\w]{4}",
    "price-range": r"Price Range [\w\-\> ]*",
    "tender-number": r"AO[\d]*",
}

value_patterns = {
    "title": r"[ .\w\d\-\+]*",
    "closing-date": r"[\w]{1,2}\/[\w]{1,2}\/[\w]{4} [\w]{1,2}\:[\w]{2}",
    "open-date": r"[\w]{1,2}\/[\w]{1,2}\/[\w]{4}",
    "price-range": {"min-price": r"\>? *[\d]{2,}\-?", "max-price": r"\-[\d]{3,}"},
    "tender-number": r"AO[\d]*",
}


def parse_value_regex(pattern, field_value):
    compiled_pattern = re.compile(pattern)
    match = compiled_pattern.search(field_value)
    if match:
        return match.group(0)
    return None


def parse_value(field_name, field_value):
    if field_name in value_patterns:
        pattern = value_patterns[field_name]
    else:
        return field_value
    if isinstance(pattern, str):
        return {field_name: parse_value_regex(pattern, field_value)}
    elif isinstance(pattern, dict):
        parsed_values = {}
        for sub_key, sub_pattern in pattern.items():
            parsed_values[sub_key] = parse_value_regex(sub_pattern, field_value)
        return parsed_values


def convert_value(field_name, value):
    return {
        "title": lambda: value.replace("Title ", ""),
        "closing-date": lambda: datetime.datetime.strptime(value, r"%d/%m/%Y %H:%M"),
        "open-date": lambda: datetime.datetime.strptime(value, r"%d/%m/%Y"),
        "max-price": lambda: int(value.replace("-", "").strip()),
        "min-price": lambda: int(value.replace("-", "").replace(">", "").strip()),
        "tender-number": lambda: value,
    }.get(field_name, lambda: None)()


def parse_fields(message_body):
    values = {}
    for key, pattern in patterns.items():
        compiled_pattern = re.compile(pattern)
        match = compiled_pattern.search(message_body)
        if match:
            result_parsed_values = parse_value(key, match.group(0))
            if isinstance(result_parsed_values, str):
                values[key] = result_parsed_values
            elif isinstance(result_parsed_values, dict):
                for sub_key, sub_pattern in result_parsed_values.items():
                    values[sub_key] = sub_pattern
    convert_values = {}
    for field_name, value in values.items():
        if value:
            convert_values[field_name] = convert_value(field_name, value)
    return convert_values

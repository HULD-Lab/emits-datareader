import pandas as pd
import re
import datetime

patterns = {
    "Title": r"Title [ .\w\d\-\+]*",
    "Closing date": r"Closing date [\w]{1,2}\/[\w]{1,2}\/[\w]{4} [\w]{1,2}\:[\w]{2}",
    "Open date": r"Open date [\w]{1,2}\/[\w]{1,2}\/[\w]{4}",
    "Price range": r"Price Range [\w\- ]*",
    "Tender number": r"AO[\d]*",
}

value_patterns = {
    "Title": r"[ .\w\d\-\+]*",
    "Closing date": r"[\w]{1,2}\/[\w]{1,2}\/[\w]{4} [\w]{1,2}\:[\w]{2}",
    "Open date": r"[\w]{1,2}\/[\w]{1,2}\/[\w]{4}",
    "Price range": {"Min price": r"[\d]*\-", "Max price": r"\-[\d]*"},
    "Tender number": r"AO[\d]*",
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
        "Title": lambda: value.replace("Title ",""),
        "Closing date": lambda: datetime.datetime.strptime(value, r"%d/%m/%Y %H:%M"),
        "Open date": lambda: datetime.datetime.strptime(value, r"%d/%m/%Y").date(),
        "Max price": lambda: int(value.replace("-", "")),
        "Min price": lambda: int(value.replace("-", "")),
        "Tender number": lambda: value,
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
        convert_values[field_name] = convert_value(field_name, value)
    return convert_values
import re
import datetime

patterns = {
    "title": r"Title [ .\w\d\-\+]*",
    "closing-date": r"Closing date [\w]{1,2}\/[\w]{1,2}\/[\w]{4} [\w]{1,2}\:[\w]{2}",
    "open-date": r"Open date [\w]{1,2}\/[\w]{1,2}\/[\w]{4}",
    "price-range": r"Price Range [\w\-\> ]*",
    "tender-number": r"AO[\d]*",
    "spec-prov": r"Special Prov\. [\w{2}\+?]*",
    "products": r"Products [\w \&\/\\\s;]*Technology[ ]{1,2}Domains",
    "technology-domains": r"Technology[ ]{1,2}Domains[\w \&\/\\\s\,\;\-]*Establishment",
    "tender-type": r"Tender Type [\w]*",
    "esthablishment": r"Establishment [\w]*",
}

value_patterns = {
    "title": r".*",
    "closing-date": r"[\w]{1,2}\/[\w]{1,2}\/[\w]{4} [\w]{1,2}\:[\w]{2}",
    "open-date": r"[\w]{1,2}\/[\w]{1,2}\/[\w]{4}",
    "price-range": {"min-price": r"\>? *[\d]{2,}\-?", "max-price": r"\-[\d]{3,}"},
    "tender-number": r"AO[\d]*",
    "spec-prov": r"([A-Z]{2}\+?)+",
    "products": r".*",
    "technology-domains": r".*",
    "esthablishment": r".*",
}


def parse_value_regex(pattern, field_value):
    compiled_pattern = re.compile(pattern, re.MULTILINE)
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
        "title": lambda: value.replace("Title ", "").strip(),
        "closing-date": lambda: datetime.datetime.strptime(value, r"%d/%m/%Y %H:%M"),
        "open-date": lambda: datetime.datetime.strptime(value, r"%d/%m/%Y"),
        "max-price": lambda: int(value.replace("-", "").strip()),
        "min-price": lambda: int(value.replace("-", "").replace(">", "").strip()),
        "tender-number": lambda: value,
        "spec-prov": lambda: value.split("+"),
        "products": lambda: list(
            map(
                str.strip,
                value.replace("Products", "")
                .replace("Technology  Domains", "")
                .split("/"),
            )
        ),
        "technology-domains": lambda: list(
            map(
                str.strip,
                value.replace("Establishment", "")
                .replace("Technology  Domains", "")
                .replace(";", "/")
                .split("/"),
            )
        ),
        "tender-type": lambda: value.replace("Tender Type", "").strip(),
        "esthablishment": lambda: value.replace("Establishment", "").strip(),
    }.get(field_name, lambda: None)()


def calculate_max_price():
    """Calculcates the max price if is not set. The algorithm has not been specified yet.
    
    Returns:
        int -- the calculated max price
    """
    #Experimental implementation
    return 9999


def calculate_min_price():
    """Calculcates the min price if is not set. The algorithm has not been specified yet.
    
    Returns:
        int -- the calculated min price
    """
    #Experimental implementation
    return 0

def find_description(message_body):
    lines = message_body.split("\n")
    empty_count = 0
    start_search = False
    stop_adding = False
    description = ""
    for line in lines:
        if "Last Update Date" in line:
            start_search = True
        if start_search and len(line.strip()) == 0:
            empty_count += 1
        if empty_count > 3:
            stop_adding = True
        if empty_count > 0 and start_search and not stop_adding:
            description += line.strip() + " "
    return description.strip()


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
    if "max-price" not in convert_values:
        convert_values["max-price"] = calculate_max_price()
    if "min-price" not in convert_values:
        convert_values["min-price"] = calculate_min_price()
    convert_values["description"] = find_description(message_body)
    return convert_values

import json
from termcolor import colored
from pygments import highlight, lexers, formatters


def get_label(log_method: str):
    lm_upper = log_method.upper()
    on_color = "on_white" if lm_upper == "CRITICAL" else None
    colors = {
        "INFO": "green",
        "DEBUG": "cyan",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red",
    }
    return colored(lm_upper, colors[lm_upper], on_color)


def pretty_print_json(logger, log_method: str, event_dict):
    formatted_json = json.dumps(event_dict, indent=4, sort_keys=True)
    colorful_json = highlight(
        formatted_json,
        lexers.JsonLexer(),
        formatters.TerminalFormatter(),
    )
    return str.encode(colorful_json)


def filter_event(event_dict):
    non_required_for_dev = [
        "event",
        "level",
        "method",
        "request_id",
        "url",
        "timestamp",
    ]

    for key in non_required_for_dev:
        if key in event_dict:
            del event_dict[key]

    return event_dict


def pretty_print_for_dev(logger, log_method: str, event_dict):
    label = get_label(log_method)
    primary = f"{label}:     {event_dict['event']}"
    secondary = ""

    filtered_event = filter_event(event_dict)
    if len(filtered_event):
        formatted_json = json.dumps(filtered_event, sort_keys=True)
        colored_event = highlight(
            formatted_json,
            lexers.JsonLexer(),
            formatters.TerminalFormatter(),
        )
        secondary = f"{colored_event or ''}"

    text = f"{primary}        {secondary}"
    encoded = str.encode(text)

    return encoded

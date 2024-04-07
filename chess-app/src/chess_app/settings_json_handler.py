from json import load


def dfs(node, path=''):
    result = ''
    if isinstance(node, dict):
        for key, value in node.items():
            result += f'<h1>{key}</h1>'
            if isinstance(value, dict):
                result += dfs(value, f'{path}.{key}')
            else:
                try:
                    if isinstance(node, str):
                        dfs(load(node), path)
                    else:
                        raise TypeError()
                except TypeError:
                    result += handle_value(value, path, key)
    return result


def handle_value(value, path, key):
    result = ''
    if isinstance(value, bool):
        result += handle_boolean(value, path, key)
    elif isinstance(value, (int, float)):
        result += handle_number(value, path, key)
    elif isinstance(value, str):
        result += handle_string(value, path, key)
    elif isinstance(value, (list, tuple)):
        if all(isinstance(item, str) for item in value):
            result += handle_iterable_string(value, path, key)
        elif all(isinstance(item, (list, tuple)) and all(isinstance(sub_item, str) for sub_item in item) for item in
                 value):
            result += handle_iterable_iterable_string(value, path, key)
        elif all(isinstance(item, (int, float)) for item in value):
            result += handle_iterable_number(value, path, key)
        elif all(isinstance(item, bool) for item in value):
            result += handle_iterable_boolean(value, path, key)
        else:
            # Generic iterable handling
            pass
    return result


def handle_boolean(value, path, key):
    # Boolean handling
    return f'<p>{key}: {value}</p>'


def handle_number(value, path, key):
    # Number handling
    return f'<p>{key}: {value}</p>'


def handle_string(value, path, key):
    json_value = parse_json(value)
    if json_value:
        # Recursively handle JSON string
        return dfs(json_value, path + '.' + key)
    else:
        # String handling
        return f'<p>{key}: {value}</p>'


def handle_iterable_string(value, path, key):
    # Iterable of strings handling
    return f'<p>{key}: {", ".join(value)}</p>'


def handle_iterable_iterable_string(value, path, key):
    # Iterable of iterables of strings handling
    result = f'<p>{key}:</p>'
    for idx, item in enumerate(value):
        result += f'<p>Item {idx + 1}: {", ".join(item)}</p>'
    return result


def handle_iterable_number(value, path, key):
    # Iterable of numbers handling
    result = f'<p>{key}:</p>'
    for idx, item in enumerate(value):
        result += f'<p>Item {idx + 1}: {item}</p>'
    return result


def handle_iterable_boolean(value, path, key):
    # Iterable of booleans handling
    result = f'<p>{key}:</p>'
    for idx, item in enumerate(value):
        result += f'<p>Item {idx + 1}: {item}</p>'
    return result

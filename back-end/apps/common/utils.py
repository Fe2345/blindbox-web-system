import re


def snake_to_camel(name: str) -> str:
    """snake_case -> camelCase"""
    parts = name.split("_")
    return parts[0] + "".join(w.capitalize() for w in parts[1:])


def camel_to_snake(name: str) -> str:
    """camelCase -> snake_case"""
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name).lower()


def keys_to_camel(data):
    """递归将 dict 的 key 从 snake_case 转为 camelCase"""
    if isinstance(data, dict):
        return {snake_to_camel(k): keys_to_camel(v) for k, v in data.items()}
    if isinstance(data, list):
        return [keys_to_camel(item) for item in data]
    return data


def keys_to_snake(data):
    """递归将 dict 的 key 从 camelCase 转为 snake_case"""
    if isinstance(data, dict):
        return {camel_to_snake(k): keys_to_snake(v) for k, v in data.items()}
    if isinstance(data, list):
        return [keys_to_snake(item) for item in data]
    return data

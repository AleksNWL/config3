import re


def parse_config(config_text):
    lines = config_text.strip().splitlines()
    parsed_config = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue

        const_decl = re.match(r"(\w+)\s*->\s*(\w+);", line)
        if const_decl:
            const_name = const_decl.group(1)
            const_value = const_decl.group(2)
            parsed_config[const_name] = const_value
            continue

        const_expr = re.match(r"\^{(\w+)}", line)
        if const_expr:
            const_name = const_expr.group(1)
            if const_name in parsed_config:
                continue
            else:
                raise SyntaxError(f"Undefined constant {const_name}")

        dict_match = re.match(r"(\w+)\s*=\s*\[([^\]]+)\];", line)
        if dict_match:
            dict_name = dict_match.group(1)
            dict_content = dict_match.group(2).strip()
            parsed_dict = parse_dict_content(dict_content, parsed_config)
            parsed_config[dict_name] = parsed_dict
            continue

        if '->' in line:
            key, value = line.split('->')
            key = key.strip()
            value = value.strip().strip(';')

            if ':' in value or '/' in value or '@' in value:
                value_parts = re.split(r'(:|/@)', value)
                resolved_parts = []
                for part in value_parts:
                    if part in [":", "/", "@"]:
                        resolved_parts.append(part)
                    elif part.startswith('^'):
                        const_name = part[1:]
                        if const_name in parsed_config:
                            resolved_parts.append(parsed_config[const_name])
                        else:
                            raise SyntaxError(f"Undefined constant {const_name}")
                    else:
                        resolved_parts.append(part)
                parsed_config[key] = ''.join(resolved_parts)
            else:
                if value.startswith('^'):
                    const_name = value[1:]
                    if const_name in parsed_config:
                        parsed_config[key] = parsed_config[const_name]
                    else:
                        raise SyntaxError(f"Undefined constant {const_name}")
                else:
                    parsed_config[key] = value
            continue

        raise SyntaxError(f"Invalid syntax: {line}")

    resolved_config = resolve_constants(parsed_config)

    return resolved_config


def resolve_constants(parsed_config):
    resolved_config = {}
    for key, value in parsed_config.items():
        if isinstance(value, str) and value.startswith('^'):
            const_name = value[1:]
            if const_name in parsed_config:
                resolved_config[key] = parsed_config[const_name]
            else:
                raise SyntaxError(f"Undefined constant {const_name}")
        else:
            resolved_config[key] = value
    return resolved_config


def parse_dict_content(content, parsed_config):
    items = content.split(",")
    parsed_dict = {}
    for item in items:
        item = item.strip()
        if not item:
            continue
        key_value = item.split(":")
        if len(key_value) != 2:
            raise SyntaxError(f"Invalid key-value pair: {item}")
        key = key_value[0].strip()
        value = key_value[1].strip()

        if value.startswith("^"):
            const_name = value[1:]
            if const_name in parsed_config:
                parsed_dict[key] = parsed_config[const_name]
            else:
                raise SyntaxError(f"Undefined constant {const_name}")
        elif value.isdigit():
            parsed_dict[key] = int(value)
        elif value.startswith("[") and value.endswith("]"):
            parsed_dict[key] = parse_dict_content(value[1:-1], parsed_config)
        else:
            parsed_dict[key] = value
    return parsed_dict

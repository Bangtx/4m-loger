def json_build_object(*args):
    pairs = []
    for i in range(0, len(args), 2):
        key = args[i]
        value = args[i + 1]
        pairs.append(f'"{key}": "{value}"')
    return '{' + ', '.join(pairs) + '}'
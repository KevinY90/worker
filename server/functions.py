from collections import defaultdict


def get_path_to_target_value(path, obj):
    if not path:
        return obj
    key = path.pop()
    is_array = key.split('=')
    if len(is_array) > 1:
        key, target = is_array[0], is_array[1]
        for item in obj:
            if item[key] == target:
                return get_path_to_target_value(path, item)
    return get_path_to_target_value(path, obj[key])


def create_parser(fields):
    fields = fields.split(',')
    targeted_fields = {}
    for item in fields:
        field, *func_args = item.split('-')
        fn_name, *args = func_args
        targeted_fields[field] = (function_map[fn_name], args)

    def parser(response):
        results = []
        for target, (fn, args) in targeted_fields.items():
            path = target.split('.')
            path.reverse()
            val = get_path_to_target_value(path, response)
            function_results = fn(val, *args)
            if function_results:
                results.append((target, fn.__name__, val))
        return results
    return parser


def percent(response_val, amount, percent):
    return int(response_val) * int(percent) > int(amount)


def less_than(response_val, value):
    return int(response_val) < int(value)


def greater_than(response_val, value):
    return int(response_val) > int(value)


def equals(response_val, value):
    return response_val == value


def did_update(response_val, previous):
    return response_val != previous


def notify():
    return True


function_map = {
    'percent': percent,
    'less_than': less_than,
    'greater_than': greater_than,
    'equals': equals,
    'did_update': did_update,
    'notify': notify,
}

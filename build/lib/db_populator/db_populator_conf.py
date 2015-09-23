import importlib

from django.conf import settings

def str_to_class(s):

    modules = s.split(".")
    concrete = modules[-1]
    modules = ".".join(modules[:-1])

    mod = importlib.import_module(modules)
    return getattr(mod, concrete)

def concrete_list(l):
    return list(map(str_to_class, l))

def unpack_requirements(reqs):
    return list(map(concrete_nested_dict, reqs))

def concrete_nested_dict(d):
    if not isinstance(d, dict):
        return d

    for key in d.keys():
        if isinstance(key, str) and "." in key and not key.startswith(".") and not key.endswith("."):
            # then we assume it is a submoduled class
            concrete_key = str_to_class(key)
            d[concrete_key] = d.pop(key)

    for key in d.keys():
        if isinstance(d[key], dict):
            d[key] = concrete_nested_dict(d[key])

    return d

IGNORE = concrete_list(settings.DB_POPULATOR_IGNORE)

ALLOW_MULTIPLE = concrete_list(settings.DB_POPULATOR_ALLOW_MULTIPLE)

REQUIREMENTS = unpack_requirements(settings.DB_POPULATOR_REQUIREMENTS)

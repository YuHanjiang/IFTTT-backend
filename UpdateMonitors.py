import glob
import re
import importlib

monitors = {}


def read_filenames():
    names = glob.glob('Monitors/*.py')
    return names


def import_monitors():
    regex = 'Monitors/(.*).py'
    for name in read_filenames():
        module_search = re.search(regex, name)
        if module_search is not None:
            module_name = module_search.group(1)
            module = importlib.import_module('.' + module_name, 'Monitors')
            monitors[module_name] = module


def update_api_list():
    # @ todo
    return None


def __main__():
    import_monitors()
    update_api_list()


__main__()

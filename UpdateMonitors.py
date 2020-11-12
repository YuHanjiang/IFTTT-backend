import glob
import re
import mysql.connector
import importlib 
import json

monitors = {}


def read_filenames():
    names = glob.glob('Monitors/*.py')
    return names


def import_monitors():
    regex = '^Monitors[/|\\\\](.*).py$'
    for name in read_filenames():
        module_search = re.search(regex, name)
        if module_search is not None:
            module_name = module_search.group(1)
            module = importlib.import_module('.' + module_name, 'Monitors')
            monitors[module_name] = module


def update_api_list(): 
    with open("DatabaseConfig.json") as file: 
        fileDic = json.load(file)
        db = mysql.connector.connect(
            host=fileDic["host"],
            user=fileDic["user"],
            password=fileDic["pwd"],
            database=fileDic["db"]
        )

    cursor = db.cursor()

    for monitor_name in monitors.keys():
        vars_string = ''
        for var in monitors[monitor_name].monitor_var:
            if vars_string == '':
                vars_string += var
            else:
                vars_string = vars_string + ',' + var
        cursor.execute("INSERT IGNORE INTO monitors VALUES(%s, %s)", (monitor_name, vars_string))

    db.commit()


def update_monitors():
    import_monitors()
    update_api_list()

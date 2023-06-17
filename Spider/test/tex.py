import pkgutil
import inspect
import sys
def get_imported_libraries():
    imported_libraries = set()
    for module_name in list(sys.modules.keys()):
        if module_name not in sys.builtin_module_names:
            imported_libraries.add(module_name.split('.')[0])
    return imported_libraries

def get_required_libraries():
    caller_frame = inspect.currentframe().f_back
    required_libraries = set()
    for name, val in caller_frame.f_globals.items():
        if inspect.ismodule(val):
            required_libraries.add(name)
    return required_libraries

imported_libraries = get_imported_libraries()
required_libraries = get_required_libraries()
print(imported_libraries)
print(required_libraries)
missing_libraries = required_libraries - imported_libraries
print("Missing libraries:", missing_libraries)

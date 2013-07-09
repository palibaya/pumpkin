import importlib
def get_obj(class_name, args):
    module_path, c_class_str = class_name.rsplit('.', 1)
    module = importlib.import_module(module_path)
    c_class = getattr(module, c_class_str)
    return c_class(*args)


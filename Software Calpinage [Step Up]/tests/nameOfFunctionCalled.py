import inspect

class PrintColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def show_function_name(func=None,color="OKGREEN",output=False, arg_name=None):
    def decorator(func):
        color_code = getattr(PrintColors, color.upper(), "")
        end_code = PrintColors.ENDC
        def wrapper(*args, **kwargs):
            print(f"{color_code}Executing function: {func.__name__}{end_code}")        
            return func(*args, **kwargs)
        return wrapper
    if func is None:
        return decorator
    else:
        return decorator(func)
"""

def show_function_name(func=None, color="OKGREEN", output=False, arg_name=None):
    def decorator(func):
        color_code = getattr(PrintColors, color.upper(), "")
        end_code = PrintColors.ENDC

        def get_arg_name(args, kwargs):
            # Récupérer les noms des paramètres de la fonction décorée
            func_args = func.__code__.co_varnames[1:len(args)+1]

            # Vérifier si l'argument a été passé en tant qu'argument positionnel
            if arg_name in func_args:
                index = func_args.index(arg_name)
                return arg_name, args[index]

            # Vérifier si l'argument a été passé en tant qu'argument nommé
            if arg_name in kwargs:
                return arg_name, kwargs[arg_name]

            return None, None

        def wrapper(*args, **kwargs):
            real_arg_name, real_arg_value = get_arg_name(args, kwargs)

            if output and real_arg_name is not None:
                print(f"{color_code}Executing function: {func.__name__}, {real_arg_name} = {real_arg_value}{end_code}")
            else:
                print(f"{color_code}Executing function: {func.__name__}{end_code}")
            return func(*args, **kwargs)

        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)
        """
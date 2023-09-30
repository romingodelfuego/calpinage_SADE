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

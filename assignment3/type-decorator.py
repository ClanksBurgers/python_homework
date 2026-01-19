#Task 2

def type_converter(type_of_output):
    def decorator(func):
        def wrapper(*args, **kwargs):
            x = func(*args, **kwargs)
            return type_of_output(x)
        return wrapper
    return decorator

@type_converter(str)
def returns_integer():
    return 42

@type_converter(int)
def return_string():
    return "Numbers"

if __name__ == "__main__":
    y = returns_integer()
    print(type(y).__name__)

    try:
        y = return_string()
        print("shouldn't get here")
    except ValueError:
        print("can't convert to int") 

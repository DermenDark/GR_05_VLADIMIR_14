# ================== VALIDATION DECORATOR ==================
def validate_input_num(check_func, error_message):
    def decorator(func):


        
        def wrapper():
            while True:
                try:
                    value = func()
                    if not check_func(value):
                        print(error_message)
                        continue
                    return value
                except ValueError:
                    print("Input is not/not a valid number.")
        return wrapper
    return decorator
from functools import wraps

def pw_trace(step_name):
    def decorator(func):
        @wraps(func)  
        def wrapper(*args, **kwargs):
            logged_in_page = kwargs.get('logged_in_page') or (args[0] if args else None)
            
            if logged_in_page:
                logged_in_page.context.tracing.group(step_name)
            try:
                return func(*args, **kwargs)  
            finally:
                if logged_in_page:
                    logged_in_page.context.tracing.group_end()
        return wrapper
    return decorator
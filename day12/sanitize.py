import bleach

def clean_text(value):
    if not isinstance(value, str):
        return value
    return bleach.clean(value, tags=[], strip=True)
import difflib


def get_diff(old, new):
    if not old:
        return new
    d = difflib.unified_diff(
        old.splitlines(), new.splitlines(), lineterm=""
    )
    return "\n".join(d)

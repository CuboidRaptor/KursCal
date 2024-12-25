import sys

class Error:
    def __init__(self, e: str, msg: str):
        self.e = e
        self.msg = msg
        self.string = f"{e}: {msg}"

def err(e: str, msg: str) -> Error:
    error = Error(e, msg)
    _ = sys.stderr.write(f"{error.string}\n")

    return error
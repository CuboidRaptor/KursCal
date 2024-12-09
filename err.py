import sys

class Error:
    def __init__(self, e: str, msg: str):
        self.e: str = e
        self.msg: str = msg

def err(e: str, msg: str) -> Error:
    _ = sys.stderr.write(f"{e}: {msg}\n")

    return Error(e, msg)
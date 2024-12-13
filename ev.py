import op
import err

from collections import deque
from decimal import Decimal, InvalidOperation, getcontext

getcontext().prec = 15

def format_stack(stack: deque[Decimal]) -> str:
    formatted_strings = [format(i, "f") for i in stack]
    joined = ", ".join(formatted_strings)

    return f"[{joined}]"

def ev(s: str) -> deque[Decimal] | err.Error:
    stack: deque[Decimal] = deque()
    tokens = s.replace("\n", " ").split() # replace newlines with spaces so blocks of text work

    for token in tokens:
        try:
            stack.append(Decimal(token))
            continue

        except InvalidOperation:
            # (from decimal library)
            pass

        error = op.handle(stack, token)

        if error: # error!
            return error
        
    return stack
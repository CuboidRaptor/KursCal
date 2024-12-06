import op

from collections import deque
from decimal import Decimal, InvalidOperation, getcontext

getcontext().prec = 15
gstack: deque[Decimal] = deque()

def format_stack(stack: deque[Decimal]) -> str:
    formatted_strings: list[str] = list(map(lambda x: format(x, "f"), stack))
    joined = ", ".join(formatted_strings)

    return f"[{joined}]"

def ev(s: str) -> None:
    global gstack
    tokens = s.split()
    op_stack: deque[Decimal] = deque()

    for token in tokens:
        try:
            op_stack.append(Decimal(token))
            continue

        except InvalidOperation:
            # (from decimal library)
            pass

        error = op.handle(gstack, op_stack, token)

        if error: # error!
            return
        
    gstack.extend(op_stack)
    print(f"op_stack: {format_stack(op_stack)}")
    print(f"gstack: {format_stack(gstack)}")
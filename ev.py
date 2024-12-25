import err
import math

from collections import deque
from decimal import Decimal, InvalidOperation, getcontext

getcontext().prec = 15
def trypop(stack: deque[Decimal], token: str, index: int=-1) -> Decimal | err.Error:
    try:
        return stack.pop()

    except IndexError:
        return err.err("StackError", f"Not enough items on the stack at operator \"{token}\"")

# dictionary for operations
# "op_name": (number_of_numbers_needed_from_stack, lambda stack, *args: ...)
# operations like stack popping a specific index will have stack_nums=0
def prec(stack, *args):
    # man, python anon funcs suck....
    getcontext().prec = math.floor(args[0])

OPS = {
    "sd": (0, lambda stack: stack.clear()),
    "prec": (1, prec), # function defined previously because inline doesn't support assignment
    "sqrt": (1, lambda stack, *args: stack.append(args[0].sqrt())),
    "log10": (1, lambda stack, *args: stack.append(args[0].log10())),
    "ln": (1, lambda stack, *args: stack.append(args[0].ln())),
    "+": (2, lambda stack, *args: stack.append(args[1] + args[0])),
    "-": (2, lambda stack, *args: stack.append(args[1] - args[0])),
    "*": (2, lambda stack, *args: stack.append(args[1] * args[0])),
    "/": (2, lambda stack, *args: stack.append(args[1] / args[0])),
    "**": (2, lambda stack, *args: stack.append(args[1] ** args[0])),
    "rt": (2, lambda stack, *args: stack.append(args[0] ** (1 / args[1]))),
    "log": (2, lambda stack, *args: stack.append(args[0].log10() / args[1].log10())),
}

def handle(stack: deque[Decimal], token: str) -> None | err.Error:
    global OPS
    try:
        pops: list[Decimal] = []

        for i in range(0, OPS[token][0]):
            popped = trypop(stack, token)

            if isinstance(popped, err.Error):
                return popped

            else:
                pops.append(popped)

        OPS[token][1](stack, *pops)

    except KeyError:
        return err.err("OperatorError", f"Unknown Operator \"{token}\"")

def format_stack(stack: deque[Decimal]) -> str:
    formatted_strings = [format(i, "f") for i in stack]
    joined = "\n".join(formatted_strings)

    return joined

def ev(s: str) -> deque[Decimal] | err.Error:
    stack: deque[Decimal] = deque()
    tokens = s.replace("\n", " ").split() # replace newlines with spaces so blocks of text work

    for token in tokens:
        try:
            stack.append(Decimal(token))
            continue

        except InvalidOperation: # (from decimal library)
            # not a number
            error = handle(stack, token)

            if isinstance(error, err.Error): # error!
                return error
        
    return stack
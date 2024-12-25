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

def handle(stack: deque[Decimal], token: str) -> None | err.Error:
    # commands, i.e. zeronary operators
    if token == "sd":
        # stack delete
        # deletes stack
        stack.clear()

    else:
        # not zeronary operator
        pop1: Decimal | err.Error = trypop(stack, token) # first pop for unary operators
        if isinstance(pop1, err.Error):
            return pop1

        if token == "prec":
            getcontext().prec = math.floor(pop1)

        elif token == "sqrt":
            stack.append(pop1.sqrt())

        elif token == "log10":
            stack.append(pop1.log10())

        elif token == "ln":
            stack.append(pop1.ln())

        else:
            # not unary operator
            pop2: Decimal | err.Error = trypop(stack, token) # pop again for binary operators
            if isinstance(pop2, err.Error):
                return pop2

            if token == "+":
                stack.append(pop2 + pop1)

            elif token == "-":
                stack.append(pop2 - pop1)

            elif token == "*":
                stack.append(pop2 * pop1)

            elif token == "/":
                stack.append(pop2 / pop1)

            elif token == "**":
                stack.append(pop2 ** pop1)

            elif token == "rt":
                stack.append(pop2 ** (1 / pop1))

            elif token == "log":
                stack.append(pop1.log10() / pop2.log10())

            else:
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

        except InvalidOperation:
            # (from decimal library)
            pass

        error = handle(stack, token)

        if error is not None: # error!
            return error
        
    return stack
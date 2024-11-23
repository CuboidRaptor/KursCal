import math
import err

from typing import Callable
from collections import deque
from decimal import Decimal, getcontext

def repeat(op: Callable[[Decimal, Decimal], Decimal], *args: Decimal):
    # runs binary operator op for every arg left to right
    out = args[0]

    for i in args[1:]:
        out = op(out, i)

    return out

def trypop(stack: deque[Decimal], token: str, index: int=-1) -> Decimal | err.Error:
    try:
        return stack.pop()

    except IndexError:
        return err.err("StackError", f"Not enough items on the stack at operator \"{token}\"")

def handle(gstack: deque[Decimal], op_stack: deque[Decimal], token: str) -> None | err.Error:
    # commands, i.e. zeronary operators
    if token == "sc":
        # stack copy
        # append gstack to opstack
        op_stack.extend(gstack)

    elif token == "sd":
        # stack delete
        # deletes both stacks
        gstack.clear()
        op_stack.clear()

    elif token == "sp":
        # stack pop
        # pops from gstack to opstack
        popped: Decimal | err.Error = trypop(gstack, token)
        if isinstance(popped, err.Error):
            return popped

        op_stack.append(popped)

    else:
        # not zeronary operator
        pop1: Decimal | err.Error = trypop(op_stack, token) # first pop for unary operators
        if isinstance(pop1, err.Error):
            return pop1

        if token == "prec":
            getcontext().prec = math.floor(pop1)

        elif token == "sqrt":
            op_stack.append(pop1.sqrt())

        elif token == "log10":
            op_stack.append(pop1.log10())

        elif token == "ln":
            op_stack.append(pop1.ln())

        else:
            # not unary operator
            pop2: Decimal | err.Error = trypop(op_stack, token) # pop again for binary operators
            if isinstance(pop2, err.Error):
                return pop2

            if token == "+":
                op_stack.append(pop2 + pop1)

            elif token == "-":
                op_stack.append(pop2 - pop1)

            elif token == "*":
                op_stack.append(pop2 * pop1)

            elif token == "/":
                op_stack.append(pop2 / pop1)

            elif token == "**":
                op_stack.append(pop2 ** pop1)

            elif token == "rt":
                op_stack.append(pop2 ** (1 / pop1))

            elif token == "log":
                op_stack.append(pop1.log10() / pop2.log10())

            else:
                return err.err("OperatorError", f"Unknown Operator \"{token}\"")
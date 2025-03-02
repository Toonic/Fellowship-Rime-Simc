"""Module for parsing SimFell condition lines."""

from typing import Any, Optional
import operator
import re

from base import BaseSpell, BaseCharacter
from simfell_parser.model import Condition


class SimFileConditionParser:
    """Class for parsing SimFell condition lines."""

    possible_operators = {
        "==": operator.eq,
        "!=": operator.ne,
        ">": operator.gt,
        ">=": operator.ge,
        "<": operator.lt,
        "<=": operator.le,
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        "and": lambda x, y: x and y,
        "or": lambda x, y: x or y,
        "not": lambda x: not x,
        "xor": lambda x, y: bool(x) ^ bool(y),
    }

    def __init__(self, condition: str):
        self._condition = condition

    def convert(self, value: str) -> Any:
        """Convert a value to a Python object."""

        if value.isdigit():
            return int(value)

        if value.lower() == "true":
            return True

        if value.lower() == "false":
            return False

        return value

    def parse_expression(self, expression: str) -> Any:
        """Parse and evaluate a complex expression."""

        # Tokenize the expression
        tokens = re.split(r"(\s+|\b|\(|\))", expression)
        stack = []

        for token in tokens:
            token = token.strip()
            if not token:
                continue

            if token.isdigit():
                stack.append(int(token))
            elif token in SimFileConditionParser.possible_operators:
                if token == "not":
                    operand = stack.pop()
                    result = SimFileConditionParser.possible_operators[token](
                        operand
                    )
                else:
                    right = stack.pop()
                    left = stack.pop()
                    result = SimFileConditionParser.possible_operators[token](
                        left, right
                    )
                stack.append(result)
            elif token.lower() in ["true", "false"]:
                stack.append(token.lower() == "true")
            elif token == "(":
                stack.append(token)
            elif token == ")":
                # Evaluate the expression within parentheses
                sub_expr = []
                while stack and stack[-1] != "(":
                    sub_expr.append(stack.pop())
                stack.pop()  # Remove the '(' from the stack
                sub_expr.reverse()
                # Evaluate the sub-expression
                result = self.parse_expression(" ".join(map(str, sub_expr)))
                stack.append(result)
            else:
                # Handle variables or attributes
                stack.append(self.convert(token))

        return stack[0] if stack else None

    def parse(self) -> Condition:
        """Parse the condition."""
        for op in SimFileConditionParser.possible_operators.keys():
            if op in self._condition:
                left, right = self._condition.split(op, 1)
                return Condition(
                    left=left.strip(),
                    operator=op,
                    right=self.parse_expression(right.strip()),
                )

        raise ValueError(f"Invalid condition: {self._condition}")

    @staticmethod
    def map_to_character_attribute(
        condition: Condition, character: BaseCharacter
    ) -> Optional[Any]:
        """Map a condition to a character attribute."""

        attribute_name = condition.left.split(".", 1)[1]
        character_value = getattr(character, attribute_name, None)

        if character_value is not None:
            op_func = SimFileConditionParser.possible_operators.get(
                condition.operator
            )
            if op_func:
                print(
                    f"\t--> Checking if {attribute_name}({character_value}) "
                    + f"{condition.operator} {condition.right}"
                )
                return op_func(character_value, condition.right)

        return None

    @staticmethod
    def map_to_spell_attribute(
        condition: Condition, spell: BaseSpell
    ) -> Optional[Any]:
        """Map a condition to a spell attribute."""

        spell_name = condition.left.split(".", 1)[1]
        if spell_name.split(".")[0] != spell.simfell_name:
            return None

        attribute_name = spell_name.split(".", 1)[1]
        spell_value = getattr(spell, attribute_name, None)

        if spell_value is not None:
            op_func = SimFileConditionParser.possible_operators.get(
                condition.operator
            )
            if op_func:
                print(
                    f"\t--> Checking if {spell_name}({spell_value}) "
                    + f"{condition.operator} {condition.right}"
                )
                return op_func(spell_value, condition.right)

        return None

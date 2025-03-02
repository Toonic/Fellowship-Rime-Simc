"""Module for parsing SimFell files."""

import re
from typing import List, Tuple

from simfell_parser.model import (
    Action,
    SimFellConfiguration,
    Equipment,
    GemTier,
)
from simfell_parser.enums import Gem, TierSet, Tier
from simfell_parser.condition_parser import SimFileConditionParser


class SimFileParser:
    """Class for parsing SimFell files."""

    def __init__(self, file_path: str):
        self._file_path = file_path

    def _handle_comments(self, line: str) -> str:
        """Handle comments in the line."""

        if "#" in line:
            return line[: line.index("#")]
        return line

    def parse(self) -> SimFellConfiguration:
        """Parse the SimFell file."""

        data = {"actions": [], "gear": {}}

        with open(self._file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                line = self._handle_comments(line)

                key, value = self._parse_line(line)

                if key.startswith("action") or key.startswith("actions"):
                    data["actions"].extend(value)
                elif key.startswith("gear_"):
                    data["gear"][key.split("_")[1]] = value
                else:
                    data[key] = value

        return SimFellConfiguration(**data)

    def _parse_list_like_line(self, list_line: str) -> List[Action]:
        """
        Parse a list-like line of the SimFell file
        into a list of Actions.
        """

        pattern = r"(?P<name>/[^,]+)(?:,if=(?P<conditions>[^,]+))?"
        actions = []

        for match in re.finditer(pattern, list_line):
            name = match.group("name").strip()
            conditions_str = match.group("conditions")
            conditions = []

            if conditions_str:
                conditions = [
                    SimFileConditionParser(cond.strip()).parse()
                    for cond in conditions_str.split(" and ")
                ]

            actions.append(Action(name=name, conditions=conditions))

        return actions

    def _parse_gear_line(self, gear_line: str) -> Equipment:
        """
        Parse a gear line of the SimFell file
        into an Equipment object.
        """

        pattern = (
            r"(?P<name>[^,]+),int=(?P<int>\d+),stam=(?P<stam>\d+)"
            + r"(?:,exp=(?P<exp>\d+))?(?:,crit=(?P<crit>\d+))"
            + r"?(?:,haste=(?P<haste>\d+))?(?:,spirit=(?P<spirit>\d+))"
            + r"?(?:,gem_bonus=(?P<gem_bonus>\d+))?(?:,gem=(?P<gem>[^,]+))"
            + r"?(?:,set=(?P<set>[^,]+))?"
            + r",ilvl=(?P<ilvl>\d+),tier=(?P<tier>\d+)"
        )

        for match in re.finditer(pattern, gear_line):
            name = match.group("name")
            int_ = int(match.group("int"))
            stam = int(match.group("stam"))
            exp = int(match.group("exp")) if match.group("exp") else None
            crit = int(match.group("crit")) if match.group("crit") else None
            haste = int(match.group("haste")) if match.group("haste") else None
            spirit = (
                int(match.group("spirit")) if match.group("spirit") else None
            )
            gem_bonus = (
                int(match.group("gem_bonus"))
                if match.group("gem_bonus")
                else None
            )
            gem = match.group("gem")
            ilvl = int(match.group("ilvl"))
            tier = int(match.group("tier"))
            tier_set = match.group("set")

            return Equipment(
                name=name,
                intellect=int_,
                stamina=stam,
                expertise=exp,
                crit=crit,
                haste=haste,
                spirit=spirit,
                gem_bonus=gem_bonus,
                gem=(
                    GemTier(
                        tier=Tier[gem.split("_")[1].upper()],
                        gem=Gem(gem.split("_")[0]),
                    )
                    if gem
                    else None
                ),
                ilvl=ilvl,
                tier=Tier(tier),
                tier_set=TierSet(tier_set) if tier_set else None,
            )

    def _parse_line(self, line: str) -> Tuple[
        str,
        str | List[Action] | Equipment,
    ]:
        """Parse a line of the SimFell file."""

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        # Handle "list-like" values for actions
        if key.startswith("action") or key.startswith("actions"):
            return key, self._parse_list_like_line(value)
        # Handle values for gear
        if key.startswith("gear_"):
            return key, self._parse_gear_line(value)

        return key, value

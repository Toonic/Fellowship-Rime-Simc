"""Main file for simulating Character DPS."""

import sys
import argparse
from typing import Optional
from copy import deepcopy

from base import Character
from characters.Rime import RimeSpell, RimeTalent
from characters.Rime.preset import RimePreset
from Sim import Simulation


def main(arguments: argparse.Namespace):
    """Main function."""

    if arguments.preset and arguments.custom_character:
        raise ValueError(
            "Cannot provide both preset and custom character. "
            + "Please provide only one."
        )

    print("------------------")
    print(" Starting new Sim")
    print("------------------")

    if arguments.custom_character:
        try:
            stats = [
                int(stat) for stat in arguments.custom_character.split("-")
            ]
        except ValueError as e:
            raise ValueError(
                "Custom character must be formatted as "
                + "intellect-crit-expertise-haste-spirit"
            ) from e

        if len(stats) != 5:
            raise ValueError(
                "Custom character must be formatted as "
                + "intellect-crit-expertise-haste-spirit"
            )
        for stat in stats:
            if stat < 0:
                raise ValueError(
                    "All stats must be positive integers. "
                    + f"Invalid stat: {stat}"
                )

        character = Character(
            intellect=stats[0],
            crit=stats[1],
            expertise=stats[2],
            haste=stats[3],
            spirit=stats[4],
        )
    elif arguments.preset:
        # Use preset if provided.
        character = RimePreset[arguments.preset].value
    else:
        character = RimePreset.DEFAULT.value

    # Parse the talent tree argument.
    # e.g. Combination of "2-12-3" means Talent 1.2, 2.1, 2.2, 3.3
    # = Coalescing Ice, Unrelenting Ice, Icy Flow, Soulfrost Torrent
    if arguments.talent_tree:
        talents = arguments.talent_tree.split("-")
        for index, talent in enumerate(talents):
            for i in talent:
                rime_talent = RimeTalent.get_by_identifier(f"{index+1}.{i}")
                if rime_talent:
                    character.add_talent(rime_talent.value.name)

    # Spells casted in order.
    character.add_spell_to_rotation(RimeSpell.WRATH_OF_WINTER)
    character.add_spell_to_rotation(RimeSpell.ICE_BLITZ)
    character.add_spell_to_rotation(RimeSpell.DANCE_OF_SWALLOWS)
    character.add_spell_to_rotation(RimeSpell.COLD_SNAP)
    character.add_spell_to_rotation(RimeSpell.BURSTING_ICE)
    character.add_spell_to_rotation(RimeSpell.FREEZING_TORRENT)
    character.add_spell_to_rotation(RimeSpell.ICE_COMET)
    character.add_spell_to_rotation(RimeSpell.GLACIAL_BLAST)
    character.add_spell_to_rotation(RimeSpell.FROST_BOLT)

    # Sim Options - Uncomment one to run.
    match arguments.simulation_type:
        case "average_dps":
            average_dps(character, arguments.duration, arguments.enemy_count)
        case "stat_weights":
            stat_weights(character, arguments.duration, arguments.enemy_count)
        case "debug_sim":
            debug_sim(character, arguments.duration, arguments.enemy_count)


def stat_weights(
    character: Character, duration: int, enemy_count: Optional[int] = None
) -> None:
    """Calculates the stat weights of the character."""

    print("==== Doing Stat Weights ==== ")
    stat_increase = 200
    target_count = 4 if enemy_count is None else enemy_count
    character_base = character
    base_dps = average_dps(character_base, duration, target_count, "base")

    def update_stats(
        character: Character, stat_increase: int, stat_name: str
    ) -> float:
        character_updated = character
        character_updated.update_stats(
            intellect=(
                character_updated.intellect_points + stat_increase
                if stat_name == "intellect"
                else character_updated.intellect_points
            ),
            crit=(
                character_updated.crit_points + stat_increase
                if stat_name == "crit"
                else character_updated.crit_points
            ),
            expertise=(
                character_updated.expertise_points + stat_increase
                if stat_name == "expertise"
                else character_updated.expertise_points
            ),
            haste=(
                character_updated.haste_points + stat_increase
                if stat_name == "haste"
                else character_updated.haste_points
            ),
            spirit=(
                character_updated.spirit_points + stat_increase
                if stat_name == "spirit"
                else character_updated.spirit_points
            ),
        )

        return average_dps(
            character_updated,
            duration,
            target_count,
            stat_name,
        )

    int_dps = update_stats(character, stat_increase, "intellect")
    crit_dps = update_stats(character, stat_increase, "crit")
    expertise_dps = update_stats(character, stat_increase, "expertise")
    haste_dps = update_stats(character, stat_increase, "haste")
    spirit_dps = update_stats(character, stat_increase, "spirit")

    print("--------------")
    print("Stat Weights:")
    print(f"Intellect: {1 + ((int_dps - base_dps) / base_dps):.2f}")
    print(f"Crit: {1 + ((crit_dps - base_dps) / base_dps):.2f}")
    print(f"Expertise: {1 + ((expertise_dps - base_dps) / base_dps):.2f}")
    print(f"Haste: {1 + ((haste_dps - base_dps) / base_dps):.2f}")
    print(f"Spirit: {1 + ((spirit_dps - base_dps) / base_dps):.2f}")
    print("--------------")


def debug_sim(character: Character, duration: int, enemy_count: int) -> None:
    """Runs a debug simulation.
    Creates a deterministic simulation with 0 crit and spirit.
    """

    sim = Simulation(
        character,
        duration=duration,
        enemy_count=enemy_count,
        do_debug=True,
        is_deterministic=False,
    )
    sim.run()


def update_progress(progress: float) -> None:
    """Updates the progress bar in the console."""
    bar_length = 40
    block = int(round(bar_length * progress))
    text = f"\rProgress: [{'#' * block + '-' * (bar_length - block)}] {progress * 100:.2f}%"
    sys.stdout.write(text)
    sys.stdout.flush()


def average_dps(
    character: Character,
    duration: int,
    enemy_count: int,
    stat_name: Optional[str] = None,
) -> float:
    """Runs a simulation and returns the average DPS."""

    if stat_name:
        print(f"Stat Weight: {stat_name}\n-------------")

    run_count = 2000
    dps_running_total = 0
    dps_lowest = float("inf")
    dps_highest = float("-inf")

    for run_index in range(run_count):
        update_progress(run_index / run_count)
        character_copy = deepcopy(character)
        sim = Simulation(
            character_copy,
            duration=duration,
            enemy_count=enemy_count,
            do_debug=False,
            is_deterministic=False,
        )
        dps = sim.run()
        dps_lowest = min(dps, dps_lowest)
        dps_highest = max(dps, dps_highest)

        dps_running_total += dps
    avg_dps = dps_running_total / run_count

    # Ensure progress bar is full
    update_progress(1)

    # Clear the progress bar line
    sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.flush()

    print(f"Highest DPS: {dps_highest:.2f}")
    print(f"Average DPS: {avg_dps:.2f}")
    print(f"Lowest DPS: {dps_lowest:.2f}\n")

    return avg_dps


if __name__ == "__main__":
    # Create parser for command line arguments.
    parser = argparse.ArgumentParser(description="Simulate Rime DPS.")

    parser.add_argument(
        "-s",
        "--simulation-type",
        type=str,
        default="average_dps",
        help="Type of simulation to run.",
        choices=["average_dps", "stat_weights", "debug_sim"],
        required=True,
    )
    parser.add_argument(
        "-e",
        "--enemy-count",
        type=int,
        default=1,
        help="Number of enemies to simulate.",
        required=True,
    )
    parser.add_argument(
        "-t",
        "--talent-tree",
        type=str,
        default="",
        help="Talent tree to use. Format: (row1-row2-row3), "
        + "e.g., 13-1-2 means Talent 1.1, Talent 1.3, Talent 2.1, Talent 3.2",
    )
    parser.add_argument(
        "-p",
        "--preset",
        type=str,
        default="",
        help="Preset to use. Possible values: "
        + ",".join([preset.name for preset in RimePreset]),
        choices=[preset.name for preset in RimePreset],
    )
    parser.add_argument(
        "-c",
        "--custom-character",
        type=str,
        default="",
        help="Custom character to use. "
        + "Format: intellect-crit-expertise-haste-spirit",
    )
    parser.add_argument(
        "-d",
        "--duration",
        type=int,
        default=120,
        help="Duration of the simulation.",
    )

    # Parse arguments.
    args = parser.parse_args()

    # Run the simulation.
    main(args)

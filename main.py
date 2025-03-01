"""Main file for simulating Character DPS."""

import argparse
from typing import Optional
from copy import deepcopy
from rich.table import Table, box
from rich.console import Console
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    MofNCompleteColumn,
)

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

    print()

    console = Console()
    table = Table(title="Rime DPS Simulation", box=box.SIMPLE)
    table.add_column(
        "Attribute", style="blue", justify="center", vertical="middle"
    )
    table.add_column("Value", style="yellow", justify="center")

    table.add_row("Simulation Type", arguments.simulation_type)
    table.add_row("Enemy Count", str(arguments.enemy_count))
    table.add_row("Duration", str(arguments.duration))
    if arguments.simulation_type == "stat_weights":
        table.add_row("Stat Weights Gain", str(arguments.stat_weights_gain))
    table.add_row(
        "Preset",
        arguments.preset if arguments.preset else RimePreset.DEFAULT.name,
        end_section=True,
    )

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

    table.add_row(
        "Talent Tree",
        "\n".join(character.talents) if character.talents else "N/A",
        end_section=True,
    )
    table.add_row(
        "Custom Character",
        (
            "\n".join(
                f"{key}: {value}"
                for key, value in {
                    "int": character.intellect_points,
                    "crit": character.crit_points,
                    "exp": character.expertise_points,
                    "haste": character.haste_points,
                    "spirit": character.spirit_points,
                }.items()
            )
            if arguments.custom_character
            else "N/A"
        ),
        end_section=True,
    )

    # Sim Options - Uncomment one to run.
    match arguments.simulation_type:
        case "average_dps":
            average_dps(
                table,
                character,
                arguments.duration,
                arguments.run_count,
                arguments.enemy_count,
                arguments.experimental_feature,
            )
        case "stat_weights":
            stat_weights(
                table,
                character,
                arguments.duration,
                arguments.run_count,
                arguments.stat_weights_gain,
                arguments.experimental_feature,
                arguments.enemy_count,
            )
        case "debug_sim":
            debug_sim(
                character,
                arguments.duration,
                arguments.enemy_count,
            )

    # Print the final results
    console.print("\n")
    console.print(table)


def stat_weights(
    table: Table,
    character: Character,
    duration: int,
    run_count: int,
    stat_increase: int,
    use_experimental: bool,
    enemy_count: Optional[int] = None,
) -> None:
    """Calculates the stat weights of the character."""

    target_count = 4 if enemy_count is None else enemy_count
    character_base = character
    base_dps = average_dps(
        table,
        character_base,
        duration,
        run_count,
        target_count,
        use_experimental=use_experimental,
        stat_name="base",
    )

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
            table,
            character_updated,
            duration,
            run_count,
            target_count,
            use_experimental=use_experimental,
            stat_name=stat_name,
        )

    int_dps = update_stats(character, stat_increase, "intellect")
    crit_dps = update_stats(character, stat_increase, "crit")
    expertise_dps = update_stats(character, stat_increase, "expertise")
    haste_dps = update_stats(character, stat_increase, "haste")
    spirit_dps = update_stats(character, stat_increase, "spirit")

    table.add_row("\n[white]Stat Weights", "\n[white]-------------")
    table.add_row(
        "Intellect", f"[magenta]{1 + ((int_dps - base_dps) / base_dps):.2f}"
    )
    table.add_row(
        "Crit", f"[magenta]{1 + ((crit_dps - base_dps) / base_dps):.2f}"
    )
    table.add_row(
        "Expertise",
        f"[magenta]{1 + ((expertise_dps - base_dps) / base_dps):.2f}",
    )
    table.add_row(
        "Haste", f"[magenta]{1 + ((haste_dps - base_dps) / base_dps):.2f}"
    )
    table.add_row(
        "Spirit", f"[magenta]{1 + ((spirit_dps - base_dps) / base_dps):.2f}"
    )


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


def average_dps(
    table: Table,
    character: Character,
    duration: int,
    run_count: int,
    enemy_count: int,
    use_experimental: bool,
    stat_name: Optional[str] = None,
) -> float:
    """Runs a simulation and returns the average DPS."""

    with Progress(
        TextColumn(
            f"[bold]{stat_name if stat_name else 'Calculating DPS'}[/bold] "
            + "[progress.percentage]{task.percentage:>3.0f}%"
        ),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
        TextColumn("•"),
        TimeRemainingColumn(),
    ) as progress:
        dps_running_total = 0
        dps_lowest = float("inf")
        dps_highest = float("-inf")

        task = progress.add_task(f"{stat_name}", total=run_count)

        for _ in range(run_count):
            character_copy = deepcopy(character)
            sim = Simulation(
                character_copy,
                duration=duration,
                enemy_count=enemy_count,
                do_debug=False,
                is_deterministic=False,
            )
            dps = sim.run()

            progress.update(task, advance=1)

            dps_lowest = min(dps, dps_lowest)
            dps_highest = max(dps, dps_highest)

            dps_running_total += dps
        avg_dps = dps_running_total / run_count

    table.add_row(
        "Average DPS" if not stat_name else f"Average DPS ({stat_name})",
        f"[bold magenta]{avg_dps:.2f}",
    )
    table.add_row(
        "Lowest DPS" if not stat_name else f"Lowest DPS ({stat_name})",
        f"[bold magenta]{dps_lowest:.2f}",
    )
    table.add_row(
        "Highest DPS" if not stat_name else f"Highest DPS ({stat_name})",
        f"[bold magenta]{dps_highest:.2f}",
        end_section=True,
    )

    # Experimental: Damage Table
    # ---------------------------
    if not stat_name and use_experimental:
        damage_sum = sum(damage for _, damage in sim.damage_table.items())

        table.add_row(
            "[bold yellow]-------- Experimental!",
            "[bold yellow]Do not trust! --------",
        )
        table.add_row("[white]Damage Table", "[white]-------------")
        for spell, damage in sim.damage_table.items():
            table.add_row(
                spell, f"[magenta]{round(damage, 3)} ({damage/damage_sum:.2%})"
            )

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
    parser.add_argument(
        "-r",
        "--run-count",
        type=int,
        default=2000,
        help="Number of runs to average DPS.",
    )
    parser.add_argument(
        "-g",
        "--stat-weights-gain",
        type=float,
        default=20,
        help="Gain of stat weights for the simulation.",
    )
    parser.add_argument(
        "-x",
        "--experimental-feature",
        action="store_true",
        help="Enable experimental features such as the damage table.",
    )

    # Parse arguments.
    args = parser.parse_args()

    # Run the simulation.
    main(args)

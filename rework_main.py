"""Main file for the rework sim."""

import argparse
from copy import deepcopy
from rich import box
from rich.console import Console
from rich.table import Table
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    MofNCompleteColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)


from characters.Rime import Rime
from characters.Rime.rime import (
    # WrathOfWinter,
    FrostBolt,
    # IceBlitz,
    ColdSnap,
    # DanceOfSwallows,
    # FreezingTorrent,
    BurstingIce,
    GlacialBlast,
    # IceComet,
)
from characters.Rime.preset import RimePreset
from characters.Rime.talent import RimeTalent
from simfell_parser.simfile_parser import SimFileParser, SimFellConfiguration
from simfell_parser.model import Gear
from rework_sim import Simulation


def handle_configuration(
    arguments: argparse.Namespace,
) -> SimFellConfiguration:
    """Handles the configuration based on the arguments."""

    checked_arguments = [
        arguments.preset,
        arguments.custom_character,
        arguments.talent_tree,
        arguments.enemy_count,
    ]

    if arguments.simfile and any(checked_arguments):
        raise ValueError(
            "Cannot provide both SimFile configuration and custom. "
            + "Please provide only one."
        )
    if not arguments.simfile and not any(checked_arguments):
        raise ValueError(
            "Must provide either a preset or a SimFell file. "
            + "Please provide one."
        )

    # Parse the simfile if provided.
    if arguments.simfile:
        simfile_parser = SimFileParser(arguments.simfile)
        configuration = simfile_parser.parse()
    else:
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

            character = Rime(
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

        configuration = SimFellConfiguration(
            name="Custom Configuration",
            hero="Rime",
            intellect=character.get_main_stat(),
            crit=character.get_crit(),
            expertise=character.get_expertise(),
            haste=character.get_haste(),
            spirit=character.get_spirit(),
            enemies=arguments.enemy_count,
            duration=arguments.duration,
            talents=arguments.talent_tree,
            run_count=arguments.run_count,
            trinket1=None,
            trinket2=None,
            actions=[],
            gear=Gear(helmet=None, shoulder=None),
        )

    return configuration


def main(arguments: argparse.Namespace):
    """Main function."""

    configuration = handle_configuration(arguments)

    print()

    console = Console()
    table = Table(title="Rime DPS Simulation", box=box.SIMPLE)
    table.add_column(
        "Attribute", style="blue", justify="center", vertical="middle"
    )
    table.add_column("Value", style="yellow", justify="center")

    table.add_row("Simulation Type", arguments.simulation_type)
    table.add_row("Enemy Count", str(configuration.enemies))
    table.add_row("Duration", str(configuration.duration))
    table.add_row("Run Count", str(configuration.run_count))
    if arguments.simulation_type == "stat_weights":
        table.add_row("Stat Weights Gain", str(arguments.stat_weights_gain))
    table.add_row(
        "Preset",
        arguments.preset if arguments.preset else RimePreset.DEFAULT.name,
        end_section=True,
    )

    character = Rime(
        intellect=configuration.intellect,
        crit=configuration.crit,
        expertise=configuration.expertise,
        haste=configuration.haste,
        spirit=configuration.spirit,
    )

    # Parse the talent tree argument.
    # e.g. Combination of "2-12-3" means Talent 1.2, 2.1, 2.2, 3.3
    # = Coalescing Ice, Unrelenting Ice, Icy Flow, Soulfrost Torrent
    if configuration.talents:
        talents = configuration.talents.split("-")
        for index, talent in enumerate(talents):
            for i in talent:
                rime_talent = RimeTalent.get_by_identifier(f"{index+1}.{i}")
                if rime_talent:
                    character.add_talent(rime_talent.value.name)

    # TODO: This should be a list of SimFell Actions.
    # character.rotation.append(WrathOfWinter().simfell_name)
    # character.rotation.append(IceBlitz().simfell_name)
    # character.rotation.append(DanceOfSwallows().simfell_name)
    character.rotation.append(ColdSnap().simfell_name)
    character.rotation.append(BurstingIce().simfell_name)
    # character.rotation.append(IceComet().simfell_name)
    character.rotation.append(GlacialBlast().simfell_name)
    character.rotation.append(FrostBolt().simfell_name)

    table.add_row(
        "Talent Tree",
        "\n".join(character.talents) if character.talents else "N/A",
        end_section=True,
    )
    table.add_row(
        "Character",
        (
            "\n".join(
                f"{key}: {value}"
                for key, value in {
                    "int": character.get_main_stat(),
                    "crit": f"{round(character.get_crit(), 2)}%",
                    "exp": f"{round(character.get_expertise(), 2)}%",
                    "haste": f"{round(character.get_haste(), 2)}%",
                    "spirit": f"{round(character.get_spirit(), 2)}%",
                }.items()
            )
        ),
        end_section=True,
    )

    # Sim Options - Uncomment one to run.
    match arguments.simulation_type:
        case "average_dps":
            raise NotImplementedError("Average DPS not implemented yet.")
            # average_dps(
            #     table,
            #     character,
            #     configuration.duration,
            #     configuration.run_count,
            #     configuration.enemies,
            #     arguments.experimental_feature,
            # )
        case "stat_weights":
            raise NotImplementedError("Stat Weights not implemented yet.")
            # stat_weights(
            #     table,
            #     character,
            #     configuration.duration,
            #     configuration.run_count,
            #     arguments.stat_weights_gain,
            #     arguments.experimental_feature,
            #     configuration.enemies,
            # )
        case "debug_sim":
            debug_sim(
                table,
                character,
                configuration.duration,
                configuration.enemies,
            )

    # Print the final results
    console.print("\n")
    console.print(table)


def debug_sim(
    table: Table, character: Rime, duration: int, enemy_count: int
) -> None:
    """Runs a debug simulation.
    Creates a deterministic simulation with 0 crit and spirit.
    """

    total = 0
    run_count = 10

    with Progress(
        TextColumn(
            "[bold]Running Debug Simulation[/bold] "
            + "[progress.percentage]{task.percentage:>3.0f}%"
        ),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
        TextColumn("•"),
        TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task("Running Debug Simulation", total=run_count)

        for _ in range(run_count):
            sim = Simulation(
                deepcopy(character),
                duration=duration,
                enemy_count=enemy_count,
                do_debug=True,
            )
            total += sim.run() / duration

            progress.update(task, advance=1)

    table.add_row("Total DPS", f"[bold magenta]{total:.2f}")
    table.add_row("Average DPS", f"[bold magenta]{total / run_count:.2f}")


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
        help="Number of enemies to simulate.",
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
    parser.add_argument(
        "-f",
        "--simfile",
        type=str,
        default="",
        help="Path to the SimFell file.",
    )

    # Parse arguments.
    args = parser.parse_args()

    # Run the simulation.
    main(args)

import sys
import ast
from Character import Character
from Spell import Spell
from Sim import Simulation
from copy import copy
from rime import TALENT_MAP #todo other chars?

SIM_MODES = {
    "average": "average_dps",
    "weights": "stat_weights",
    "debug": "debug_sim"
}

def parse_args():
    """Parses command-line arguments and returns attributes, talents, and sim mode."""
    args = sys.argv[1:]  # Ignore the script name
    attributes = {}
    selected_talents = []
    sim_mode = "debug"  # Default mode

    for arg in args:
        if "=" in arg:
            key, value = arg.split("=")
            key = key.lower()

            if key in {"intellect", "crit", "expertise", "haste", "spirit"}:
                try:
                    attributes[key] = int(value)
                except ValueError:
                    print(f"Invalid value for {key}: {value}. Must be an integer.")
                    sys.exit(1)
            elif key == "talents":
                try:
                    talent_numbers = ast.literal_eval(value)  # Convert string to list safely
                    if isinstance(talent_numbers, list):
                        for num in talent_numbers:
                            if num in TALENT_MAP:
                                selected_talents.append(TALENT_MAP[num])
                            else:
                                print(f"Warning: Talent {num} is not recognized and will be ignored.")
                except (ValueError, SyntaxError):
                    print(f"Invalid format for talents: {value}. Expected format: talents=[1.1,1.2,1.3]")
                    sys.exit(1)
            elif key == "sim":
                if value in SIM_MODES:
                    sim_mode = value
                else:
                    print(f"Invalid simulation mode '{value}'. Available options: {list(SIM_MODES.keys())}")
                    sys.exit(1)

    return attributes, selected_talents, sim_mode

def main():
    print("----------------------------")
    print("Starting new Sim")
    print("----------------------------")

    # Default character stats
    base_stats = {
        "intellect": 270,
        "crit": 60,
        "expertise": 60,
        "haste": 140,
        "spirit": 40
    }

    # Override defaults with command-line arguments
    user_stats, selected_talents, sim_mode = parse_args()
    base_stats.update(user_stats)

    # Create character with modified stats
    character = Character(
        intellect=base_stats["intellect"],
        crit=base_stats["crit"],
        expertise=base_stats["expertise"],
        haste=base_stats["haste"],
        spirit=base_stats["spirit"]
    )


       # Add selected talents
    for talent in selected_talents:
        character.add_talent(talent)

    print(f"Character created with stats: {base_stats}")
    print(f"Talents selected: {selected_talents}")
    
    ## Spells casted in order.
    character.add_spell(Spell("Wrath of Winter", cast_time=0, cooldown=600, mana_generation=0, winter_orb_cost=0, damage_percent=0, isBuff=True, ticks=10, debuffDuration=20))
    character.add_spell(Spell("Ice Blitz", cast_time=0, cooldown=120, mana_generation=0, winter_orb_cost=0, damage_percent=0, isBuff=True, ticks=0, debuffDuration=20))
    character.add_spell(Spell("Dance of Swallows", cast_time=0, cooldown=60, mana_generation=0, winter_orb_cost=2, damage_percent=53, isDebuff=True, ticks=0, debuffDuration=20))
    character.add_spell(Spell("Cold Snap", cast_time=0, cooldown=8, mana_generation=0, winter_orb_cost=-1, damage_percent=204))  # Cold Snap spell
    character.add_spell(Spell("Bursting Ice", cast_time=2.0, cooldown=10, mana_generation=6, winter_orb_cost=0, damage_percent=366, isDebuff=True, ticks=6, debuffDuration=3, doDebuffDamage=True))
    character.add_spell(Spell("Glacial Blast", cast_time=2.0, cooldown=0, mana_generation=0, winter_orb_cost=2, damage_percent=504))
    character.add_spell(Spell("Freezing Torrent", cast_time=2.0, cooldown=10, mana_generation=6, winter_orb_cost=0, damage_percent=390, channeled=True, ticks=6))
    character.add_spell(Spell("FrostBolt", cast_time=1.5, cooldown=0, mana_generation=3, winter_orb_cost=0, damage_percent=73))

    sim_function = globals().get(SIM_MODES[sim_mode])  # Get function by name
    if sim_function:
        print(f"Running simulation mode: {sim_mode}")
        sim_function(character)
    else:
        print(f"Error: Simulation function '{SIM_MODES[sim_mode]}' not found.")


def stat_weights(character):
    print("==== Doing Stat Weights ==== ")
    statIncrease = 50
    characterBase = character
    baseDPS = average_dps(characterBase)

    characterUpdated = character
    characterUpdated.update_stats(intellect=characterUpdated.intellectPoints + statIncrease, crit=characterUpdated.critPoints, expertise=characterUpdated.expertisePoints, haste=characterUpdated.hastePoints, spirit=characterUpdated.spiritPoints)
    intDPS = average_dps(characterUpdated)

    characterUpdated = character
    characterUpdated.update_stats(intellect=characterUpdated.intellectPoints, crit=characterUpdated.critPoints + statIncrease, expertise=characterUpdated.expertisePoints, haste=characterUpdated.hastePoints, spirit=characterUpdated.spiritPoints)
    critDPS = average_dps(characterUpdated)

    characterUpdated = character
    characterUpdated.update_stats(intellect=characterUpdated.intellectPoints, crit=characterUpdated.critPoints, expertise=characterUpdated.expertisePoints + statIncrease, haste=characterUpdated.hastePoints, spirit=characterUpdated.spiritPoints)
    expertiseDPS = average_dps(characterUpdated)

    characterUpdated = character
    characterUpdated.update_stats(intellect=characterUpdated.intellectPoints, crit=characterUpdated.critPoints, expertise=characterUpdated.expertisePoints, haste=characterUpdated.hastePoints + statIncrease, spirit=characterUpdated.spiritPoints)
    hasteDPS = average_dps(characterUpdated)

    characterUpdated = character
    characterUpdated.update_stats(intellect=characterUpdated.intellectPoints, crit=characterUpdated.critPoints, expertise=characterUpdated.expertisePoints, haste=characterUpdated.hastePoints, spirit=characterUpdated.spiritPoints + statIncrease)
    spiritDPS = average_dps(characterUpdated)

    print(f'Stat Weights:')
    print(f'Intellect: {1 + ((intDPS - baseDPS) / baseDPS):.2f}')
    print(f'Crit: {1 + ((critDPS - baseDPS) / baseDPS):.2f}')
    print(f'Expertise: {1 + ((expertiseDPS - baseDPS) / baseDPS):.2f}')
    print(f'Haste: {1 + ((hasteDPS - baseDPS) / baseDPS):.2f}')
    print(f'Spirit: {1 + ((spiritDPS - baseDPS) / baseDPS):.2f}')
    print("--------------")

def debug_sim(character):
    sim = Simulation(character, duration=120, doDebug = True)
    sim.run()

def average_dps(character):
    runCount = 2000
    dpsRunningTotal = 0
    dpsLowest = 1000000
    dpsHighest = 0
    for i in range(runCount):
        characterCopy = copy(character)
        sim = Simulation(characterCopy, duration=120, doDebug = False)
        dps = sim.run()
        if dps < dpsLowest:
            dpsLowest = dps
        if dps > dpsHighest:
            dpsHighest = dps
        dpsRunningTotal += dps
    averageDPS = dpsRunningTotal / runCount
    print(f'Highest DPS: {dpsHighest:.2f}')
    print(f'Average DPS: {averageDPS:.2f}')
    print(f'Lowest DPS: {dpsLowest:.2f}')
    return averageDPS

if __name__ == "__main__":
    main()
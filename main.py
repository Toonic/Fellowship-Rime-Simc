from Character import Character
from Spell import Spell
from Sim import Simulation
from copy import copy

def main():
    print("----------------------------")
    print("Starting new Sim")
    print("----------------------------")
    ## Create your character below by plugging in their Point Stats, not % Stats.
    #Test Character
    character = Character(intellect=300, crit=160, expertise=90, haste=120, spirit=50)

    ## Talents
    ## Row 1 - 2 Points Each
    #character.add_talent("Chillblain")
    character.add_talent("Coalescing Ice")
    #character.add_talent("Glacial Assault") #Doodoo
    ## Row 2 - 1 Point Each
    character.add_talent("Unrelenting Ice")
    character.add_talent("Icy Flow")
    ## Row 3 - 3 Points Each
    #character.add_talent("Wisdom of the North")
    #character.add_talent("Avalanche")
    character.add_talent("Soulfrost Torrent")
    
    ## Spells casted in order.
    character.add_spell(Spell("Wrath of Winter", cast_time=0, cooldown=600, mana_generation=0, winter_orb_cost=0, damage_percent=0, isBuff=True, ticks=10, debuffDuration=20))
    character.add_spell(Spell("Ice Blitz", cast_time=0, cooldown=120, mana_generation=0, winter_orb_cost=0, damage_percent=0, isBuff=True, ticks=0, debuffDuration=20))
    character.add_spell(Spell("Dance of Swallows", cast_time=0, cooldown=60, mana_generation=0, winter_orb_cost=2, damage_percent=53, isDebuff=True, ticks=0, debuffDuration=20))
    #character.add_spell(Spell("Ice Comet", cast_time=0, cooldown=0, mana_generation=0, winter_orb_cost=3, damage_percent=300))
    #character.add_spell(Spell("Glacial Blast", cast_time=2.0, cooldown=0, mana_generation=0, winter_orb_cost=2, damage_percent=504))
    character.add_spell(Spell("Cold Snap", cast_time=0, cooldown=8, mana_generation=0, winter_orb_cost=-1, damage_percent=204))  # Cold Snap spell
    character.add_spell(Spell("Bursting Ice", cast_time=2.0, cooldown=15, mana_generation=6, winter_orb_cost=0, damage_percent=366, isDebuff=True, ticks=6, debuffDuration=3, doDebuffDamage=True))
    character.add_spell(Spell("Ice Comet", cast_time=0, cooldown=0, mana_generation=0, winter_orb_cost=3, damage_percent=300, min_target_count=2, max_target_count=1000))
    character.add_spell(Spell("Glacial Blast", cast_time=2.0, cooldown=0, mana_generation=0, winter_orb_cost=2, damage_percent=504, min_target_count=1, max_target_count=2))
    character.add_spell(Spell("Freezing Torrent", cast_time=2.0, cooldown=10, mana_generation=6, winter_orb_cost=0, damage_percent=390, channeled=True, ticks=6))
    character.add_spell(Spell("FrostBolt", cast_time=1.5, cooldown=0, mana_generation=3, winter_orb_cost=0, damage_percent=73))

    ## Sim Options - Uncomment one to run.
    #average_dps(character,1)
    average_dps(character,5)
    #stat_weights(character)
    #debug_sim(character)


def stat_weights(character):
    print("==== Doing Stat Weights ==== ")
    statIncrease = 200
    target_count = 4
    characterBase = character
    baseDPS = average_dps(characterBase, target_count)

    characterUpdated = character
    characterUpdated.update_stats(intellect=characterUpdated.intellectPoints + statIncrease, crit=characterUpdated.critPoints, expertise=characterUpdated.expertisePoints, haste=characterUpdated.hastePoints, spirit=characterUpdated.spiritPoints)
    intDPS = average_dps(characterUpdated, target_count)

    characterUpdated = character
    characterUpdated.update_stats(intellect=characterUpdated.intellectPoints, crit=characterUpdated.critPoints + statIncrease, expertise=characterUpdated.expertisePoints, haste=characterUpdated.hastePoints, spirit=characterUpdated.spiritPoints)
    critDPS = average_dps(characterUpdated, target_count)

    characterUpdated = character
    characterUpdated.update_stats(intellect=characterUpdated.intellectPoints, crit=characterUpdated.critPoints, expertise=characterUpdated.expertisePoints + statIncrease, haste=characterUpdated.hastePoints, spirit=characterUpdated.spiritPoints)
    expertiseDPS = average_dps(characterUpdated, target_count)

    characterUpdated = character
    characterUpdated.update_stats(intellect=characterUpdated.intellectPoints, crit=characterUpdated.critPoints, expertise=characterUpdated.expertisePoints, haste=characterUpdated.hastePoints + statIncrease, spirit=characterUpdated.spiritPoints)
    hasteDPS = average_dps(characterUpdated, target_count)

    characterUpdated = character
    characterUpdated.update_stats(intellect=characterUpdated.intellectPoints, crit=characterUpdated.critPoints, expertise=characterUpdated.expertisePoints, haste=characterUpdated.hastePoints, spirit=characterUpdated.spiritPoints + statIncrease)
    spiritDPS = average_dps(characterUpdated, target_count)

    print("--------------")
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

def average_dps(character, enemy_count):
    runCount = 2000
    dpsRunningTotal = 0
    dpsLowest = 1000000
    dpsHighest = 0
    for i in range(runCount):
        characterCopy = copy(character)
        sim = Simulation(characterCopy, duration=180, enemyCount = enemy_count, doDebug = False)
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
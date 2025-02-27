from Spell import Spell
from functools import cached_property

class Character:
    intellectPerPoint = 1
    critPerPoint = 0.21
    expertisePerPoint = 0.21
    hastePerPoint = 0.21
    spiritPerPoint = 0.21
    def __init__(self, intellect, crit, expertise, haste, spirit):
        self.intellectPoints = intellect
        self.critPoints = crit
        self.expertisePoints = expertise
        self.hastePoints = haste
        self.spiritPoints = spirit
        self.mana = 0
        self.winter_orbs = 0
        self.spells = []  # This will hold the character's available spells
        self.talents = [] # All the talents.
        self.anima_spikes = Spell("Anima Spikes", cast_time=0, cooldown=0, mana_generation=0, winter_orb_cost=0, damage_percent=36, hits=3)
        #Damage is set to 1560 because of ingame bug.
        self.soulfrost = Spell("Soulfrost Torrent", cast_time=2.0, cooldown=10, mana_generation=12, winter_orb_cost=0, damage_percent=1560, channeled=True, ticks=12)
        self.boosted_blast = Spell("Glacial Blast", cast_time=0, cooldown=0, mana_generation=0, winter_orb_cost=2, damage_percent=604)

        self.soulfrost_buff = Spell("Soulfrost Torrent", isBuff=True, debuffDuration=100000)
        self.glacial_assault_buff = Spell("Glacial Assault", isBuff=True, debuffDuration=100000)
        self.cometBonus = Spell("Ice Comet", cast_time=0, cooldown=0, mana_generation=0, winter_orb_cost=0, damage_percent=300)

    def _calculate_stat_value(self, points, statPerPoint):
        return points * statPerPoint

    @cached_property
    def intellect(self):
        return self._calculate_stat_value(self.intellectPoints, Character.intellectPerPoint)

    @cached_property
    def crit(self):
        return self._calculate_stat_value(self.critPoints, Character.critPerPoint) + 5 #5% base crit
    
    @cached_property
    def expertise(self):
        return self._calculate_stat_value(self.expertisePoints, Character.expertisePerPoint)
    
    @cached_property
    def haste(self):
        return self._calculate_stat_value(self.hastePoints, Character.hastePerPoint)

    @cached_property
    def spirit(self):
        return self._calculate_stat_value(self.spiritPoints, Character.spiritPerPoint)

    def add_spell(self, spell):
        self.spells.append(spell)
    
    def add_talent(self, talent):
        self.talents.append(talent)

    def update_stats(self, intellect, crit, expertise, haste, spirit):
        self.intellect_points = intellect
        self.crit_points = crit
        self.expertise_points = expertise
        self.haste_points = haste
        self.spirit_points = spirit
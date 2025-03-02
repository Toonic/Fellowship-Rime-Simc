from base import BaseCharacter
from base import BaseSpell

class Rime(BaseCharacter):
    """Stat Point DR """

    main_stat_per_point = 1
    critPerPoint = 0.21
    expertisePerPoint = 0.21
    hastePerPoint = 0.21
    spiritPerPoint = 0.21

    anima = 0
    winter_orbs = 0

    def __init__(self, intellect, crit, expertise, haste, spirit):
        super().__init__(intellect, crit, expertise, haste, spirit)
        self.anima = 0
        self.winter_orbs = 0

class RimeSpell(BaseSpell):
    """Base information for Rime Spells"""

    anima_gained = 0
    winter_orb_cost = 0

    def __init__(self,
                 anima_gained = 0, 
                 winter_orb_cost = 0,
                 *args, **kwargs,):
        super().__init__(*args, **kwargs)
        self.anima_gained = anima_gained
        self.winter_orb_cost = winter_orb_cost

    

class Frost_Bolt(RimeSpell):
    """Frostbolt Spell"""

    def __init__(self):
        super().__init__("Frostbolt",
                         cast_time=1.5,
                         damage_percent=73,
                         anima_gained=3)
        
class Cold_Snap(RimeSpell):
    """Cold Snap Spell"""

    def __init__(self):
        super().__init__("Cold Snap",
                         damage_percent=219,
                         winter_orb_cost=-1)
        
class Freezing_Torrent(RimeSpell):
    """Freezing Torrent Spell"""

    def __init__(self):
        super().__init__("Freezing Torrent",
                         cast_time=2.0,
                         cooldown=10,
                         damage_percent=390,
                         anima_gained=6,
                         channeled=True,
                         ticks=6)
        
#TODO: Make this a Debuff instead of a Spell.
class Bursting_Ice(RimeSpell):
    """Bursting Ice Spell"""

    def __init__(self):
        super().__init__("Bursting Ice",
                         cast_time=2.0,
                         cooldown=15,
                         damage_percent=366,
                         anima_gained=6,
                         ticks=6,
                         is_debuff=True,
                         duration=3)
        
class Glacial_Blast(RimeSpell):
    """Glacial Blast Spell"""

    def __init__(self):
        super().__init__("Glacial Blast",
                         cast_time=2.0,
                         damage_percent=504,
                         winter_orb_cost=2)
        
class Ice_Comet(RimeSpell):
    """Ice Comet Spell"""

    def __init__(self):
        super().__init__("Ice Comet",
                         damage_percent=300,
                         winter_orb_cost=3)
        
class Dance_Of_Swallows(RimeSpell):
    """Dance of Swallows Spell"""

    def __init__(self):
        super().__init__("Dance of Swallows",
                         cooldown=60,
                         damage_percent=53,
                         winter_orb_cost=2,)

class Ice_Blitz(RimeSpell):
    """Ice Blitz Spell"""

    def __init__(self):
        super().__init__("Ice Blitz",
                         cooldown=120,
                         damage_percent=73)

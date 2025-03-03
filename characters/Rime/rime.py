from base import BaseCharacter
from base import BaseSpell


# Defines the Rime Character class.
class Rime(BaseCharacter):
    """Stat Point DR"""

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

    def configure_spell_book(self):
        self.spells = {
            Frost_Bolt().simfell_name: Frost_Bolt(),
            Cold_Snap().simfell_name: Cold_Snap(),
            Freezing_Torrent().simfell_name: Freezing_Torrent(),
            # Bursting_Ice().simfell_name: Bursting_Ice(),
            Glacial_Blast().simfell_name: Glacial_Blast(),
            Ice_Comet().simfell_name: Ice_Comet(),
            # Dance_Of_Swallows().simfell_name: Dance_Of_Swallows(),
            # ce_Blitz().simfell_name: Ice_Blitz(),
        }
        # I couldn't find a clean way to handle this. Up for solutions.
        for spell in self.spells.values():
            spell.character = self

    def gain_anima(self, amount):
        self.anima += amount
        if self.anima >= 10:
            self.anima = 0
            self.gain_winter_orbs(1)
            # TODO: Cast Anima Spikes.

    def gain_winter_orbs(self, amount):
        self.winter_orbs += amount
        if self.winter_orbs > 5:
            self.winter_orbs = 5

    def lose_winter_orbs(self, amount):
        self.winter_orbs -= amount
        if self.winter_orbs < 0:
            self.winter_orbs = 0


# Defines the RimeSpell class.
# Rime gains anima for casting spells and uses winter_orbs to cast spells.
class RimeSpell(BaseSpell):
    """Base information for Rime Spells"""

    anima_gain = 0
    winter_orb_cost = 0
    anima_per_tick = 0

    def __init__(
        self,
        *args,
        anima_gain=0,
        winter_orb_cost=0,
        anima_per_tick=0,
        **kwargs,
    ):
        self.anima_gain = anima_gain
        self.winter_orb_cost = winter_orb_cost
        self.anima_per_tick = anima_per_tick
        super().__init__(*args, **kwargs)

    def is_ready(self):
        return (
            super().is_ready()
            and self.character.winter_orbs >= self.winter_orb_cost
        )

    def on_cast_complete(self, character):
        character.gain_anima(self.anima_gain)  # Gain Anima on Complete.
        if self.winter_orb_cost > 0:  # Lose Winter Orbs on Complete.
            character.lose_winter_orbs(self.winter_orb_cost)
        if self.winter_orb_cost < 0:  # Gain Winter Orbs on Complete.
            character.gain_winter_orbs(abs(self.winter_orb_cost))


class Frost_Bolt(RimeSpell):
    """Frost Bolt Spell"""

    def __init__(self):
        super().__init__(
            "Frost Bolt", cast_time=1.5, damage_percent=73, anima_gain=3
        )


class Cold_Snap(RimeSpell):
    """Cold Snap Spell"""

    def __init__(self):
        super().__init__("Cold Snap", damage_percent=219, winter_orb_cost=-1)


class Freezing_Torrent(RimeSpell):
    """Freezing Torrent Spell"""

    # TODO: Future note to myself in the future:
    # I need to code PPM for Soulfrost.

    def __init__(self):
        super().__init__(
            "Freezing Torrent",
            cast_time=2.0,
            cooldown=10,
            damage_percent=390,
            anima_per_tick=1,
            channeled=True,
            ticks=6,
        )

    def on_tick(self, character):
        character.anima += self.anima_per_tick


# TODO: Make this a Debuff instead of a Spell.
class Bursting_Ice(RimeSpell):
    """Bursting Ice Spell"""

    def __init__(self):
        super().__init__(
            "Bursting Ice",
            cast_time=2.0,
            cooldown=15,
            damage_percent=366,
            anima_per_tick=1,
            ticks=6,
            duration=3,
        )


class Glacial_Blast(RimeSpell):
    """Glacial Blast Spell"""

    def __init__(self):
        super().__init__(
            "Glacial Blast",
            cast_time=2.0,
            damage_percent=504,
            winter_orb_cost=2,
        )

    def crit_chance_modifiers(self, character, crit_chance):
        if "Glacial Assault" in character.talents:
            crit_chance += 20
        return crit_chance


class Ice_Comet(RimeSpell):
    """Ice Comet Spell"""

    def __init__(self):
        super().__init__("Ice Comet", damage_percent=300, winter_orb_cost=3)


class Dance_Of_Swallows(RimeSpell):
    """Dance of Swallows Spell"""

    def __init__(self):
        super().__init__(
            "Dance of Swallows",
            cooldown=60,
            damage_percent=53,
            winter_orb_cost=2,
        )


class Ice_Blitz(RimeSpell):
    """Ice Blitz Spell"""

    def __init__(self):
        super().__init__("Ice Blitz", cooldown=120, damage_percent=73)

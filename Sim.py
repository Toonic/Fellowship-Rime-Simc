"""Simulates the character's damage output."""

import random
from copy import deepcopy
from base import Character, Spell


class Simulation:
    """Simulates the character's damage output."""

    def __init__(
        self,
        character: Character,
        duration: int,
        enemy_count: int = 1,
        do_debug: bool = True,
        is_deterministic: bool = False,
    ):
        self.character = character
        self.time = 0
        self.duration = duration
        self.total_damage = 0
        self.do_debug = do_debug
        self.gcd = 0
        self.debuffs = []
        self.buffs = []
        self.enemy_count = enemy_count
        self.is_deterministic = is_deterministic

        self.damage_table = {}

        if is_deterministic:
            self.character.crit = 0
            self.character.spirit = 0

    def _fill_damage_table(self, key: str, damage: float) -> None:
        """Fill the damage table with the given key and damage."""

        self.damage_table[key] = self.damage_table.get(key, 0) + damage

    # Whenever we gain orbs, we want to cast 3 Anime Spikes.
    def gain_orb(self, do_spikes=True) -> None:
        """Ensures orb is gained during cast"""

        self.character.winter_orbs += 1
        if self.do_debug:
            print(
                f"Time {self.time:.2f}: Gained Orbs - "
                + f"Count: {self.character.winter_orbs}"
            )
        self.update_time(0.01)

        if do_spikes:
            for _ in range(self.character.spells["anima spikes"].hits):
                damage = self.character.spells["anima spikes"].damage(
                    self.character
                )
                self.total_damage += damage
                self._fill_damage_table(
                    self.character.spells["anima spikes"].name, damage
                )

                if self.do_debug:
                    print(
                        f"Time {self.time:.2f}: "
                        + f"Cast {self.character.spells['anima spikes'].name},"
                        + f" dealing {damage:.2f} damage"
                    )

        # If we are capped on Orbs, cap on 5.
        if self.character.winter_orbs > 5:
            if self.do_debug:
                print("Over capped on Orbs")
            self.character.winter_orbs = 5

    def lose_orb(self, orb_cost):
        """Ensures orb is lost during cast"""

        for _ in range(orb_cost):
            self.character.winter_orbs -= 1
            if "Wisdom of the North" in self.character.talents:
                for spell in self.character.rotation:
                    if spell.name in (
                        "Ice Blitz",
                        "Dance of Swallows",
                        "Winters Blessing",
                    ):
                        spell.update_cooldown(1)  # Reduces the cooldown by 1.
        if orb_cost > 0 and self.do_debug:
            print(
                f"Time {self.time:.2f}: Used Orbs - "
                + f"Count: {self.character.winter_orbs}"
            )
        if orb_cost > 0 and random.uniform(0, 100) < self.character.spirit:
            for _ in range(orb_cost):
                self.gain_orb()

    # Handle all Damage.
    def do_damage(
        self,
        spell: Spell,
        damage: float,
        anima_gained: float,
        orb_cost: int,
        is_cast: bool = True,
    ) -> None:
        """Does damage to the enemy (dummy)"""

        damage = self.apply_damage_multipliers(spell, damage)
        self.apply_glacial_assault(spell)
        self.update_spell_cooldowns(spell)
        aoe_count = self.determine_aoe_count(spell)

        for i in range(aoe_count):
            damage = self.apply_critical_hit(spell, damage)
            damage = self.apply_aoe_damage_reduction(spell, damage, i)
            self.total_damage += damage
            self._fill_damage_table(spell.name, damage)

        self.manage_mana_and_orbs(spell, anima_gained, orb_cost)
        self.handle_debug_output(spell, damage, is_cast)

    def apply_damage_multipliers(self, spell: Spell, damage: float) -> float:
        """Apply damage multipliers based on active buffs and talents."""

        damage_multipliers = {
            "Wrath of Winter": 1.15,
            "Ice Blitz": (
                1.25
                if "Wisdom of the North" in self.character.talents
                else 1.15
            ),
            "Soulfrost Torrent": (
                1.2 if "Chillblain" in self.character.talents else 1.0
            ),
            "Freezing Torrent": (
                1.2 if "Chillblain" in self.character.talents else 1.0
            ),
            "Bursting Ice": (
                1.2 if "Coalescing Ice" in self.character.talents else 1.0
            ),
        }

        for buff in self.buffs:
            if buff.name in damage_multipliers:
                damage *= damage_multipliers[buff.name]

        if "Avalanche" in self.character.talents and spell.name == "Ice Comet":
            # Multiply by:
            # - 3x if the crit hits 8% of the time
            # - 2x if it hits 30% of the time
            # - 1x otherwise.
            damage *= (
                3
                if random.uniform(0, 100) < 8
                else 2 if random.uniform(0, 100) < 30 else 1
            )
        return damage

    def apply_glacial_assault(self, spell: Spell) -> None:
        """Apply Glacial Assault buff if conditions are met."""

        if (
            spell.name == "Cold Snap"
            and "Glacial Assault" in self.character.talents
        ):
            self.character.glacial_assault_buff.apply_debuff()
            self.buffs.append(self.character.glacial_assault_buff)

    def update_spell_cooldowns(self, spell: Spell) -> None:
        """Update cooldowns for specific spells."""

        cooldown_updates = {
            "Unrelenting Ice": ("Bursting Ice", 0.5),
            "Icy Flow": ("Freezing Torrent", 0.2),
        }

        for talent, (spell_name, cooldown) in cooldown_updates.items():
            if talent in self.character.talents and spell.name in (
                "Soulfrost Torrent",
                "Freezing Torrent",
                "Anima Spikes",
                "Dance of Swallows",
            ):
                for character_spell in self.character.rotation:
                    if character_spell.name == spell_name:
                        character_spell.update_cooldown(cooldown)

    def determine_aoe_count(self, spell: Spell) -> int:
        """Determine the number of targets affected by AoE spells."""

        return {
            "Ice Comet": self.enemy_count,
            "Bursting Ice": self.enemy_count,
            "Soulfrost Torrent": (
                min(self.enemy_count, 5)
                if "Chillblain" in self.character.talents
                else 1
            ),
            "Freezing Torrent": (
                min(self.enemy_count, 5)
                if "Chillblain" in self.character.talents
                else 1
            ),
        }.get(spell.name, 1)

    def apply_critical_hit(self, spell: Spell, damage: float) -> float:
        """Calculate and apply critical hit damage."""

        crit_chance = self.character.crit
        if "Soulfrost Torrent" in self.character.talents and spell.name in (
            "Anima Spikes",
            "Dance of Swallows",
        ):
            crit_chance += 10 if not self.is_deterministic else 0
        if (
            spell.name == "Glacial Blast"
            and "Glacial Assault" in self.character.talents
        ):
            crit_chance += 20 if not self.is_deterministic else 0

        if random.uniform(0, 100) < crit_chance:
            damage *= 2
            if (
                "Soulfrost Torrent" in self.character.talents
                and random.uniform(0, 100) < 25
            ):
                if not any(
                    buff.name == "Soulfrost Torrent" for buff in self.buffs
                ):
                    self.character.soulfrost_buff.apply_debuff()
                    self.buffs.append(self.character.soulfrost_buff)
        return damage

    def apply_aoe_damage_reduction(
        self, spell: Spell, damage: float, index: int
    ) -> float:
        """Apply AoE damage reduction if applicable."""

        if (
            spell.name in ("Soulfrost Torrent", "Freezing Torrent")
            and "Chillblain" in self.character.talents
            and index != 0
        ):
            damage *= 0.2
        return damage

    def manage_mana_and_orbs(
        self, spell: Spell, anima_gained: float, orb_cost: int
    ) -> None:
        """Manage mana and orb resources."""

        if (
            spell.name == "Bursting Ice"
            and "Coalescing Ice" in self.character.talents
            and self.enemy_count == 1
        ):
            self.character.mana += 2
        self.character.mana += anima_gained

        anima_spikes = self.character.spells["anima spikes"]

        for buff in self.buffs:
            if buff.name == "Ice Blitz":
                for _ in range(int(anima_gained)):
                    damage = anima_spikes.damage(self.character)
                    self.total_damage += damage
                    self._fill_damage_table(anima_spikes.name, damage)

                    if self.do_debug:
                        print(
                            f"Time {self.time:.2f}: "
                            + f"Cast {anima_spikes.name}, "
                            + f"dealing {damage:.2f} damage"
                        )

        if orb_cost < 0:
            self.gain_orb()
        else:
            self.lose_orb(orb_cost)

        if self.character.mana >= 10:
            self.character.mana = 0
            self.gain_orb()

        if spell.name == "Cold Snap":
            for _ in range(10):
                self.do_dance_of_swallows()
        elif spell.name == "Freezing Torrent":
            self.do_dance_of_swallows()

    def handle_debug_output(
        self, spell: Spell, damage: float, is_cast: bool
    ) -> None:
        """Output debug information if debugging is enabled."""
        if self.do_debug:
            action = "hit" if is_cast else "ticks"
            print(
                f"Time {self.time:.2f}: Your {spell.name} {action} for "
                + f"{damage:.2f} damage"
            )

    def do_dance_of_swallows(self) -> None:
        """Handles the Dance of Swallows."""

        for debuff in self.debuffs:
            if debuff.name == "Dance of Swallows":
                self.do_damage(debuff, debuff.damage(self.character), 0, 0)

    def update_time(self, delta_time: int) -> None:
        """Updates the time and cooldowns."""

        self.time += delta_time
        self.gcd -= delta_time

        # Update spell cooldowns
        for spell in self.character.rotation:
            spell.update_cooldown(delta_time)

        # Process debuffs
        for (
            debuff
        ) in self.debuffs:  # Iterate over a copy to avoid modification issues
            debuff.update_remaining_debuff_duration(delta_time)
            # Handle multiple ticks within the delta_time interval
            if debuff.ticks > 0:
                while (
                    self.time >= debuff.next_tick_time
                    and debuff.remaining_debuff_duration > 0
                ):
                    self.do_damage(
                        debuff,
                        debuff.damage(self.character) / debuff.ticks,
                        debuff.mana_generation / debuff.ticks,
                        debuff.winter_orb_cost,
                        False,
                    )
                    debuff.next_tick_time += (
                        debuff.debuff_duration / debuff.ticks
                    )  # Schedule next tick

            # Remove expired debuff
            if debuff.remaining_debuff_duration <= 0:
                if debuff in self.debuffs:
                    if self.do_debug:
                        print(f"Removing {debuff.name}")
                    self.debuffs.remove(debuff)

        # Process buffs similarly
        for buff in self.buffs:
            buff.update_remaining_debuff_duration(delta_time)

            if buff.ticks > 0:
                while self.time >= buff.next_tick_time:
                    if buff.name == "Wrath of Winter":
                        self.gain_orb()
                buff.next_tick_time += (
                    buff.debuff_duration / buff.ticks
                )  # Schedule next tick

            if buff.remaining_debuff_duration <= 0:
                self.buffs.remove(buff)

                # Hacky Buff Handling
                if buff.name == "Wrath of Winter":
                    self.character.haste -= 30

    # Generic Run
    def run(self) -> float:
        """Runs the simulation."""

        for spell in self.character.rotation:
            spell.reset_cooldown()

        for spell in self.character.spells.values():
            self.damage_table[spell.name] = 0

        while self.time < self.duration:
            if self.gcd > 0:
                self.update_time(self.gcd)

            # Locate a spell that we can cast.
            spell = next(
                (
                    s
                    for s in self.character.rotation
                    if s.is_ready(self.character, self.enemy_count)
                ),
                None,
            )

            if spell is not None:
                check = False

                # Check for spells
                for test_spell in self.character.rotation:
                    if spell.name != test_spell.name:
                        if (
                            spell.effective_cast_time(self.character) == 0
                            and test_spell.remaining_cooldown > 0
                            and test_spell.remaining_cooldown
                            < (1.5 / (1 + self.character.haste / 100))
                        ):
                            if self.do_debug:
                                print(
                                    f"Waiting for {test_spell.name} "
                                    + "(GCD Trigger)"
                                )
                            self.update_time(test_spell.remaining_cooldown)
                            check = True
                            break

                        if (
                            test_spell.remaining_cooldown
                            < spell.effective_cast_time(self.character)
                            and test_spell.remaining_cooldown > 0
                        ):
                            if self.do_debug:
                                print(f"Waiting for {test_spell.name}")
                            self.update_time(test_spell.remaining_cooldown)
                            check = True
                            break
                    else:
                        break

                if check:
                    continue

            if spell is None:
                if self.do_debug:
                    print(f"Time {self.time:.2f}: No ready spell available")
                self.update_time(0.1)
                continue

            self.gcd = 1.5 / (1 + self.character.haste / 100)

            if self.do_debug:
                print(f"Time {self.time:.2f}: Cast {spell.name}.")

            non_boosted_spell = None

            # Replace Freezing Torrent with Soulfrost if applicable
            if spell.name == "Freezing Torrent" and any(
                buff.name == "Soulfrost Torrent" for buff in self.buffs
            ):
                non_boosted_spell = deepcopy(spell)
                spell = self.character.soulfrost
                # Remove Soulfrost from buffs
                self.buffs = [
                    buff
                    for buff in self.buffs
                    if buff.name != "Soulfrost Torrent"
                ]

            # Replace Glacial Blast with Boosted Blast if applicable
            elif (
                spell.name == "Glacial Blast"
                and "Glacial Assault" in self.character.talents
            ):
                glacial_assault_count = sum(
                    1 for buff in self.buffs if buff.name == "Glacial Assault"
                )
                if glacial_assault_count == 4:
                    self.buffs = [
                        buff
                        for buff in self.buffs
                        if buff.name != "Glacial Assault"
                    ]
                    non_boosted_spell = deepcopy(spell)
                    spell = self.character.boosted_blast

            self.update_time(0.01)

            if spell.channeled:
                # Cast -> Cooldown Starts -> Channel Starts
                # -> Channel Finished -> Done.

                if non_boosted_spell:
                    non_boosted_spell.set_cooldown()
                else:
                    spell.set_cooldown()

                for _ in range(spell.ticks):
                    self.do_damage(
                        spell,
                        spell.damage(self.character) / spell.ticks,
                        spell.mana_generation / spell.ticks,
                        spell.winter_orb_cost,
                    )
                    self.update_time(
                        spell.effective_cast_time(self.character) / spell.ticks
                    )

            elif spell.is_debuff:
                self.update_time(spell.effective_cast_time(self.character))
                spell.apply_debuff()
                if spell.winter_orb_cost > 0:
                    self.lose_orb(spell.winter_orb_cost)
                if spell.ticks > 0:
                    spell.next_tick_time = (
                        self.time + spell.debuff_duration / spell.ticks
                    )
                self.debuffs.append(spell)

                if non_boosted_spell:
                    non_boosted_spell.set_cooldown()
                else:
                    spell.set_cooldown()

            elif spell.is_buff:
                # Cast -> Cast Duration Starts -> "Hits"
                # -> Cooldown Starts -> Done

                self.update_time(spell.effective_cast_time(self.character))
                # Lazy coding
                spell.apply_debuff()
                if spell.ticks > 0:
                    spell.next_tick_time = (
                        self.time + spell.debuff_duration / spell.ticks
                    )
                self.buffs.append(spell)

                # Hacky Buff Coding
                if spell.name == "Wrath of Winter":
                    self.character.haste += 30

                if non_boosted_spell:
                    non_boosted_spell.set_cooldown()
                else:
                    spell.set_cooldown()
            else:
                # Cast -> Cast Duration Starts -> "Hits"
                # -> Cooldown Starts -> Done

                self.update_time(spell.effective_cast_time(self.character))
                self.do_damage(
                    spell,
                    spell.damage(self.character),
                    spell.mana_generation,
                    spell.winter_orb_cost,
                )

                if non_boosted_spell:
                    non_boosted_spell.set_cooldown()
                else:
                    spell.set_cooldown()

        dps = self.total_damage / self.duration
        if self.do_debug:
            print(f"Total Damage: {self.total_damage:.2f}, DPS: {dps:.2f}")

        return dps

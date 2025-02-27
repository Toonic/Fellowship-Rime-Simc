import random

from base import Character, Spell

# from copy import copy


class Simulation:
    def __init__(
        self,
        character: Character,
        duration: int,
        enemy_count: int = 1,
        do_debug: bool = True,
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

    # Whenever we gain orbs, we want to cast 3 Anime Spikes.
    def gain_orb(self, do_spikes=True):
        """Ensures orb is gained during cast"""

        self.character.winter_orbs += 1
        if self.do_debug:
            print(
                f"Time {self.time:.2f}: Gained Orbs - "
                + f"Count: {self.character.winter_orbs}"
            )
        self.update_time(0.01)
        if do_spikes:
            for _ in range(self.character.anima_spikes.hits):
                damage = self.character.anima_spikes.damage(self.character)
                self.total_damage += damage
                if self.do_debug:
                    print(
                        f"Time {self.time:.2f}: "
                        + f"Cast {self.character.anima_spikes.name}, "
                        + f"dealing {damage:.2f} damage"
                    )

        # If we are capped on Orbs, cap on 5.
        if self.character.winter_orbs > 5:
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
    ):
        """Does damage to the enemy (dummy)"""
        for buff in self.buffs[:]:
            # If we have Wrath of Winter active. Deal 15% more damage.
            if buff.name == "Wrath of Winter":
                damage *= 1.15
            if buff.name == "Ice Blitz":
                if "Wisdom of the North" in self.character.talents:
                    damage *= 1.25
                else:
                    damage *= 1.15

        if (
            spell.name in ("Soulfrost Torrent", "Freezing Torrent")
            and "Chillblain" in self.character.talents
        ):
            damage *= 1.2

        if (
            spell.name == "Bursting Ice"
            and "Coalescing Ice" in self.character.talents
        ):
            damage *= 1.2

        if "Avalanche" in self.character.talents and spell.name == "Ice Comet":
            if random.uniform(0, 100) < 30:
                if random.uniform(0, 100) < 8:
                    damage *= 3
                else:
                    damage *= 2

        if (
            spell.name == "Cold Snap"
            and "Glacial Assault" in self.character.talents
        ):
            self.character.glacial_assault_buff.apply_debuff()
            self.buffs.append(self.character.glacial_assault_buff)

        if (
            spell.name in ("Soulfrost Torrent", "Freezing Torrent")
            and "Unrelenting Ice" in self.character.talents
        ):
            # The previous name "spell" colidited with
            # already defined variable.
            for character_spell in self.character.rotation:
                if character_spell.name == "Bursting Ice":
                    character_spell.update_cooldown(0.5)

        if "Icy Flow" in self.character.talents and (
            spell.name in ("Anima Spikes", "Dance of Swallows")
        ):
            # The previous name "spell" colidited with
            # already defined variable.
            for character_spell in self.character.rotation:
                if character_spell.name == "Freezing Torrent":
                    character_spell.update_cooldown(0.2)

        aoe_count = 1
        if spell.name == "Ice Comet":
            aoe_count = self.enemy_count
        if (
            spell.name in ("Soulfrost Torrent", "Freezing Torrent")
            and "Chillblain" in self.character.talents
        ):
            aoe_count = min(self.enemy_count, 5)
        if spell.name == "Bursting Ice":
            aoe_count = self.enemy_count

        for i in range(aoe_count):
            # Crit Calcs
            crit_chance = self.character.crit

            # Check if Soulfrost Torrent to modify Anima Spikes.
            if "Soulfrost Torrent" in self.character.talents and (
                spell.name in ("Anima Spikes", "Dance of Swallows")
            ):
                crit_chance += 10
            if (
                spell.name == "Glacial Blast"
                and "Glacial Assault" in self.character.talents
            ):
                crit_chance += 20

            # Roll the Crit.
            if random.uniform(0, 100) < crit_chance:
                damage *= 2  # Critical hit
                # Roll for Soulfrost Torrent buff.
                can_apply = True
                if (
                    "Soulfrost Torrent" in self.character.talents
                    and random.uniform(0, 100) < 25
                ):
                    for buff in self.buffs:
                        if buff.name == "Soulfrost Torrent":
                            can_apply = False
                    if can_apply:
                        self.character.soulfrost_buff.apply_debuff()
                        self.buffs.append(self.character.soulfrost_buff)

            # Do other stuff.
            if (
                spell.name in ("Soulfrost Torrent", "Freezing Torrent")
                and "Chillblain" in self.character.talents
                and i != 0
            ):
                damage = damage * 0.2
            self.total_damage += damage

        if (
            spell.name == "Bursting Ice"
            and "Coalescing Ice" in self.character.talents
            and self.enemy_count == 1
        ):
            self.character.mana += 2
        self.character.mana += anima_gained
        for buff in self.buffs[:]:
            if buff.name == "Ice Blitz":
                for i in range(int(anima_gained)):
                    damage = self.character.anima_spikes.damage(self.character)
                    self.total_damage += damage
                    if self.do_debug:
                        print(
                            f"Time {self.time:.2f}: "
                            + f"Cast {self.character.anima_spikes.name}, "
                            + f"dealing {damage:.2f} damage"
                        )

        if self.do_debug:
            if is_cast:
                print(
                    f"Time {self.time:.2f}: Your {spell.name} hit "
                    + f"for {damage:.2f} damage"
                )
            else:
                print(
                    f"Time {self.time:.2f}: Your {spell.name} ticks "
                    + f"for {damage:.2f} damage"
                )

        if orb_cost < 0:
            self.gain_orb()
        else:
            self.lose_orb(orb_cost)

        if self.character.mana >= 10:
            self.character.mana = 0
            self.gain_orb()

        if spell.name == "Cold Snap":
            for i in range(10):
                self.do_dance_of_swallows()
        if spell.name == "Freezing Torrent":
            self.do_dance_of_swallows()

    def do_dance_of_swallows(self):
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

        while self.time < self.duration:
            spell = None

            if self.gcd > 0:
                self.update_time(self.gcd)

            # Locate a spell that we can cast.
            for candidate_spell in self.character.rotation:
                if candidate_spell.is_ready(self.character, self.enemy_count):
                    spell = candidate_spell
                    break

            if spell is None:
                if self.do_debug:
                    print(f"Time {self.time:.2f}: No ready spell available")
                continue

            self.gcd = 1.5 / (1 + self.character.haste / 100)

            # Update the cooldown on the spell.
            if self.do_debug:
                print(f"Time {self.time:.2f}: Cast {spell.name}.")
            spell.set_cooldown()

            # Check to see if replacing Freezing with Soulfrost Torrent
            if spell.name == "Freezing Torrent":
                for buff in self.buffs[:]:
                    if buff.name == "Soulfrost Torrent":
                        spell = self.character.soulfrost
                        self.buffs.remove(buff)

            # Check to see if replacing Blast with Better Blast
            glacial_assault_count = 0
            if (
                spell.name == "Glacial Blast"
                and "Glacial Assault" in self.character.talents
            ):
                for buff in self.buffs:
                    if buff.name == "Glacial Assault":
                        glacial_assault_count += 1
                if glacial_assault_count == 5:
                    for buff in self.buffs[:]:
                        if buff.name == "Glacial Assault":
                            self.buffs.remove(buff)
                    spell = self.character.boosted_blast

            self.update_time(0.01)

            if spell.channeled:
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
            elif spell.is_buff:
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
            else:
                self.update_time(spell.effective_cast_time(self.character))
                self.do_damage(
                    spell,
                    spell.damage(self.character),
                    spell.mana_generation,
                    spell.winter_orb_cost,
                )

        dps = self.total_damage / self.duration
        if self.do_debug:
            print(f"Total Damage: {self.total_damage:.2f}, DPS: {dps:.2f}")
        return dps

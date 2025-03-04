from typing import Dict, List
from base.spell import BaseDebuff


class Simulation:
    def __init__(self, character, duration=180, enemyCount=1, doDebug=False):
        self.character = character
        character.set_simulation(self)
        self.duration = duration
        self.enemyCount = enemyCount
        self.doDebug = doDebug
        self.time = 0
        self.gcd = 0
        self.abilityQueue = []
        self.debuffs: Dict[str, BaseDebuff] = {}
        self.damage = 0

    def update_time(self, delta_time: float):
        delta_time = round(delta_time, 2)
        self.time += delta_time
        self.gcd -= delta_time

        # Update spell cooldowns
        for spell in self.character.spells.values():
            spell.update_cooldown(delta_time)

        # Update Players Buffs
        for buff_key in list(self.character.buffs.keys()):
            buff = self.character.buffs.get(buff_key)
            buff.update_remaining_duration(delta_time)

        # Update Debuffs on an Enemy.
        # TODO: In the future we will want to keep track of each enemy and each debuff
        #      This will be important for Multi-Dotting  in the future.

        for debuff_key in list(self.debuffs.keys()):
            print(debuff_key)
            debuff = self.debuffs.get(debuff_key)
            debuff.update_remaining_duration(delta_time)

    def run(self):
        while self.time <= self.duration:
            if self.gcd > 0:
                self.update_time(self.gcd)

            for spell in self.character.rotation:
                if self.character.spells[spell].is_ready():
                    print(
                        f"Time {self.time:.2f}: "
                        + f"Casting {self.character.spells[spell].name}. "
                    )
                    self.character.spells[spell].cast()
                    break
            else:
                self.update_time(0.1)

        print(self.damage / self.duration)

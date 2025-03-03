class Simulation:
    def __init__(self, character, duration=180, enemyCount=1, doDebug=False):
        self.character = character
        character.set_simulation(self)
        self.duration = duration
        self.enemyCount = enemyCount
        self.doDebug = doDebug
        self.time = 0
        self.abilityQueue = []
        self.buffs = []
        self.debuffs = []

    def update_time(self, delta_time):
        self.time += delta_time
        # self.gcd -= delta_time

        # Update spell cooldowns
        for spell in self.character.spells.values():
            spell.update_cooldown(delta_time)

        # TODO: Update Players Buffs

        # TODO: Update Debuffs on All Enemies.

    def run(self):
        while self.time < self.duration:
            for spell in self.character.rotation:
                if self.character.spells[spell].is_ready():
                    self.character.spells[spell].cast()
                    print(
                        f"Time {self.time:.2f}: "
                        + f"Casting {self.character.spells[spell].name}. "
                    )
                    break
            else:
                self.update_time(0.1)

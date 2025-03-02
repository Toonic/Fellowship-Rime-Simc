class Simulation:
    def __init__(self, character, duration=180, enemyCount=1, doDebug=False):
        self.character = character
        self.duration = duration
        self.enemyCount = enemyCount
        self.doDebug = doDebug
        self.time = 0
        self.abilityQueue = []
        self.buffs = []
        self.debuffs = []

    def run(self):
        while self.time < self.duration:
            self.time += 1

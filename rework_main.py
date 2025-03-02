from characters.Rime import Rime
from rework_sim import Simulation


def main():
    print("----------------------------")
    print("Starting new Sim")
    print("----------------------------")
    ## Create your character below by plugging in their Point Stats, not % Stats.

    character = Rime(100, 100, 100, 100, 100)

    debug_sim(character)


def debug_sim(character):
    sim = Simulation(character, duration=120, doDebug=True)
    sim.run()


if __name__ == "__main__":
    main()

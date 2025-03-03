from characters.Rime import Rime
from characters.Rime.rime import FrostBolt, IceBlitz
from rework_sim import Simulation


def main():
    print("----------------------------")
    print("Starting new Sim")
    print("----------------------------")
    ## Create your character below by plugging in their Point Stats, not % Stats.

    # TODO: Parse this in from the SimFell File and or the other way.
    character = Rime(100, 100, 100, 100, 100)
    # TODO: This should be a list of SimFell Actions.
    character.rotation.append(IceBlitz().simfell_name)
    character.rotation.append(FrostBolt().simfell_name)

    debug_sim(character)


def debug_sim(character):
    sim = Simulation(character, duration=180, doDebug=True)
    sim.run()


if __name__ == "__main__":
    main()

"""Test the parser."""

from simfell_parser.condition_parser import SimFileConditionParser
from simfell_parser.simfile_parser import SimFileParser


parser = SimFileParser("test.simfell")
configuration = parser.parse()
# print(configuration.parsed_json)


print(f"Character Anima: {configuration.character.anima}\n")

print("Summary of actions and results:")
for action in configuration.actions:
    # Action = Spell
    # Imagine like we are looping through character rotation

    print(f"Action: '{action.name}', Conditions: {len(action.conditions)}")

    character_result = SimFileConditionParser.evaluate_character(
        action.conditions, configuration.character
    )
    spell_result = SimFileConditionParser.evaluate_spell(
        action.conditions,
        configuration.character,
    )

    print(f"\tCharacter Result: {character_result}")
    print(f"\tSpell Result: {spell_result}")
    print("\t=====================\n")

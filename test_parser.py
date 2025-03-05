"""Test the parser."""

from simfell_parser.condition_parser import SimFileConditionParser
from simfell_parser.simfile_parser import SimFileParser
from simfell_parser.utils import SpellTypeT


parser = SimFileParser("test.simfell")
configuration = parser.parse()
# print(configuration.parsed_json)


print(f"Character Anima: {configuration.character.anima}\n")

print("Summary of actions and results:")
for action in configuration.actions:
    # Action = Spell
    # Imagine like we are looping through character rotation

    print(f"Action: '{action.name}', Conditions: {len(action.conditions)}")

    spell: SpellTypeT = configuration.character.spells.get(
        action.name.split("/")[1], None
    )
    if not spell:
        print(f"Spell '{action.name}' not found in character spells")
        continue

    character_result = SimFileConditionParser.evaluate_character(
        action.conditions, configuration.character
    )
    spell_result = SimFileConditionParser.evaluate_spell(
        action.conditions,
        configuration.character,
    )

    is_spell_ready = spell.is_ready()

    print(f"\tCharacter Result: {character_result}")
    print(f"\tSpell Result: {spell_result}")
    print(f"\tSpell Ready: {is_spell_ready}")
    print("\t=====================\n")

from collections.abc import Callable

# Every spell follows the same contract: (target, power) -> description
Spell = Callable[[str, int], str]


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target} for {power} damage"


def heal(target: str, power: int) -> str:
    return f"Heal restores {target} for {power} HP"


def spell_combiner(
    spell1: Spell, spell2: Spell
) -> Callable[[str, int], tuple[str, str]]:
    def combined(target: str, power: int) -> tuple[str, str]:
        result_1: str = spell1(target, power)
        result_2: str = spell2(target, power)
        return (result_1, result_2)

    return combined


def power_amplifier(base_spell: Spell, multiplier: int) -> Spell:
    def amplify(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)

    return amplify


def conditional_caster(
    condition: Callable[[str, int], bool], spell: Spell
) -> Spell:
    def cast(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"

    return cast


def spell_sequence(spells: list[Spell]) -> Callable[[str, int], list[str]]:
    def combined(target: str, power: int) -> list[str]:
        return [s(target, power) for s in spells]

    return combined


def main() -> None:
    print("Testing spell combiner...")
    combined = spell_combiner(fireball, heal)
    hit, restore = combined("Dragon", 50)
    print(f"Combined spell result: {hit}, {restore}")

    print("\nTesting power amplifier...")
    mega_fireball = power_amplifier(fireball, 3)
    print(f"Original: {fireball('Dragon', 10)}")
    print(f"Amplified: {mega_fireball('Dragon', 10)}")

    print("\nTesting conditional caster...")
    powerful = conditional_caster(lambda target, power: power >= 20, fireball)
    print(f"power 50: {powerful('Dragon', 50)}")
    print(f"power 5:  {powerful('Dragon', 5)}")

    print("\nTesting spell sequence...")
    barrage = spell_sequence([fireball, heal, fireball])
    for result in barrage("Dragon", 30):
        print(result)


if __name__ == "__main__":
    main()

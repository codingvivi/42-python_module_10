from collections.abc import Callable
from typing import Any


def mage_counter() -> Callable:
    count: int = 0

    def increment() -> int:
        nonlocal count
        count += 1
        return count

    return increment


def spell_accumulator(initial_power: int) -> Callable:
    total_power: int = initial_power

    def power_up(increase: int) -> int:
        nonlocal total_power
        total_power += increase

        return total_power

    return power_up


def enchantment_factory(enchantment_type: str) -> Callable:
    def enchant(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"

    return enchant


def memory_vault() -> dict[str, Callable]:
    vault: dict[str, Any] = {}

    def _save(key: str, value: Any):
        nonlocal vault
        vault[key] = value

    def _load(key: str) -> Any:
        nonlocal vault
        return vault.get(key) if key in vault else "Memory not found"

    return {"store": _save, "recall": _load}


def main() -> None:
    print("Testing mage counter...")
    counter_a = mage_counter()
    counter_b = mage_counter()
    print(f"counter_a call 1: {counter_a()}")
    print(f"counter_a call 2: {counter_a()}")
    print(f"counter_b call 1: {counter_b()}")

    print("\nTesting spell accumulator...")
    accumulate = spell_accumulator(100)
    print(f"Base 100, add 20: {accumulate(20)}")
    print(f"Base 100, add 30: {accumulate(30)}")

    print("\nTesting enchantment factory...")
    flaming = enchantment_factory("Flaming")
    frozen = enchantment_factory("Frozen")
    print(flaming("Sword"))
    print(frozen("Shield"))

    print("\nTesting memory vault...")
    vault = memory_vault()
    vault["store"]("secret", 42)
    print("Store 'secret' = 42")
    print(f"Recall 'secret': {vault['recall']('secret')}")
    print(f"Recall 'unknown': {vault['recall']('unknown')}")


if __name__ == "__main__":
    main()

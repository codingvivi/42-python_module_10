import functools
import operator
from collections.abc import Callable
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0
    ops: dict[str, Callable[[int, int], int]] = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": max,
        "min": min,
    }
    if operation not in ops:
        raise ValueError(f"Unknown operation: {operation}")
    return functools.reduce(ops[operation], spells)


def partial_enchanter(
    base_enchantment: Callable[..., str],
) -> dict[str, Callable[..., str]]:
    out: dict[str, Callable[..., str]] = {
        element: functools.partial(base_enchantment, 50, element)
        for element in ["fire", "ice", "lightning"]
    }

    return out


@functools.lru_cache
def memoized_fibonacci(n: int) -> int:
    if n < 2:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    @functools.singledispatch
    def cast(spell: Any) -> str:
        return "Unknown spell type"

    @cast.register
    def _(spell: int) -> str:
        return f"{spell} damage"

    @cast.register
    def _(spell: str) -> str:
        return spell

    @cast.register(list)
    def _(spell: list[Any]) -> str:
        return f"{len(spell)} spells"

    return cast


def main() -> None:
    print("Testing spell reducer...")
    powers = [10, 20, 30, 40]
    print(f"Sum: {spell_reducer(powers, 'add')}")
    print(f"Product: {spell_reducer(powers, 'multiply')}")
    print(f"Max: {spell_reducer(powers, 'max')}")

    print("\nTesting partial enchanter...")

    def base_enchantment(power: int, element: str, target: str) -> str:
        return f"{element.title()} {target} (power {power})"

    enchanters = partial_enchanter(base_enchantment)
    print(enchanters["fire"]("Sword"))
    print(enchanters["ice"]("Shield"))

    print("\nTesting memoized fibonacci...")
    for n in (0, 1, 10, 15):
        print(f"Fib({n}): {memoized_fibonacci(n)}")
    print(memoized_fibonacci.cache_info())

    print("\nTesting spell dispatcher...")
    cast = spell_dispatcher()
    print(f"Damage spell: {cast(42)}")
    print(f"Enchantment: {cast('fireball')}")
    print(f"Multi-cast: {cast([1, 2, 3])}")
    print(cast(3.14))


if __name__ == "__main__":
    main()

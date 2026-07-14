import functools
import inspect
import time
from collections.abc import Callable
from typing import Any


def spell_timer(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    # args and keyword args
    # * collects into tuple, ** into dict
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Casting {func.__name__}...")
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"Spell completed in {elapsed:.3f} seconds")
        return result

    return wrapper


def power_validator(min_power: int) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        # Bind against the real signature so we find 'power' by name,
        # whether it is the first argument (standalone spell) or comes
        # after 'self' (instance method).
        signature = inspect.signature(func)

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            bound = signature.bind(*args, **kwargs)
            power = bound.arguments["power"]
            if power >= min_power:
                return func(*args, **kwargs)
            return "Insufficient power for this spell"

        return wrapper

    return decorator


def retry_spell(max_attempts: int) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt < max_attempts:
                        print(
                            "Spell failed, retrying... "
                            f"(attempt {attempt}/{max_attempts})"
                        )
            return f"Spell casting failed after {max_attempts} attempts"

        return wrapper

    return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        return len(name) >= 3 and all(c.isalpha() or c.isspace() for c in name)

    @power_validator(10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


def main() -> None:
    print("Testing spell timer...")

    @spell_timer
    def fireball() -> str:
        time.sleep(0.1)
        return "Fireball cast!"

    print(f"Result: {fireball()}")

    print("\nTesting retrying spell...")

    @retry_spell(3)
    def cursed_spell() -> str:
        raise RuntimeError("the mana is unstable")

    print(cursed_spell())

    misfires = {"count": 0}

    @retry_spell(3)
    def unstable_spell() -> str:
        misfires["count"] += 1
        if misfires["count"] < 2:
            raise RuntimeError("the mana is unstable")
        return "Waaaaaagh spelled !"

    print(unstable_spell())

    print("\nTesting MageGuild...")
    print(MageGuild.validate_mage_name("Merlin"))
    print(MageGuild.validate_mage_name("Al"))
    guild = MageGuild()
    print(guild.cast_spell("Lightning", 15))
    print(guild.cast_spell("Ember", 5))


if __name__ == "__main__":
    main()

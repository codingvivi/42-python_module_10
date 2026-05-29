import functools
import time
from collections.abc import Callable


def spell_timer(func: Callable) -> Callable:
    @functools.wraps(func)
    # args and keyword args
    # * collects into tuple, ** into dict
    def wrapper(*args, **kwargs):
        print(f"Casting {func.__name__}...")
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"Spell completed in {elapsed:.3f} seconds")
        return result

    return wrapper


def power_validator(min_power: int) -> Callable:
    def decorator(func):
        @functools.wraps(func)
        def wrapper(power, *args, **kwargs):
            return (
                func(power, *args, **kwargs)
                if power >= min_power
                else "Insufficient power for this spell"
            )

        return wrapper

    return decorator


def retry_spell(max_attempts: int) -> Callable:
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for a in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    print(f"{a} / {max_attempts}")
                    continue

            return f"Spell failed after {max_attempts}"

        return wrapper

    return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        return len(name) >= 3 and all(c.isalpha() or c.isspace() for c in name)

    @power_validator(3)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


def main() -> None: ...


if __name__ == "__main__":
    main()

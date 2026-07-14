from typing import Any


def artifact_sorter(artifacts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    # lambda arg: expression
    # always only one expression allowed!
    return sorted(artifacts, key=lambda a: a["power"], reverse=True)


def power_filter(
    mages: list[dict[str, Any]], min_power: int
) -> list[dict[str, Any]]:
    return list(filter(lambda m: m["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda s: f"* {s} *", spells))


def mage_stats(mages: list[dict[str, Any]]) -> dict[str, Any]:
    # Callable[[arg1, arg2, ...], ret]
    return {
        "max_power": max(mages, key=lambda m: m["power"])["power"],
        "min_power": min(mages, key=lambda m: m["power"])["power"],
        # map returns an iterable that sum then consumes
        "avg_power": round(
            sum(map(lambda m: m["power"], mages)) / len(mages), 2
        ),
    }


def main() -> None:
    # Lambda Sanctum Test Data
    artifacts = [
        {"name": "Shadow Blade", "power": 105, "type": "relic"},
        {"name": "Wind Cloak", "power": 108, "type": "relic"},
        {"name": "Earth Shield", "power": 110, "type": "focus"},
        {"name": "Ice Wand", "power": 86, "type": "weapon"},
    ]
    mages = [
        {"name": "Luna", "power": 64, "element": "shadow"},
        {"name": "Ember", "power": 79, "element": "lightning"},
        {"name": "Luna", "power": 84, "element": "lightning"},
        {"name": "Luna", "power": 57, "element": "fire"},
        {"name": "Kai", "power": 89, "element": "earth"},
    ]
    spells = ["fireball", "earthquake", "blizzard", "freeze"]

    print("Testing artifact sorter...")
    ranked = artifact_sorter(artifacts)
    for stronger, weaker in zip(ranked, ranked[1:], strict=False):
        print(
            f"{stronger['name']} ({stronger['power']} power) comes before "
            f"{weaker['name']} ({weaker['power']} power)"
        )

    print("\nTesting power filter...")
    strong_mages = power_filter(mages, 80)
    print(f"Mages with power >= 80: {[m['name'] for m in strong_mages]}")

    print("\nTesting spell transformer...")
    print(" ".join(spell_transformer(spells)))

    print("\nTesting mage stats...")
    print(mage_stats(mages))


if __name__ == "__main__":
    main()

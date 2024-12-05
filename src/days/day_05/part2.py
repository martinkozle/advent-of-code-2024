from functools import partial

from src.prep import run_with_prep
from src.timing import timing


def sort_key(rules_dict: dict[int, set[int]], elements: set[int], a: int) -> int:
    return len(rules_dict[a] & set(elements))


@timing
def main(inp: str) -> None:
    rules_str, updates_str = inp.split("\n\n")
    rules = [
        tuple(int(rule) for rule in rule_str.split("|"))
        for rule_str in rules_str.split("\n")
    ]
    updates = [
        list(map(int, update_str.split(","))) for update_str in updates_str.split("\n")
    ]

    rules_dict: dict[int, set[int]] = {}
    for left, right in rules:
        if left not in rules_dict:
            rules_dict[left] = set()
        rules_dict[left].add(right)

    total = 0

    for update in updates:
        correct = True
        lefts: set[int] = set()
        rights: set[int] = set(update)

        for number in update:
            lefts.add(number)
            rights.remove(number)
            for right_rule in rules_dict[number]:
                if right_rule in lefts:
                    correct = False
                    break

            if not correct:
                break

        if not correct:
            update_set = set(update)
            update.sort(key=partial(sort_key, rules_dict, update_set), reverse=True)
            total += update[len(update) // 2]

    print(total)


if __name__ == "__main__":
    run_with_prep(main)

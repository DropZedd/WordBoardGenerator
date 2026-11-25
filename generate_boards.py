import json
import random
from collections import defaultdict
from itertools import product
from pathlib import Path

COMMON_FILE = Path("common_words.txt")
ALL_FILE = Path("all_words.txt")
OUTPUT_FILE = Path("boards.json")
BOARD_LIMIT = 1500
MAX_WORDS_PER_BOARD = 24


def load_words(path, min_length=1, max_length=None):
    words = set()
    with path.open(encoding="utf-8") as file:
        for line in file:
            word = line.strip().upper()
            if word.isalpha() and len(word) >= min_length and (
                max_length is None or len(word) <= max_length
            ):
                words.add(word)
    return words


def signature(word):
    return "".join(sorted(word))


def main():
    if not COMMON_FILE.exists() or not ALL_FILE.exists():
        raise SystemExit(
            "Missing word lists. The GitHub Actions workflow downloads both "
            "common_words.txt and all_words.txt before running this script."
        )

    common_set = load_words(COMMON_FILE)
    full_dict = load_words(ALL_FILE, min_length=4, max_length=9)
    valid_words = full_dict

    # Index words by their sorted letters. This avoids scanning the entire
    # dictionary for every root while producing the same letter-multiset matches.
    words_by_signature = defaultdict(list)
    for word in valid_words:
        words_by_signature[signature(word)].append(word)

    root_candidates = sorted(
        word for word in common_set
        if 6 <= len(word) <= 8 and word in valid_words
    )
    random.shuffle(root_candidates)

    boards = []
    for root in root_candidates[:BOARD_LIMIT]:
        letters = sorted(set(root))
        limits = [root.count(char) for char in letters]
        matches = set()

        # Every valid sub-multiset of the root's letters maps directly to
        # possible dictionary words. No letters can be used more often than
        # they appear in the root.
        for counts in product(*(range(limit + 1) for limit in limits)):
            word_length = sum(counts)
            if not 4 <= word_length <= len(root):
                continue
            candidate_signature = "".join(
                char * count for char, count in zip(letters, counts)
            )
            matches.update(words_by_signature.get(candidate_signature, ()))

        common_matches = sorted(
            (word for word in matches if word in common_set),
            key=lambda word: (len(word), word),
        )
        obscure_matches = sorted(
            (word for word in matches if word not in common_set),
            key=lambda word: (len(word), word),
        )

        selected = common_matches[:MAX_WORDS_PER_BOARD]
        if len(selected) < 12:
            selected += obscure_matches[: max(0, 18 - len(selected))]

        if root not in selected:
            if selected:
                selected[-1] = root
            else:
                selected = [root]

        selected = sorted(set(selected), key=lambda word: (len(word), word))

        if len(selected) >= 8:
            boards.append({"root": root, "words": selected})

    with OUTPUT_FILE.open("w", encoding="utf-8") as output:
        json.dump(boards, output, ensure_ascii=False, separators=(",", ":"))

    print(f"Generated {len(boards)} boards from {len(root_candidates)} root candidates.")
    print(f"Saved output to {OUTPUT_FILE} ({OUTPUT_FILE.stat().st_size:,} bytes).")


if __name__ == "__main__":
    main()

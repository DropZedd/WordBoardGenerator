import json
import random
from collections import defaultdict
from itertools import product
from pathlib import Path

COMMON_FILE = Path("common_words.txt")
WOS_FILE = Path("wos_dictionary.txt")
OUTPUT_FILE = Path("boards.json")
BOARD_LIMIT = 1500
MAX_WORDS_PER_BOARD = 24
MIN_WORDS_PER_BOARD = 8


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
    if not COMMON_FILE.exists() or not WOS_FILE.exists():
        raise SystemExit(
            "Missing word lists. The GitHub Actions workflow downloads both "
            "common_words.txt and wos_dictionary.txt before running this script."
        )

    # Start with the community-compiled Words on Stream dictionary, then keep
    # only entries also present in the US English common-word list. That
    # removes most obscure/archaic entries and uses the source's swear-free list.
    common_words = load_words(COMMON_FILE, min_length=4, max_length=9)
    wos_words = load_words(WOS_FILE, min_length=4, max_length=9)
    valid_words = common_words & wos_words

    if not valid_words:
        raise SystemExit(
            "No words remain after filtering. Check the downloaded word lists."
        )

    # Index words by their sorted letters so each root only checks possible
    # letter multisets instead of scanning the entire dictionary.
    words_by_signature = defaultdict(list)
    for word in valid_words:
        words_by_signature[signature(word)].append(word)

    root_candidates = sorted(
        word for word in valid_words if 6 <= len(word) <= 8
    )
    random.shuffle(root_candidates)

    boards = []
    for root in root_candidates[:BOARD_LIMIT]:
        letters = sorted(set(root))
        limits = [root.count(char) for char in letters]
        matches = set()

        # Enumerate every usable sub-multiset of the root's letters.
        for counts in product(*(range(limit + 1) for limit in limits)):
            word_length = sum(counts)
            if not 4 <= word_length <= len(root):
                continue

            candidate_signature = "".join(
                char * count for char, count in zip(letters, counts)
            )
            matches.update(words_by_signature.get(candidate_signature, ()))

        # Every selected entry has passed BOTH the WoS list and common,
        # swear-free list. There is deliberately no obscure-word fallback.
        selected = sorted(matches, key=lambda word: (len(word), word))
        selected = selected[:MAX_WORDS_PER_BOARD]

        if root not in selected:
            if len(selected) >= MAX_WORDS_PER_BOARD:
                selected[-1] = root
            else:
                selected.append(root)
            selected = sorted(set(selected), key=lambda word: (len(word), word))

        if len(selected) >= MIN_WORDS_PER_BOARD:
            boards.append({"root": root, "words": selected})

    if not boards:
        raise SystemExit(
            "No boards met the minimum word count after common-word filtering."
        )

    with OUTPUT_FILE.open("w", encoding="utf-8") as output:
        json.dump(boards, output, ensure_ascii=False, separators=(",", ":"))

    total_words = sum(len(board["words"]) for board in boards)
    print(f"Generated {len(boards)} clean boards from {len(root_candidates)} root candidates.")
    print(f"Average words per board: {total_words / len(boards):.1f}")
    print(f"Saved output to {OUTPUT_FILE} ({OUTPUT_FILE.stat().st_size:,} bytes).")


if __name__ == "__main__":
    main()

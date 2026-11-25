# WordBoardGenerator

Generate up to 1,500 word boards without installing Python on your computer.

## Run the generator

1. Open the **Actions** tab at the top of this repository.
2. Select **Generate Word Boards** in the left sidebar.
3. Click **Run workflow**, then click the green **Run workflow** button.
4. Wait for the run to finish successfully.
5. Open that completed run and scroll to **Artifacts**.
6. Download **word-boards**. It contains `boards.json`.

The generated file is an artifact; it is not automatically committed to this repository. Artifacts are kept for 30 days.

## What it generates

- Up to 1,500 randomly ordered root-word boards.
- Root words are 6–8 letters and must appear in the common-word list and full dictionary.
- Candidate words are 4–8 letters and must be formable from the root letters, without using any letter more times than it appears in the root.
- Boards contain up to 24 words, prioritizing common words, and are kept only when they contain at least 8 words.

The generator uses an indexed letter-multiset lookup to avoid repeatedly scanning the entire dictionary for every root.

## Word-list sources

The workflow downloads these lists when it runs; the word lists are not copied into this repository:

- Common words: [first20hours/google-10000-english](https://github.com/first20hours/google-10000-english), using its US English swear-free list.
- Full dictionary: [dwyl/english-words](https://github.com/dwyl/english-words), using `words_alpha.txt`.

Please review the source repositories' license terms before using generated boards commercially. In particular, the common-word dataset states that commercial use may require separate licensing.

## Files

- `generate_boards.py` — board-generation script.
- `.github/workflows/generate.yml` — GitHub Actions workflow with the manual Run workflow button.

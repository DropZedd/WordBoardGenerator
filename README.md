# WordBoardGenerator

Generate up to 1,500 cleaner Words on Stream-style word boards without installing Python on your computer.

## Run the generator

1. Open the **Actions** tab at the top of this repository.
2. Select **Generate Word Boards** in the left sidebar.
3. Click **Run workflow**, then click the green **Run workflow** button.
4. Wait for the run to finish successfully.
5. Open that completed run and scroll to **Artifacts**.
6. Download **word-boards**. It contains `boards.json`.

The generated file is an artifact; it is not automatically committed to this repository. Artifacts are kept for 30 days.

## Word selection and filtering

The generator starts with a community-compiled Words on Stream word list, then intersects it with a US English common-word list marked as swear-free.

This means:

- Words must appear in the Words on Stream community list.
- Words must also appear in the common-word list.
- Obscure and archaic entries that are not in the common-word list are excluded.
- The generator does not fall back to obscure dictionary entries just to fill a board.
- Common plurals and verb forms are kept when they appear in both source lists.
- Candidate words are 4–9 letters and must be formable from the root letters, without using any letter more times than it appears in the root.
- Root words are 6–8 letters.
- Boards contain up to 24 words and are kept only when they contain at least 8 words.

The community Words on Stream list is not confirmed to be the official game's current dictionary. This process uses it as a starting point, then applies a stricter everyday-word filter.

## Word-list sources

The workflow downloads these lists when it runs:

- Words on Stream community dictionary: [OnyxA314/words_on_stream_solver](https://github.com/OnyxA314/words_on_stream_solver), which credits u/BandedOtter for compiling the list.
- Common words: [first20hours/google-10000-english](https://github.com/first20hours/google-10000-english), using its US English swear-free list.

Please review the source repositories' license terms before using generated boards commercially. In particular, the common-word dataset states that commercial use may require separate licensing.

## Files

- `generate_boards.py` — board-generation script.
- `.github/workflows/generate.yml` — GitHub Actions workflow with the manual Run workflow button.

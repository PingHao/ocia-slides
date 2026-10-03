---
name: catholic-bible-sources
description: Fetch, verify, and link Catholic Bible (思高本/NABRE) and Catechism texts with exact chapter URLs. Use when quoting or verifying scripture/CCC passages for Catholic materials (OCIA slide decks, handouts, scripture panels), or when making per-chapter "source" links.
---

# Catholic Bible & Catechism Sources

Rule: quote only from Catholic sources — English NABRE (USCCB), Chinese 思高本 (思高聖經學會). Never NIV/KJV or other non-Catholic translations. Some projects enforce this via AGENTS.md — obey it.

## Bible — English (NABRE, USCCB)

Chapter URL pattern:
```
https://bible.usccb.org/bible/{book}/{chapter}
```
- `{book}` is lowercase, no spaces; numbered books attach the digit directly: `genesis`, `exodus`, `deuteronomy`, `numbers`, `isaiah`, `ezekiel`, `john`, `acts`, `romans`, `1corinthians`, `1samuel`, `2kings`.
- Example: Exodus 24 → https://bible.usccb.org/bible/exodus/24
- Chapter pages include verse numbers inline. Fetch the page to verify exact wording before quoting verbatim.

## Bible — Chinese (思高本, ccreadbible)

Chapter URL pattern:
```
https://www.ccreadbible.org/chinesebible/sigao/{Book}_bible_Ch_{N}_.html
```
- `{Book}` = English book name, capitalized; numbered books use underscore: `Genesis`, `Exodus`, `Numbers`, `Deuteronomy`, `Isaiah`, `Ezekiel`, `Acts`, `Romans`, `1_Corinthians`, `1_Samuel`.
- `{N}` = chapter number, NOT zero-padded: `Ch_5_.html`, `Ch_24_.html`.
- Examples:
  - Exodus 24 → https://www.ccreadbible.org/chinesebible/sigao/Exodus_bible_Ch_24_.html
  - 1 Corinthians 10 → https://www.ccreadbible.org/chinesebible/sigao/1_Corinthians_bible_Ch_10_.html
- Book index (every book with all chapter links, Chinese/English names side by side): https://www.ccreadbible.org/chinesebible/sigao — fetch it (HTML format) to confirm a book's folder name before constructing URLs.
- Caution: the `.htm` variant (`/sigao/Exodus/024.htm`) does NOT exist — 404s. Use the `{Book}_bible_Ch_{N}_.html` form.

## Catechism of the Catholic Church (CCC)

- **English** (Vatican): https://www.vatican.va/archive/ENG0015/_INDEX.HTM — paragraphs are grouped in `__Pxx.HTM` files; the file↔paragraph mapping is not guessable (e.g. `__P9.HTM` holds §§27-30). Use the index to locate the right section file before citing.
- **Chinese** (思高對照): https://www.ccreadbible.org/Members/Bona/For-Bible/catechism — a section index (paginated, 卷/部分/條文); navigate into the section to reach the paragraph text.

## Workflow

1. Determine the passage(s) for each language — zh 思高 and en NABRE may use different book/chapter names.
2. Fetch the chapter URL to verify exact wording before quoting verbatim; if quoting from memory, mark it (e.g. 「意譯」/ paraphrase) or verify first.
3. When a UI asks for a source link, link the exact chapter, not the site root.
4. For multi-passage entries (e.g. Ex 2:1-10 + Acts 7:29-30), link each passage's own chapter separately.

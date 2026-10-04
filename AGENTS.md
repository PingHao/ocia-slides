# AGENTS.md

OCIA 慕道課程簡報專案（HTML slide deck）。編輯講義內容時，請遵守以下經文與教理引用來源規則。

## 聖經引用 (Bible References)

All Bible quotes and references must come from these Catholic sources:

- **English:** https://bible.usccb.org/bible (NABRE, USCCB)
- **Chinese (思高本):** https://www.ccreadbible.org/chinesebible/sigao (思高聖經學會)

Do not quote from other translations (e.g. NIV, KJV) or non-Catholic sources.

## 天主教教理 (Catechism References)

All Catechism of the Catholic Church (CCC / 《天主教教理》) quotes and references must come from:

- **English:** https://www.vatican.va/archive/ENG0015/_INDEX.HTM
- **Chinese:** https://www.ccreadbible.org/Members/Bona/For-Bible/catechism (思高本對照)

Verify paragraph numbers against these sources before adding or citing them.

Exact chapter URL patterns (both bibles) and navigation notes are documented in the repo-local `catholic-bible-sources` skill (`.kilo/skills/catholic-bible-sources/SKILL.md`) — use it to fetch, verify, and link specific chapters.

## SSH keys & secrets

Never read, display, copy, or transmit private keys or credentials — including anything under `~/.ssh/` (private keys, agent sockets, known_hosts), `.env` files, or API tokens. Exercise keys only through their intended tools (`ssh -T`, `git push`) without printing their contents. `~/.ssh/**` is additionally blocked by Kilo permissions (deny rules in `~/.config/kilo/kilo.jsonc`).

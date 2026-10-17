# Indus research — Claude Code starter kit

1. Unzip this folder somewhere, e.g. `~/indus`.
2. In a terminal: `cd ~/indus && claude`. Claude Code reads `CLAUDE.md` automatically.
3. First message to paste:

   > Read CLAUDE.md and CURRENT-STATUS.md. Run the setup and the smoke test. Then give me a 5-line audit of where we stand and propose ONE pre-registered next round, choosing from the open leads in CLAUDE.md. Don't start fitting until I say go.

What you need to supply yourself:
- `data/kuiper.txt`: the archive.org OCR text of Kuiper (1991), *Aryans in the Rigveda*. Claude Code can find and download it for you.
- Gulf seal publications (Laursen 2010; Al-Sindi's Bahrain seal volumes) as PDFs in `data/sources/`. They unlock the strongest open lead.

Contents:
- `CLAUDE.md`: project memory and rules for Claude Code.
- `CURRENT-STATUS.md`: one row per round, 1–45.
- `indus-lab/`: all rounds, code, data, reports.
- `setup/`: external-data fetcher (pinned commits), paths, requirements, smoke test.
- `data/derived/`: small extracts (CDLI Dilmun/Meluhha lines, Kuiper word list).

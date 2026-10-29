# 01 ICIT corpus via lipi (primary corpus)
- **What:** `inscriptions.csv`, 5,679 records (inscribed sides), 38 columns; the text is in column 35 (`text`), as ICIT sign numbers. Upstream `LICENSE` and `README.md` are kept alongside.
- **From:** field-cady/indus_valley_script_corpus, an export of yajnadevam/lipi, which is derived from the Interactive Corpus of Indus Texts (Wells & Fuls) and Mahadevan 1977. Copied unchanged from `indus-lab/raw/`; sha256 c22d39c3…3429.
- **Licence:** MIT (Copyright 2024 Michael Carlson).
- **Warning:** the `sanskrit` and `translation` columns are one researcher's proposed readings (Yajnadevam). They are **not evidence** and are left out of `library/inscriptions/inscriptions.csv` and the PDFs.
- **Text notation:** `+` = the text ends there; `[` / `]` = broken; `/` = new line; `000` = a sign that cannot be read. Stored in drawn order; reverse right-to-left (R/L) texts for reading order (see `indus-lab/round30/foreign_context.py`).

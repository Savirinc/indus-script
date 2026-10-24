# Round 57 addendum: Kandahar, Jaya and Afghan place names (descriptive, 24 Oct 2026)

**Not pre-registered and not scored.** The names were chosen after seeing Bhaty's claim (The Ranveer Show slide: "55 Jaya / Dzhaya (Herat District, Afghanistan)", sign pair read ja-ya, 75 entries). This is description under the round 57 instrument.

- `names_check.py` uses Bhaty's key (Yajnadevam's with 435/436 → o), the round 57 skeletons and 1,000 shuffles (seeds 57201+). See `names_check.log`.
  - Kandahar, Qandahar and Gandhāra (kntkr) match 0 texts.
  - Jaya (skeleton "c", one consonant): 390 texts vs a wrong-key mean of 487.
  - Jayah (ck): 5 vs 10.
- `geo_check.py` uses GeoNames Afghanistan (AF.txt, CC BY 4.0; 75,843 places, 217,066 normalised name forms). Fetch it with `curl -O https://download.geonames.org/export/dump/AF.zip`; it is not committed. See `geo_check.log`.
  - "Jāyah" is a real village (Herat, admin 11).
  - **25.8%** of all 295 two-sign text readings under the atlas key are Afghan place names. 200 wrong keys give **26.4%** on average (range 14–36%).
  - The pair 003-156 ("jaya") reads as an Afghan place under 294 of 1,000 wrong keys (*mata, mara, sama, sada, jaka, vaya*…).
- In the ICIT transcription (readings-atlas `ledger.csv`), 22 of her 38 listed seal IDs (H-2218 to H-2239, incised tablets) read *jara* (003-861) or *cān* (034-700), not *jaya*.
  - The rest use five different second signs (156, 154, 430, 151, 158), and some run in the reverse direction.
  - Shortughai is in Takhar, about 700 km from Herat.

Conclusion (descriptive): "a reading is an Afghan place" holds for about one short reading in four under any key, so it carries no evidence. Round 57 (NULL) stands.
